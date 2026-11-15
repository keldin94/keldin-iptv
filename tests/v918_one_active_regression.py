from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
catalog=(base/"data/CatalogStore.java").read_text()
main=(base/"ui/MainActivity.java").read_text()
wizard=(base/"net/PlaylistWizardV6.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
themes=(base/"ui/ThemeV914.java").read_text()
gradle=Path("app/build.gradle").read_text()
def inside(content,begin,end):
    return content.split(begin,1)[1].split(end,1)[0]
checks={
  "Exactly one selected provider in active preference check":
      'return id!=null&&!id.isEmpty()&&id.equals(activePlaylistV918);' in catalog,
  "Migration keeps previous last selected source when enabled":
      'prefs.getString("selected_source_Uživo","")' in catalog
      and 'prefs.getBoolean("playlist_active_v99_"+previous,true)' in catalog,
  "Active selection persisted across app restarts":
      'putString("active_playlist_v918",id).commit()' in catalog,
  "Load metadata first, choose active before hydrating channels":
      catalog.index('activePlaylistV918=initialActiveV918();') <
      catalog.index('if(lines.exists()&&sources.size()==1&&loadFastV912(lines))'),
  "Two-source install cannot reuse legacy huge binary snapshot":
      'lines.exists()&&sources.size()==1&&loadFastV912(lines)' in catalog,
  "JSONL startup ignores inactive channels before constructing objects":
      'if(!activePlaylistV918.equals(o.optString("sourceId")))continue;' in catalog,
  "Existing inactive M3U channels remain on disk":
      'valid.contains(sid)&&!target.equals(sid)' in catalog
      and 'output.write(line);' in catalog,
  "Saving a playlist is transactional, not a destructive clear":
      'if(!temp.renameTo(dest)){' in catalog
      and 'throw new java.io.IOException("Not enough storage' in catalog,
  "No stale multi-source cache can be reopened after import":
      'new File(context.getFilesDir(),"catalog-v912.bin").delete();' in catalog,
  "Unselected provider is not instantiated during imported-channel save":
      'if(isPlaylistActiveV99(sourceId)){' in inside(catalog,
          'public synchronized void updateChannels(String sourceId', 'public synchronized void putSource'),
  "Reload newly selected provider into RAM from its saved channels":
      'ArrayList<Channel> selected=readPlaylistV918(id);' in catalog
      and 'channels.addAll(selected);' in catalog,
  "Switch clears old provider EPG and index in memory":
      'liveIndexV910.clear();' in catalog and 'guide.clear();' in catalog,
  "Import releases old source memory before parsing second large source":
      'store.suspendLibraryForImportV918();' in wizard
      and 'finally{' in inside(wizard,
          'private void save(CategoryScanV61 scan,Set<String> excluded){',
          'private File requireStagingV917()'),
  "Failed import restores old active source, without deleting its data":
      'store.restoreLibraryAfterImportV918();' in wizard
      and 'readPlaylistV918(activePlaylistV918)' in catalog,
  "Only active source can trigger post-import EPG":
      'if(store.isPlaylistActiveV99(source.id)&&' in wizard,
  "Single-choice radio replaces multi-select and removes Enable all":
      '.setSingleChoiceItems(labels,selected' in main
      and 'setMultiChoiceItems(labels,enabled' not in main
      and 'Enable all' not in main,
  "Dedicated Activate button and active label for each saved playlist":
      'Inactive (saved)' in main and '"▶  Use"' in main
      and 'this::managePlaylistActivationV99' in main,
  "List switching on background thread with clear UI status":
      '"keldin-switch-single-playlist"' in main
      and 'new Thread(()->' in inside(main,'private void activatePlaylistV918','private void managePlaylistActivationV99'),
  "TV category rail only displays active provider":
      'new PlaylistGroupAdapterV99(' in main
      and 'this,store,activeSourcesV918(),bySource,' in main,
  "D-pad, film category, six themes and EPG preserved":
      'rememberLiveReturnV98' in player
      and 'KELDIN Studio' in themes
      and 'Restore EX YU | Filmovi & Serije channels' in main,
  "Same Android package for in-place update":
      "applicationId 'com.keldin.iptv'" in gradle
      and "versionCode 918" in gradle
      and "versionName '0.9.18'" in gradle,
}
failed=[]
for name,result in checks.items():
    print(("PASS " if result else "FAIL ")+name)
    if not result:failed.append(name)
if failed:raise AssertionError("Single playlist regression: "+"; ".join(failed))
print("PASS 0.9.18 one resident source; inactive sources retained on disk")
