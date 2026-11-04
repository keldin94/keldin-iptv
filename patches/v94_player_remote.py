from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def replace_once(before,after,label):
    global s
    assert before in s, "v0.9.4 missing anchor: "+label
    s=s.replace(before,after,1)

# Explicit remote handling preempts both focused TextViews and Android's default
# D-pad focus navigation. A consumed DOWN must consume the matching UP too.
replace_once('''    private int quickActionIndex=-1;''',
'''    private int quickActionIndex=-1;
    private boolean remoteBackConsumedV94=false;''',"remote state")

anchor='''    @Override public void onBackPressed(){'''
methods='''    private boolean handleOverlayBackV94(KeyEvent event){
        int code=event.getKeyCode();
        if(code!=KeyEvent.KEYCODE_BACK&&code!=KeyEvent.KEYCODE_ESCAPE)return false;
        if(event.getAction()==KeyEvent.ACTION_UP){
            if(remoteBackConsumedV94){remoteBackConsumedV94=false;return true;}
            return false;
        }
        if(event.getAction()!=KeyEvent.ACTION_DOWN)return false;
        if(event.getRepeatCount()>0 && remoteBackConsumedV94)return true;
        if(sidePanel!=null&&sidePanel.isOpen()){
            sidePanel.hide();
            releaseQuickFocus();
            handler.removeCallbacks(hideControls);
            setControls(false);
            remoteBackConsumedV94=true;
            return true;
        }
        if(controlsVisible){
            releaseQuickFocus();
            handler.removeCallbacks(hideControls);
            setControls(false);
            remoteBackConsumedV94=true;
            return true;
        }
        return false; // No overlay: Android Back returns to the app's home screen.
    }

    private boolean handleLiveChannelStepV94(KeyEvent event){
        int code=event.getKeyCode();
        boolean vertical=(code==KeyEvent.KEYCODE_DPAD_UP||
            code==KeyEvent.KEYCODE_DPAD_DOWN||
            code==KeyEvent.KEYCODE_CHANNEL_UP||
            code==KeyEvent.KEYCODE_CHANNEL_DOWN);
        if(!vertical||current==null||!"LIVE".equals(current.kind))return false;
        if(sidePanel!=null&&sidePanel.isOpen())return false; // list navigation remains intact
        if(event.getAction()==KeyEvent.ACTION_UP)return true; // no native focus movement
        if(event.getAction()!=KeyEvent.ACTION_DOWN)return false;
        // One switch per button press, not one per long-press repeat.
        if(event.getRepeatCount()>0)return true;
        int direction=(code==KeyEvent.KEYCODE_DPAD_UP||
            code==KeyEvent.KEYCODE_CHANNEL_UP)?-1:1;
        releaseQuickFocus();
        PlaybackDiagnosticsV91.record(this,"REMOTE key: live channel "+(direction<0?"up":"down"));
        changeChannel(direction);
        return true;
    }

'''
replace_once(anchor,methods+anchor,"new unified remote helpers")
replace_once('''            sidePanel.hide();
            showControls();
            return;
        }
        finish();''',
'''            sidePanel.hide();
            handler.removeCallbacks(hideControls);
            setControls(false);
            return;
        }
        finish();''',"side panel direct Back closes video overlay")
replace_once('''        finish();
    }

    // Intercept remote navigation''',
'''        if(controlsVisible){
            releaseQuickFocus();
            handler.removeCallbacks(hideControls);
            setControls(false);
            return;
        }
        finish();
    }

    // Intercept remote navigation''',"direct back callback")
replace_once('''    @Override public boolean dispatchKeyEvent(KeyEvent event){
        if(event.getAction()==KeyEvent.ACTION_DOWN && sidePanel!=null&&sidePanel.isOpen()){''',
'''    @Override public boolean dispatchKeyEvent(KeyEvent event){
        if(handleOverlayBackV94(event))return true;
        if(handleLiveChannelStepV94(event))return true;
        if(event.getAction()==KeyEvent.ACTION_DOWN && sidePanel!=null&&sidePanel.isOpen()){''',"preempt D-pad focus handling")
replace_once('''                    if(remote==KeyEvent.KEYCODE_BACK){
                        releaseQuickFocus();return true;
                    }''',
'''                    if(remote==KeyEvent.KEYCODE_BACK){
                        releaseQuickFocus();
                        handler.removeCallbacks(hideControls);
                        setControls(false);
                        return true;
                    }''',"legacy back fallback")

# A 180k-entry catalog makes a full queue scan on every remote press
# unnecessary. Cache only the active TV category (not the entire catalog).
replace_once('''    private final ArrayList<Channel> queue=new ArrayList<>();''',
'''    private final ArrayList<Channel> queue=new ArrayList<>();
    private final ArrayList<Channel> cachedLiveGroupV94=new ArrayList<>();
    private String cachedLiveGroupKeyV94="";''',"live channel cache fields")
replace_once('''            ArrayList<Channel> group=new ArrayList<>();
            for(Channel ch:queue)
                if(ch.sourceId.equals(current.sourceId)&&ch.group.equals(current.group)
                    && "LIVE".equals(ch.kind))group.add(ch);
            if(group.isEmpty())return;''',
'''            String cacheKey=current.sourceId+"|"+current.group;
            if(!cacheKey.equals(cachedLiveGroupKeyV94)){
                cachedLiveGroupV94.clear();
                for(Channel ch:queue)
                    if(ch.sourceId.equals(current.sourceId)&&ch.group.equals(current.group)
                        && "LIVE".equals(ch.kind))cachedLiveGroupV94.add(ch);
                cachedLiveGroupKeyV94=cacheKey;
            }
            ArrayList<Channel> group=cachedLiveGroupV94;
            if(group.size()<2){
                PlaybackDiagnosticsV91.record(this,"REMOTE ZAP: category has "+group.size()+" live channel(s)");
                status.setText("No other channel in this category");
                showControls();
                return;
            }
            PlaybackDiagnosticsV91.record(this,"REMOTE ZAP: category size="+group.size()+
                " direction="+delta);''',"cache group and log device-only channel zapping")
replace_once('''    private void selectOverlayChannel(Channel ch){
        if(ch==null)return;''',
'''    private void selectOverlayChannel(Channel ch){
        if(ch==null)return;
        cachedLiveGroupKeyV94="";''',"invalidate group cache on manual channel selection")

# Preserve every existing options action but replace the system list dialog
# with a branded, scrollable, D-pad-focusable player controls sheet.
begin=s.index("    private void showOptions() {")
finish=s.index("    private void diagnoseServer() {",begin)
part=s[begin:finish]
before='''        new AlertDialog.Builder(this).setTitle(current.name+"  •  "+com.keldin.iptv.ui.UiLocaleV9.translate(this,"Options"))
            .setItems(actions,(dialog,choice)->{'''
after='''        handler.removeCallbacks(hideControls);
        TvPlaybackOptionsV94.show(this,current.name,actions,(dialog,choice)->{'''
assert before in part,"v0.9.4 old option dialog marker missing"
part=part.replace(before,after,1)
closing='''            }).setNegativeButton("Zatvori",null).show();'''
assert closing in part
part=part.replace(closing,'''            },this::scheduleHide);''',1)
s=s[:begin]+part+s[finish:]
# Leave playback state, D-pad zapping, and user configuration intact.
p.write_text(s)
print("v0.9.4: Back closes entire overlay; Up/Down always zaps live channels; native options list replaced with polished TV dialog")
