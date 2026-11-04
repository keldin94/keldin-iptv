#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v9-test
javac -encoding UTF-8 -d /tmp/keldin-v9-test \
  app/src/main/java/com/keldin/iptv/data/PlaylistSource.java \
  tests/EpgAutoDiscoveryV9Test.java
java -cp /tmp/keldin-v9-test EpgAutoDiscoveryV9Test
bash tests/run_v81_import_tests.sh
bash tests/run_v8_large_playlist.sh
python3 - <<'PY'
from pathlib import Path
panel=Path("app/src/main/java/com/keldin/iptv/playback/TvSidePanel.java").read_text()
player=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java").read_text()
settings=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java").read_text()
i18n=Path("app/src/main/java/com/keldin/iptv/ui/I18n.java").read_text()
assert "else if(mode==CHANNELS){hide();}" in panel, "channel-to-center transition"
assert "else if(mode==GUIDE){hide();}" in panel, "guide-to-center transition"
assert "overlay_hide_seconds" in panel and "resetAutoHide()" in panel
assert "favorite.setFocusable(true)" in player and "favorite.requestFocus()" in player
assert "setPreferredAudioLanguage" in player
assert "selectedSettingsTab==6" in settings
assert "settingsIconsV93=new TextView[7]" in settings and "selectSettingsTabV93" in settings
assert "Playlist connection timeout" in settings
assert 'ui_lang","en"' in i18n
assert '"en","bs","sl","es"' in i18n
assert Path("app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java").exists()
print("PASS: D-pad neutral step, favorite, auto-hide, seven settings tabs and multilingual labels")
PY
