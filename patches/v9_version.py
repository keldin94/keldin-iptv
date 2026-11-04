from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 801" in s and "versionName '0.8.1'" in s
s=s.replace("versionCode 801","versionCode 900",1)
s=s.replace("versionName '0.8.1'","versionName '0.9.0'",1)
p.write_text(s)
print("Keldin IPTV v0.9.0: same stable package and permanent signing certificate")
