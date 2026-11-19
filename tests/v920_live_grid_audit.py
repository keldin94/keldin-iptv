from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv")
files=["ui/MainActivity.java","ui/ChannelAdapter.java","playback/TvGridPanelV97.java","net/PlaylistSync.java","data/CatalogStore.java","data/Channel.java"]
def method(s,name):
    i=s.find(name)
    if i<0:return "[NOT FOUND: "+name+"]"
    beg=s.find("{",i)
    if beg<0:return "[NO BODY: "+name+"]"
    depth=1;k=beg+1
    while depth and k<len(s):
        if s[k]=="{":depth+=1
        elif s[k]=="}":depth-=1
        k+=1
    return s[i:k]
for rel in files:
 p=root/rel
 print("===",rel,"exists",p.exists())
 if not p.exists():continue
 s=p.read_text()
 print("LINES",s.count("\n"))
 names={
 "ui/MainActivity.java":["private void showChannelGrid(boolean guideMode)","private void showGuide()","private void play(Channel","private void activatePlaylistV918","private void onResume()"],
 "ui/ChannelAdapter.java":["public ChannelAdapter","onBindViewHolder","public void setItems","public int getItemCount"],
 "playback/TvGridPanelV97.java":["public void open(","private void render","void show","public boolean handleKey","public void hide"],
 "net/PlaylistSync.java":["public void importLocal(","public void refresh(","public void refreshEpg("],
 "data/CatalogStore.java":["public synchronized Channel channelByKey(","public synchronized Channel find","public synchronized void updateChannels","public synchronized void activatePlaylistV918","public synchronized List<Channel> channels()"],
 "data/Channel.java":["public String key()"],
 }[rel]
 for name in names:
  snippet=method(s,name)
  if "PlaylistSync" in rel and "refreshEpg" in name:snippet=snippet[:5000]
  print("--",name,"\n",snippet[:16000])
