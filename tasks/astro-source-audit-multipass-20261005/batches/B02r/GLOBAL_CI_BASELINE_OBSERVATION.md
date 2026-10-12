# Repository-wide CI observation (source-draft checkpoint)

At isolated B02r WIP commit `7d39111`, GitHub Actions `ci` run **38322205628** checked out HumanDesign and ran the repository unit/integration test step successfully: **395 passed, 4 skipped**, including `tests/test_lilly_b02r_source_ci.py`.

The unrelated repository-wide `ruff check src tests --ignore E501,I001` step **failed with 61 existing lint errors**, which is why the complete workflow conclusion is failure. The immediately preceding B02q branch exhibited the same count of 61 lint errors. This record is evidence only of the named CI steps; it does not assert an all-green CI or prove the errors are identical line-for-line without a full comparative audit. The affected work is historical source data plus its separate test; the focused B02r source test runner independently passed 69/69 before semantic reviewer feedback.

Before canonical source publication, rerun the B02r local source suite after any reviewer repairs, and distinguish focused source acceptance from existing whole-repository CI lint status. No predictive or clinical validity follows from these structural tests.
