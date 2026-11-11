from pathlib import Path
import re
base=Path("app/src/main/java/com/keldin/iptv")
skin=(base/"ui/ThemeV914.java").read_text()
main=(base/"ui/MainActivity.java").read_text()
groups=(base/"ui/PlaylistGroupAdapterV99.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
options=(base/"playback/TvPlaybackOptionsV94.java").read_text()
store=(base/"data/CatalogStore.java").read_text()
update=(base/"updates/AppUpdateManager.java").read_text()
gradle=Path("app/build.gradle").read_text()

checks={
"Five independently selectable skins":all(re.search(r'\b'+key+r'\s*=\s*\d+',skin)
    for key in ["CLASSIC","CINEMA","GUIDE","GLASS","COMPACT"]),
"Persistent theme selection without modifying sources":
    'getInt(KEY,CLASSIC)' in skin and '.putInt(KEY,choice).apply()' in skin,
"Visual theme previews":"fakePreview(" in skin and 'showGallery(' in skin,
"Default Classic layout":'private static final String[] LABELS' in skin and 'KELDIN Classic' in skin,
"Cinema hero and featured movie navigation":'"THE CINEMA"' in skin and '"Filmovi",nav,1,232' in skin,
"TV guide-focused Home opens real EPG":'"TV GUIDE"' in skin and '"TV vodič",nav,1,300' in skin,
"Glass has translucent panels":'theme==GLASS?0xa62b405b' in skin,
"Compact has two dense rows":'theme==COMPACT?10:17' in skin or 'theme==COMPACT?11:17' in skin,
"Every theme preserves familiar route IDs":
    all('"'+dest+'"' in skin for dest in ["Uživo","Filmovi","Serije","Radio","Postavke","TV vodič"]),
"Home rendered without reloading IPTV library":
    'ThemeV914.showHome(this,content,store,' in main
    and 'ThemeV914.showHome(this,content,store' in main.split('private void showHome() {')[1].split('private void landingTile(')[0],
"Appearance tab exposes gallery":'ThemeV914.showGallery(this' in main and 'ThemeV914.label(this)' in main,
"Cinema poster categories horizontal":'ThemeV914.CINEMA&&isPosters' in main
    and 'androidx.recyclerview.widget.LinearLayoutManager.HORIZONTAL' in main,
"Cinema category entries have bounded ribbon width":'horizontal?Ui.dp(context,200):-1' in groups,
"Each skin has different browse grid density":'ThemeV914.gridColumns(skinV914,isPosters)' in main,
"Player chrome style only when showing controls":
    'if(visible&&overlay!=null)' in player and 'ThemeV914.stylePlayer(this,overlay)' in player,
"Player has a new update action":'"Check for updates"' in player and 'case 13:com.keldin.iptv.updates.AppUpdateManager.check(this,true)' in player,
"Options icon and descriptions present":
    '↻","▣"' in options and 'Check for a newer signed application version' in options
    and 'Provjeri i instaliraj novu verziju aplikacije' in options,
"Update manager verifies APK before installing":
    'UpdateVersion.compare' in update and 'sha256.equalsIgnoreCase' in update,
"No new streaming or playlist data paths":
    'loadFastV912' in store and 'isPlaylistActiveV99' in store,
"Same signed Android app ID":
    "applicationId 'com.keldin.iptv'" in gradle,
"Version 0.9.14":'versionCode 914' in gradle and "versionName '0.9.14'" in gradle
}
failed=[]
for label,passed in checks.items():
    if passed:print("PASS",label)
    else:
        print("FAIL",label)
        failed.append(label)
if failed:raise AssertionError("v0.9.14: "+", ".join(failed))
print("PASS five complete theme variants, layout and player update checks")
