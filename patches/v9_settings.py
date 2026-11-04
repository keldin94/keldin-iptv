from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
anchor='''    private void showSettingsV6(){'''
assert anchor in s
s=s.replace(anchor,'''    private int selectedSettingsTab=0;
    private void showSettingsV6(){''',1)
start=s.index("    private void showSettingsV6(){")
end=s.index("    private void headingV6(",start)
method=s[start:end]
markers=[
 '        headingV6(body,I18n.t(this,"appearance"));',
 '        headingV6(body,"Playback & startup");',
 '        headingV6(body,"Content & TV guide");',
 '        headingV6(body,"Software updates");',
 '        headingV6(body,"Troubleshooting");',
 '        content.addView(layout,new LinearLayout.LayoutParams(-1,0,1));'
]
indices=[method.index(x) for x in markers]
assert indices==sorted(indices)
sections=[method[indices[i]:indices[i+1]] for i in range(5)]
suffix=method[indices[-1]:]
intro=method[:indices[0]]
nav='''        android.widget.HorizontalScrollView navigation=new android.widget.HorizontalScrollView(this);
        navigation.setHorizontalScrollBarEnabled(false);
        LinearLayout tabRow=Ui.horizontal(this);
        tabRow.setPadding(Ui.dp(this,4),Ui.dp(this,3),Ui.dp(this,4),Ui.dp(this,5));
        String[] labels={
            I18n.t(this,"video"),I18n.t(this,"audio"),I18n.t(this,"network"),
            I18n.t(this,"lists"),I18n.t(this,"appearance"),
            I18n.t(this,"updates"),I18n.t(this,"system")
        };
        for(int i=0;i<labels.length;i++){
            final int which=i;
            TextView tab=Ui.text(this,labels[i],15,
                selectedSettingsTab==i?Ui.WHITE:Ui.MUTED,true);
            tab.setFocusable(true);tab.setClickable(true);
            tab.setGravity(android.view.Gravity.CENTER);
            tab.setMinHeight(Ui.dp(this,49));
            tab.setPadding(Ui.dp(this,17),Ui.dp(this,10),
                Ui.dp(this,17),Ui.dp(this,10));
            android.graphics.drawable.GradientDrawable bg=Ui.shape(
                selectedSettingsTab==i?Ui.SURFACE:Ui.PANEL,11,this);
            if(selectedSettingsTab==i)bg.setStroke(Ui.dp(this,2),Ui.ACCENT);
            tab.setBackground(bg);
            tab.setOnClickListener(v->{selectedSettingsTab=which;render();});
            LinearLayout.LayoutParams cell=new LinearLayout.LayoutParams(-2,-2);
            cell.setMargins(Ui.dp(this,3),0,Ui.dp(this,3),0);
            tabRow.addView(tab,cell);
        }
        navigation.addView(tabRow);
        layout.addView(navigation,Ui.lp(this,-1,64));
'''
intro=intro.replace('''        ScrollView scroll=new ScrollView(this);''',nav+'''        ScrollView scroll=new ScrollView(this);''',1)
appearance,playback,content,updates,system=sections
auto_start=playback.index('        addOptionV6(body,"Automatic reconnect"')
auto_end=playback.index('        addOptionV6(body,"Remember last channel"',auto_start)
auto_block=playback[auto_start:auto_end]
playback=playback[:auto_start]+playback[auto_end:]
# Replace stale beta version label.
system=system.replace('"v0.6 beta"','com.keldin.iptv.BuildConfig.VERSION_NAME')
system=system.replace('"This preview is unlocked. Subscription billing is not enabled."',
                      '"App version and troubleshooting details."')
system=system.replace('"Android TV beta build. Please report playback and navigation errors."',
                      '"Stable Android TV build. Updates are available in the Updates tab."')
