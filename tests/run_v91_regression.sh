#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java").read_text()
settings=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java").read_text()
diagnostics=Path("app/src/main/java/com/keldin/iptv/playback/PlaybackDiagnosticsV91.java").read_text()
gradle=Path("app/build.gradle").read_text()
assert "int boxWidth=Math.min((int)(videoWidth*.84f)" in p
assert "infoFrame.setStroke" in p
assert 'channelName=Ui.text(this,"",23,' in p
assert 'Ui.space(this,7)' in p
assert 'Math.min(timeout,120))*1000L' in p
assert "handler.postDelayed(bufferingCheck,22000)" not in p
assert "Math.max(8000,secs*1000)" in p
assert 'PlaybackDiagnosticsV91.watch(this,player);' in p
assert "PlaybackDiagnosticsV91.report(this)" in p
assert "AUTO RETRY requested" in p
assert 'selectedSettingsTab==6' in settings
assert "Buffer stall recovery" in settings
assert "Playback diagnostics" in settings
assert "onDroppedVideoFrames" in diagnostics
assert "onPositionDiscontinuity" in diagnostics
assert 'versionCode 901' in gradle and "versionName '0.9.1'" in gradle
assert "applicationId 'com.keldin.iptv'" in gradle
assert "KELDIN_SIGNING_FILE" in gradle
assert "getSharedPreferences" in settings and "ui_lang" in Path("app/src/main/java/com/keldin/iptv/ui/I18n.java").read_text()
print("PASS: compact framed info overlay, configurable stream watchdog, diagnostics and persistent stable identity")
PY
