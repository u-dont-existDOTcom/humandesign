# Processing heartbeat and payment-required hotfix

Owner outcome: people must see whether processing is active, and provider failure must not look like an indefinite freeze.

Observed gateway logs: three successful HTTP requests lasting 178.946 s, 31.904 s, and 136.016 s followed by HTTP 402 after 0.096 s. Thus the final refusal itself was fast after earlier lengthy processing. The gateway source forwards the upstream status. Venice documents bearer 402 as insufficient API credit; exact balance and error body were not retained by the old app. Do not claim a balance, trigger purchases, change providers or alter model effort.

Small repair: stable total/stage elapsed timers; server acknowledgement age from successful polling; guarded worker heartbeat; count/time of received stream events (metadata only); stage/repair-attempt indicator; indeterminate activity display rather than fabricated percent. A lost server heartbeat must visibly become stale. Terminal 402 becomes a saved provider-blocked session, never a finished interview and never an automatic retry. Existing error sessions migrate without model calls. An authenticated researcher can acknowledge billing repair and allow retry; no payment is executed.

Verification: focused HTTP/engine tests including blocked-state no-call, legacy migration, guards against stale workers, elapsed start preservation, stream metadata, admin-only recovery. A slow synthetic browser flow must visibly update elapsed and liveness; simulated network loss must mark stale, and 402 must replace progress with a clear message. No real participant text or credential in tests/review/Git. Live health and asset identity are deployment checks, not a real inference success claim.

Assurance: reversible hotfix with targeted liveness/state tests and participant deployment. No scientific mapping changes, billing write, model downgrade, full survey re-coding or speculative cross-family review needed for facts settled by traces and executable tests. A source review of the exact affected diff is still required before deploy.