video_extra='''        addOptionV6(body,"Overlay auto-hide",
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("overlay_hide_seconds",6)==0?"Never":
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("overlay_hide_seconds",6)+" s",
            "Hide channel and EPG menus automatically after inactivity. Each remote key press restarts the timer.",()->{
                int[] seconds={0,3,5,6,8,12,20};
                String[] titles={"Never","3 seconds","5 seconds","6 seconds","8 seconds",
                    "12 seconds","20 seconds"};
                new AlertDialog.Builder(this).setTitle("Overlay auto-hide")
                    .setItems(titles,(d,chosen)->{
                        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                            .putInt("overlay_hide_seconds",seconds[chosen]).apply();
                        render();
                    }).show();
            });
'''
audio='''        headingV6(body,I18n.t(this,"audio"));
        final String[] audioLanguages={"Auto","Bosanski","Slovenščina","English","Deutsch",
            "Hrvatski","Srpski","Français","Español"};
        final String[] audioCodes={"","bs","sl","en","de","hr","sr","fr","es"};
        String selectedAudio=getSharedPreferences("keldin_settings",MODE_PRIVATE)
            .getString("preferred_audio_lang","");
        int audioIndex=0;
        for(int i=0;i<audioCodes.length;i++)
            if(audioCodes[i].equals(selectedAudio)){audioIndex=i;break;}
        addOptionV6(body,"Preferred audio language",audioLanguages[audioIndex],
            "Prefer this audio track when the stream offers multiple languages. Auto uses the stream default.",()->{
                new AlertDialog.Builder(this).setTitle("Preferred audio language")
                    .setItems(audioLanguages,(d,chosen)->{
                        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                            .putString("preferred_audio_lang",audioCodes[chosen]).apply();
                        render();
                    }).show();
            });
'''
network='''        headingV6(body,I18n.t(this,"network"));
'''+auto_block+'''        addOptionV6(body,"Playlist connection timeout",
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("playlist_timeout_seconds",45)+" s",
            "Timeout for additional download attempts if the IPTV server initially fails to connect.",()->{
                int[] seconds={15,30,45,60,90};
                String[] choices={"15 s","30 s","45 s","60 s","90 s"};
                new AlertDialog.Builder(this).setTitle("Playlist connection timeout")
                    .setItems(choices,(d,choice)->{
                        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                            .putInt("playlist_timeout_seconds",seconds[choice]).apply();
                        render();
                    }).show();
            });
'''
# Make all the requested settings categories genuinely separated, without duplicating controls.
method=intro+'''        if(selectedSettingsTab==0){
'''+playback+video_extra+'''        }
        if(selectedSettingsTab==1){
'''+audio+'''        }
        if(selectedSettingsTab==2){
'''+network+'''        }
        if(selectedSettingsTab==3){
'''+content+'''        }
        if(selectedSettingsTab==4){
'''+appearance+'''        }
        if(selectedSettingsTab==5){
'''+updates+'''        }
        if(selectedSettingsTab==6){
'''+system+'''        }
'''+suffix
s=s[:start]+method+s[end:]
# All settings labels and descriptions are translated at the centralized rendering method.
start=s.index("    private void addOptionV6(")
end=s.index("    private void configurePinV6(",start)
options=s[start:end]
options=options.replace('''        LinearLayout card=Ui.horizontal(this);''',
'''        final String localizedHelp=UiLocaleV9.translate(this,explanation);
        LinearLayout card=Ui.horizontal(this);''',1)
options=options.replace('''        caption.addView(Ui.text(this,heading,16,Ui.WHITE,true));''',
'''        caption.addView(Ui.text(this,UiLocaleV9.translate(this,heading),16,Ui.WHITE,true));''',1)
options=options.replace('''        caption.addView(Ui.text(this,value,12,Ui.MUTED,false));''',
'''        caption.addView(Ui.text(this,UiLocaleV9.translate(this,value),12,Ui.MUTED,false));''',1)
options=options.replace('''settingsHelp.setText(explanation);''','''settingsHelp.setText(localizedHelp);''')
s=s[:start]+options+s[end:]
p.write_text(s)
print("v0.9: horizontally navigated Video, Audio, Network, Playlists, Appearance, Updates and System tabs")
