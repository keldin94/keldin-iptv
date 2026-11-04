from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def sub(old,new,label):
 global s
 assert old in s, "v0.9.1 compact player missing marker "+label
 s=s.replace(old,new,1)

sub('''    private TextView channelName,programName,status,upNext,qualityHint,favorite;''',
'''    private TextView channelName,programName,status,upNext,qualityHint,favorite;
    private TextView quickPrevious,quickPause,quickNext,quickMore;
    private TextView[] quickActions;
    private int quickActionIndex=-1;''',"quick action fields")
anchor='''    private void createUi(){'''
assert anchor in s
methods='''    private TextView compactAction(String glyph,String description,Runnable command){
        TextView control=Ui.text(this,glyph,22,Ui.WHITE,true);
        control.setGravity(Gravity.CENTER);
        control.setContentDescription(description);
        control.setFocusable(true);
        control.setClickable(true);
        control.setOnClickListener(v->command.run());
        control.setOnFocusChangeListener((v,hasFocus)->{
            android.graphics.drawable.GradientDrawable backdrop=
                Ui.shape(hasFocus?Ui.SURFACE:0x4234455e,10,this);
            if(hasFocus)backdrop.setStroke(Ui.dp(this,2),Ui.ACCENT);
            v.setBackground(backdrop);
        });
        control.setBackground(Ui.shape(0x4234455e,10,this));
        return control;
    }

    private void updatePauseAction(){
        if(quickPause!=null)
            quickPause.setText(player!=null&&player.isPlaying()?"Ⅱ":"▶");
    }
    private void moveQuickFocus(int index){
        if(quickActions==null||index<0||index>=quickActions.length)return;
        quickActionIndex=index;
        quickActions[index].requestFocus();
        scheduleHide();
    }
    private void releaseQuickFocus(){
        if(quickActions!=null&&quickActionIndex>=0&&quickActionIndex<quickActions.length)
            quickActions[quickActionIndex].clearFocus();
        quickActionIndex=-1;
    }

'''
s=s.replace(anchor,methods+anchor,1)
sub('''        overlay=Ui.vertical(this);overlay.setPadding(Ui.dp(this,45),Ui.dp(this,30),Ui.dp(this,45),Ui.dp(this,27));
        overlay.setBackgroundColor(0xa6091020);
        FrameLayout.LayoutParams overLp=new FrameLayout.LayoutParams(-1,-2,Gravity.BOTTOM);
        screen.addView(overlay,overLp);''',
'''        overlay=Ui.vertical(this);
        overlay.setPadding(Ui.dp(this,19),Ui.dp(this,10),
            Ui.dp(this,17),Ui.dp(this,9));
        android.graphics.drawable.GradientDrawable compactFrame=
            Ui.shape(0xe6132335,19,this);
        compactFrame.setStroke(Ui.dp(this,1),0x994e7187);
        overlay.setBackground(compactFrame);
        int screenWidth=getResources().getDisplayMetrics().widthPixels;
        int width=Math.min((int)(screenWidth*.88f),Ui.dp(this,1230));
        FrameLayout.LayoutParams overLp=
            new FrameLayout.LayoutParams(width,-2,Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        overLp.bottomMargin=Ui.dp(this,20);
        screen.addView(overlay,overLp);''',"compact framed overlay")
sub('''        TextView top=Ui.text(this,"KELDIN IPTV   •   FULL",12,Ui.ACCENT,true);top.setLetterSpacing(.1f);
        channelName=Ui.text(this,"",29,Ui.WHITE,true);
        programName=Ui.text(this,"",17,Ui.WHITE,false);
        upNext=Ui.text(this,"",12,Ui.MUTED,false);''',
'''        TextView top=Ui.text(this,"KELDIN IPTV  •  FULL",10,Ui.ACCENT,true);
        top.setLetterSpacing(.08f);
        channelName=Ui.text(this,"",22,Ui.WHITE,true);
        programName=Ui.text(this,"",14,Ui.WHITE,false);
        upNext=Ui.text(this,"",11,Ui.MUTED,false);''',"smaller typography")
sub('''        nameBlock.addView(top);nameBlock.addView(Ui.space(this,6));
        nameBlock.addView(channelName);nameBlock.addView(Ui.space(this,7));
        nameBlock.addView(programName);nameBlock.addView(Ui.space(this,3));nameBlock.addView(upNext);''',
'''        nameBlock.addView(top);nameBlock.addView(Ui.space(this,2));
        nameBlock.addView(channelName);nameBlock.addView(Ui.space(this,3));
        nameBlock.addView(programName);nameBlock.addView(Ui.space(this,1));nameBlock.addView(upNext);''',"tight row spacing")
