from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv")
catalog=(root/"data/CatalogStore.java").read_text()
main=(root/"ui/MainActivity.java").read_text()
side=(root/"playback/TvSidePanel.java").read_text()
grid=(root/"playback/TvGridPanelV97.java").read_text()
player=(root/"playback/PlayerActivity.java").read_text()
logos=(root/"ui/LogoLoader.java").read_text()
gradle=Path("app/build.gradle").read_text()
checks={
 "Prefs read once per playlist, not per channel":'enabled.contains(c.sourceId)' in catalog and 'for(PlaylistSource src:sources)' in catalog,
 "Source-specific live index":'liveChannelsForSourceV910' in catalog and 'liveIndexV910' in catalog,
 "Invalidated when playlist updated":'liveIndexReadyV910=false' in catalog,
 "Grid uses source index":'store.liveChannelsForSourceV910(active.sourceId)' in grid,
 "Category navigation uses source index":'indexSourceV910();' in side and 'groupLiveV910.get(selectedCategory)' in side,
 "Preview limited to 48 icons":'preview.size()>=48' in side,
 "No full catalog scan while preview focus moves":'for(Channel c:store.channels())' not in side,
 "Bounded asynchronous image work":'new java.util.concurrent.ArrayBlockingQueue<>(24)' in logos and 'newFixedThreadPool' not in logos,
 "Channel switching keeps existing cached group":'cachedLiveGroupV94' in player and 'cachedLiveGroupKeyV94' in player,
 "Browser avoids SHA hashes for unhidden titles":'!hiddenTitles.isEmpty()&&hiddenTitles.contains(' in main,
 "Browser avoids global rescans per category":'filterIndexedV910(' in main and 'sourceItemsV910' in main and 'groupItemsV910' in main,
 "Disabled playlist behavior retained":'isPlaylistActiveV99' in catalog and 'activeSourceIdsV910' in main,
 "Film broadcaster classification unchanged":'isLiveFilmGroup' in main and 'isLiveFilmGroup' in catalog,
 "App identity unchanged":"applicationId 'com.keldin.iptv'" in gradle,
 "Version 0.9.10":'versionCode 910' in gradle and "versionName '0.9.10'" in gradle,
}
for label,passed in checks.items():
    if not passed:raise AssertionError("v0.9.10: "+label)
    print("PASS",label)
