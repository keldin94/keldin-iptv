from pathlib import Path

def swap(s, before, after, label):
    if before not in s:
        raise RuntimeError("v0.4 marker missing: "+label)
    return s.replace(before,after,1)

store=Path("app/src/main/java/com/keldin/iptv/data/CatalogStore.java")
s=store.read_text()
needle="    public synchronized void mergeGuide(Map<String, List<GuideProgram>> more) { guide.putAll(more); }"
addition='''    /** Lightweight guide access for on-video EPG, capped by the viewer to 60 items. */
    public synchronized List<GuideProgram> schedule(Channel ch, long nowMs) {
        List<GuideProgram> source=guide.get(ch.tvgId);
        if(source==null)source=guide.get(ch.id);
        if(source==null)source=guide.get(ch.name);
        ArrayList<GuideProgram> result=new ArrayList<>();
        if(source==null)return result;
        long adjusted=nowMs-guideOffsetHours()*3600_000L;
        for(GuideProgram g:source)
            if(g.end>=adjusted-3600_000L && g.start<=adjusted+24*3600_000L)
                result.add(g);
        result.sort((a,b)->Long.compare(a.start,b.start));
        return result;
    }
'''
s=swap(s,needle,addition+needle,"guide access")
store.write_text(s)

player=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=player.read_text()
s=swap(s,"import android.content.Intent;","import android.content.Intent;\nimport android.content.SharedPreferences;","prefs import")
s=swap(s,"    private boolean controlsVisible=true;",
'''    private boolean controlsVisible=true;
    private TvSidePanel sidePanel;
    private SharedPreferences playbackPreferences;''',"side panel fields")
s=swap(s,"        store=new CatalogStore(this);",
'''        store=new CatalogStore(this);
        playbackPreferences=getSharedPreferences("keldin_playback",MODE_PRIVATE);
        playbackMode=Math.max(0,Math.min(3,playbackPreferences.getInt("preferred_mode",1)));''',"preferred playback mode")
s=swap(s,"        setControls(true);\n    }\n    @Override protected void onStart()",
'''        setControls(true);
        sidePanel=new TvSidePanel(this,screen,store,channel->selectOverlayChannel(channel));
    }
    @Override protected void onStart()''',"panel setup")
s=swap(s,'''                    readySince=System.currentTimeMillis();retryAttempt=0;
                    status.setText("Povezano  •  Reprodukcija");
                    scheduleHide();''',
'''                    readySince=System.currentTimeMillis();retryAttempt=0;
                    playbackPreferences.edit().putInt("preferred_mode",playbackMode).apply();
                    status.setText("Povezano  •  Reprodukcija");
                    if(sidePanel==null||!sidePanel.isOpen())scheduleHide();''',"remember working stream mode")
s=swap(s,"        retryAttempt=0;playbackMode=0;startStream();",
          "        retryAttempt=0;startStream();","keep mode on channel change")
s=swap(s,'''                    case 1:playbackMode=(playbackMode+1)%4;retryAttempt=0;
                        Toast.makeText(this,playbackModeName(),Toast.LENGTH_SHORT).show();startStream();break;''',
'''                    case 1:playbackMode=(playbackMode+1)%4;retryAttempt=0;
                        playbackPreferences.edit().putInt("preferred_mode",playbackMode).apply();
                        Toast.makeText(this,playbackModeName(),Toast.LENGTH_SHORT).show();startStream();break;''',"save manual playback mode")
