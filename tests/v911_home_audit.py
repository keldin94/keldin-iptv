from pathlib import Path
import re
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
for name in ["navigate","render","onResume","onBackPressed","showHome","showSettingsV6","createShell"]:
    pattern=re.search(r'(?:private|public|protected|@Override)\s+(?:void|boolean|View)\s+'+name+r'\s*\([^)]*\)\s*\{',s)
    if not pattern:
        pattern=re.search(r'void\s+'+name+r'\s*\([^)]*\)\s*\{',s)
    if not pattern:continue
    depth=1;i=pattern.end();inside=False;escape=False
    while depth and i<len(s):
        ch=s[i]
        if inside:
            if escape:escape=False
            elif ch=="\\":escape=True
            elif ch=='"':inside=False
        elif ch=='"':inside=True
        elif ch=="{":depth+=1
        elif ch=="}":depth-=1
        i+=1
    text=s[pattern.start():i]
    if len(text)>13000:text=text[:13000]+"... [truncated]"
    print("METHOD",name,"SIZE",i-pattern.start(),"\n",text)
