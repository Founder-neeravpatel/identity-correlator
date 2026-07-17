# Red Team

Offensive security practice — methodology and tooling categories used across engagements and lab exercises. Practiced in isolated labs, CTF platforms (TryHackMe, HackTheBox), and authorized client environments only.

## Methodology followed

1. **Reconnaissance** — passive and active information gathering on the target scope
2. **Scanning & Enumeration** — mapping live hosts, open ports, services, versions
3. **Vulnerability Identification** — matching enumerated services against known weaknesses
4. **Exploitation** — controlled proof-of-concept exploitation within engagement scope
5. **Post-Exploitation** — privilege escalation, lateral movement assessment (scope-permitting)
6. **Reporting** — findings mapped to CVSS severity, with remediation guidance

## Tool categories used

| Phase | Tool categories (examples) |
|---|---|
| Recon | Subdomain enumeration, WHOIS/DNS tooling, Shodan/Censys |
| Scanning | Nmap, service/version detection scanners |
| Web App Testing | Burp Suite, OWASP ZAP |
| Exploitation | Metasploit Framework, manual PoC scripting |
| Post-Exploitation | Privilege escalation checklists, lateral movement mapping |
| Reporting | CVSS scoring, structured VAPT report templates |

## Notes

- Every technique practiced here is cross-referenced in [`blue-team/`](../blue-team) with the corresponding detection approach — see `detection-mapping.md`.
- No exploit code or weaponized payloads are published in this repository. Findings and methodology only.

## Case log

| Date | Environment | Scope | Summary |
|---|---|---|---|
| _(add entries as exercises are completed)_ | | | |
