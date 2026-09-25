# Horary known-outcome corpus

Purpose: durable research corpus of archived horary questions for which a later outcome is available.

## Blinding architecture

This directory contains only source/catalog metadata and outcome-free inputs. Outcome-bearing page snapshots and coded truth are deliberately kept outside the decoder project root during blind runs. This follows the repository rule that answer keys must not sit under the decoder root.

The private truth archive is versioned separately and identified here only by hash. A fresh scorer should receive this public/input layer; an evaluator receives the private truth layer only after prediction freeze.

## Current source

Skyscript Astrology Forum, "Index of Horary Charts with Answers" plus later outcome-known threads discovered during bounded search. The index itself states that linked cases have feedback/outcomes.

## Data model

- cases: stable case id, source, title/category, question metadata, reconstructibility state
- snapshots: hashes/provenance of archived source captures
- outcomes: private truth-only table, never stored in this directory during a blind run
- experiments: membership/exposure status so contaminated and untouched subsets can both be audited

This corpus is intended to grow beyond the current pilot. Do not overwrite older coded outcomes; supersede them with provenance and retain the prior coding.
