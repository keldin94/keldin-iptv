#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
b=Path("app/src/main/java/com/keldin/iptv")
s=(b/"ui/MainActivity.java").read_text()
u=(b/"ui/Ui.java").read_text()
a=(b/"ui/ChannelAdapter.java").read_text()
c=(b/"ui/CategoryAdapter.java").read_text()
o=(b/"playback/TvPlaybackOptionsV94.java").read_text()
p=(b/"playback/PlayerActivity.java").read_text()
assert 'selected.setMaxWidth(Ui.dp(this,230))' in s
assert 'card.setContentDescription(name.getText()+" • "+selected.getText())' in s
assert 'new LinearLayout.LayoutParams(0,-2,1)' in s
assert 'LinearLayout.LayoutParams lp=Ui.lp(this,-1,56)' in s
assert 'notice.getText().toString().startsWith("Imported ")' in s
assert 'Color.rgb(10,13,19)' in u and 'Color.rgb(91,170,255)' in u
assert 'Ui.dp(context,46)' in c and '0xff203b53' in c
assert 'guideMode?116:132' in a
assert '0xff141b29' in o and '0xff202b3c' in o
assert 'channelName=Ui.text(this,"",21,Ui.WHITE,true);' in p
assert 'private boolean navigateQuickRowV95(KeyEvent event)' in p
assert 'case 12:openAppSettingsV96();break;' in p
print("PASS: global design tokens, tight rows/cards/panels, readable focus and Settings shortcut preserved")
PY
