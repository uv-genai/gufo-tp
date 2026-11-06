#ifndef GUFO_SERVER_CONTINUATION_TYPES_HPP_
#define GUFO_SERVER_CONTINUATION_TYPES_HPP_

#include <cstddef>
#include <cstdint>
#include <string_view>

#include "src/ext/continuation.hpp"

namespace gufo::server {

// The continuation bases and token id are runtime contracts (RFC step 6).
// These aliases keep the serving spelling; cache policy below stays here.
using ext::ContinuationInputPrefix;
using ext::ContinuationSnapshot;
using ext::ContinuationState;
using ext::ContinuationToken;
using ext::PrefixInputIdentity;

enum class SnapshotEventAction : std::uint8_t {
  kRemoved,
  kSkipped,
};

enum class SnapshotEventReason : std::uint8_t {
  kByteCapacity,
  kEntryCapacity,
  kExactReplacement,
  kCaptureFailure,
  kReservationMismatch,
};

/// Continuation boundaries take precedence over optional history/retry copies.
/// A branch point is a continuation boundary learned where two prompts
/// diverged; it stays a branch point after the older prompt's checkpoints go.
enum class SnapshotPurpose : std::uint8_t {
  kContinuation,
  kHistory,
  kRetry,
  kBranchPoint,
};

/// Sanitized snapshot-retention event.
///
/// Token values and prompt contents are deliberately absent.
struct SnapshotEvent {
  SnapshotEventAction action{SnapshotEventAction::kSkipped};
  SnapshotEventReason reason{SnapshotEventReason::kByteCapacity};
  std::size_t snapshot_bytes{0};
  std::size_t token_count{0};
  std::size_t retained_snapshot_bytes{0};
  std::size_t reserved_snapshot_bytes{0};
  std::size_t capacity_bytes{0};
};

/// Explains a miss without exposing prompt or token contents.
struct ContinuationLookup {
  std::string_view miss_reason;
  std::size_t common_prefix_tokens{0};
  std::size_t checkpoint_tokens{0};
};

}  // namespace gufo::server

#endif
