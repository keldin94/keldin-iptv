from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv")
main=(root/"ui/MainActivity.java").read_text()
catalog=(root/"data/CatalogStore.java").read_text()
logos=(root/"ui/LogoLoader.java").read_text()
gradle=Path("app/build.gradle").read_text()

checks={
 "Home detaches large live/film/series grids":'releaseHeavyBrowseV911();' in main
    and 'activeGridV911.setAdapter(null);' in main
    and 'activeCategoryListV911.setAdapter(null);' in main,
 "Browse adapter refs registered":'activeGridV911=grid;' in main
    and 'activeCategoryListV911=categories;' in main,
 "Home releases source channel index":'store.clearLiveIndexV911();' in main
    and 'public synchronized void clearLiveIndexV911()' in catalog,
 "Home not redrawn again during onResume":'("Početna".equals(page)||"Favoriti".equals(page))' not in main
    and 'if(store!=null && content!=null && "Favoriti".equals(page))render();' in main,
 "Playback return only when navigation unchanged":'expectedNavigationV911!=navigationGenerationV911' in main
    and 'navigationGenerationV911++;' in main,
 "UI data retained":'setPlaylistActiveV99' in catalog
    and 'selected_source_' in main
    and 'return_live_pending_v98' in main,
 "Reduce static image cache in RAM":'new LruCache<String,Bitmap>(6*1024)' in logos,
 "Unchanged package identity":"applicationId 'com.keldin.iptv'" in gradle,
 "Incremental Android update":'versionCode 911' in gradle and "versionName '0.9.11'" in gradle,
}
for label,ok in checks.items():
    if not ok:raise AssertionError("Home v0.9.11 regression: "+label)
    print("PASS",label)
print("PASS lightweight Home on repeated returns without deleting saved playlist data")