s=swap(s,
'''        TextView hints=Ui.text(this,"↑ ↓  Kanali     OK  Opcije     MENU  Opcije     BACK  Nazad",12,Ui.MUTED,false);''',
'''        TextView hints=Ui.text(this,"← Kanali   → TV vodič   ↑↓ Promjena   OK Opcije   BACK Izlaz",12,Ui.MUTED,false);''',
"tv remote hints")
start=s.index("    @Override public boolean onKeyDown(int key,KeyEvent event){")
end=s.index("    private void showOptions() {",start)
reworked='''    private void selectOverlayChannel(Channel ch){
        if(ch==null)return;
        for(int i=0;i<queue.size();i++){
            if(queue.get(i).key().equals(ch.key())){
                position=i;
                current=queue.get(i);
                retryAttempt=0;
                if(store.rememberLast())store.recordPlayed(current);
                startStream();
                return;
            }
        }
        queue.add(ch);
        position=queue.size()-1;
        current=ch;
        retryAttempt=0;
        if(store.rememberLast())store.recordPlayed(current);
        startStream();
    }

    private void showExitConfirmation(){
        if(isFinishing()||isDestroyed())return;
        handler.removeCallbacks(hideControls);
        new AlertDialog.Builder(this)
            .setTitle("Želiš li izaći iz Keldin IPTV?")
            .setMessage("Reprodukcija će se zaustaviti.")
            .setPositiveButton("Izađi",(d,w)->finishAffinity())
            .setNeutralButton("Početna",(d,w)->finish())
            .setNegativeButton("Nastavi gledati",(d,w)->scheduleHide())
            .show();
    }

    @Override public void onBackPressed(){
        if(sidePanel!=null&&sidePanel.isOpen()){
            sidePanel.hide();
            showControls();
            return;
        }
        showExitConfirmation();
    }

    // Intercept remote navigation before RecyclerView consumes focus movement.
    @Override public boolean dispatchKeyEvent(KeyEvent event){
        if(event.getAction()==KeyEvent.ACTION_DOWN && sidePanel!=null&&sidePanel.isOpen()){
            int key=event.getKeyCode();
            if(key==KeyEvent.KEYCODE_DPAD_UP){sidePanel.move(-1);return true;}
            if(key==KeyEvent.KEYCODE_DPAD_DOWN){sidePanel.move(1);return true;}
            if(key==KeyEvent.KEYCODE_DPAD_LEFT){sidePanel.left();return true;}
            if(key==KeyEvent.KEYCODE_DPAD_RIGHT){sidePanel.right();return true;}
            if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){
                sidePanel.select();return true;
            }
            if(key==KeyEvent.KEYCODE_BACK){sidePanel.hide();showControls();return true;}
        }
        return super.dispatchKeyEvent(event);
    }

    @Override public boolean onKeyDown(int key,KeyEvent event){
        if(key==KeyEvent.KEYCODE_BACK){onBackPressed();return true;}
        if("LIVE".equals(current.kind)&&key==KeyEvent.KEYCODE_DPAD_LEFT){
            handler.removeCallbacks(hideControls);
            setControls(false);
            sidePanel.openChannels(current);
            return true;
        }
        if("LIVE".equals(current.kind)&&key==KeyEvent.KEYCODE_DPAD_RIGHT){
            handler.removeCallbacks(hideControls);
            setControls(false);
            sidePanel.openGuide(current);
            return true;
        }
        if(key==KeyEvent.KEYCODE_DPAD_UP||key==KeyEvent.KEYCODE_CHANNEL_UP){changeChannel(-1);return true;}
        if(key==KeyEvent.KEYCODE_DPAD_DOWN||key==KeyEvent.KEYCODE_CHANNEL_DOWN){changeChannel(1);return true;}
        if(key==KeyEvent.KEYCODE_MENU||key==KeyEvent.KEYCODE_SETTINGS){showOptions();return true;}
        if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){showOptions();return true;}
        if(key==KeyEvent.KEYCODE_DPAD_LEFT||key==KeyEvent.KEYCODE_DPAD_RIGHT){
            if(player!=null&&!current.kind.equals("LIVE")){
                long delta=key==KeyEvent.KEYCODE_DPAD_RIGHT?10000:-10000;
                player.seekTo(Math.max(0,player.getCurrentPosition()+delta));
            }
            showControls();return true;
        }
        if(key==KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE){
            if(player!=null){if(player.isPlaying())player.pause();else player.play();}
            return true;
        }
        return super.onKeyDown(key,event);
    }

'''
s=s[:start]+reworked+s[end:]
player.write_text(s)

main=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
m=main.read_text()
needle='''    private void createShell() {'''
main_back='''    @Override public void onBackPressed(){
        new AlertDialog.Builder(this)
            .setTitle("Želiš li izaći iz Keldin IPTV?")
            .setMessage("Aplikacija će se zatvoriti.")
            .setPositiveButton("Izađi",(d,w)->finish())
            .setNegativeButton("Ostani",null)
            .show();
    }

'''
m=swap(m,needle,main_back+needle,"main exit confirm")
m=m.replace('v0.3  •  Sve otključano','v0.4  •  Sve otključano')
main.write_text(m)

gradle=Path("app/build.gradle")
g=gradle.read_text()
g=swap(g,"versionCode 3","versionCode 4","v4 code")
g=swap(g,"versionName '0.3.0-stream-probe'","versionName '0.4.0-tv-remote-panels'","v4 name")
# Separate package: debug signing changes between GitHub-hosted runs.
g=swap(g,"applicationIdSuffix '.gamma'","applicationIdSuffix '.delta'","v4 package")
gradle.write_text(g)
print("Keldin IPTV v0.4 overlay and navigation patch complete")
