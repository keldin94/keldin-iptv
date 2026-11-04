from pathlib import Path
import re
targets={
"playback/PlayerActivity.java":[r"favorite",r"@Override public boolean onKeyDown",r"dispatchKeyEvent",r"createUi",r"setControls",r"hideControls",r"showControls",r"Audio",r"guideSync",r"requestGuideIfNeeded",r"showOptions",r"onBackPressed"],
"net/PlaylistSync.java":[r"class PlaylistSync",r"refreshEpg",r"xml",r"epg",r"parse",r"guideUrl",r"HttpURLConnection",r"open(",r"connectTimeout"],
"data/PlaylistSource.java":[r"public",r"epg",r"guide",r"playlistUrl"],
"data/CatalogStore.java":[r"toggleFavorite",r"guide",r"language",r"SharedPreferences"],
"ui/MainActivity.java":[r"showSettingsV6",r"private void showGuide",r"showGuide(",r"language",r"showOptions",r"setText(",r"onBackPressed",r"favorites"],
"ui/I18n.java":[r"CODES",r"NAMES",r"put("],
}
root=Path("app/src/main/java/com/keldin/iptv")
for path,keys in targets.items():
    p=root/path
    if not p.exists():
        print("MISSING",path)
        continue
    lines=p.read_text().splitlines()
    print(f"\n=== {path} ({len(lines)} lines) ===")
    indexes=set()
    for i,line in enumerate(lines):
        if any(re.search(re.escape(k),line,re.I) for k in keys):
            indexes.update(range(max(0,i-2),min(len(lines),i+5)))
    if path.endswith("PlayerActivity.java"):
        indexes.update(range(0,min(130,len(lines))))
    if path.endswith("PlaylistSync.java"):
        indexes.update(range(0,min(150,len(lines))))
    if path.endswith("PlaylistSource.java"):
        indexes.update(range(len(lines)))
    if path.endswith("CatalogStore.java"):
        indexes={i for i in indexes if i<210 or i>260}
    for i in sorted(indexes):
        print(f"{i+1:04d}: {lines[i]}")
