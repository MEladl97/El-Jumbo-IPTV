#!/usr/bin/env python3
"""Local-only Xtream catalogue inventory. Does not download or export playback URLs."""
import collections, getpass, json, os, pathlib, urllib.parse, urllib.request
base=input("Xtream server URL (https preferred): ").strip().rstrip("/")
user=input("Username: ").strip()
password=getpass.getpass("Password (not saved): ")
out=pathlib.Path("lionz_inventory.json")
if not base.startswith(("https://","http://")): raise SystemExit("Invalid URL")
def api(action):
    q=urllib.parse.urlencode({"username":user,"password":password,"action":action})
    req=urllib.request.Request(base+"/player_api.php?"+q,headers={"User-Agent":"ElJumboInventory/1.0"})
    with urllib.request.urlopen(req,timeout=35) as resp:
        data=json.load(resp)
    if not isinstance(data,list): raise ValueError("Unexpected API response for "+action)
    return data
mapping={"live":"get_live_streams","movies":"get_vod_streams","series":"get_series"}
inventory={"note":"Metadata only. No credentials, tokens or playback URLs.","categories":{},"counts":{}}
for kind,action in mapping.items():
    try:
        entries=api(action)
        names=sorted(set(str(x.get("name") or x.get("title") or "").strip() for x in entries if x.get("name") or x.get("title")))
        inventory["categories"][kind]=names
        inventory["counts"][kind]=len(entries)
        print(kind,len(entries))
    except Exception as e:
        inventory["categories"][kind]=[]
        inventory["counts"][kind]=None
        print(kind,"failed:",type(e).__name__)
out.write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding="utf-8")
print("Saved metadata-only inventory:",out.resolve())
print("Keep this file private; do not upload it to a public repository without reviewing it.")
