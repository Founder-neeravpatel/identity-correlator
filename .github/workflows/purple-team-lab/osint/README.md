# OSINT & Social Media Investigation

Open-source intelligence methodology used to support cyber crime investigations, fraud cases, and digital forensics work. This section documents **methodology and tool categories**, not investigation results tied to real, identifiable individuals — case-specific findings stay in client reports, not this public repo.

## Methodology

1. **Scoping** — define what's being investigated and what's in/out of scope (legal and ethical boundaries set first)
2. **Identity resolution** — correlating usernames, emails, and profiles across platforms using publicly available information only
3. **Timeline reconstruction** — building a chronological picture of publicly posted activity relevant to the case
4. **Verification** — cross-referencing findings across multiple independent sources before treating anything as fact
5. **Reporting** — structured findings suitable for handover to legal teams or law enforcement, with sources documented

## Tool categories

| Purpose | Examples |
|---|---|
| Username correlation | Sherlock, WhatsMyName |
| People/entity link analysis | Maltego |
| Reverse image search | Google Images, TinEye |
| Domain/WHOIS intelligence | WHOIS lookups, Shodan |
| Archive lookups | Wayback Machine |
| Metadata extraction | ExifTool |

## Ethical & legal boundaries

- Work is limited to publicly available information — no unauthorized account access, social engineering of targets, or data purchased from breach markets
- Every investigation is tied to a legitimate case (client engagement, law enforcement request, or authorized internal investigation)
- Findings are reported through proper legal/client channels, not published

## Case log

| Date | Case type | Outcome |
|---|---|---|
| _(add entries as exercises/cases are completed — keep anonymized)_ | | |

## Tooling

See [`tools/`](./tools) — an automated identity correlator built for the identity resolution step above, with optional Apify integration for JavaScript-rendered platform checks.
