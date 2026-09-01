# ruff: noqa: E501
"""AstroHD-first production landing page with relationship work kept secondary."""

from __future__ import annotations

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AstroHD research pilot</title>
  <style>
    :root { color-scheme:light; --ink:#1f2933; --muted:#52606d; --line:#cbd2d9; --soft:#f5f7fa; --accent:#2f5d62; }
    * { box-sizing:border-box; }
    body { margin:0; color:var(--ink); font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    main { width:min(58rem,calc(100% - 2rem)); margin:clamp(2rem,8vw,6rem) auto; }
    h1 { max-width:13ch; margin:.4rem 0 .8rem; font-size:clamp(2.5rem,8vw,5rem); line-height:.98; letter-spacing:-.045em; }
    h2 { margin:0 0 .45rem; font-size:1.3rem; }
    p { margin:.5rem 0; }
    .eyebrow { color:var(--accent); font-weight:800; letter-spacing:.09em; text-transform:uppercase; font-size:.8rem; }
    .lede { max-width:44rem; color:var(--muted); font-size:1.16rem; }
    .choices { display:grid; grid-template-columns:1.25fr 1fr; gap:1rem; margin-top:2.2rem; }
    article { display:flex; flex-direction:column; padding:1.25rem; border:1px solid var(--line); border-radius:.8rem; }
    article.primary { border-top:5px solid var(--accent); }
    .tag { color:var(--accent); font-size:.82rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; }
    a { display:inline-block; margin-top:auto; padding-top:1rem; color:var(--accent); font-weight:800; }
    .note { margin-top:1.5rem; padding:1rem; background:var(--soft); color:var(--muted); }
    @media (max-width:42rem) { .choices { grid-template-columns:1fr; } main { margin-top:2rem; } }
  </style>
</head>
<body>
<main>
  <p class="eyebrow">Developmental research pilot</p>
  <h1>Start with one person.</h1>
  <p class="lede">A relationship claim depends on whether the natal AstroHD layer describes individuals first. The first test therefore freezes one person's natal predictions before asking about their behavior.</p>
  <section class="choices" aria-label="Available research tests">
    <article class="primary">
      <p class="tag">First test</p>
      <h2>Natal AstroHD</h2>
      <p>One person's birth-derived predictions, a neutral GPT interview, then an exact prediction-versus-answer reveal.</p>
      <a href="/astrohd/">Start the owner natal test →</a>
    </article>
    <article>
      <p class="tag">Secondary development mode</p>
      <h2>AstroRRF relationship study</h2>
      <p>Two people's frozen chart and relationship signals compared with a chart-blind relationship questionnaire.</p>
      <a href="/relationship">Open the relationship study →</a>
    </article>
  </section>
  <p class="note">Neither test silently changes its model during a participant's run. Submissions are retained privately; a later model version requires a separate training, review, and release step.</p>
</main>
</body>
</html>"""
