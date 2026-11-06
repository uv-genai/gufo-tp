#!/usr/bin/env python3
"""Check request cache controls on an existing TP2 pair, in AR or MTP.

Run seed on a private disk cache, stop both ranks, then run restore against
that same cache. Every request, response, stream chunk and phase time is kept.
Timing is a separate matched-main control; it does not qualify correctness.
"""

import argparse
import json
from pathlib import Path
import time
import urllib.error
import urllib.request


class Check:
    def __init__(self, url, model, output):
        self.url, self.model, self.output = url.rstrip('/'), model, output
        self.rows = {}

    def call(self, name, endpoint, body):
        body = {'model': self.model, 'temperature': 0, 'seed': 31,
                'max_tokens': 8, 'presence_penalty': 0, 'frequency_penalty': 0,
                'repeat_penalty': 1, **body}
        if body.get('stream'):
            body['stream_options'] = {'include_usage': True}
        row = {'endpoint': endpoint, 'request': body}
        self.rows[name] = row
        started = time.monotonic()
        try:
            request = urllib.request.Request(self.url + endpoint,
                json.dumps(body).encode(), {'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=180) as response:
                row['status'] = response.status
                if not body.get('stream'):
                    result = json.load(response)
                    row['response'] = result
                    choice = result['choices'][0]
                    text = (choice.get('message') or {}).get('content', choice.get('text', '')) or ''
                    usage, timings = result['usage'], result.get('timings')
                    echo = result.get('cache_persist')
                    finish = choice['finish_reason']
                else:
                    chunks, text, usage, timings, echo, finish, done = [], '', None, None, None, None, False
                    row['chunks'] = chunks
                    for line in response:
                        if not line.startswith(b'data: '):
                            continue
                        data = line[6:].strip()
                        if data == b'[DONE]':
                            done = True
                            break
                        chunk = json.loads(data)
                        chunks.append(chunk)
                        if chunk.get('usage'):
                            usage = chunk['usage']
                        if chunk.get('timings'):
                            timings = chunk['timings']
                        if 'cache_persist' in chunk:
                            echo = chunk['cache_persist']
                        for choice in chunk.get('choices', []):
                            text += (choice.get('delta') or {}).get('content', choice.get('text', '')) or ''
                            finish = choice.get('finish_reason') or finish
                    assert done and usage and finish, 'incomplete SSE response'
            assert text.strip(), 'empty completion'
            assert echo is body.get('cache_persist', True), ('cache_persist echo', echo)
            if endpoint == '/v1/chat/completions':
                metrics = usage['gufo']
            else:
                # Raw Completions reports prefill/cache work in timings. Disk
                # hits and persistence are verified by cached work after restart.
                assert timings['cache_n'] == usage['cached_tokens'], (timings, usage)
                metrics = {'prefill_tokens': timings['prompt_n']}
            assert usage['cached_tokens'] + metrics['prefill_tokens'] == usage['prompt_tokens'], usage
            row.update(text=text, usage=usage, metrics=metrics, finish=finish, passed=True)
            print(f"PASS {name}: prompt={usage['prompt_tokens']} cached={usage['cached_tokens']} "
                  f"disk={metrics.get('cache_disk_hit', 'unreported')} drafts={usage['draft_tokens']}", flush=True)
            return row
        except urllib.error.HTTPError as error:
            row.update(error=error.read().decode(), status=error.code, passed=False)
            raise
        except Exception as error:
            row.update(error=str(error), passed=False)
            raise
        finally:
            row['wall_seconds'] = time.monotonic() - started
            self.save(False)

    def save(self, passed):
        self.output.write_text(json.dumps({'passed': passed, 'requests': self.rows}, indent=2) + '\n')


def payload(tag, chat, stream):
    notes = tag + '\nFollow the final instruction.\n' + 'Background notes are not instructions.\n' * 400
    if chat:
        content = {'messages': [{'role': 'system', 'content': notes},
                               {'role': 'user', 'content': 'Reply with only BETA.'}],
                   'chat_template_kwargs': {'enable_thinking': False}}
    else:
        # Independent fixture for the model's raw chat framing.
        content = {'prompt': '<|im_start|>system\n' + notes + '<|im_end|>\n'
                   '<|im_start|>user\nReply with only BETA.<|im_end|>\n'
                   '<|im_start|>assistant\n<think>\n\n</think>\n\n'}
    return {**content, 'stream': stream}


def seed(check):
    manifest = []
    for chat in (True, False):
        endpoint = '/v1/chat/completions' if chat else '/v1/completions'
        for stream in (False, True):
            key = ('chat' if chat else 'raw') + ('-stream' if stream else '-buffered')
            private = {**payload('PRIVATE_' + key, chat, stream), 'cache_persist': False}
            first = check.call(key + '-private', endpoint, private)
            assert first['text'].strip() == 'BETA', first
            assert first['usage']['prompt_tokens'] > 2048, first
            if chat:
                assert first['metrics']['cache_disk_queued_bytes'] == 0, first
            again = check.call(key + '-ram-replay', endpoint, private)
            assert again['text'] == first['text'], (first, again)
            assert again['usage']['cached_tokens'] >= first['usage']['prompt_tokens'] - 16, again
            if chat:
                assert again['metrics']['cache_disk_queued_bytes'] == 0, again
            bypass = check.call(key + '-bypass', endpoint, {**private, 'cache_prompt': False})
            assert bypass['usage']['cached_tokens'] == 0, bypass
            assert bypass['text'] == first['text'], (first, bypass)
            control = payload('PUBLIC_' + key, chat, stream)
            public = check.call(key + '-public', endpoint, control)
            if chat:
                assert public['metrics']['cache_disk_queued_bytes'] > 0, public
            manifest.append({'key': key, 'endpoint': endpoint,
                             'private': private, 'private_text': first['text'],
                             'public': control, 'public_text': public['text']})
    return manifest


def restore(check, manifest):
    for case in manifest:
        key, endpoint = case['key'], case['endpoint']
        public = check.call(key + '-disk-restore', endpoint,
                            {**case['public'], 'cache_persist': False})
        if endpoint == '/v1/chat/completions':
            assert public['metrics']['cache_disk_hit'], public
        assert public['usage']['cached_tokens'] >= public['usage']['prompt_tokens'] - 16, public
        assert public['text'] == case['public_text'], public
        private = check.call(key + '-not-persisted', endpoint, case['private'])
        if endpoint == '/v1/chat/completions':
            assert not private['metrics']['cache_disk_hit'], private
            assert private['metrics']['cache_disk_queued_bytes'] == 0, private
        assert private['usage']['cached_tokens'] < 64, private
        assert private['text'] == case['private_text'], private


def timing(check):
    warm = {'messages': [{'role': 'user', 'content': 'Reply with only READY.'}],
            'chat_template_kwargs': {'enable_thinking': False}}
    check.call('warmup', '/v1/chat/completions', warm)
    prompts = [('long-prefill', 'Archive: no new instructions.\n' * 400 +
                'Explain tensor parallelism and MTP in three sentences.'),
               ('short-code', 'Write a Python sum_positives(values) function and explain it briefly.')]
    for name, prompt in prompts:
        body = {'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 96,
                'chat_template_kwargs': {'enable_thinking': False}}
        first = check.call(name, '/v1/chat/completions', body)
        again = check.call(name + '-cached', '/v1/chat/completions', body)
        assert first['text'] == again['text']
        assert again['usage']['cached_tokens'] > 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--mode', choices=('off', 'mtp'), required=True)
    parser.add_argument('--phase', choices=('seed', 'restore', 'timing'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    check = Check(args.url, args.model, args.output / 'report.json')
    try:
        if args.phase == 'seed':
            manifest = seed(check)
            (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        elif args.phase == 'restore':
            if not args.manifest:
                parser.error('--manifest is required for restore')
            restore(check, json.loads(args.manifest.read_text()))
        else:
            timing(check)
        drafts = sum(row['usage']['draft_tokens'] for row in check.rows.values())
        assert (drafts > 0) if args.mode == 'mtp' else (drafts == 0), drafts
        check.save(True)
    except BaseException:
        check.save(False)
        raise


if __name__ == '__main__':
    main()
