from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv")
def source(name):
    return (root/name).read_text()
main=source("ui/MainActivity.java")
player=source("playback/PlayerActivity.java")
side=source("playback/TvSidePanel.java")
channel=source("data/Channel.java")
catalog=source("data/CatalogStore.java")
checks={
    "live films detection":"g.contains(\"filmski\")" in channel and "g.contains(\"ex yu\")" in channel,
    "genuine VOD excluded":'u.contains("/movie/")||u.contains("/series/")' in channel,
    "cache corrects VOD film channels":'!"LIVE".equals(c.kind)&&Channel.isLiveFilmGroup' in catalog,
    "live browsing recovers old classifications":"liveFilmV98" in main and 'effectiveKindV98' in main,
    "adult filter defaults hidden":'getBoolean("hide_adult_content_v93",true)' in main,
    "adult state labels":'?"Hidden":"Visible"' in main,
    "adult option after category management":main.index('addOptionV6(body,"Adult channels & content"')>main.index('addOptionV6(body,"Manage series categories"'),
    "top toolbar safe inset":"Ui.dp(this,48),Ui.dp(this,9)" in main,
    "player writes CURRENT channel on pause":"rememberLiveReturnV98();" in player and 'current.group' in player,
    "MainActivity restores the actual group":'return_live_pending_v98' in main and 'selectedGroup=playedGroup' in main,
    "category selection starts at current live group":'selectedCategory=channel.group' in side,
    "category logo preview follows focus":'updateCategoryLogoPreviewV98();' in side and 'new LogoOnlyAdapter(matching)' in side,
}
for label,ok in checks.items():
    if not ok:raise AssertionError("v0.9.8 regression: "+label)
    print("PASS",label)
g=Path("app/build.gradle").read_text()
assert "versionCode 908" in g and "versionName '0.9.8'" in g
print("PASS same Android package, versionCode 908")
