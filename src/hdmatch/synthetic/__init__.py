"""Frozen-model synthetic case generation and declared noise tiers."""

from .generator import BlindSyntheticBundle, SyntheticGenerator
from .noise import NoiseTier, apply_noise, noise_parameters_payload
from .sealing import (
    AnswerKeyEnvelope,
    AnswerKeySealingError,
    SealingMetadata,
    assert_no_plaintext_answer_keys,
    decrypt_answer_key_bytes,
    decrypt_answer_key_json,
    generate_key_file,
    seal_answer_key,
    seal_answer_key_file,
)

__all__ = [
    "AnswerKeyEnvelope",
    "AnswerKeySealingError",
    "BlindSyntheticBundle",
    "NoiseTier",
    "SealingMetadata",
    "SyntheticGenerator",
    "apply_noise",
    "noise_parameters_payload",
    "assert_no_plaintext_answer_keys",
    "decrypt_answer_key_bytes",
    "decrypt_answer_key_json",
    "generate_key_file",
    "seal_answer_key",
    "seal_answer_key_file",
]
