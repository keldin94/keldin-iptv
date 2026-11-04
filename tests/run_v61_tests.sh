#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v61-parser
javac -encoding UTF-8 -d /tmp/keldin-v61-parser \
  app/src/main/java/com/keldin/iptv/data/Channel.java \
  app/src/main/java/com/keldin/iptv/net/M3uParser.java \
  app/src/main/java/com/keldin/iptv/net/CategoryScanV61.java \
  tests/FilteredM3uV61SmokeTest.java
java -Xmx280m -cp /tmp/keldin-v61-parser FilteredM3uV61SmokeTest
