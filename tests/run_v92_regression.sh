#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java").read_text()
side=Path("app/src/main/java/com/keldin/iptv/playback/TvSidePanel.java").read_text()
gradle=Path("app/build.gradle").read_text()
assert "quickActions=new TextView[]{quickPrevious,quickPause,quickNext,favorite,quickMore}" in p
assert "quickActions[quickActionIndex].performClick();" in p
assert 'favorite.setText(store.favorite(current)?"♥":"♡")' in p
assert "releaseQuickFocus();" in p and "KEYCODE_DPAD_UP||remote==KeyEvent.KEYCODE_DPAD_DOWN" in p
assert "if(controlsVisible && favorite!=null)" not in p
assert "compactFrame" not in p  # use a single v0.9.1 framed overlay, not a second layout
assert "infoFrame.setStroke" in p
assert "PlaybackDiagnosticsV91.watch(this,player);" in p
assert "playback_stall_seconds" in p and "minBuffer=liveStream?Math.max(8000" in p
assert "new LogoOnlyAdapter(logoOnly)" in side
assert "holder.logo.setVisibility(View.VISIBLE)" in side
assert "com.keldin.iptv.ui.LogoLoader.load" in side
assert "versionCode 902" in gradle and "versionName '0.9.2'" in gradle
assert "applicationIdSuffix '.updatepreview'" in gradle
assert "KELDIN_SIGNING_FILE" in gradle
assert "keldin_playback" in Path("app/src/main/java/com/keldin/iptv/playback/PlaybackDiagnosticsV91.java").read_text()
print("PASS: remote control icon rail and D-pad channel surf, logo rows, live stutter diagnostics, stable update identity")
PY
