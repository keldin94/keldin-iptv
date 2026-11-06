#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
main=(base/"ui/MainActivity.java").read_text()
player=(base/"playback/PlayerActivity.java").read_text()
local=(base/"ui/UiLocaleV9.java").read_text()
i18n=(base/"ui/I18n.java").read_text()
assert 'UiLocaleV9.translate(this,"LIBRARY")' in main
assert 'BuildConfig.VERSION_NAME' in main
assert 'java.util.Locale.forLanguageTag(store.language())' in main
assert 'UiLocaleV9.translate(MainActivity.this,' in main
assert 'UiLocaleV9.translate(PlayerActivity.this,' in player
assert 'Checking server response...' in player
assert 'put("LIBRARY","BIBLIOTEKA","KNJIŽNICA","BIBLIOTHEK")' in local
assert 'put("Settings","Postavke","Nastavitve","Einstellungen")' in local
assert 'put("Playback options","Opcije reprodukcije","Možnosti predvajanja","Wiedergabeoptionen")' in local
assert 'put("Search","Pretraga","Iskanje","Suche")' in local
assert '"en","bs","sl"' in i18n
assert 'getString("ui_lang","en")' in i18n
print("PASS: English-default core navigation, localized authored labels and player dialog controls")
PY
