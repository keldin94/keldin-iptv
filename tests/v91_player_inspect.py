from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text().splitlines()
for a,b in [(48,105),(100,161),(154,260),(263,375)]:
 print(f"PLAYER LINES {a}..{b}")
 for i in range(a-1,min(b,len(s))):
  print(f"{i+1:04}: {s[i]}")
