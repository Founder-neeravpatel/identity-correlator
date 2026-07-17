# Attack → Detection Mapping

The core purple team artifact: for every offensive technique practiced, the matching detection logic on the blue team side.

| Red Team Technique | MITRE ATT&CK ID | Blue Team Detection Approach |
|---|---|---|
| Network scanning (Nmap) | T1595 | Splunk alert on high volume of connection attempts from single source in short window |
| Brute-force login attempts | T1110 | Failed-login threshold alerting, account lockout monitoring |
| Phishing-based initial access | T1566 | Email gateway log review, suspicious attachment/link detection |
| Privilege escalation attempts | T1068 | Process creation monitoring for unexpected privilege changes |
| Lateral movement (SMB/RDP) | T1021 | Unusual internal authentication pattern alerts |
| Data exfiltration over C2 | T1041 | Outbound traffic baseline deviation, DNS tunneling detection |

_This table grows as new techniques are added to `red-team/` — every entry here should have a corresponding Splunk search or detection rule referenced in `blue-team/detections/`._
