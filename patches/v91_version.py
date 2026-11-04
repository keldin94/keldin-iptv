from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 900" in s and "versionName '0.9.0'" in s
s=s.replace("versionCode 900","versionCode 901",1)
s=s.replace("versionName '0.9.0'","versionName '0.9.1'",1)
p.write_text(s)
print("Stable package com.keldin.iptv updated to 0.9.1; signing identity unchanged")
