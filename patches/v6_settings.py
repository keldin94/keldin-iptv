from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
assert "showSettingsV6();" in s
insert='''    private void showSettingsV6(){
        LinearLayout layout=Ui.vertical(this);
        ScrollView scroll=new ScrollView(this);
        scroll.setVerticalScrollBarEnabled(false);
        LinearLayout body=Ui.vertical(this);
        body.setPadding(Ui.dp(this,5),Ui.dp(this,4),Ui.dp(this,5),Ui.dp(this,12));
        scroll.addView(body);
        layout.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
        settingsHelp=Ui.text(this,
            "Select an option to see what it does. Changes apply throughout the app.",
            12,Ui.MUTED,false);
        settingsHelp.setPadding(Ui.dp(this,15),Ui.dp(this,10),Ui.dp(this,15),Ui.dp(this,10));
        settingsHelp.setBackground(Ui.shape(Ui.PANEL,10,this));
        layout.addView(settingsHelp,Ui.lp(this,-1,50));

        headingV6(body,I18n.t(this,"appearance"));
        addOptionV6(body,I18n.t(this,"language"),
            I18n.languageNames()[I18n.selectedLanguage(this)],
            "Select the app language. English is the default; playlist titles are unchanged.",()->{
                new AlertDialog.Builder(this).setTitle("Language / Jezik")
                    .setSingleChoiceItems(I18n.languageNames(),I18n.selectedLanguage(this),
                        (d,which)->{store.setLanguage(I18n.languageCodes()[which]);d.dismiss();refreshAppearance();})
                    .setNegativeButton(I18n.t(this,"cancel"),null).show();
            });
        String[] palette={"Ocean cyan","Indigo","Emerald","Amber","Monochrome"};
        addOptionV6(body,"Accent color",palette[store.accentIndex()],
            "Change only the selected-item and icon accent; the dark interface stays consistent.",()->{
                new AlertDialog.Builder(this).setTitle("Accent color")
                    .setSingleChoiceItems(palette,store.accentIndex(),(d,which)->{
                        store.setAccentIndex(which);d.dismiss();refreshAppearance();
                    }).setNegativeButton(I18n.t(this,"cancel"),null).show();
            });
        addOptionV6(body,"Text size",new String[]{"Compact","Standard","Large"}[store.fontScaleIndex()],
            "Adjust interface text size for different TV sizes and viewing distances.",()->{
                String[] opts={"Compact","Standard","Large"};
                new AlertDialog.Builder(this).setTitle("Text size")
                    .setSingleChoiceItems(opts,store.fontScaleIndex(),(d,which)->{
                        store.setFontScaleIndex(which);d.dismiss();refreshAppearance();
                    }).show();
            });
        addOptionV6(body,"Panel transparency",store.panelOpacity()+"%",
            "Adjust transparency of channel lists and the EPG over the playing video.",()->{
                int[] values={55,65,75,84,92,98};
                String[] labels={"55%","65%","75%","84%","92%","98%"};
                new AlertDialog.Builder(this).setTitle("Panel transparency")
                    .setSingleChoiceItems(labels,-1,(d,which)->{
                        store.setPanelOpacity(values[which]);d.dismiss();render();
                    }).show();
            });

        headingV6(body,"Playback & startup");
        addOptionV6(body,I18n.t(this,"startup"),
            store.openLastChannelAtStart()?"Last live channel":"Home screen",
            "Open the last watched live channel when the playlist is available, or show the home menu.",()->{
                store.setOpenLastChannelAtStart(!store.openLastChannelAtStart());render();
            });
        int[] buffers={1,3,6,12};
        addOptionV6(body,"Buffer",store.bufferSeconds()+" s",
            "A smaller buffer reduces delay; a larger buffer may improve stability.",()->{
                String[] choices={"1 s · Minimal","3 s · Balanced","6 s · Stable","12 s · Slow network"};
                new AlertDialog.Builder(this).setTitle("Playback buffer")
                    .setItems(choices,(d,choice)->{
                        store.setBufferSeconds(buffers[choice]);render();
                    }).show();
            });
        addOptionV6(body,"Automatic reconnect",store.autoRetry()?"On":"Off",
            "Reconnect interrupted live streams automatically, using the working player mode.",()->{
                store.setAutoRetry(!store.autoRetry());render();
            });
        addOptionV6(body,"Remember last channel",store.rememberLast()?"On":"Off",
            "Save the most recently watched content and playback progress.",()->{
                store.setRememberLast(!store.rememberLast());render();
            });

        headingV6(body,"Content & TV guide");
        addOptionV6(body,"Playlists and country filters",store.sources().size()+" playlists",
            "Reopen an existing playlist to include or exclude countries. No URL needs to be typed again.",()->navigate("Moje liste"));
        addOptionV6(body,"EPG time offset",String.format(Locale.ROOT,"%+d hours",store.guideOffsetHours()),
            "Correct the timezone offset of the TV guide relative to local time.",()->{
                String[] options=new String[25];
                for(int i=-12;i<=12;i++)options[i+12]=String.format(Locale.ROOT,"%+d hours",i);
                new AlertDialog.Builder(this).setTitle("EPG time offset")
                    .setSingleChoiceItems(options,store.guideOffsetHours()+12,(d,which)->{
                        store.setGuideOffsetHours(which-12);d.dismiss();render();
                    }).show();
            });
        addOptionV6(body,"Parental PIN",store.parentalLocked()?"Enabled":"Disabled",
            "Hide adult-labelled groups until you enter your PIN. This is a basic local parental control.",this::configurePinV6);
        addOptionV6(body,"Settings backup","Export / Import",
            "Save or restore appearance and player settings only. Playlists and access credentials are excluded.",()->backupActionsV6());

        headingV6(body,"Troubleshooting");
        addOptionV6(body,"Crash diagnostics",com.keldin.iptv.ui.CrashReporter.summary(this),
            "Show the last recorded fatal Java crash without exposing playlist addresses or passwords.",()->{
                new AlertDialog.Builder(this).setTitle("Diagnostics")
                    .setMessage(CrashReporter.details(this))
                    .setPositiveButton("OK",null).show();
            });
        addOptionV6(body,"Keldin IPTV Full","v0.6 beta",
            "This preview is unlocked. Subscription billing is not enabled.",()->{
                new AlertDialog.Builder(this).setTitle("Keldin IPTV")
                    .setMessage("Android TV beta build. Please report playback and navigation errors.")
                    .setPositiveButton("OK",null).show();
            });
        content.addView(layout,new LinearLayout.LayoutParams(-1,0,1));
    }
    private void headingV6(LinearLayout body,String heading){
        body.addView(Ui.space(this,14));
        TextView label=Ui.text(this,heading.toUpperCase(Locale.ROOT),12,Ui.ACCENT,true);
        label.setLetterSpacing(.13f);
        body.addView(label);
        body.addView(Ui.space(this,11));
    }
    private void addOptionV6(LinearLayout body,String heading,String value,String explanation,Runnable command){
        LinearLayout card=Ui.horizontal(this);
        card.setPadding(Ui.dp(this,18),0,Ui.dp(this,17),0);
        card.setFocusable(true);card.setClickable(true);
        card.setBackground(Ui.shape(Ui.PANEL,13,this));
        LinearLayout caption=Ui.vertical(this);
        caption.addView(Ui.text(this,heading,16,Ui.WHITE,true));
        caption.addView(Ui.text(this,value,12,Ui.MUTED,false));
        card.addView(caption,new LinearLayout.LayoutParams(0,-2,1));
        card.addView(Ui.text(this,"›",24,Ui.ACCENT,true));
        card.setOnClickListener(v->{settingsHelp.setText(explanation);command.run();});
        card.setOnFocusChangeListener((v,focus)->{
            if(focus&&settingsHelp!=null)settingsHelp.setText(explanation);
            android.graphics.drawable.GradientDrawable bg=Ui.shape(
                focus?Ui.SURFACE:Ui.PANEL,13,this);
            if(focus)bg.setStroke(Ui.dp(this,2),Ui.ACCENT);
            v.setBackground(bg);
        });
        LinearLayout.LayoutParams lp=Ui.lp(this,-1,69);lp.bottomMargin=Ui.dp(this,8);
        body.addView(card,lp);
    }
    private void configurePinV6(){
        if(store.parentalLocked()){
            EditText current=new EditText(this);current.setHint("Current PIN");
            current.setInputType(InputType.TYPE_CLASS_NUMBER|InputType.TYPE_NUMBER_VARIATION_PASSWORD);
            new AlertDialog.Builder(this).setTitle("Parental protection")
                .setView(current).setPositiveButton("Verify",(d,w)->{
                    if(store.checkPin(current.getText().toString()))askNewPinV6();
                    else message("Incorrect PIN");
                }).setNegativeButton("Cancel",null).show();
        }else askNewPinV6();
    }
    private void askNewPinV6(){
        EditText entry=new EditText(this);
        entry.setHint("4–8 digits; leave blank to disable");
        entry.setInputType(InputType.TYPE_CLASS_NUMBER|InputType.TYPE_NUMBER_VARIATION_PASSWORD);
        new AlertDialog.Builder(this).setTitle("New parental PIN")
            .setView(entry).setPositiveButton("Save",(d,w)->{
                String value=entry.getText().toString().trim();
                if(!value.isEmpty() && !value.matches("[0-9]{4,8}")){
                    message("PIN must contain 4–8 digits");return;
                }
                store.setParentalPin(value);render();
            }).setNegativeButton("Cancel",null).show();
    }
    private void backupActionsV6(){
        String[] actions={"Export preferences","Restore preferences"};
        new AlertDialog.Builder(this).setTitle("Settings backup")
            .setItems(actions,(d,which)->{
                Intent i=new Intent(which==0?Intent.ACTION_CREATE_DOCUMENT:Intent.ACTION_OPEN_DOCUMENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);
                i.setType("application/json");
                if(which==0)i.putExtra(Intent.EXTRA_TITLE,"keldin-settings.json");
                startActivityForResult(i,which==0?377:378);
            }).show();
    }

'''
# insert before old showSettings to preserve old method but new one wins
start=s.index("    private void showSettings() {")
s=s[:start]+insert+s[start:]
# onActivityResult handling for backup. Backup helper is separate Java.
needle='''        if(request!=PICK_M3U||result!=RESULT_OK||data==null||data.getData()==null)return;'''
assert needle in s
s=s.replace(needle,'''        if((request==377||request==378)&&result==RESULT_OK&&data!=null&&data.getData()!=null){
            try{
                if(request==377)SettingsBackupV6.write(this,data.getData());
                else {SettingsBackupV6.read(this,data.getData());refreshAppearance();}
                message(request==377?"Settings exported":"Settings restored");
            }catch(Exception ex){message("Backup error: "+ex.getClass().getSimpleName());}
            return;
        }
        if(request!=PICK_M3U||result!=RESULT_OK||data==null||data.getData()==null)return;''',1)
p.write_text(s)
print("v0.6 comprehensive settings page complete")
