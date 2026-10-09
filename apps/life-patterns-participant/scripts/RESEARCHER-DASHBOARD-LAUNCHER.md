# Life Patterns researcher desktop launcher

This is an owner-local convenience client for the existing private Railway researcher dashboard. It does not replace server-side authorization.

**Files**
- `life_patterns_local_dashboard.py`: obtains the authorized `PARTICIPANT_ADMIN_TOKEN` from the installed Railway CLI without printing it, reads feedback over HTTPS, and writes a mode-0600 escaped HTML report to the configured local path. `--check` refreshes/verifies data without launching a browser.
- `open_researcher_dashboard.py`: opens the full dashboard using a private temporary navigation file and falls back to the local report when the online browser launch fails. The temporary file is deleted after navigation.

**Local config** (create privately as `~/.config/life-patterns/dashboard-viewer.json`, mode 0600):

```json
{
  "railway_cli": "/absolute/path/to/railway",
  "dashboard_url": "https://your-own-service.up.railway.app",
  "project_id": "<project id>",
  "environment_id": "<environment id>",
  "service_id": "<service id>",
  "local_report": "/absolute/path/to/Downloads/Life-Patterns-Question-Feedback-Current.html"
}
```

Configure the OS application menu with `Terminal=false` and `Exec=/usr/bin/python3 /absolute/path/to/open_researcher_dashboard.py`. Keep both Python scripts installed in the same directory. Do not put the admin token in the desktop file, repository, command line, browser process arguments, or local report.

On a GNOME/Wayland desktop, the earlier clipboard-based launcher may lose the copied credential when its short-lived process closes; do not rely on `wl-copy`, `xclip` or GTK clipboard ownership. The online viewer relies on the already-supported `#key` fragment handoff, which the remote admin frontend consumes into sessionStorage and removes from the address bar. The temporary handoff file must have restrictive permissions and be removed after navigation.

**Validation:** Run `python3 life_patterns_local_dashboard.py --check --config ~/.config/life-patterns/dashboard-viewer.json`, inspect the 0600 local report, then test the menu launch. The reviewer-only admin API must continue returning HTTP 401 without credentials.
