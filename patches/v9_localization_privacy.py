from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistSync.java")
s=p.read_text()
old='''} catch (Exception e) { callback(callback,store.channels().size(),"EPG nije dostupan: " + e.getMessage(),null); }'''
assert old in s,"EPG error callback marker not found"
# Network exception messages sometimes contain URLs with provider passwords.
s=s.replace(old,''' } catch (Exception e) { callback(callback,store.channels().size(),"EPG nije dostupan",null); }''',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
old='''        notice.setText(source.name+"  •  "+count+" kanala  •  "+epg);'''
new='''        String epgLabel=epg==null?"":epg.startsWith("EPG nije dostupan")?
            I18n.t(this,"guide_unavailable"):epg.startsWith("EPG nije podešen")?
            I18n.t(this,"epg_missing_url"):epg;
        notice.setText(source.name+"  •  "+count+" "+I18n.t(this,"channels_count")
            +"  •  "+epgLabel);'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
old='"Connected  •  Playing"'
assert old in s
s=s.replace(old,'com.keldin.iptv.ui.UiLocaleV9.translate(PlayerActivity.this,"Connected  •  Playing")',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java")
s=p.read_text()
anchor='''        put("Connecting...","Povezivanje...","Povezovanje...","Verbinden...");'''
assert anchor in s
s=s.replace(anchor,anchor+'''
        put("Connected  •  Playing","Povezano  •  Reprodukcija","Povezano  •  Predvajanje","Verbunden  •  Wiedergabe");
        put("Playback will stop.","Reprodukcija će se zaustaviti.","Predvajanje se bo ustavilo.","Die Wiedergabe wird beendet.");
''',1)
p.write_text(s)
print("v0.9: language-consistent status and protected IPTV credentials in EPG failures")
