#!/usr/bin/env bash
set -euo pipefail
mkdir -p /tmp/keldin-v6-parser
javac -encoding UTF-8 -d /tmp/keldin-v6-parser \
  app/src/main/java/com/keldin/iptv/data/Channel.java \
  app/src/main/java/com/keldin/iptv/net/M3uParser.java \
  tests/ParserV6SmokeTest.java
java -Xmx320m -cp /tmp/keldin-v6-parser ParserV6SmokeTest
