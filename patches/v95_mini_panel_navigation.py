from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()

def rep(before,after,label):
    global s
    if before not in s:
        raise AssertionError("v95 mini panel missing "+label)
    s=s.replace(before,after,1)

rep('''    private boolean remoteBackConsumedV94=false;''',
'''    private boolean remoteBackConsumedV94=false;
    private TextView quickChannelList;
    private boolean remoteHorizontalConsumedV95=false;''',
"fields")

rep('''    private void createUi(){''',
'''    private void openChannelListV95(){
        if(current==null||sidePanel==null||!"LIVE".equals(current.kind))return;
        handler.removeCallbacks(hideControls);
        setControls(false);
        sidePanel.openChannels(current);
    }

    private void openGuideFromQuickV95(){
        if(current==null||sidePanel==null||!"LIVE".equals(current.kind))return;
        handler.removeCallbacks(hideControls);
        setControls(false);
        sidePanel.openGuide(current);
        requestGuideIfNeeded();
    }

    // The mini-player owns LEFT/RIGHT until its first/last button is reached.
    // A second physical press at the boundary opens channels / TV guide.
    // UP/DOWN are left to the existing live channel zapping handler.
    private boolean navigateQuickRowV95(KeyEvent event){
        final int key=event.getKeyCode();
        if(key!=KeyEvent.KEYCODE_DPAD_LEFT && key!=KeyEvent.KEYCODE_DPAD_RIGHT)
            return false;
        if(event.getAction()==KeyEvent.ACTION_UP){
            if(remoteHorizontalConsumedV95){
                remoteHorizontalConsumedV95=false;
                return true;
            }
            return false;
        }
        if(event.getAction()!=KeyEvent.ACTION_DOWN || !controlsVisible ||
            quickActions==null || (sidePanel!=null&&sidePanel.isOpen()))return false;
        remoteHorizontalConsumedV95=true;
        if(event.getRepeatCount()>0)return true;
        int dir=key==KeyEvent.KEYCODE_DPAD_LEFT?-1:1;
        if(quickActionIndex<0){
            // Default centre point is Pause (index 2 after Channels button).
            moveQuickFocus(dir<0?1:3);
        }else if(dir<0 && quickActionIndex==0){
            openChannelListV95();
        }else if(dir>0 && quickActionIndex==quickActions.length-1){
            openGuideFromQuickV95();
        }else{
            moveQuickFocus(quickActionIndex+dir);
        }
        return true;
    }

    private void createUi(){''',"quick focus and edge actions")

rep('''        quickPrevious=compactAction("◀◀","Previous channel",()->changeChannel(-1));''',
'''        quickChannelList=compactAction("☷",tr("tv_channels"),this::openChannelListV95);
        quickPrevious=compactAction("◀◀","Previous channel",()->changeChannel(-1));''',
"new channel button")

rep('''        quickActions=new TextView[]{quickPrevious,quickPause,quickNext,favorite,quickMore};''',
'''        quickActions=new TextView[]{
            quickChannelList,quickPrevious,quickPause,quickNext,favorite,quickMore
        };''',"six controls")

rep('''        row.addView(right,Ui.lp(this,252,-2));''',
'''        row.addView(right,Ui.lp(this,308,-2));''',"six button width")

rep('''        if(handleLiveChannelStepV94(event))return true;''',
'''        if(handleLiveChannelStepV94(event))return true;
        if(navigateQuickRowV95(event))return true;''',"intercept horizontal before Android focus/onKeyDown")

rep('''                moveQuickFocus(1);
                return true;
            }
        }
        if(event.getAction()==KeyEvent.ACTION_UP && quickActionIndex>=0''',
'''                moveQuickFocus(2); // Focus Pause after adding Channels button.
                return true;
            }
        }
        if(event.getAction()==KeyEvent.ACTION_UP && quickActionIndex>=0''',
"initial OK focus")

p.write_text(s)
print("PASS: v0.9.5 six-button mini-player, horizontal D-pad navigation and edge shortcuts")
