#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java").read_text()
ui=Path("app/src/main/java/com/keldin/iptv/playback/TvPlaybackOptionsV94.java").read_text()
g=Path("app/build.gradle").read_text()
assert 'versionCode 904' in g and "versionName '0.9.4'" in g
assert 'KELDIN_SIGNING_FILE' in g
assert "private boolean handleOverlayBackV94(KeyEvent event)" in p
assert "private boolean handleLiveChannelStepV94(KeyEvent event)" in p
assert "remoteBackConsumedV94=false" in p
assert "if(handleOverlayBackV94(event))return true;" in p
assert "if(handleLiveChannelStepV94(event))return true;" in p
assert "if(controlsVisible){" in p[p.index("    @Override public void onBackPressed()"):p.index("    @Override public boolean dispatchKeyEvent(")]
assert "handler.removeCallbacks(hideControls);" in p
assert "setControls(false);" in p[p.index("    private boolean handleOverlayBackV94"):p.index("    private boolean handleLiveChannelStepV94")]
assert "if(event.getAction()==KeyEvent.ACTION_UP)return true;" in p
assert "if(event.getRepeatCount()>0)return true;" in p
assert "releaseQuickFocus();\\n        changeChannel(direction);" in p
assert "sidePanel!=null&&sidePanel.isOpen())return false;" in p
assert "quickActions[quickActionIndex].performClick();" in p
assert "TvPlaybackOptionsV94.show(this,current.name,actions" in p
assert '.setItems(actions,(dialog,choice)->' not in p
assert 'void onSelected(android.content.DialogInterface dialog,int action)' in ui
assert 'callback.onSelected(dialog,index);' in ui
assert 'category.setLetterSpacing(.14f)' in ui
assert 'item.setFocusable(true);' in ui
assert 'dialog.setOnShowListener(' in ui
assert 'dialog.setCanceledOnTouchOutside(true);' in ui
assert 'w.setDimAmount(.61f);' in ui
assert 'actions.length&&i<SYMBOLS.length' in ui
print("PASS: Back closes mini-overlay, Up/Down zaps while controls focused, styled D-pad options")
PY
