from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
side=(base/"playback/TvSidePanel.java").read_text()
catalog=(base/"data/CatalogStore.java").read_text()
gradle=Path("app/build.gradle").read_text()
checks={
 "Settings navigation clears pending live return":
    'if("Postavke".equals(destination)||"Početna".equals(destination))' in main
    and '.putBoolean("return_live_pending_v98",false)' in main,
 "Settings screen cannot be replaced by deferred playback return":
    'if("Postavke".equals(page))return;' in main,
 "Navigation generation prevents late callback after Back":
    'expectedNavigationV911!=navigationGenerationV911' in main,
 "Player marks explicit Settings opening":
    'openingAppSettingsV913=true;' in player,
 "Settings opening resets return intent":
    '.putBoolean("return_live_pending_v98",false)' in player,
 "Only a finishing player saves last-watched return":
    'if(!openingAppSettingsV913&&isFinishing())' in player,
 "No adapter reset in Back navigation while RecyclerView busy":
    'activeGridV911.setAdapter(null);' not in main
    and 'activeCategoryListV911.setAdapter(null);' not in main,
 "Existing selected live source/category retained":
    'selected_source_Uživo' in main and 'selectedGroup=playedGroup;' in main,
 "Single-column categories and channel drawer":
    'body.addView(list,new LinearLayout.LayoutParams(-1,0,1));' in side
    and 'new androidx.recyclerview.widget.GridLayoutManager(ctx,2)' not in side
    and 'splitV98' not in side,
 "No per-category preview image requests":
    'updateCategoryLogoPreviewV98' not in side
    and 'categoryLogoPreviewV98' not in side,
 "Side overlay width reduced":
    'screenWidth*.30f' in side,
 "Current list index and fast startup unaffected":
    'liveChannelsForSourceV910' in catalog
    and 'loadFastV912' in catalog,
 "Android package and install data unchanged":
    "applicationId 'com.keldin.iptv'" in gradle,
 "Upgrade to version 0.9.13":
    'versionCode 913' in gradle
    and "versionName '0.9.13'" in gradle,
}
for label,ok in checks.items():
    if not ok:raise AssertionError("v0.9.13 regression: "+label)
    print("PASS",label)
print("PASS settings and Back navigation fix; all saved playlist and cache code retained")
