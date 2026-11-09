#!/usr/bin/env python3
"""Generate an M3U from explicitly approved, publicly playable stream entries."""
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "sources" / "approved_channels.json"
output = ROOT / "El_Jumbo_Free_TV.m3u"
channels = json.loads(source.read_text(encoding="utf-8"))
lines = ["#EXTM3U"]
for channel in channels:
    url = channel["url"].strip()
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f"Invalid or non-HTTPS URL for {channel['name']}")
    if any(x in url.lower() for x in ("username=", "password=", "token=", "apikey=", "api_key=")):
        raise ValueError(f"Possible credential in URL for {channel['name']}")
    def clean(value):
        return str(value).replace("\n", " ").replace("\r", " ").replace('"', "'")
    name = clean(channel["name"])
    group = clean(channel.get("group", "Free TV"))
    tvgid = clean(channel.get("tvg_id", ""))
    lines.extend([f'#EXTINF:-1 tvg-id="{tvgid}" group-title="{group}",{name}', url])
output.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {len(channels)} channels to {output.name}")
