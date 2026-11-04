from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text().splitlines()
print("=== V91 PLAYER DIAGNOSTIC AUDIT ===")
for first,last in [(60,100),(140,242),(258,286),(380,430)]:
    print("== RANGE",first,last,"==")
    for i in range(first-1,min(last,len(s))):
        print(f"{i+1:04d}: {s[i]}")
print("=== app data paths ===")
g=Path("app/build.gradle").read_text().splitlines()
for x in g:
    if any(k in x for k in ("applicationId","versionName","versionCode","signingConfig")):print(x)
