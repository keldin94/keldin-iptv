from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
catalog=(base/"data/CatalogStore.java").read_text()
main=(base/"ui/MainActivity.java").read_text()
gradle=Path("app/build.gradle").read_text()

checks={
 "Binary cache validated against JSONL file size and timestamp":
    'in.readLong()!=json.length()' in catalog and 'in.readLong()!=json.lastModified()' in catalog,
 "Fast snapshot read before legacy JSON parsing":
    catalog.index('loadFastV912(lines)') < catalog.index('new java.io.BufferedReader('),
 "Original JSONL fallback preserved":
    'while((line=input.readLine())!=null&&channels.size()<350000)' in catalog,
 "Cache write is atomic via temporary file":
    'catalog-v912.tmp' in catalog and 'tmp.renameTo(dest)' in catalog,
 "Synchronous binary migration avoided":
    'new Thread(' in catalog and '"keldin-fast-library"' in catalog,
 "Cache updates when playlist data changes":
    'writeFastV912(dest,new java.util.ArrayList<>(channels))' in catalog,
 "Concurrent snapshot writes serialized":
    'synchronized(FAST_CACHE_LOCK_V912)' in catalog,
 "Shared source/category strings pooled":
    'poolStringV912(in.readUTF(),groupsPool)' in catalog and 'poolStringV912(o.optString("group","Ostalo"),groupPool)' in catalog,
 "Last watched channel found in one pass":
    'priority.putIfAbsent(recent.get(i),i)' in catalog and 'Integer at=priority.get(c.key())' in catalog,
 "Startup no longer copies all channels just to test empty":
    'store.hasAnyActiveChannelsV912()' in main,
 "Recent channel lookup off UI thread":
    '"keldin-startup-last-channel"' in main and 'store.lastLiveChannel();' in main,
 "Avoid autoplay if user navigated away":
    'initialNavigationV912!=navigationGenerationV911' in main,
 "Keep active/inactive source preferences":
    'isPlaylistActiveV99' in catalog,
 "Preserve package ID for in-place update":
    "applicationId 'com.keldin.iptv'" in gradle,
 "Version incremented":'versionCode 912' in gradle and "versionName '0.9.12'" in gradle,
}
for label,ok in checks.items():
    if not ok:raise AssertionError("v0.9.12 regression: "+label)
    print("PASS",label)
