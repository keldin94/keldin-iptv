from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv")
for rel in ["net/PlaylistSync.java","net/EpgParser.java","data/PlaylistSource.java"]:
 file=p/rel
 print("===== "+rel+" =====")
 for i,line in enumerate(file.read_text().splitlines()):
  print("%4d "%(i+1)+line)
main=(p/"ui/MainActivity.java").read_text().splitlines()
print("===== MainActivity init methods =====")
terms=["private PlaylistSync","new PlaylistSync","onCreate(","onDestroy(","store=new","store =","loadLibrary","Loading library","mainHandler.post","store.load","refreshEpg"]
setlines=set()
for i,line in enumerate(main):
 if any(t in line for t in terms):
  for j in range(max(0,i-7),min(len(main),i+13)):setlines.add(j)
for i in sorted(setlines):
 print("%4d "%(i+1)+main[i])
