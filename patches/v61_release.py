from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 6" in s and "applicationIdSuffix '.zeta'" in s
s=s.replace("versionCode 6","versionCode 7")
s=s.replace("versionName '0.6.0-editorial'","versionName '0.6.1-import-hotfix'")
s=s.replace("applicationIdSuffix '.zeta'","applicationIdSuffix '.eta'")
p.write_text(s)
print("Keldin IPTV v0.6.1 version package set")
