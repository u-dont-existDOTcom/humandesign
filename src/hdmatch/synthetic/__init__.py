"""Synthetic data generation support."""

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
    "SealingMetadata",
    "assert_no_plaintext_answer_keys",
    "decrypt_answer_key_bytes",
    "decrypt_answer_key_json",
    "generate_key_file",
    "seal_answer_key",
    "seal_answer_key_file",
]
