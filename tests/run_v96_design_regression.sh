#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
b=Path("app/src/main/java/com/keldin/iptv")
ui=(b/"ui/Ui.java").read_text()
main=(b/"ui/MainActivity.java").read_text()
side=(b/"playback/TvSidePanel.java").read_text()
panel=(b/"playback/TvPlaybackOptionsV94.java").read_text()
player=(b/"playback/PlayerActivity.java").read_text()
assert "Color.rgb(10,13,19)" in ui
assert 'private void addOptionV6(LinearLayout body,String heading,String value,' in main
assert 'TextView selected=Ui.text(this,UiLocaleV9.translate(this,value)' in main
assert 'settingsHelp.setText(help)' in main
assert 'settingsShortcutV96' in main
assert 'notice.setSingleLine(true);' in main
assert '0xff141b29' in panel
assert 'overlay.setPadding(Ui.dp(this,16),Ui.dp(this,10)' in player
assert 'Ui.dp(ctx,58)' in side
print("PASS: v0.9.6 balanced dark TV density, settings focused descriptions and player controls")
PY
