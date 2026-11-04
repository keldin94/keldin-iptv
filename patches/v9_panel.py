from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/TvSidePanel.java")
s=p.read_text()
def swap(a,b,label):
    global s
    assert a in s,label
    s=s.replace(a,b,1)

swap("    private FrameLayout panel;",'''    private final android.os.Handler autoHideHandler=
        new android.os.Handler(android.os.Looper.getMainLooper());
    private final Runnable autoHideTask=()->hide();
    private void resetAutoHide(){
        autoHideHandler.removeCallbacks(autoHideTask);
        int seconds=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getInt("overlay_hide_seconds",6);
        if(mode!=HIDDEN&&seconds>0)
            autoHideHandler.postDelayed(autoHideTask,Math.min(30,seconds)*1000L);
    }
    private String tr(String key){return com.keldin.iptv.ui.I18n.t(ctx,key);}
    private FrameLayout panel;''',"timeout fields")
swap('''        mode=CHANNELS;
        refresh();
    }
    public void openGuide''','''        mode=CHANNELS;
        refresh();resetAutoHide();
    }
    public void openGuide''',"channels timeout")
swap('''        mode=GUIDE;
        refresh();
    }
    public void left()''','''        mode=GUIDE;
        refresh();resetAutoHide();
    }
    public void left()''',"guide timeout")
swap('''    public void left(){
        if(mode==CHANNELS){mode=CATEGORIES;refresh();}
        else if(mode==GUIDE_DETAIL){mode=GUIDE;refresh();}
        else if(mode==GUIDE){mode=CHANNELS;refresh();}
    }
    public void right(){
        if(mode==CATEGORIES){mode=CHANNELS;refresh();}
        else if(mode==CHANNELS){mode=GUIDE;refresh();}
        else if(mode==GUIDE){mode=GUIDE_DETAIL;refresh();}
    }''','''    public void left(){
        if(mode==CHANNELS){mode=CATEGORIES;refresh();resetAutoHide();}
        else if(mode==GUIDE_DETAIL){mode=GUIDE;refresh();resetAutoHide();}
        else if(mode==GUIDE){hide();}
    }
    public void right(){
        if(mode==CATEGORIES){mode=CHANNELS;refresh();resetAutoHide();}
        else if(mode==CHANNELS){hide();}
        else if(mode==GUIDE){mode=GUIDE_DETAIL;refresh();resetAutoHide();}
    }''',"center step between panels")
swap('''    public void move(int direction){
        if(rows.isEmpty())return;''','''    public void move(int direction){
        resetAutoHide();
        if(rows.isEmpty())return;''',"move timer")
swap('''    public void select(){
        if(selection<0||selection>=rows.size())return;''','''    public void select(){
        resetAutoHide();
        if(selection<0||selection>=rows.size())return;''',"select timer")
swap('''    public void hide(){
        mode=HIDDEN;''','''    public void hide(){
        autoHideHandler.removeCallbacks(autoHideTask);
        mode=HIDDEN;''',"hide timer cancellation")
s=s.replace('all.title="Sve kategorije";all.subtitle=total+" kanala";rows.add(all);',
            'all.title=tr("all_categories");all.subtitle=total+" "+tr("channels_count");rows.add(all);')
s=s.replace('?"Ostalo":c.group;', '?tr("other"):c.group;')
s=s.replace('g.getValue()+" kanala"','g.getValue()+" "+tr("channels_count")')
s=s.replace('r.subtitle=now?"● LIVE"','r.subtitle=now?"● "+tr("now")')
s=s.replace('''                empty.title="TV vodič nije dostupan";
                empty.subtitle="Dodaj XMLTV / EPG URL u postavkama liste.";''',
'''                empty.title=tr("guide_unavailable");
                com.keldin.iptv.data.PlaylistSource src=store.sourceById(current.sourceId);
                empty.subtitle=(src==null||src.guideUrl().isEmpty())?
                    tr("epg_missing_url"):tr("epg_no_programs");''')
s=s.replace('''            mode==CHANNELS?"TV Channels":mode==CATEGORIES?"Categories":
                mode==GUIDE?"TV Guide":"TV Guide · Details",''',
'''            mode==CHANNELS?tr("tv_channels"):mode==CATEGORIES?tr("categories"):
                mode==GUIDE?tr("guide"):tr("guide")+" · "+tr("details"),''')
s=s.replace('mode==CHANNELS?selectedCategory:"Select category",12,MUTED,false);',
            'mode==CHANNELS?("Sve kategorije".equals(selectedCategory)?tr("all_categories"):selectedCategory):tr("select_category"),12,MUTED,false);')
s=s.replace('rows.size()+" stavki"','rows.size()+" "+tr("items")')
s=s.replace('''            mode==CATEGORIES?"→ Kanali   •   ↑↓ Odaberi   •   OK Otvori":
                mode==GUIDE?"← Channels   •   → Detail guide   •   OK Info":
                mode==GUIDE_DETAIL?"← Quick guide   •   BACK Close":
                    "← Kategorije   •   → EPG   •   OK Gledaj",11,MUTED,false);''',
'''            mode==CATEGORIES?"→ "+tr("tv_channels")+"   •   ↑↓   •   OK":
                mode==GUIDE?"← "+tr("video")+"   •   → "+tr("details")+"   •   OK":
                mode==GUIDE_DETAIL?"← "+tr("guide")+"   •   BACK":
                    "← "+tr("categories")+"   •   → "+tr("video")+"   •   OK",11,MUTED,false);''')
s=s.replace('''                    "Nema dodatnog opisa emisije.":r.program.description)
                .setPositiveButton("Zatvori",null).show();''',
'''                    tr("no_description"):r.program.description)
                .setPositiveButton(tr("close"),null).show();''')
p.write_text(s)
print("v0.9: neutral video center, scrollable panels, user-selected menu duration, translated EPG hints")
