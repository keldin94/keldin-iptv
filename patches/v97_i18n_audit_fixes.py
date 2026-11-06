from pathlib import Path
root=Path("app/src/main/java/com/keldin/iptv")
p=root/"ui/UiLocaleV9.java"
s=p.read_text()
marker='''        put("LIBRARY","BIBLIOTEKA","KNJIŽNICA","BIBLIOTHEK");'''
if marker not in s:raise AssertionError("v97 locale insertion anchor")
additional='''        put16("TV Grid","TV mreža","Mreža kanalov","Cuadrícula TV","Grade de TV",
            "टीवी ग्रिड","شبكة القنوات","Grille TV","Kisi TV","TV-Raster",
            "TV Izgarası","TVグリッド","TV 그리드","电视网格","Сетка каналов","টিভি গ্রিড");
        put16("No schedule available","Nema rasporeda","Spored ni na voljo",
            "No hay programación","Sem programação","कार्यक्रम उपलब्ध नहीं",
            "لا يتوفر جدول","Aucun programme disponible","Jadwal tidak tersedia",
            "Kein Programm verfügbar","Program yok","番組表がありません",
            "편성표 없음","无节目表","Расписание недоступно","সময়সূচি নেই");
        put16("All channels","Svi kanali","Vsi kanali","Todos los canales",
            "Todos os canais","सभी चैनल","كل القنوات","Toutes les chaînes",
            "Semua saluran","Alle Sender","Tüm kanallar","すべてのチャンネル",
            "모든 채널","所有频道","Все каналы","সব চ্যানেল");
'''
s=s.replace(marker,additional+marker,1)
marker='''        String[] full=FULL.get(value);'''
if marker not in s:raise AssertionError("v97 full language runtime")
s=s.replace(marker,'''        // Core labels already have complete 16-language translations in I18n.
        // Reuse them instead of falling back to English for 12 locales.
        switch(value){
            case "Settings":return I18n.t(context,"settings");
            case "Home":return I18n.t(context,"home");
            case "Search":return I18n.t(context,"search");
            case "Continue watching":return I18n.t(context,"continue");
            case "Close":return I18n.t(context,"close");
            case "Cancel":return I18n.t(context,"cancel");
            case "Appearance":return I18n.t(context,"appearance");
            case "Language":return I18n.t(context,"language");
            case "TV Channels":return I18n.t(context,"tv_channels");
            case "TV Guide":return I18n.t(context,"guide");
            case "Categories":return I18n.t(context,"categories");
            case "Favorites":return I18n.t(context,"favorites");
            case "Play":return I18n.t(context,"play");
        }
        String[] full=FULL.get(value);''',1)
p.write_text(s)

p=root/"playback/TvSidePanel.java";s=p.read_text()
s=s.replace('''                r.subtitle=c.group+(store.favorite(c)?"  •  ♥":"");''',
'''                GuideProgram active=store.current(c,System.currentTimeMillis());
                r.subtitle=active==null?(store.favorite(c)?"♥":""):
                    active.title+(store.favorite(c)?"  •  ♥":"");''',1)
s=s.replace('''mode==GUIDE_DETAIL?"← "+tr("guide")+"   •   BACK":''',
'''mode==GUIDE_DETAIL?"← "+tr("guide")+"   •   "+tr("close"):''',1)
p.write_text(s)

p=root/"playback/TvGridPanelV97.java";s=p.read_text()
s=s.replace('''            "← → ↑ ↓   •   OK   •   BACK",11,Ui.MUTED,false);''',
'''            "← → ↑ ↓   •   OK   •   "+I18n.t(ctx,"close"),11,Ui.MUTED,false);''')
p.write_text(s)

p=root/"playback/PlayerActivity.java";s=p.read_text()
s=s.replace('''"\\nAko sve aplikacije prekidaju, provjeri IPTV server i broj aktivnih veza."''',
'''com.keldin.iptv.ui.UiLocaleV9.translate(this,
                            "If all apps keep buffering, check the IPTV server and concurrent connections.")''')
# Current diagnostics text is always built in the player language, not hardcoded.
s=s.replace('''"Player mode: "''',
'''com.keldin.iptv.ui.UiLocaleV9.translate(this,"Player mode")+": "''')
s=s.replace('''"\\nLast error: "''',
'''"\\n"+com.keldin.iptv.ui.UiLocaleV9.translate(this,"Last error")+": "''')
p.write_text(s)

p=root/"ui/UiLocaleV9.java";s=p.read_text()
marker='''        put("LIBRARY","BIBLIOTEKA","KNJIŽNICA","BIBLIOTHEK");'''
note='''        put("If all apps keep buffering, check the IPTV server and concurrent connections.",
            "Ako sve aplikacije prekidaju, provjeri IPTV server i broj aktivnih veza.",
            "Če se vse aplikacije zatikajo, preveri strežnik IPTV in število povezav.",
            "Wenn alle Apps puffern, IPTV-Server und gleichzeitige Verbindungen prüfen.");
'''
s=s.replace(marker,note+marker,1)
p.write_text(s)
print("PASS: 16-language core and TV Grid labels; EPG-only channel subtitles; translated player diagnostics")
