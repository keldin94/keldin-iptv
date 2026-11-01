from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/data/CatalogStore.java")
s=p.read_text()
needle="public final class CatalogStore {\n"
assert needle in s
s=s.replace(needle,needle+'''    private static volatile CatalogStore sharedInstance;
    /** A single app-level catalogue prevents reparsing tens of thousands of items on every player launch. */
    public static CatalogStore shared(Context context) {
        CatalogStore instance=sharedInstance;
        if(instance==null) synchronized(CatalogStore.class) {
            instance=sharedInstance;
            if(instance==null) sharedInstance=instance=new CatalogStore(context.getApplicationContext());
        }
        return instance;
    }
''',1)
p.write_text(s)
for path in ["app/src/main/java/com/keldin/iptv/ui/MainActivity.java",
             "app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java"]:
    f=Path(path)
    s=f.read_text()
    assert "new CatalogStore(this)" in s
    s=s.replace("new CatalogStore(this)","CatalogStore.shared(this)")
    f.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/Ui.java")
s=p.read_text()
s=s.replace("Color.rgb(8,12,22)","Color.rgb(9,18,31)")
s=s.replace("Color.rgb(18,25,41)","Color.rgb(17,32,49)")
s=s.replace("Color.rgb(24,33,52)","Color.rgb(23,43,63)")
s=s.replace("Color.rgb(142,153,176)","Color.rgb(151,174,193)")
s=s.replace("Color.rgb(244,246,255)","Color.rgb(244,249,254)")
s=s.replace("Color.rgb(173,157,255)","Color.rgb(77,211,244)")
s=s.replace("Color.rgb(79,225,178)","Color.rgb(83,221,194)")
s=s.replace("new int[]{Color.rgb(51,39,103),Color.rgb(23,41,81),Color.rgb(14,23,45)}",
            "new int[]{Color.rgb(21,64,89),Color.rgb(14,39,62),Color.rgb(9,23,39)}")
s=s.replace("Color.rgb(15,12,33)","Color.rgb(6,21,33)")
s=s.replace("0xff39446a","0xff274f66")
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/ChannelAdapter.java")
s=p.read_text()
s=s.replace('''        tile.setBackground(Ui.shape(0xff2a3155,13,c));''','''        // No decorative square behind the broadcaster's own logo.
        tile.setBackgroundColor(Color.TRANSPARENT);''')
s=s.replace('''        TextView initials=Ui.text(c,"TV",17,Ui.WHITE,true);''',
'''        TextView initials=Ui.text(c,"▶",18,Ui.ACCENT,true);''')
start=s.index('''        String text=ch.name.replaceAll''')
end=s.index('''        GuideProgram current=store.current''',start)
s=s[:start]+'''        h.initials.setText("▶");
        h.initials.setVisibility(View.GONE);
        LogoLoader.load(h.logo,ch.logo,loaded -> {
            h.initials.setVisibility(loaded ? View.GONE : View.VISIBLE);
        });
'''+s[end:]
s=s.replace("0xffc9d1e9","0xffc3d9e7").replace("0xff9c8ffd","0xff4dd3f4")
s=s.replace("0xff303b5e","0xff254d65")
p.write_text(s)
print("v0.5 theme, shared catalog and borderless channel cards ready")
