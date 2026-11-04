from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 903" in s and "versionName '0.9.3'" in s
s=s.replace("versionCode 903","versionCode 904",1)
s=s.replace("versionName '0.9.3'","versionName '0.9.4'",1)
p.write_text(s)
print("Keldin IPTV v0.9.4 — unchanged package id and permanent release signer")
