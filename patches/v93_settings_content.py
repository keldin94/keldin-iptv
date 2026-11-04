from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
needle='''        if(selectedSettingsTab==3){
        headingV6(body,"Content & TV guide");'''
assert needle in s,"v0.9.3 Playlist settings tab not located"
s=s.replace(needle,needle+'''
        addOptionV6(body,"Hide adult content",
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getBoolean("hide_adult_content_v93",true)?"On":"Off",
            "Always filter explicit titles and categories in live TV, movies and series. On is the default. This setting is saved between updates.",()->{
                android.content.SharedPreferences prefs=
                    getSharedPreferences("keldin_settings",MODE_PRIVATE);
                boolean current=prefs.getBoolean("hide_adult_content_v93",true);
                if(current){
                    new AlertDialog.Builder(this).setTitle("Show restricted content?")
                        .setMessage("This will show adult-labelled titles and categories again. Your playlists are not changed.")
                        .setPositiveButton("Show",(d,w)->{
                            prefs.edit().putBoolean("hide_adult_content_v93",false).apply();
                            render();
                        })
                        .setNegativeButton(tr("cancel"),null).show();
                }else{
                    prefs.edit().putBoolean("hide_adult_content_v93",true).apply();
                    render();
                }
            });
        addOptionV6(body,"Manage movie categories","Show / Hide",
            "Choose precisely which movie groups appear. Hidden groups remain in your source playlist and can be restored.",()->manageContentCategoriesV93("MOVIES"));
        addOptionV6(body,"Manage series categories","Show / Hide",
            "Choose precisely which series groups appear. Hidden groups can be re-enabled without downloading the playlist.",()->manageContentCategoriesV93("SERIES"));
        addOptionV6(body,"Restore hidden movies and series","Reset hidden titles",
            "Restore individual movies and series you previously hid. Category exclusions are managed separately.",()->{
                new AlertDialog.Builder(this).setTitle("Restore hidden titles?")
                    .setMessage("Restore individually hidden films and series without changing playlist or category filters?")
                    .setPositiveButton("Restore",(d,w)->{
                        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                            .remove("hidden_media_items_v93")
                            .remove("hidden_series_v93")
                            .apply();
                        render();
                    })
                    .setNegativeButton(tr("cancel"),null).show();
            });
''',1)
p.write_text(s)
print("v0.9.3: persistent adult-block toggle, show/hide movie and series categories, restore hidden titles")