sub('''        right.addView(live);right.addView(Ui.space(this,7));right.addView(qualityHint);
        right.addView(Ui.space(this,9));right.addView(favorite);
        row.addView(right,Ui.lp(this,190,-2));''',
'''        right.addView(live);right.addView(Ui.space(this,2));right.addView(qualityHint);
        LinearLayout buttons=Ui.horizontal(this);
        buttons.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
        quickPrevious=compactAction("◀◀","Previous channel",()->changeChannel(-1));
        quickPause=compactAction("Ⅱ","Play or pause",()->{
            if(player!=null){
                if(player.isPlaying())player.pause();else player.play();
                updatePauseAction();
            }
        });
        quickNext=compactAction("▶▶","Next channel",()->changeChannel(1));
        quickMore=compactAction("⋯","Playback options",this::showOptions);
        favorite.setTextSize(24f);
        favorite.setGravity(Gravity.CENTER);
        favorite.setContentDescription("Add or remove favorite");
        favorite.setPadding(0,0,0,0);
        favorite.setBackground(Ui.shape(0x4234455e,10,this));
        quickActions=new TextView[]{quickPrevious,quickPause,quickNext,favorite,quickMore};
        for(TextView action:quickActions){
            LinearLayout.LayoutParams item=Ui.lp(this,44,45);
            item.leftMargin=Ui.dp(this,3);
            buttons.addView(action,item);
        }
        right.addView(Ui.space(this,6));
        right.addView(buttons,Ui.lp(this,-1,47));
        row.addView(right,Ui.lp(this,252,-2));''',"five inline remote controls")
sub('''        overlay.addView(Ui.space(this,19));''',
'''        overlay.addView(Ui.space(this,5));''',"less gap before help")
s=s.replace('''        favorite.setText(store.favorite(current)?
            "♥  "+tr("remove_favorite"):"♡  "+tr("add_favorite"));''',
'''        favorite.setText(store.favorite(current)?"♥":"♡");
        favorite.setContentDescription(store.favorite(current)?
            tr("remove_favorite"):tr("add_favorite"));
        updatePauseAction();''',1)
sub('''        if(!visible&&favorite!=null)favorite.clearFocus();''',
'''        if(!visible)releaseQuickFocus();''',"clear quick controls focus when hidden")
# Remove the pre-existing Down-to-heart interception which causes the reported inability to channel surf.
old='''        if(controlsVisible && favorite!=null){
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
'''
assert old in s,"old favorite D-pad trap missing"
s=s.replace(old,"",1)
# Any key, even when the Android focus system consumes it, is intercepted.
anchor='''        return super.dispatchKeyEvent(event);
    }

    @Override public boolean onKeyDown'''
assert anchor in s, "player dispatchKeyEvent marker missing"
s=s.replace(anchor,'''        if(event.getAction()==KeyEvent.ACTION_DOWN && current!=null){
            int remote=event.getKeyCode();
            if("LIVE".equals(current.kind) &&
                (remote==KeyEvent.KEYCODE_DPAD_UP||remote==KeyEvent.KEYCODE_DPAD_DOWN||
                 remote==KeyEvent.KEYCODE_CHANNEL_UP||remote==KeyEvent.KEYCODE_CHANNEL_DOWN)){
                // Up/down MUST change live channels even when the compact controls have focus.
                releaseQuickFocus();
                changeChannel(remote==KeyEvent.KEYCODE_DPAD_UP||
                    remote==KeyEvent.KEYCODE_CHANNEL_UP?-1:1);
                return true;
            }
            if(controlsVisible && quickActions!=null){
                if(quickActionIndex>=0){
                    if(remote==KeyEvent.KEYCODE_DPAD_LEFT){
                        moveQuickFocus(Math.max(0,quickActionIndex-1));return true;
                    }
                    if(remote==KeyEvent.KEYCODE_DPAD_RIGHT){
                        moveQuickFocus(Math.min(quickActions.length-1,quickActionIndex+1));return true;
                    }
                    if(remote==KeyEvent.KEYCODE_DPAD_CENTER||
                       remote==KeyEvent.KEYCODE_ENTER){
                        quickActions[quickActionIndex].performClick();
                        scheduleHide();
                        return true;
                    }
                    if(remote==KeyEvent.KEYCODE_BACK){
                        releaseQuickFocus();return true;
                    }
                }
            }
            if((remote==KeyEvent.KEYCODE_DPAD_CENTER||
                remote==KeyEvent.KEYCODE_ENTER) && "LIVE".equals(current.kind)){
                if(!controlsVisible)showControls();
                moveQuickFocus(1);
                return true;
            }
        }
        return super.dispatchKeyEvent(event);
    }

    @Override public boolean onKeyDown''',1)
# Avoid accidentally opening the options menu on OK while the overlay is already focused;
# dispatchKeyEvent above handles the center button for live TV.
p.write_text(s)
print("v0.9.1: compact framed 88%-width HUD, prev/pause/next/favorite/options controls, reliable up/down channel zapping")
