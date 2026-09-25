# Life Patterns v2 owner UX feedback — HTML surface — 2026-09-13

Status: OWNER PRODUCT FEEDBACK / IMPLEMENTATION DIRECTION.

The owner rejected the Work-mediated terminal relay as an adequate product-judgment surface and explicitly pointed back to the earlier HTML app as the preferable interaction model.

The earlier participant-facing HTML shell still exists at `src/hdmatch/api/life_patterns_interview_ui.py`. Its card/chat presentation, conversational layout, and direct browser interaction remain useful presentation assets.

The problem with the old path was not the HTML/CSS. The problem was the pre-v2 backend behavior behind it, especially automatic person-level map generation from approved episodes. That backend authority remains superseded by the accepted participant-adjudicated v2 semantics.

Therefore:

- preserve/reuse the good HTML presentation shell;
- do not restore the old automatic map-generation semantics;
- keep v2 episode facts and participant-adjudicated person-level patterns as the semantic authority;
- hide internal research codes such as `accept | correct | not-supported` behind natural-language controls;
- do not require the owner to operate a terminal or act as a relay between Work and a CLI for product judgment;
- the next owner-judgment surface should be directly usable in a browser or as a standalone HTML prototype.

This feedback does not change the accepted v2 semantic contract. `semantic_change_required=false`.

Current recommendation: build the smallest browser/standalone HTML owner prototype by reusing the existing visual shell while replacing only the interaction logic needed for the v2 flow. Do not add production auth, recovery, voice, deployment, external collection, target-model activity, or spending at this stage.
