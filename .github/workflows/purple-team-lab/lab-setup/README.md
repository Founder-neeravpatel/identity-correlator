# Purple Team Home Lab Setup — Windows (16GB RAM)

This is the practical lab that backs up everything documented in `red-team/`, `blue-team/`, `forensics/`, and `research/`. Every VM here is isolated from your real network and from the internet by default — nothing here can accidentally attack a real target or leak data.

---

## What we're building

| Machine | Role | RAM |
|---|---|---|
| Kali Linux | Attacker machine (red team tools) | 4 GB |
| Metasploitable2 | Deliberately vulnerable target | 1 GB |
| DVWA (Damn Vulnerable Web App) | Web app testing target | runs inside Kali/Docker, ~1 GB |
| Windows 10 Evaluation VM | Windows target + forensics practice | 4 GB |
| Ubuntu + Splunk Free | Blue team — log monitoring / SIEM | 4 GB |

⚠️ **With 16GB total RAM, don't run all 5 at once.** Run 2-3 at a time depending on the exercise (e.g. Kali + Metasploitable2 for a red team exercise; Windows VM + Splunk for a blue team exercise).

---

## STEP 1 — Install the hypervisor (VirtualBox)

1. Go to **https://www.virtualbox.org/wiki/Downloads**
2. Download **"Windows hosts"** version
3. Run the installer, keep default options, finish installation
4. Also download the **VirtualBox Extension Pack** from the same page (needed for USB/network features) — open it, it'll install itself through VirtualBox

---

## STEP 2 — Set up an isolated network (critical safety step)

This ensures your lab VMs can talk to each other but **cannot reach your real home network or the internet** unless you explicitly allow it.

1. Open VirtualBox → **File → Host Network Manager**
2. Click **"Create"** — this makes a Host-Only network (e.g. `vboxnet0`)
3. Leave DHCP enabled on it
4. Every VM you create below, set its network adapter to **"Host-only Adapter"** pointing to this network (instructions per-VM below)

This is the single most important step — it's what makes the lab safe to attack without any real-world risk.

---

## STEP 3 — Kali Linux (Attacker machine)

1. Go to **https://www.kali.org/get-kali/#kali-virtual-machines**
2. Download the **VirtualBox 64-bit image** (comes pre-built, no manual OS install needed)
3. Extract the downloaded file, double-click the `.vbox` file — it opens directly in VirtualBox
4. Before starting it: right-click the VM → **Settings → Network → Adapter 1 → Attached to: Host-only Adapter** → select the network from Step 2
5. Start the VM. Default login: `kali` / `kali`

---

## STEP 4 — Metasploitable2 (Vulnerable target)

This is a deliberately broken Linux VM built specifically for practicing exploitation safely.

1. Go to **https://sourceforge.net/projects/metasploitable/** → download
2. Extract the `.vmdk` file
3. In VirtualBox: **New** → Name it "Metasploitable2" → Type: Linux → Version: Other Linux (64-bit) → 1024 MB RAM
4. When asked for a hard disk, choose **"Use an existing virtual hard disk file"** and select the extracted `.vmdk`
5. Settings → Network → Adapter 1 → **Host-only Adapter** (same network as Kali)
6. Start it. Default login: `msfadmin` / `msfadmin`

**Test the setup:** from Kali, run `ping <metasploitable-ip>` (find its IP by logging into Metasploitable and running `ifconfig`). If it replies, your isolated network is working.

---

## STEP 5 — DVWA (Web app testing target)

Easiest method: run it as a Docker container inside Kali (Kali comes with Docker-friendly tooling).

1. Open a terminal in Kali
2. Install Docker: `sudo apt update && sudo apt install docker.io -y`
3. Run DVWA:
   ```
   sudo docker run -d -p 80:80 vulnerables/web-dvwa
   ```
4. Open a browser inside Kali, go to `http://localhost` — DVWA login page loads (default: `admin` / `password`)

This keeps DVWA fully inside your isolated Kali VM — nothing extra to network-isolate.

---

## STEP 6 — Windows 10 Evaluation VM (Windows target + forensics practice)

Microsoft provides free, legal evaluation VMs for testing.

1. Go to **https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/**
2. Download the **VirtualBox** version of the Windows 10/11 evaluation VM
3. Extract and import it: VirtualBox → **File → Import Appliance** → select the extracted file
4. Settings → Network → Adapter 1 → **Host-only Adapter**
5. Allocate 4096 MB RAM in settings before starting
6. This VM expires after ~90 days (evaluation license) — re-download when it does

Use this VM for: Windows-based exploitation practice, malware analysis (with snapshots — see Step 8), and forensics practice (Sysinternals, Autopsy, Volatility).

---

## STEP 7 — Ubuntu + Splunk Free (Blue team / SIEM)

1. Download Ubuntu Desktop ISO: **https://ubuntu.com/download/desktop**
2. In VirtualBox: **New** → 4096 MB RAM, 25 GB disk → attach the Ubuntu ISO → install normally
3. Network adapter → **Host-only Adapter**
4. Once Ubuntu is installed, download Splunk Free: **https://www.splunk.com/en_us/download/splunk-enterprise.html** (choose the `.deb` package, select "Free" license during setup — 500MB/day ingest limit, plenty for lab use)
5. Install it:
   ```
   sudo dpkg -i splunk*.deb
   sudo /opt/splunk/bin/splunk start --accept-license
   ```
6. Access Splunk's web UI from inside the Ubuntu VM browser at `http://localhost:8000`

Now point your other lab VMs' logs to this Splunk instance (via a universal forwarder, or by manually uploading log files for practice) to build the detections documented in `blue-team/detections/`.

---

## STEP 8 — Snapshots (always do this before any exercise)

Before running any exploit, malware sample, or risky test on any VM:

1. Select the VM in VirtualBox → **Machine → Take Snapshot**
2. Name it something like "clean-state"
3. After your exercise, you can **restore** to this snapshot instantly if anything breaks or gets infected — this is especially critical before malware analysis

---

## Suggested first exercises (to populate your `writeups/` folder)

1. **Red → Blue exercise 1:** Scan Metasploitable2 from Kali with Nmap, exploit one known vulnerable service, then write up how you'd detect that scan/exploit in Splunk
2. **Web exercise:** Run through DVWA's SQL injection and XSS challenges at increasing difficulty settings, document findings
3. **Forensics exercise:** Take a snapshot of the Windows VM, make some file/registry changes, then use Autopsy or Sysinternals to reconstruct what happened — practice for real DFIR case writeups

---

## Safety reminders

- Never set any lab VM's network adapter to **"Bridged"** — that exposes it to your real network
- Never download or run malware samples outside an isolated, snapshotted VM
- Keep host-only network fully separate from any client work — this lab is for practice only
