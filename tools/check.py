#!/usr/bin/env python3
"""Checks the plugin payload against Plugin Hub's rules and the live APIs."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = ROOT / "hackernews.crosspoint-plugin"
OFFLINE = "--offline" in sys.argv
errors = []


def check(ok, message):
    print(("ok   " if ok else "FAIL ") + message)
    if not ok:
        errors.append(message)


def fetch(url, headers=None):
    # curl, because some Python installs ship without usable root certificates.
    command = ["curl", "--silent", "--show-error", "--fail", "--max-time", "30"]
    for name, value in (headers or {}).items():
        command += ["--header", f"{name}: {value}"]
    return subprocess.run(command + [url], check=True, capture_output=True).stdout


manifest = json.loads((PAYLOAD / "manifest.json").read_text())
device_raw = (PAYLOAD / "device.json").read_bytes()
device = json.loads(device_raw)

check(PAYLOAD.name == manifest["name"] + ".crosspoint-plugin", "payload folder matches manifest name")
check(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]) is not None, "version is MAJOR.MINOR.PATCH")
check(device.get("version") == manifest["version"], "device.json version matches manifest")
for name in manifest["files"]:
    safe = not name.startswith("/") and ".." not in name and "\\" not in name
    check(safe and (PAYLOAD / name).is_file(), f"declared file exists: {name}")
on_disk = sorted(p.relative_to(PAYLOAD).as_posix() for p in PAYLOAD.rglob("*") if p.is_file())
check(on_disk == sorted(manifest["files"]), "every payload file is declared in manifest files")
check(len(device_raw) < 8192, f"device.json is under 8 KB ({len(device_raw)} bytes)")
check(1 <= device["browse"]["page_size"] <= 16, "page_size is between 1 and 16")
readme = (PAYLOAD / "README.md").read_bytes()
check(len(readme) <= 16384 and readme.isascii(), "payload README is plain ASCII and under 16 KB")

if not OFFLINE:
    browse = device["browse"]
    size = browse["page_size"]
    feeds = {"Front Page": browse["url"], "Search": browse["search"]["url"]}
    feeds.update({entry["title"]: entry["url"] for entry in browse["lists"] if "url" in entry})
    first_url = None
    for title, template in feeds.items():
        url = template.replace("{offset}", "0").replace("{limit}", str(size + 1)).replace("{query}", "rust")
        try:
            hits = json.loads(fetch(url))[browse["items"]]
            titled = [hit for hit in hits if hit.get(browse["fields"]["title"])]
            check(0 < len(titled) <= size + 1, f"{title}: {len(titled)} stories")
            first_url = first_url or next((hit["url"] for hit in titled if hit.get("url")), None)
        except Exception as error:  # report and keep checking the other feeds
            check(False, f"{title}: {error}")
    if first_url:
        try:
            text = fetch(device["download"]["url"].replace("{url}", first_url), device["download"]["headers"])
            check(len(text) > 200, f"article download returned {len(text)} bytes of text")
        except Exception as error:
            check(False, f"article download: {error}")

sys.exit(1 if errors else 0)
