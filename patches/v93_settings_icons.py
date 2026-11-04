from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
def rep(old,new,label):
 global s
 assert old in s, "v0.9.3 settings marker missing: "+label
 s=s.replace(old,new,1)
rep("    private int selectedSettingsTab=0;",'''    private int selectedSettingsTab=0;
    private TextView[] settingsIconsV93;
    private String settingsScopeV93(int i){
        String lang=store==null?"en":store.language();
        String[] en={
            "Picture, playback, buffer and overlay behaviour",
            "Audio tracks and preferred sound language",
            "IPTV server connections and automatic reconnect",
            "Playlists, parental controls, EPG and content filters",
            "App language, text size, colors and transparency",
            "Check, download and install signed app updates",
            "Playback diagnostics, version and troubleshooting"
        };
        String[] bs={
            "Slika, reprodukcija, buffer i ponašanje menija",
            "Audio zapisi i željeni jezik zvuka",
            "IPTV serveri i automatsko povezivanje",
            "Liste, roditeljska zaštita, EPG i filteri sadržaja",
            "Jezik, veličina teksta, boje i prozirnost",
            "Provjera i instalacija potpisanih ažuriranja",
            "Dijagnostika reprodukcije i podaci o aplikaciji"
        };
        String[] sl={
            "Slika, predvajanje, medpomnilnik in meniji",
            "Zvočne sledi in prednostni jezik zvoka",
            "Strežniki IPTV in samodejna povezava",
            "Seznami, starševski nadzor, EPG in filtri",
            "Jezik, velikost besedila, barve in prosojnost",
            "Preverjanje in nameščanje podpisanih posodobitev",
            "Diagnostika predvajanja in podatki aplikacije"
        };
        String[] de={
            "Bild, Wiedergabe, Puffer und Menüs",
            "Audiospuren und bevorzugte Sprache",
            "IPTV-Verbindungen und automatische Wiederherstellung",
            "Playlists, Jugendschutz, EPG und Inhaltsfilter",
            "Sprache, Textgröße, Farben und Transparenz",
            "Signierte Updates suchen und installieren",
            "Wiedergabediagnose und App-Informationen"
        };
        String[] selected="bs".equals(lang)?bs:"sl".equals(lang)?sl:"de".equals(lang)?de:en;
        return selected[Math.max(0,Math.min(selected.length-1,i))];
    }
    private void selectSettingsTabV93(int index){
        selectedSettingsTab=Math.max(0,Math.min(6,index));
        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
            .putInt("settings_section_v93",selectedSettingsTab).apply();
        render();
        if(settingsIconsV93!=null){
            final int pos=selectedSettingsTab;
            settingsIconsV93[pos].post(()->{
                if(settingsIconsV93!=null&&pos<settingsIconsV93.length)
                    settingsIconsV93[pos].requestFocus();
            });
        }
    }
''',"settings tab focus/persistence helpers")
rep('''        page=destination;searchQuery="";
        selectedGroup=getSharedPreferences("keldin_settings",MODE_PRIVATE)''',
'''        page=destination;searchQuery="";
        if("Postavke".equals(page))
            selectedSettingsTab=getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("settings_section_v93",0);
        selectedGroup=getSharedPreferences("keldin_settings",MODE_PRIVATE)''',"restore saved settings section")
