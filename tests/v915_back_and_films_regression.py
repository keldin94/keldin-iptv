from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
wizard=(base/"net/PlaylistWizardV6.java").read_text()
channel=(base/"data/Channel.java").read_text()
scan=(base/"net/CategoryScanV61.java").read_text()
themes=(base/"ui/ThemeV914.java").read_text()
gradle=Path("app/build.gradle").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
checks={
 "Back does not rebuild full Live TV UI in onResume":
   'if("Uživo".equals(page)){' in main and
   'selectedSourceV99=prefs.getString("return_live_source_v99","");' in main and
   'page="Uživo";\n            selectedGroup=playedGroup;' not in main,
 "Last watched source and category are persisted":
   '.putString("selected_group_Uživo",playedGroup)' in main and
   '.putString("selected_source_Uživo",' in main and
   'return_live_key_v98' in main,
 "Back restores the channel via existing grouped index, not full render":
   'restoreLiveSelectionV915.accept(selectedSourceV99,selectedGroup)' in main
   and 'filterIndexedV910(' in main
   and 'item.itemView.requestFocus()' in main,
 "Live return callback cleared on navigation away":
   'if(!"Uživo".equals(destination))restoreLiveSelectionV915=null;' in main,
 "No synchronous live index purge on Home":
   'store.clearLiveIndexV911();' not in main,
 "Back into existing Home does not delete favorites or channel catalog":
   'store.clearLiveIndexV911();' not in main and 'store.updateChannels(' not in main.split('private void showHome() {')[1].split('private void landingTile(')[0],
 "Visible film category recovery inside Live TV":
   '"Restore EX YU | Filmovi & Serije channels"' in main and
   'this::restoreFilmChannelsV915' in main,
 "Recovery uses existing playlist import wizard":
   'new com.keldin.iptv.net.PlaylistWizardV6(this,store,chosen,' in main,
 "Recovery only includes active playlists":
   'if(store.isPlaylistActiveV99(src.id))active.add(src);' in main,
 "Wizard can force re-enable previously excluded Live TV":
   'if(recoverFilmChannelsV915&&i==0)enabled[i]=true;' in wizard,
 "Wizard preselects only film broadcaster category":
   'if(recoverFilmChannelsV915&&com.keldin.iptv.data.Channel.isLiveFilmGroup(' in wizard,
 "Other category exclusions remain intact":
   'enabled[i+4]=old.isEmpty() ? (!huge||local) : !old.contains(name);' in wizard and
   'store.setExcludedGroups(source.id,excluded)' in wizard,
 "Previous saved data remains until successful reimport":
   'store.updateChannels(source.id,chosen.channels)' in wizard and
   'if(chosen.channels.isEmpty())throw' in wizard,
 "Exact EX YU live group recognized":
   'g.contains("filmovi")' in channel and
   'g.contains("serije")' in channel and
   'isLiveFilmGroup(group,url)' in scan,
 "Theme support preserved":
   'ThemeV914.showHome(this,content,store,' in main and
   'KELDIN Cinema' in themes,
 "Shared TV player unchanged":
   'rememberLiveReturnV98' in player,
 "Same app identity and preserved install data":
   "applicationId 'com.keldin.iptv'" in gradle and
   'versionCode 915' in gradle and "versionName '0.9.15'" in gradle,
}
failed=[]
for name,ok in checks.items():
    print(("PASS " if ok else "FAIL ")+name)
    if not ok:failed.append(name)
if failed:raise AssertionError("; ".join(failed))
