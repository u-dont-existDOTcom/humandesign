"""Deterministic person-exclusive dataset splitting and cohort guards."""

from __future__ import annotations

import random
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from hdmatch.human.dataset import HumanCase, HumanDataset, human_dataset_sha256


class PersonSplitManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["person-split-v1"] = "person-split-v1"
    seed: int
    development_ids: tuple[str, ...]
    validation_ids: tuple[str, ...]
    final_test_ids: tuple[str, ...]
    dataset_hash: str

    @field_validator("development_ids", "validation_ids", "final_test_ids")
    @classmethod
    def reject_blank_participant_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(identifier.strip() for identifier in value)
        if any(not identifier for identifier in normalized):
            raise ValueError("person-split participant IDs cannot be blank")
        return normalized

    @model_validator(mode="after")
    def disjoint(self) -> PersonSplitManifest:
        identifiers = self.development_ids + self.validation_ids + self.final_test_ids
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("person split contains duplicate participant IDs")
        groups = [set(self.development_ids), set(self.validation_ids), set(self.final_test_ids)]
        if groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]:
            raise ValueError("person split contains overlapping participant IDs")
        if not self.development_ids:
            raise ValueError("development split cannot be empty")
        return self


def create_person_splits(
    dataset: HumanDataset,
    seed: int,
    validation_fraction: float = 0.2,
    final_test_fraction: float = 0.2,
) -> PersonSplitManifest:
    if not 0.0 <= validation_fraction < 1.0 or not 0.0 <= final_test_fraction < 1.0:
        raise ValueError("split fractions must be within [0, 1)")
    if validation_fraction + final_test_fraction >= 1.0:
        raise ValueError("development split must retain positive mass")
    existing = {case.cohort for case in dataset.cases} - {"unassigned"}
    if existing:
        if any(case.cohort == "unassigned" for case in dataset.cases):
            raise ValueError("cannot mix assigned and unassigned cohort labels")
        development = sorted(
            case.participant_id for case in dataset.cases if case.cohort == "development"
        )
        validation = sorted(
            case.participant_id for case in dataset.cases if case.cohort == "validation"
        )
        final = sorted(case.participant_id for case in dataset.cases if case.cohort == "final_test")
    else:
        identifiers = sorted(case.participant_id for case in dataset.cases)
        random.Random(seed).shuffle(identifiers)
        final_count = round(len(identifiers) * final_test_fraction)
        validation_count = round(len(identifiers) * validation_fraction)
        final = sorted(identifiers[:final_count])
        validation = sorted(identifiers[final_count : final_count + validation_count])
        development = sorted(identifiers[final_count + validation_count :])
    if not development:
        raise ValueError("development split cannot be empty")
    return PersonSplitManifest(
        seed=seed,
        development_ids=tuple(development),
        validation_ids=tuple(validation),
        final_test_ids=tuple(final),
        dataset_hash=human_dataset_sha256(dataset),
    )


def enforce_training_cohort(cases: tuple[HumanCase, ...] | list[HumanCase]) -> None:
    forbidden = sorted(case.participant_id for case in cases if case.cohort != "development")
    if forbidden:
        raise ValueError(f"fitting accepts development people only; rejected: {forbidden}")


def validate_manifest_for_dataset(
    dataset: HumanDataset,
    manifest: PersonSplitManifest,
) -> None:
    """Bind a split to exactly one dataset and every person in it."""

    if manifest.dataset_hash != human_dataset_sha256(dataset):
        raise ValueError("split manifest dataset hash does not match the human dataset")
    dataset_ids = {case.participant_id for case in dataset.cases}
    manifest_ids = (
        set(manifest.development_ids) | set(manifest.validation_ids) | set(manifest.final_test_ids)
    )
    if dataset_ids != manifest_ids:
        raise ValueError("split manifest must assign every dataset person exactly once")
    expected = {
        **{identifier: "development" for identifier in manifest.development_ids},
        **{identifier: "validation" for identifier in manifest.validation_ids},
        **{identifier: "final_test" for identifier in manifest.final_test_ids},
    }
    mismatched = sorted(
        case.participant_id
        for case in dataset.cases
        if case.cohort != "unassigned" and case.cohort != expected[case.participant_id]
    )
    if mismatched:
        raise ValueError(f"dataset cohort labels disagree with split manifest: {mismatched}")


def select_partition(
    dataset: HumanDataset,
    manifest: PersonSplitManifest,
    partition: Literal["development", "validation", "final_test"],
) -> tuple[HumanCase, ...]:
    validate_manifest_for_dataset(dataset, manifest)
    selected_ids = set(getattr(manifest, f"{partition}_ids"))
    cases = tuple(
        case.model_copy(update={"cohort": partition})
        for case in dataset.cases
        if case.participant_id in selected_ids
    )
    if {case.participant_id for case in cases} != selected_ids:
        raise ValueError("split manifest references people missing from dataset")
    return cases
