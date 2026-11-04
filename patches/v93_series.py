from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/SeriesBrowserV6.java")
s=p.read_text()
anchor='''    public static List<Channel> unique(List<Channel> episodes){'''
assert anchor in s
s=s.replace(anchor,'''    public static String seriesBase(Channel selected){
        return base(selected).toLowerCase(Locale.ROOT);
    }
'''+anchor,1)
p.write_text(s)
print("v0.9.3: consistent series identity across seasons and episodes")
