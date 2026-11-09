# El Jumbo IPTV — Family Playlist
A public M3U playlist generated from a curated list of authorised, free-to-access streams. This repository contains no Lionz credentials or protected content.

**M3U URL:** https://raw.githubusercontent.com/MEladl97/El-Jumbo-IPTV/main/El_Jumbo_Free_TV.m3u

## Add or remove channels
Edit `sources/approved_channels.json` with sources that explicitly permit your intended use. The GitHub Action builds the M3U after each edit and once daily. A scheduled rebuild **does not discover new streams or restore broken upstream links**; source changes require maintenance. Playback and territorial availability are not guaranteed.

## Run locally
```sh
python tools/build_playlist.py
```

## Movies and series
M3U is best for linear streams. A legitimate VOD catalogue needs authorised playback sources and a separate API to retain seasons and episodes. TMDB metadata alone does not grant streaming rights.

## Security
Do not commit IPTV usernames, passwords, tokens or signed URLs to this public repository. If you need to inventory an existing subscription, use a local-only tool with environment variables, and export metadata without protected playback URLs.
