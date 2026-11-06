#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
s=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java").read_text()
assert "private void openChannelListV95()" in s
assert "private void openGuideFromQuickV95()" in s
assert "private boolean navigateQuickRowV95(KeyEvent event)" in s
assert "quickChannelList=compactAction" in s
assert "quickChannelList,quickPrevious,quickPause,quickNext,favorite,quickMore" in s
assert "row.addView(right,Ui.lp(this,308,-2))" in s
assert "moveQuickFocus(dir<0?1:3);" in s
assert "quickActionIndex==0" in s and "openChannelListV95();" in s
assert "quickActionIndex==quickActions.length-1" in s and "openGuideFromQuickV95();" in s
assert "moveQuickFocus(quickActionIndex+dir);" in s
assert "if(event.getRepeatCount()>0)return true;" in s
assert "if(remoteHorizontalConsumedV95)" in s
assert "moveQuickFocus(2); // Focus Pause" in s
dispatch=s.index("    @Override public boolean dispatchKeyEvent(KeyEvent event){")
pre=s[dispatch:s.index("    @Override public boolean onKeyDown",dispatch)]
assert pre.index("if(navigateQuickRowV95(event))return true;")<pre.index("if(event.getAction()==KeyEvent.ACTION_DOWN && sidePanel!=null")
assert "if(handleOverlayBackV94(event))return true;" in pre
assert "if(handleLiveChannelStepV94(event))return true;" in pre
assert "if(sidePanel!=null&&sidePanel.isOpen()" in s
print("PASS: buttons, D-pad boundaries, no repeated edge triggers, Back and UP/DOWN preserved")
PY
