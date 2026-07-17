#!/usr/bin/env python3
"""
Identity Correlator — Public Username Presence Checker
Author: Neerav Patel

Checks whether a given username exists on a range of public platforms by
querying each platform's public profile URL and reading the HTTP response.
This is the "identity resolution" step of the OSINT methodology documented
in ../README.md — used to build a picture of a subject's public digital
footprint using only publicly available information.

ETHICAL / LEGAL NOTICE:
- Only checks whether a public profile URL resolves — no login, no
  authentication bypass, no scraping of content behind a login wall.
- Use only for authorized investigations (client engagements, law
  enforcement requests, or your own accounts for testing).
- This tool does not access, store, or exfiltrate private data.

Optional Apify integration:
For platforms that require JavaScript rendering to confirm a profile
(rather than a simple HTTP status check), this script can hand off to an
Apify Actor via the Apify API instead of a raw request — see
`check_via_apify()` below. This keeps the core tool dependency-free while
allowing a heavier headless-browser check when needed.
"""

import argparse
import json
import socket
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

TIMEOUT = 6

# Each entry: platform name -> profile URL template using {username}
# All of these are PUBLIC profile pages — no API keys or auth required.
PLATFORMS = {
    "GitHub": "https://github.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Instagram": "https://www.instagram.com/{username}/",
    "X (Twitter)": "https://x.com/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "Medium": "https://medium.com/@{username}",
    "Pinterest": "https://www.pinterest.com/{username}/",
    "Telegram": "https://t.me/{username}",
    "YouTube": "https://www.youtube.com/@{username}",
    "Twitch": "https://www.twitch.tv/{username}",
    "Steam": "https://steamcommunity.com/id/{username}",
    "HackerNews": "https://news.ycombinator.com/user?id={username}",
}


def check_platform(name, url_template, username):
    url = url_template.format(username=username)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (identity-correlator OSINT tool)"}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.getcode()
        exists = status == 200
        return {"platform": name, "url": url, "status": status, "exists": exists}
    except urllib.error.HTTPError as e:
        # A 404 cleanly means "not found" — that's a normal, expected result
        return {"platform": name, "url": url, "status": e.code, "exists": e.code == 200}
    except (urllib.error.URLError, socket.timeout, Exception) as e:
        return {"platform": name, "url": url, "status": None, "exists": None, "error": str(e)}


def check_via_apify(username, apify_token, actor_id="apify/instagram-scraper"):
    """
    Hand off a profile check to an Apify Actor for platforms that need
    JavaScript rendering to confirm a profile exists.

    Default actor_id targets the public "apify/instagram-scraper" Actor,
    which reads public Instagram profile data with no login required.
    Input schema for that Actor: {"usernames": [...], "resultsType": "userInfo"}

    If you swap in a different Actor, check its own Input tab in Apify
    Console for the correct field names — schemas vary between Actors.

    Requires: pip install apify-client
    """
    try:
        from apify_client import ApifyClient
    except ImportError:
        return {"platform": "Apify", "error": "apify-client not installed — run: pip install apify-client"}

    client = ApifyClient(apify_token)
    run_input = {"usernames": [username], "resultsType": "userInfo"}
    run = client.actor(actor_id).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    exists = len(items) > 0 and not items[0].get("error")
    return {
        "platform": "Instagram (via Apify)",
        "apify_run_id": run.get("id"),
        "exists": exists,
        "profile_data": items[0] if items else None,
    }


def correlate(username, max_workers=8):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(check_platform, name, tmpl, username): name
            for name, tmpl in PLATFORMS.items()
        }
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda r: r["platform"])


def print_report(username, results):
    found = [r for r in results if r.get("exists")]
    not_found = [r for r in results if r.get("exists") is False]
    errored = [r for r in results if r.get("exists") is None]

    print(f"\n=== Identity Correlation Report: '{username}' ===")
    print(f"Scan time: {datetime.now(timezone.utc).isoformat()}\n")

    print(f"[+] Found on {len(found)} platform(s):")
    for r in found:
        print(f"    {r['platform']:<15} {r['url']}")

    print(f"\n[-] Not found on {len(not_found)} platform(s)")
    if errored:
        print(f"[!] Could not check {len(errored)} platform(s) (network/blocking issues):")
        for r in errored:
            print(f"    {r['platform']:<15} {r.get('error','unknown error')}")


def save_json(username, results, path):
    with open(path, "w") as f:
        json.dump({"username": username, "results": results,
                    "scan_time": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Identity Correlator — check public username presence across platforms. "
                     "Authorized OSINT investigations only."
    )
    parser.add_argument("username", help="Username to check across platforms")
    parser.add_argument("--output", help="Save results to a JSON file")
    parser.add_argument("--apify-token", help="Optional: Apify API token to enable Instagram profile check")
    parser.add_argument("--apify-actor", default="apify/instagram-scraper",
                         help="Apify Actor ID to use (default: apify/instagram-scraper)")
    args = parser.parse_args()

    print("[*] Ethical use reminder: only investigate subjects you are authorized to.")
    confirm = input("    Type 'yes' to continue: ").strip().lower()
    if confirm != "yes":
        print("[!] Aborted — authorization not confirmed.")
        return

    results = correlate(args.username)

    if args.apify_token:
        print("[*] Running Instagram check via Apify (apify/instagram-scraper)...")
        apify_actor = args.apify_actor or "apify/instagram-scraper"
        apify_result = check_via_apify(args.username, args.apify_token, apify_actor)
        results.append(apify_result)

    print_report(args.username, results)

    if args.output:
        save_json(args.username, results, args.output)
        print(f"\n[+] JSON report saved: {args.output}")


if __name__ == "__main__":
    main()
