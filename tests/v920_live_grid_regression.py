from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
pager=(base/"ui/PagedLiveGridV920.java").read_text()
catalog=(base/"data/CatalogStore.java").read_text()
adapter=(base/"ui/ChannelAdapter.java").read_text()
player_grid=(base/"playback/TvGridPanelV97.java").read_text()
gradle=Path("app/build.gradle").read_text()
checks={
"Live TV loads indexed channels only, without 180K Movies/Series":
  '"Uživo".equals(page)' in main and
  'store.liveChannelsForSourceV910(store.activePlaylistIdV918())' in main,
"Live TV indexed in the background before UI is shown":
  'prepared.liveChannelsForSourceV910(prepared.activePlaylistIdV918());' in main and
  main.index('prepared.liveChannelsForSourceV910(') < main.index('runOnUiThread(()->{'),
"TV Guide reads only the indexed active source":
  'for(Channel c:store.liveChannelsForSourceV910(' in main,
"Channel adapter starts empty and receives a capped initial window":
  'new ChannelAdapter(store,\n                java.util.Collections.emptyList()' in main
  and 'new PagedLiveGridV920(grid,liveAdapter,gridManager)' in main,
"Page manager maintains a strict 384-card window":
  'private static final int MAX_DISPLAYED=384;' in pager
  and 'end=Math.min(n,first+MAX_DISPLAYED);' in pager
  and 'first=Math.max(0,end-MAX_DISPLAYED)' in pager,
"More channels loaded as needed while scrolling":
  'private void requestMore(boolean downward)' in pager
  and 'end=Math.min(all.size(),end+PAGE);' in pager
  and 'first=Math.max(0,first-PAGE);' in pager,
"Category selection changes bounded channel window":
  'if(channelPagerV920!=null)channelPagerV920.show(filtered);' in main,
"Back to last channel supports far-focus without all cards":
  'channelPagerV920.show(restored,focusIndex)' in main and
  'channelPagerV920.localIndex(focusIndex)' in main,
"Full TV broadcaster group remains in fast Live TV index":
  '&& !Channel.isLiveFilmGroup(c.group,c.url)' in catalog,
"Player popup TV Grid includes broadcasters in EX YU Filmovi & Serije":
  'Channel.isLiveFilmGroup(ch.group,ch.url)' in player_grid,
"Malformed or zero-duration XMLTV does not divide by zero":
  'if(current!=null&&current.end>current.start)' in adapter
  and 'Math.max(1L,current.end-current.start)' in adapter,
"Live TV Java UI exception falls back to playable playlist picker":
  'catch(RuntimeException error)' in main
  and 'page="Moje liste";' in main
  and 'showLists();' in main,
"No changes to stored playlists or signed package identity":
  'activePlaylistIdV918' in catalog
  and "applicationId 'com.keldin.iptv'" in gradle,
"Android version upgraded monotonically":
  'versionCode 920' in gradle and "versionName '0.9.20'" in gradle,
}
failed=[]
for name,pass_ in checks.items():
 print(("PASS " if pass_ else "FAIL ")+name)
 if not pass_:failed.append(name)
if failed:raise AssertionError("v0.9.20: "+"; ".join(failed))
print("PASS Live TV low-memory changes with 384-card paging and safe media import")
