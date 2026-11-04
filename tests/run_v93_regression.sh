#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v93-test
javac -encoding UTF-8 -d /tmp/keldin-v93-test \
  app/src/main/java/com/keldin/iptv/data/ContentFilterV93.java \
  tests/ContentFilterV93Test.java
java -cp /tmp/keldin-v93-test ContentFilterV93Test
python3 - <<'PY'
from pathlib import Path
m=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java").read_text()
g=Path("app/build.gradle").read_text()
s=Path("app/src/main/java/com/keldin/iptv/ui/SeriesBrowserV6.java").read_text()
assert 'versionCode 903' in g and "versionName '0.9.3'" in g
assert 'applicationIdSuffix' in g and 'KELDIN_SIGNING_FILE' in g
assert 'title.setCompoundDrawables(brand,null,null,null);' in m
assert 'homeTileV93(primary,"▣"' in m
assert 'homeTileV93(primary,"▶"' in m
assert 'homeTileV93(primary,"▤"' in m
assert 'homeTileV93(primary,"♫"' in m
assert 'continue' not in m[m.index("    private void showHome() {"):m.index("    private void landingTile(",m.index("    private void showHome() {"))]
assert 'toolbar.addView(add,addLp);' not in m
assert "selectSettingsTabV93" in m and 'settingsIconsV93' in m
assert 'settingsScopeV93(selectedSettingsTab)' in m
assert 'settings_section_v93' in m
assert 'new TextView[7]' in m
assert 'browseCategoriesV93' in m and 'KEYCODE_DPAD_LEFT' in m
assert 'manageContentCategoriesV93' in m
assert 'ContentFilterV93.isExplicit(ch.group,ch.name)' in m
assert 'getBoolean("hide_adult_content_v93",true)' in m
assert 'java.util.Collections.reverse(section)' in m
assert 'hidden_media_items_v93' in m and 'hidden_series_v93' in m
assert 'filteredChannelsSafeV93(String query)' in m
assert m.count('filteredChannelsSafeV93(searchQuery)')==2
assert 'public static String seriesBase(Channel selected)' in s
assert 'UiLocaleV9.translate(this,"Choose categories to display")' in m
print("PASS: home hero cards, unclipped focus, tabs, category management, explicit blocking, preferences")
PY
