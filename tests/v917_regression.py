from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
theme=(base/"ui/ThemeV914.java").read_text()
studio=(base/"ui/StudioHomeV917.java").read_text()
main=(base/"ui/MainActivity.java").read_text()
wizard=(base/"net/PlaylistWizardV6.java").read_text()
epg=(base/"net/EpgParser.java").read_text()
source=(base/"data/PlaylistSource.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
store=(base/"data/CatalogStore.java").read_text()
gradle=Path("app/build.gradle").read_text()
checks={
 "Six themes preserve previous numeric values":
   'CLASSIC=0, CINEMA=1, GUIDE=2, GLASS=3, COMPACT=4, STUDIO=5' in theme,
 "KELDIN Studio selectable and persistent":
   'KELDIN Studio' in theme and 'Math.min(STUDIO,saved)' in theme,
 "Independent Studio hero with real navigation":
   'StudioHomeV917.populate(a,body,nav)' in theme
   and 'nav.go("Uživo")' in studio and 'nav.go("TV vodič")' in studio,
 "Studio media cards cover TV Movies Series Radio Settings":
   all(',"'+p+'"' in studio or '("'+p+'")' in studio
       for p in ["Uživo","Filmovi","Serije","Radio","Postavke"]),
 "Original player implementation not replaced":
   'ThemeV914.stylePlayer(this,overlay)' in player and 'setControls(' in player,
 "Studio appearance includes player and category layouts":
   'theme==STUDIO?0xff111c1b' in theme and
   'theme==STUDIO?0xf1142724' in theme,
 "All saved IPTV lists and five existing themes preserved":
   'isPlaylistActiveV99' in store and 'KELDIN Classic' in theme
   and 'KELDIN Compact' in theme,
 "M3U staged outside evictable Android cache":
   'new File(activity.getFilesDir(),"keldin-import-staging")' in wizard,
 "Staging cleaned only after completion":
   'tempFile.delete();tempFile=null;' in wizard,
 "Missing staged download is retried in background":
   'private File requireStagingV917()' in wizard and
   'new FileInputStream(requireStagingV917())' in wizard,
 "EPG gets downloaded on completed playlist import":
   'backgroundGuideV917.refreshEpg(source' in wizard,
 "EPG auto fetch starts after UI library is visible":
   'mainHandler.postDelayed(this::autoEpgV917,2500)' in main
   and 'new PlaylistSync(this,store)' in main,
 "No synchronous EPG network on the UI thread":
   'sync.refreshEpg(source,(count,status,error)->' in main,
 "EPG queues only active playlists sequentially":
   'store.isPlaylistActiveV99(source.id)' in main and
   'epgQueueV917.pollFirst()' in main and 'nextEpgV917();' in main,
 "EPG refreshes visible channel grid without full rerender":
   'adapter.notifyDataSetChanged();' in main and
   'redrawGuideCardsV917();' in main,
 "M3U XMLTV URL path and query handling":
   'feed.getQuery()' in source and
   '"username".equals(key)' in source and '"password".equals(key)' in source,
 "XMLTV display-name mapping":
   'knownNames.get(normal(channelNameText.toString()))' in epg and
   'aliases.putIfAbsent(sourceChannelId,wantedName)' in epg,
 "Signed in-place update and app identity unchanged":
   "applicationId 'com.keldin.iptv'" in gradle
   and "versionCode 917" in gradle and "versionName '0.9.17'" in gradle,
}
failed=[]
for k,v in checks.items():
 print(("PASS " if v else "FAIL ")+k)
 if not v:failed.append(k)
if failed:raise AssertionError(", ".join(failed))
print("PASS v0.9.17 preserves channels, fast UI and existing player")
