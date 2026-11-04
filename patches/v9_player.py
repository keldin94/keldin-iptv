from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def swap(a,b,label):
    global s
    assert a in s,label
    s=s.replace(a,b,1)
swap('''    private void createUi(){''','''    private String tr(String key){return com.keldin.iptv.ui.I18n.t(this,key);}
    private void togglePlayerFavorite(){
        if(current==null)return;
        store.toggleFavorite(current);
        updateInfo();
        showControls();
        favorite.requestFocus();
    }
    private void createUi(){''',"player locale and favorite toggle")
swap('''        favorite=Ui.text(this,"",14,Ui.WHITE,true);favorite.setGravity(Gravity.RIGHT);''',
'''        favorite=Ui.text(this,"",14,Ui.WHITE,true);favorite.setGravity(Gravity.RIGHT);
        favorite.setFocusable(true);
        favorite.setClickable(true);
        favorite.setMinHeight(Ui.dp(this,46));
        favorite.setPadding(Ui.dp(this,9),Ui.dp(this,9),Ui.dp(this,9),Ui.dp(this,9));
        favorite.setOnClickListener(v->togglePlayerFavorite());
        favorite.setOnFocusChangeListener((v,focused)->{
            android.graphics.drawable.GradientDrawable shape=Ui.shape(
                focused?Ui.SURFACE:0x00000000,10,this);
            if(focused)shape.setStroke(Ui.dp(this,2),Ui.ACCENT);
            favorite.setBackground(shape);
        });''',"D-pad focusable heart")
swap('''        favorite.setText(store.favorite(current)?"♥  FAVORIT":"♡  Dodaj u favorite");''',
'''        favorite.setText(store.favorite(current)?
            "♥  "+tr("remove_favorite"):"♡  "+tr("add_favorite"));''',"favorite localization")
swap('''        if(overlay!=null)overlay.setVisibility(visible?View.VISIBLE:View.GONE);''',
'''        if(overlay!=null)overlay.setVisibility(visible?View.VISIBLE:View.GONE);
        if(!visible&&favorite!=null)favorite.clearFocus();''',"avoid hidden focus")
swap('''        if(key==KeyEvent.KEYCODE_BACK){onBackPressed();return true;}
        if("LIVE".equals(current.kind)&&key==KeyEvent.KEYCODE_DPAD_LEFT){''',
'''        if(key==KeyEvent.KEYCODE_BACK){onBackPressed();return true;}
        if(controlsVisible && favorite!=null){
            if(key==KeyEvent.KEYCODE_DPAD_DOWN){
                favorite.requestFocus();
                scheduleHide();
                return true;
            }
            if(favorite.hasFocus()){
                if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){
                    togglePlayerFavorite();
                    return true;
                }
                if(key==KeyEvent.KEYCODE_DPAD_UP){
                    favorite.clearFocus();
                    scheduleHide();
                    return true;
                }
            }
        }
        if("LIVE".equals(current.kind)&&key==KeyEvent.KEYCODE_DPAD_LEFT){''',"favorite remote selection")
s=s.replace('''        TextView live=Ui.text(this,"●  UŽIVO",16,Ui.GREEN,true);''',
            '''        TextView live=Ui.text(this,"●  "+tr("live"),16,Ui.GREEN,true);''')
s=s.replace('''            upNext.setText("Slijedi u "+time+"  •  "+next.title);''',
            '''            upNext.setText(tr("next")+" "+time+"  •  "+next.title);''')
s=s.replace('''        } else upNext.setText("Grupa: "+current.group);''',
            '''        } else upNext.setText(tr("group")+": "+current.group);''')
swap('''        guideSync.refreshEpg(src,(count,status,error)->{
            if(isFinishing()||isDestroyed()||sidePanel==null)return;
            if(sidePanel.isOpen()&&current!=null)
                sidePanel.openGuide(current);
        });''',
'''        guideSync.refreshEpg(src,(count,status,error)->handler.post(()->{
            if(isFinishing()||isDestroyed()||sidePanel==null)return;
            if(sidePanel.isOpen() && current!=null &&
                    status!=null && status.startsWith("EPG:"))
                sidePanel.openGuide(current);
            if(status!=null && status.startsWith("EPG nije dostupan"))
                Toast.makeText(this,tr("epg_load_error"),Toast.LENGTH_SHORT).show();
        }));''',"correct EPG callback status and UI")
swap('''        player.prepare();''',
'''        String preferredAudio=getSharedPreferences("keldin_settings",MODE_PRIVATE)
            .getString("preferred_audio_lang","");
        if(!preferredAudio.isEmpty())
            player.setTrackSelectionParameters(player.getTrackSelectionParameters()
                .buildUpon().setPreferredAudioLanguage(preferredAudio).build());
        player.prepare();''',"working default audio language preference")
p.write_text(s)
print("v0.9: focusable favorite, localized player overlay, default audio track, corrected EPG refresh")
