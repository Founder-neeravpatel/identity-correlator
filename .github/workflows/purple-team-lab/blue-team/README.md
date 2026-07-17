# Blue Team

Defensive security practice — SIEM monitoring, detection engineering, and incident response, built primarily around Splunk.

## Focus areas

- **Log monitoring & correlation** — centralizing and correlating logs across endpoints, network, and applications
- **Detection engineering** — writing and tuning detection rules mapped to MITRE ATT&CK techniques (see [`../red-team/detection-mapping.md`](../red-team/detection-mapping.md))
- **Incident response** — triage, containment, eradication, and recovery process
- **Threat hunting** — proactive searches for indicators not caught by existing alerts

## Tooling

| Category | Tools |
|---|---|
| SIEM | Splunk |
| Network monitoring | Wireshark |
| Endpoint monitoring | Sysinternals Suite (Process Monitor, Process Explorer) |
| Threat intel enrichment | VirusTotal, AlienVault OTX |

## Incident Response process followed

1. **Identification** — alert triage, initial validation
2. **Containment** — isolating affected systems
3. **Eradication** — removing root cause
4. **Recovery** — restoring normal operations safely
5. **Lessons Learned** — post-incident report and detection gap analysis

## Detections folder

See [`detections/`](./detections) for documented Splunk search logic mapped to specific attack techniques.

## Case log

| Date | Scenario | Outcome |
|---|---|---|
| _(add entries as exercises are completed)_ | | |
