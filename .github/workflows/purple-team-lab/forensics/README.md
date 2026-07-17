# Digital Forensics

Digital forensics workflow followed for incident investigations, cyber crime cases, and evidence handling — built to hold up to legal/compliance scrutiny.

## Process followed

1. **Identification** — determine what evidence exists and where (devices, logs, cloud accounts, memory)
2. **Preservation** — create forensic images/hashes before any analysis; original evidence is never analyzed directly
3. **Chain of custody** — every person who handles evidence, and when, is logged (see `chain-of-custody-template.md`)
4. **Analysis** — static and memory forensics, timeline reconstruction, artifact recovery
5. **Documentation** — findings recorded with method, tool, and version used, so results are reproducible
6. **Reporting** — structured report suitable for legal proceedings or internal stakeholders

## Tool categories

| Purpose | Tools |
|---|---|
| Disk imaging & analysis | Autopsy, FTK Imager |
| Memory forensics | Volatility |
| Network forensics | Wireshark |
| Mobile/APK analysis | MobSF |
| File carving | Foremost, PhotoRec |

## Chain of custody

See [`chain-of-custody-template.md`](./chain-of-custody-template.md) — used on every case involving physical or digital evidence handoff.

## Case log

| Date | Case type | Evidence type | Outcome |
|---|---|---|---|
| _(add entries as exercises/cases are completed — keep anonymized)_ | | | |
