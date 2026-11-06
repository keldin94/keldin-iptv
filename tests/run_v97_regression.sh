#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
b=Path("app/src/main/java/com/keldin/iptv")
main=(b/"ui/MainActivity.java").read_text()
channel=(b/"ui/ChannelAdapter.java").read_text()
cat=(b/"ui/CategoryAdapter.java").read_text()
side=(b/"playback/TvSidePanel.java").read_text()
player=(b/"playback/PlayerActivity.java").read_text()
grid=(b/"playback/TvGridPanelV97.java").read_text()
locale=(b/"ui/UiLocaleV9.java").read_text()
g=Path("app/build.gradle").read_text()
assert "versionCode 907" in g and "versionName '0.9.7'" in g
assert "applicationId 'com.keldin.iptv'" in g
# Every previously cut item must measure the content, not force 40 / 49 / 69dp.
assert 'toolbar.addView(header,new LinearLayout.LayoutParams(0,-2,1));' in main
assert 'header.setMinimumHeight(Ui.dp(this,63))' in main
assert 'layout.addView(settingsHelp,Ui.lp(this,-1,-2));' in main
assert 'layout.addView(settingsMetaV96,Ui.lp(this,-1,-2));' in main
assert 'card.setMinimumHeight(Ui.dp(this,62));' in main
assert 'label.setMaxLines(2);' in cat
assert 'ViewGroup.LayoutParams.WRAP_CONTENT' in cat
assert 'ViewGroup.LayoutParams.WRAP_CONTENT' in channel
assert 'program.setMinHeight(Ui.dp(c,32));' in channel
assert 'box.addView(program,Ui.lp(c,-1,-2));' in channel
assert 'mode==CHANNELS?.38f' in side
assert 'int alpha=Math.max(222' in side
assert 'body.addView(list,new LinearLayout.LayoutParams(-1,0,1));' in side
assert 'if(mode==CATEGORIES){\n            LinearLayout split=' not in side
assert 'row.setMinimumHeight(Ui.dp(ctx,70));' in side
assert 'ViewGroup.LayoutParams.WRAP_CONTENT' in side
assert 'title.setMaxLines(2)' in side and 'subtitle.setMaxLines(2)' in side
assert 'active.title+' in side and 'r.subtitle=c.group+' not in side
# Quick player, side drawer, grid: real callbacks, no new player or stream URL.
assert 'new TvGridPanelV97(' in player
assert 'this::openTvGridV97' in player
assert 'this::openGuideFromQuickV95' in player
assert 'quickGridV97,quickGuideV97,quickChannelList' in player
assert 'moveQuickFocus(4); // Pause stays' in player
assert 'gridPanelV97.handleKey(event)' in player
assert 'if(gridPanelV97!=null&&gridPanelV97.isOpen())' in player
assert 'new GridLayoutManager(ctx,columns)' in grid
assert 'adapter=new GridAdapter()' in grid
assert 'host.addView(scrim' in grid
assert 'choose.onChannel(selected)' in grid
assert 'new ExoPlayer' not in grid
assert 'ContentFilterV93.isExplicit' in grid
# Selected-language labels use the 16-language dictionary.
assert 'put16("TV Grid"' in locale
assert 'case "Settings":return I18n.t(context,"settings")' in locale
assert 'case "Search":return I18n.t(context,"search")' in locale
print("PASS: v0.9.7 measured typography, full-width category list, TV Grid D-pad and 16-language core navigation")
PY
