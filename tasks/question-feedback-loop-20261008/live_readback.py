"""Privacy-safe administrative health check using Railway-injected environment access."""
import json
import os
from urllib.request import Request, urlopen

base = "https://life-patterns-participant-production.up.railway.app"
header = {"Authorization": "Bearer " + os.environ["PARTICIPANT_ADMIN_TOKEN"]}
for path, field in (
    ("/api/admin/question-feedback", "feedback"),
    ("/api/admin/gpt-submissions", "submissions"),
    ("/api/admin/sessions", "sessions"),
):
    with urlopen(Request(base + path, headers=header), timeout=30) as response:
        data = json.load(response)
        count = data["total"] if field == "feedback" else len(data[field])
        print(json.dumps({"endpoint": field, "http": response.status, "count": count}))
