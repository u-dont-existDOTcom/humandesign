# Life Patterns browser regressions

Run only against the loopback synthetic fixture, never a participant service. The runner rejects a non-loopback target. No model credentials or inference calls are used.

From the repository root, install the Python development lock and editable package. Then:

```sh
npm --prefix tests/browser ci
PYTHONPATH=src:tests/browser .venv/bin/python -m uvicorn fixture_server:app --host 127.0.0.1 --port 18765
```

In another shell:

```sh
BROWSER_PATH=/path/to/installed/chromium npm --prefix tests/browser test
```

The runner defaults to an installed Brave executable; `BROWSER_PATH` can select a Chromium-family browser. `PUPPETEER_MODULE` can select an already-installed module instead of installing a second copy. `LIFE_PATTERNS_TEST_OUTPUT` sets the output directory. The default is `/tmp/life-patterns-browser-results`.

For recorded runs, invoke the runner through the project's active Universal test-efficiency observer. The fixture binds loopback only and its session-drop endpoint exists only in this test server. Screenshots and data are synthetic. Stop only the fixture/browser processes created for this run after testing.

These tests validate transport, phase, visibility, retention and deterministic model-boundary wiring. They do not certify the current model's semantic judgment or replace owner evaluation.
