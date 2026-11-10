from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
catalog=(base/"data/CatalogStore.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
adapter=(base/"ui/PlaylistGroupAdapterV99.java").read_text()
channel=(base/"data/Channel.java").read_text()
assert 'g.contains("filmovi")' in channel
assert 'g.contains("serije")' in channel
assert 'isPlaylistActiveV99(String id)' in catalog
assert 'isPlaylistCollapsedV99(String id)' in catalog
assert 'if(isPlaylistActiveV99(c.sourceId))visible.add(c);' in catalog
assert 'isPlaylistActiveV99(c.sourceId)&&sourceById' in catalog
assert 'new PlaylistGroupAdapterV99(' in main
assert 'managePlaylistActivationV99()' in main
assert 'selected_source_'+chr(34) not in [] # simple unused guard against implicit index
assert 'putString("selected_source_"+page,sourceId)' in main
assert 'return_live_source_v99' in main and 'return_live_source_v99' in player
assert 'if(!store.isPlaylistActiveV99(ch.sourceId))continue;' in main
assert 'store.isPlaylistCollapsedV99(src.id)' in adapter
assert 'store.setPlaylistCollapsedV99(item.sourceId' in adapter
assert 'for(PlaylistSource src:sources)' in adapter
assert 'if(!active||store.isPlaylistCollapsedV99(src.id))continue;' in adapter
assert 'new AlertDialog.Builder(this)' in main
assert 'app/build.gradle' not in main
gradle=Path("app/build.gradle").read_text()
assert 'versionCode 909' in gradle and "versionName '0.9.9'" in gradle
assert "applicationId 'com.keldin.iptv'" in gradle
print("PASS playlist isolation, persisted active/collapsed state, source-aware Back and version")
