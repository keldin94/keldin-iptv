from pathlib import Path
import re
base=Path("app/src/main/java/com/keldin/iptv")
terms={
"data/PlaylistSource.java":["guideUrl","playlistUrl","epgUrl"],
"data/CatalogStore.java":["Epg","epg","guide","refresh"],
"ui/MainActivity.java":["epg","Epg","Guide","showGuide","showChannelGrid","getGuide"],
"playback/PlayerActivity.java":["epg","Epg","Guide","requestGuide","guide"],
}
for rel,words in terms.items():
 p=base/rel
 if not p.exists():continue
 lines=p.read_text().splitlines()
 print("===== "+rel+" ("+str(len(lines))+" lines) =====")
 hits=[j for j,line in enumerate(lines) if any(w in line for w in words)]
 selection=set()
 for j in hits[:145]:
  for k in range(max(0,j-3),min(len(lines),j+5)):selection.add(k)
 for k in sorted(selection):
  print("%4d "%(k+1)+lines[k])
print("===== EPG class files =====")
for p in base.rglob("*"):
 if p.suffix==".java" and any(k in p.name.lower() for k in ["epg","guide","xmltv","playlist"]):
  print(str(p),p.stat().st_size)
