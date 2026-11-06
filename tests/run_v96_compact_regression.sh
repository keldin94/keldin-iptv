#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
menu=(base/"playback/TvPlaybackOptionsV94.java").read_text()
poster=(base/"ui/PosterAdapterV6.java").read_text()
gradle=Path("app/build.gradle").read_text()
assert "versionCode 906" in gradle and "versionName '0.9.6'" in gradle
assert 'settingsShortcutV96=Ui.button(this,"⚙"' in main
assert 'settingsShortcutV96.setContentDescription(tr("settings"))' in main
assert 'getBooleanExtra("keldin_open_settings_v96",false)' in main
assert 'if(!openSettingsV96)mainHandler.post(()->play(last));' in main
assert 'notice.setVisibility("Postavke".equals(page)?View.GONE:View.VISIBLE);' in main
assert 'int heroHeight=Math.max(Ui.dp(this,162),' in main
assert 'LinearLayout.LayoutParams catParams=Ui.lp(this,190,-1);' in main
assert 'layout.addView(tabRow,Ui.lp(this,-1,53));' in main
assert 'layout.addView(settingsMetaV96,Ui.lp(this,-1,35));' in main
assert 'layout.addView(settingsHelp,Ui.lp(this,-1,40));' in main
assert 'LinearLayout.LayoutParams lp=Ui.lp(this,-1,56);lp.bottomMargin=Ui.dp(this,4);' in main
assert 'Ui.dp(c,255)' in poster
assert 'private void openAppSettingsV96()' in player
assert 'intent.putExtra("keldin_open_settings_v96",true);' in player
assert 'case 12:openAppSettingsV96();break;' in player
assert '"Probe HLS / TS server",tr("settings")' in player
assert 'if(i==0||i==4||i==8||i==12)' in menu
assert '"Open application settings"' in menu
assert '"App-Einstellungen öffnen"' in menu
assert 'private boolean navigateQuickRowV95(KeyEvent event)' in player
assert 'if(handleOverlayBackV94(event))return true;' in player
assert 'if(handleLiveChannelStepV94(event))return true;' in player
assert 'quickChannelList=compactAction' in player
assert 'TvPlaybackOptionsV94.show(this,current.name,actions' in player
print("PASS: Compact UI on all browse sections, one Settings shortcut, player Settings and D-pad controls")
PY
