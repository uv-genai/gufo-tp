#include <gufo/ext/generated/qwen38_flash_next_constants.hpp>
#include <gufo/ext/registry.hpp>
#include <gufo/ext/text.hpp>

#include "src/models/qwen38_flash_next/probe.hpp"
#include "src/models/qwen38_flash_next/runner.hpp"
#ifdef GUFO_ENABLE_TP2_RDMA
#include "src/models/qwen38_flash_next/kernels/rocm/verbs.hpp"
#endif

namespace gufo::models::qwen38_flash_next {

#if defined(ENGINE_ENABLE_HIP)
int RunQwen38FlashNextBenchmark(
    const ext::TextBenchOptions& opt,
    const std::shared_ptr<const core::GgufReader>& reader,
    std::chrono::steady_clock::time_point model_load_start);

int RunFlashNextPrompt(const ext::TextPromptOptions& opt,
                       const core::GgufReader& reader,
                       std::chrono::steady_clock::time_point model_load_start);

int RunFlashNextChat(const ext::TextPromptOptions& opt,
                     const core::GgufReader& reader,
                     std::chrono::steady_clock::time_point model_load_start);
#endif

}  // namespace gufo::models::qwen38_flash_next

void qwen38_flash_next_provider_register(gufo::ext::Registry& registry) {
  registry.AddProvider(gufo::ext::generated::extension_qwen38_flash_next::
                           kProvider_flash_next_q4);
#if defined(ENGINE_ENABLE_HIP)
  registry.AddTextProvider({
      .id = "flash-next-q4",
      .probe = &gufo::models::qwen38_flash_next::ProbeFlashNext,
      .probe_gguf = &gufo::models::qwen38_flash_next::ProbeFlashNextGguf,
      .create = &gufo::models::qwen38_flash_next::CreateQwenFlashNextTextRunner,
      .bench_driver =
          &gufo::models::qwen38_flash_next::RunQwen38FlashNextBenchmark,
      .prompt_driver = &gufo::models::qwen38_flash_next::RunFlashNextPrompt,
      .chat_driver = &gufo::models::qwen38_flash_next::RunFlashNextChat,
#ifdef GUFO_ENABLE_TP2_RDMA
      .create_tp_transport =
          +[](const gufo::ext::TextTpTransportOptions& options,
              std::string* error)
          -> std::shared_ptr<gufo::ext::TextTpTransport> {
        return gufo::models::qwen38_flash_next::rocm::
            CreateIbrverbsCommunicator(
                {.rank = options.rank,
                 .world_size = options.world_size,
                 .bootstrap_host = options.bootstrap_host,
                 .bootstrap_port = options.bootstrap_port,
                 .device_index = options.device_index,
                 .rdma_device = options.rdma_device,
                 .rdma_port = options.rdma_port,
                 .gid_index = options.gid_index},
                error);
      },
#endif
      .sampling_defaults =
          &gufo::models::qwen38_flash_next::FlashNextSamplingDefaults,
      .speculative_defaults = {{.backend = "mtp",
                                .max_draft_tokens = 7,
                                .min_draft_tokens = 1}},
  });
#endif
}
