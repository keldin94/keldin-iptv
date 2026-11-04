from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
old='''        String[] actions={"Ponovo poveži stream","Promijeni način reprodukcije",
            "Otvori u vanjskom playeru","Detalji greške","Dodaj/ukloni favorit",
            "Promijeni format slike","Audio zapisi","Titlovi",
            "Pauza / Nastavi","Prethodni kanal","Sljedeći kanal",
            "Provjeri odgovor servera (HLS / TS)"};'''
new='''        String[] actions={"Reconnect stream","Change playback mode",
            "Open in external player","Error details","Toggle favorite",
            "Change aspect ratio","Audio tracks","Subtitles",
            "Pause / Resume","Previous channel","Next channel",
            "Probe HLS / TS server"};
        for(int i=0;i<actions.length;i++)
            actions[i]=com.keldin.iptv.ui.UiLocaleV9.translate(this,actions[i]);'''
assert old in s, "player action list changed"
s=s.replace(old,new,1)
s=s.replace('current.name+"  •  Opcije"','current.name+"  •  "+com.keldin.iptv.ui.UiLocaleV9.translate(this,"Options")')
s=s.replace('''"Nema dostupnih zapisa."''',
'''com.keldin.iptv.ui.UiLocaleV9.translate(this,"No available tracks.")''')
s=s.replace('''String heading=type==C.TRACK_TYPE_TEXT?"Titlovi":"Audio zapisi";''',
'''String heading=com.keldin.iptv.ui.UiLocaleV9.translate(this,
            type==C.TRACK_TYPE_TEXT?"Subtitles":"Audio tracks");''')
s=s.replace('''private String lastError="Nema evidentirane greške.";''',
'''private String lastError="No errors recorded.";''')
s=s.replace('''status=Ui.text(this,"Povezivanje...",''',
'''status=Ui.text(this,com.keldin.iptv.ui.UiLocaleV9.translate(this,"Connecting..."),''')
s=s.replace('''"Povezano  •  Reprodukcija"''','''"Connected  •  Playing"''')
s=s.replace('''"Povezivanje...  pokušaj "''',
            '''com.keldin.iptv.ui.UiLocaleV9.translate(this,"Connecting...")+"  # "''')
s=s.replace('''"Greška: "+shortLabel(reason)+". MENU → Pokušaj ponovo."''',
            '''com.keldin.iptv.ui.UiLocaleV9.translate(this,"Connection failed")+": "+shortLabel(reason)+". MENU → Retry."''')
s=s.replace('''"Neuspješno: "+shortLabel(reason)+". MENU → Način reprodukcije."''',
            '''com.keldin.iptv.ui.UiLocaleV9.translate(this,"Connection failed")+": "+shortLabel(reason)+". MENU → Player mode."''')
s=s.replace('''" · novi pokušaj za "+delay+" s ("''','''" · retry in "+delay+" s ("''')
s=s.replace('''"TV vodič nije dostupan"''','''tr("guide_unavailable")''')
s=s.replace('''"Nema TV vodiča"''','''tr("guide_unavailable")''')
s=s.replace('''"← Kanali   → TV vodič   ↑↓ Promjena   OK Opcije   BACK Izlaz"''',
''' "← "+tr("tv_channels")+"   → "+tr("guide")+
            "   ↑↓ "+tr("tv_channels")+"   OK "+
            com.keldin.iptv.ui.UiLocaleV9.translate(this,"Options")+"   BACK"''')
s=s.replace('''            .setTitle("Želiš li izaći iz Keldin IPTV?")
            .setMessage("Reprodukcija će se zaustaviti.")''',
'''            .setTitle(com.keldin.iptv.ui.I18n.t(this,"exit"))
            .setMessage(com.keldin.iptv.ui.UiLocaleV9.translate(this,
                "Playback will stop."))''')
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
s=s.replace('''            .setMessage("Želiš li zatvoriti aplikaciju?")''',
'''            .setMessage(I18n.t(this,"exit"))''')
s=s.replace('''            .setTitle("Želiš li izaći iz Keldin IPTV?")''',
'''            .setTitle(I18n.t(this,"exit"))''')
p.write_text(s)
print("v0.9: player menus use English by default; selected primary locales translate common labels")
