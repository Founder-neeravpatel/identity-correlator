# OSINT Tools

## `identity_correlator.py`

A public username-presence correlator — the automated first pass of the identity resolution step described in [`../README.md`](../README.md). Given a username, it checks whether a matching public profile exists across a set of common platforms (GitHub, Reddit, Instagram, X, TikTok, YouTube, and more).

**What it checks:** only whether a public profile page resolves (HTTP 200 vs. 404). No login, no scraping of content behind authentication, no private data access.

### Usage

```bash
python3 identity_correlator.py <username>
python3 identity_correlator.py <username> --output results.json
```

You'll be asked to confirm authorization before it runs — this is intentional friction, not a bug.

---

## Optional: Apify integration for JS-rendered platforms

Some platforms don't reliably reflect "profile exists" in a plain HTTP status code — they render that client-side with JavaScript. For those cases, this tool can hand off to an [Apify](https://apify.com) Actor (a hosted headless-browser scraper) instead of a raw request.

### Why Apify here

- No need to run/maintain your own headless browser infrastructure
- Apify Store already has pre-built, maintained Actors for major platforms that respect each platform's public data (no login-wall bypassing)
- Fits directly into this repo's CI-style automation pattern — same idea as the `vapt-recon-tool`'s GitHub Actions pipeline, just for scraping instead of testing

### Setup

1. Create a free account at [apify.com](https://apify.com) ✅ (already done)
2. Get your API token: Apify Console → **Settings → Integrations → API tokens**
3. You've already tested the `apify/instagram-scraper` Actor from Apify Store — this is now the tool's default, no extra setup needed
4. Run:
   ```bash
   pip install apify-client
   python3 identity_correlator.py <username> --apify-token YOUR_TOKEN
   ```
   (`--apify-actor` defaults to `apify/instagram-scraper` — only pass it if you want to swap in a different Actor)

This adds a "Instagram (via Apify)" entry to the report with real profile data (follower count, bio, join info) instead of just an existence check — since this Actor reads full public profile info, not just a yes/no.

**Cost note:** this Actor is pay-per-result on Apify (not free per-run) — check current pricing on the Actor's page before running it at scale. Apify's free tier includes limited monthly usage.

### Linking this repo to Apify (auto-rebuild on push)

If you turn this into a full Apify Actor of its own later:

1. Apify Console → **Actors → Develop new → Link a Git repository → GitHub**
2. Authorize Apify to access this repository
3. Select `purple-team-lab` (or a dedicated repo if you split this out)
4. Every push to `main` will automatically rebuild the Actor — no extra config needed

## Ethical & Legal Boundaries

Same boundaries as documented in [`../README.md`](../README.md):
- Publicly available information only — no unauthorized account access
- Every check tied to a legitimate, authorized investigation
- Findings reported through proper legal/client channels, not published with real subject data
