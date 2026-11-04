#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v81-test
javac -encoding UTF-8 --add-modules jdk.httpserver -d /tmp/keldin-v81-test \
  tests/v81/PlaylistSync.java \
  app/src/main/java/com/keldin/iptv/net/PlaylistImportHttpV81.java \
  tests/v81/PlaylistImportV81Test.java
java --add-modules jdk.httpserver -cp /tmp/keldin-v81-test PlaylistImportV81Test
python3 - <<'PY'
from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java").read_text()
assert "PlaylistImportHttpV81.open(" in p
assert ".setMultiChoiceItems(" not in p
assert "new android.widget.ScrollView(activity)" in p
assert "checkbox.setOnCheckedChangeListener" in p
print("PASS: IPTV wizard has actual navigable category checkboxes")
PY
