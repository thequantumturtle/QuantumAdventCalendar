Short announcement: Pre-push hook changes merged

What's new
- The pre-push hook now runs Docker-first smoke tests and a frontend production build to catch build-time regressions before they reach CI.
- New environment variables:
  - `SKIP_FRONTEND_BUILD=1` — skip the frontend build for a single push.
  - `CI_FRONTEND_INSTALL=1` — run `npm ci` (or `npm install` if no lockfile) before the build.
  - `FRONTEND_BUILD_TIMEOUT_SECONDS` — timeout for the frontend build (recommended default: 300 seconds).

Why this matters
- Prevents broken frontend builds from reaching `main` and keeps CI green.
- Keeps pre-push quick by default while allowing an opt-in CI-accurate install.

Quick actions for maintainers
- If you see a failed pre-push build, re-run locally with `CI_FRONTEND_INSTALL=1` or skip for a single push with `SKIP_FRONTEND_BUILD=1`.
- To set the recommended timeout locally (PowerShell):

```powershell
$env:FRONTEND_BUILD_TIMEOUT_SECONDS = '300'
```

Thanks — please ping me if you want a short Slack/Email copy of this announcement.
