#!/usr/bin/env bash
set -euo pipefail
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
javac -encoding UTF-8 -d "$tmp" \
  app/src/main/java/com/keldin/iptv/data/Channel.java \
  app/src/main/java/com/keldin/iptv/net/CategoryScanV61.java \
  tests/FilmChannelV95Test.java
java -cp "$tmp" FilmChannelV95Test
python3 - <<'PY'
from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
a=(base/"ui/ChannelAdapter.java").read_text()
c=(base/"data/CatalogStore.java").read_text()
p=(base/"playback/PlayerActivity.java").read_text()
l=(base/"ui/UiLocaleV9.java").read_text()
d=(base/"playback/PlaybackDiagnosticsV91.java").read_text()
m=(base/"ui/MainActivity.java").read_text()
v=Path("app/build.gradle").read_text()
assert "versionCode 906" in v and "versionName '0.9.6'" in v
assert "isLiveFilmGroup(c.group,c.url)" in c
assert 'name.setMaxLines(2)' in a
assert 'headText.addView(name); // The selected category' in a
assert 'if(!guideMode)box.addView(footer,fp);' not in a
assert 'I18n.t(h.itemView.getContext(),"guide_unavailable")' in a
assert 'h.progress.setVisibility(View.GONE);' in a
assert 'tr("items")' in m
assert 'put16("Buffering..."' in l and 'I18n.selectedLanguage(context)' in l
assert "int rebufferMs=liveStream?Math.max(4500" in p
assert "Playback review (not a definitive diagnosis)" in d
print("PASS: v0.9.5 migrated categories, compact EPG card, language and playback diagnostics")
PY
