from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 901" in s and "versionName '0.9.1'" in s
s=s.replace("versionCode 901","versionCode 902",1)
s=s.replace("versionName '0.9.1'","versionName '0.9.2'",1)
p.write_text(s)
print("v0.9.2: stable package com.keldin.iptv, unchanged release signing identity")
