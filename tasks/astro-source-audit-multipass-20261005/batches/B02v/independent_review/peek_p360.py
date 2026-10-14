import json
from pathlib import Path
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
p=json.loads((b/"RULES_DRAFT.json").read_text())
for r in p["records"]:
    if 2817 <= r["record_number"] <= 2836:
        print(r["record_number"],r["source_record_kind"],":",r["source_statement"])
        print(" IF",r["preconditions"])
        print(" UN",r["exceptions_and_evidence_limits"])
