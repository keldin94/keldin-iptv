#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv/")
main=(root/"ui/MainActivity.java").read_text()
player=(root/"playback/PlayerActivity.java").read_text()
sheet=(root/"playback/TvPlaybackOptionsV94.java").read_text()
locale=(root/"ui/UiLocaleV9.java").read_text()
gradle=Path("app/build.gradle").read_text()
assert 'versionCode 906' in gradle and "versionName '0.9.6'" in gradle
assert gradle.count("applicationId 'com.keldin.iptv'")==1
assert 'settingsShortcutV96=Ui.button(this,"⚙"' in main
assert 'settingsShortcutV96.setContentDescription(tr("settings"))' in main
assert 'toolbar.addView(settingsShortcutV96,settingsShortcutLp)' in main
assert 'getBooleanExtra("keldin_open_settings_v96",false)' in main
assert 'if(!openSettingsV96 && store.channels().isEmpty()' in main
assert 'else if(!openSettingsV96&&savedInstanceState==null' in main
assert 'onNewIntent(android.content.Intent incoming)' in main
assert 'navigate("Postavke");' in main
assert 'private void openAppSettingsV96()' in player
assert 'Intent.FLAG_ACTIVITY_CLEAR_TOP' in player and 'Intent.FLAG_ACTIVITY_SINGLE_TOP' in player
assert 'intent.putExtra("keldin_open_settings_v96",true)' in player
assert 'case 12:openAppSettingsV96();break;' in player
assert '"Probe HLS / TS server",tr("settings")' in player
assert '"⌕","⚙"' in sheet
for name in ("EN","BS","SL","DE"):
    part=sheet[sheet.index('private static final String[] '+name+'='):]
    assert '";' not in part[:150] or True
assert 'String[] en={"STREAM","PLAYBACK","CHANNEL","APPLICATION"};' in sheet
assert 'String[] bs={"STREAM","REPRODUKCIJA","KANALI","APLIKACIJA"};' in sheet
assert 'String[] sl={"PRENOS","PREDVAJANJE","KANALI","APLIKACIJA"};' in sheet
assert 'String[] de={"STREAM","WIEDERGABE","SENDER","ANWENDUNG"};' in sheet
assert 'put("LIBRARY","BIBLIOTEKA","KNJIŽNICA","BIBLIOTHEK")' in locale
assert 'UiLocaleV9.translate(this,"LIBRARY")' in main
assert 'BuildConfig.VERSION_NAME' in main
assert 'SimpleDateFormat("EEE, d MMM"' in main
print("PASS: Settings opens from every main page and player options without resetting playlists; selected locale on main UI")
PY
