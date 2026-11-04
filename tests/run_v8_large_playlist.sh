#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v8-test
javac -encoding UTF-8 -d /tmp/keldin-v8-test \
  app/src/main/java/com/keldin/iptv/data/Channel.java \
  app/src/main/java/com/keldin/iptv/net/M3uParser.java \
  app/src/main/java/com/keldin/iptv/net/CategoryScanV61.java \
  tests/LargeFullPlaylistV8Test.java
java -Xmx384m -cp /tmp/keldin-v8-test LargeFullPlaylistV8Test
