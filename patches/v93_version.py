from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 902" in s and "versionName '0.9.2'" in s
s=s.replace("versionCode 902","versionCode 903",1)
s=s.replace("versionName '0.9.2'","versionName '0.9.3'",1)
p.write_text(s)
print("Keldin IPTV stable v0.9.3 — same applicationId and signing certificate")
