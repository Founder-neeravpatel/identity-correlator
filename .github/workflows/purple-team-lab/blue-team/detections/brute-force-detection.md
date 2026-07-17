# Detection: Brute-Force Login Attempts

**Maps to:** Red Team technique — Brute-force login attempts (MITRE T1110)

## Objective
Detect repeated failed authentication attempts against a single account or from a single source within a short time window, which typically indicates a brute-force or credential-stuffing attempt.

## Splunk search logic (conceptual)

```
index=auth_logs action=failure
| bucket _time span=5m
| stats count by src_ip, user, _time
| where count > 10
```

## Logic explanation
- Filters authentication logs for failed login events
- Groups failures into 5-minute windows by source IP and target username
- Flags any grouping exceeding a threshold of 10 failures — tunable based on baseline traffic

## Response playbook
1. Validate the alert isn't a false positive (e.g. misconfigured service account)
2. Check if the source IP has succeeded after failures — possible successful compromise
3. Temporarily block/rate-limit the source IP at the firewall/WAF
4. Force password reset if account shows any successful login post-brute-force window

## Tuning notes
- Threshold should be adjusted per environment traffic baseline
- Consider allow-listing known internal scanning/monitoring tools to reduce noise