start=s.index('''        android.widget.HorizontalScrollView navigation=new android.widget.HorizontalScrollView(this);''')
end=s.index('''        ScrollView scroll=new ScrollView(this);''',start)
old=s[start:end]
assert "navigation.addView(tabRow);" in old
new='''        // Icon-only tabs are always visible on Android TV. Selecting one
        // redraws only that section below the icon rail.
        final LinearLayout[] settingsBodyRefV93={null};
        LinearLayout tabRow=Ui.horizontal(this);
        tabRow.setGravity(Gravity.CENTER_VERTICAL);
        tabRow.setClipChildren(false);
        tabRow.setPadding(Ui.dp(this,6),Ui.dp(this,1),
            Ui.dp(this,6),Ui.dp(this,5));
        String[] tabNames={
            I18n.t(this,"video"),I18n.t(this,"audio"),I18n.t(this,"network"),
            I18n.t(this,"lists"),I18n.t(this,"appearance"),
            I18n.t(this,"updates"),I18n.t(this,"system")
        };
        String[] symbols={"▣","♫","⌁","▤","◉","↻","⚙"};
        selectedSettingsTab=Math.max(0,Math.min(6,selectedSettingsTab));
        settingsIconsV93=new TextView[7];
        for(int i=0;i<symbols.length;i++){
            final int position=i;
            TextView tab=Ui.text(this,symbols[i],28,
                selectedSettingsTab==i?Ui.ACCENT:Ui.MUTED,true);
            tab.setContentDescription(tabNames[i]);
            tab.setFocusable(true);tab.setClickable(true);
            tab.setGravity(Gravity.CENTER);
            android.graphics.drawable.GradientDrawable shape=
                Ui.shape(selectedSettingsTab==i?Ui.SURFACE:Ui.PANEL,13,this);
            if(selectedSettingsTab==i)shape.setStroke(Ui.dp(this,2),Ui.ACCENT);
            tab.setBackground(shape);
            tab.setOnClickListener(v->selectSettingsTabV93(position));
            tab.setOnKeyListener((v,key,event)->{
                if(event.getAction()!=android.view.KeyEvent.ACTION_DOWN)return false;
                if(key==android.view.KeyEvent.KEYCODE_DPAD_LEFT){
                    selectSettingsTabV93(Math.max(0,position-1));return true;
                }
                if(key==KeyEvent.KEYCODE_DPAD_RIGHT){
                    selectSettingsTabV93(Math.min(6,position+1));return true;
                }
                if(key==KeyEvent.KEYCODE_DPAD_DOWN){
                    LinearLayout target=settingsBodyRefV93[0];
                    if(target==null)return true;
                    for(int k=0;k<target.getChildCount();k++){
                        View child=target.getChildAt(k);
                        if(child.isFocusable()&&child.getVisibility()==View.VISIBLE){
                            child.requestFocus();return true;
                        }
                    }
                }
                return false;
            });
            tab.setOnFocusChangeListener((v,focused)->{
                android.graphics.drawable.GradientDrawable bg=Ui.shape(
                    focused?Ui.SURFACE:selectedSettingsTab==position?Ui.SURFACE:Ui.PANEL,
                    13,this);
                if(focused||selectedSettingsTab==position)
                    bg.setStroke(Ui.dp(this,2),Ui.ACCENT);
                v.setBackground(bg);
            });
            LinearLayout.LayoutParams slot=new LinearLayout.LayoutParams(
                0,Ui.dp(this,65),1f);
            slot.leftMargin=Ui.dp(this,4);
            slot.rightMargin=Ui.dp(this,4);
            tabRow.addView(tab,slot);
            settingsIconsV93[i]=tab;
        }
        layout.addView(tabRow,Ui.lp(this,-1,73));
        TextView chosenSectionLabel=Ui.text(this,tabNames[selectedSettingsTab],17,Ui.WHITE,true);
        chosenSectionLabel.setPadding(Ui.dp(this,17),Ui.dp(this,5),
            Ui.dp(this,14),Ui.dp(this,1));
        layout.addView(chosenSectionLabel);
        TextView scope=Ui.text(this,settingsScopeV93(selectedSettingsTab),13,Ui.MUTED,false);
        scope.setPadding(Ui.dp(this,17),0,Ui.dp(this,14),Ui.dp(this,11));
        layout.addView(scope);
'''
s=s[:start]+new+s[end:]
methodStart=s.index("    private void showSettingsV6(){")
methodEnd=s.index("    private void headingV6(",methodStart)
settings=s[methodStart:methodEnd]
assert "        LinearLayout body=Ui.vertical(this);" in settings
settings=settings.replace("        LinearLayout body=Ui.vertical(this);",
    "        LinearLayout body=Ui.vertical(this);\n        settingsBodyRefV93[0]=body;",1)
s=s[:methodStart]+settings+s[methodEnd:]
p.write_text(s)
print("v0.9.3: icon-only 7-section TV settings navigation, labels/scopes under selected icon, saved section, D-pad focus")
