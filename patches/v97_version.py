from pathlib import Path
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 906" in s and "versionName '0.9.6'" in s
p.write_text(s.replace("versionCode 906","versionCode 907",1)
               .replace("versionName '0.9.6'","versionName '0.9.7'",1))
print("PASS: v0.9.7 stable package identity and signing configuration preserved")
