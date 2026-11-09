#!/usr/bin/env python3
"""Build a discovery playlist from public IPTV-org country/language feeds.
Public accessibility does not establish licensing or reliability.
Never adds authenticated or tokenised links.
"""
import urllib.request, urllib.parse, pathlib, re
root=pathlib.Path(__file__).resolve().parents[1]
sources={
"Egypt":"https://iptv-org.github.io/iptv/countries/eg.m3u",
"Arabic":"https://iptv-org.github.io/iptv/languages/ara.m3u",
"UAE":"https://iptv-org.github.io/iptv/countries/ae.m3u",
}
out=["#EXTM3U"]
seen=set()
for group,url in sources.items():
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"ElJumboFamily/1.0"})
        with urllib.request.urlopen(req,timeout=30) as response:
            lines=response.read(5_000_000).decode("utf-8-sig","replace").splitlines()
        for idx,line in enumerate(lines[:-1]):
            if not line.startswith("#EXTINF:"): continue
            stream=lines[idx+1].strip()
            parsed=urllib.parse.urlsplit(stream)
            if parsed.scheme!="https" or not parsed.netloc or parsed.username or parsed.password: continue
            if any(k in urllib.parse.parse_qs(parsed.query) for k in ("username","password","token","key","auth","apikey")): continue
            if stream in seen: continue
            seen.add(stream)
            info=line.replace("\r","").replace("\n","")
            info=re.sub(r'group-title="[^"]*"',f'group-title="{group}"',info)
            if 'group-title=' not in info: info=info.replace("#EXTINF:",f'#EXTINF:-1 group-title="{group}",',1) if False else info.replace(",",f' group-title="{group}",',1)
            out.extend([info,stream])
        print(group,"processed")
    except Exception as error:
        print(group,"unavailable:",type(error).__name__)
if len(out)==1: raise SystemExit("No upstream feeds available; keeping previous playlist")
(root/"El_Jumbo_Discovery.m3u").write_text("\n".join(out)+"\n",encoding="utf-8")
print("Total unique streams",len(seen))
