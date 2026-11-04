#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-update-tests
javac -encoding UTF-8 -d /tmp/keldin-update-tests \
  app/src/main/java/com/keldin/iptv/updates/UpdateVersion.java \
  tests/UpdateVersionV7Test.java
java -cp /tmp/keldin-update-tests UpdateVersionV7Test
python3 - <<'PY'
from pathlib import Path
g=Path("app/build.gradle").read_text()
m=Path("app/src/main/AndroidManifest.xml").read_text()
assert "versionCode 904" in g and "versionName '0.9.4'" in g
assert "applicationIdSuffix '.updatepreview'" in g
assert 'android:name="android.permission.REQUEST_INSTALL_PACKAGES"' in m
assert 'android:authorities="${applicationId}.updateprovider"' in m
assert 'android:exported="false"' in m
assert Path("app/src/main/res/xml/update_paths.xml").exists()
print("PASS: stable application ID, update permission, FileProvider")
PY
