from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv")
catalog=(p/"data/CatalogStore.java").read_text()
main=(p/"ui/MainActivity.java").read_text()
group=(p/"ui/PlaylistGroupAdapterV99.java").read_text()
player=(p/"playback/PlayerActivity.java").read_text()
for name,code,keys in [
 ("CatalogStore",catalog,["public synchronized void load","public synchronized List<Channel> channels","private void loadChannels","private void saveChannels","public synchronized void updateChannels","public synchronized List<PlaylistSource> sources","public synchronized Channel lastLiveChannel","isPlaylistActiveV99","loadFastV912","writeFastV912","public synchronized void putSource"]),
 ("MainActivity",main,["private void managePlaylistActivationV99","private void showLists","private void editSource","private void showChannelGrid","private void play(","private void autoEpgV917","private void navigate","onCreate(Bundle"]),
 ("PlaylistGroupAdapter",group,["public PlaylistGroupAdapterV99","public void onBindViewHolder"]),
 ("PlayerActivity",player,["private void changeChannel","onCreate(Bundle","private void requestGuideIfNeeded"])]:
    print("========= "+name+" ========")
    lines=code.splitlines()
    for key in keys:
        for i,line in enumerate(lines):
            if key in line:
                print("---- "+key+" @ "+str(i+1))
                begin=max(0,i-3);end=min(len(lines),i+65)
                for j in range(begin,end):print(f"{j+1:4d}: "+lines[j])
                break
