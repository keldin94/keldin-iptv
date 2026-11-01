from pathlib import Path

p=Path('app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java')
s=p.read_text()

old='''            "Pauza / Nastavi","Prethodni kanal","Sljedeći kanal"};'''
new='''            "Pauza / Nastavi","Prethodni kanal","Sljedeći kanal",
            "Provjeri odgovor servera (HLS / TS)"};'''
assert old in s
s=s.replace(old,new,1)

old='''                    case 10:changeChannel(1);break;'''
new='''                    case 10:changeChannel(1);break;
                    case 11:diagnoseServer();break;'''
assert old in s
s=s.replace(old,new,1)

needle='''    private String playbackModeName() {'''
assert needle in s
method='''    private void diagnoseServer() {
        if (current==null) return;
        handler.removeCallbacks(retry);
        handler.removeCallbacks(bufferingCheck);
        releasePlayer();
        status.setText("Provjeravam odgovor servera...");
        final String channelKey=current.key();
        PlaylistSource source=store.sourceById(current.sourceId);
        String agent=!current.userAgent.isEmpty() ? current.userAgent :
            (source==null ? "VLC/3.0.21 LibVLC/3.0.21" : source.userAgent);
        if (playbackMode==1 || playbackMode==3) agent="VLC/3.0.21 LibVLC/3.0.21";
        final String requestAgent=agent;
        final String streamUrl=current.url;
        new Thread(() -> {
            StreamProbe.Result result=StreamProbe.inspect(streamUrl,requestAgent);
            runOnUiThread(() -> {
                if (isFinishing() || isDestroyed() || current==null ||
                    !channelKey.equals(current.key())) return;
                lastError=result.summary();
                status.setText("Provjera servera završena. OK → Opcije.");
                new AlertDialog.Builder(this).setTitle("Odgovor IPTV servera")
                    .setMessage(result.summary())
                    .setPositiveButton(result.isHls() ? "Pokreni kao HLS" : "Pokreni ponovo",
                        (d,w)->{
                            if(result.isHls())playbackMode=2;
                            retryAttempt=0;
                            startStream();
                        })
                    .setNegativeButton("Zatvori",null).show();
            });
        },"KeldinStreamProbe").start();
    }
'''
s=s.replace(needle,method+needle,1)

old='''        return error.getErrorCodeName()+(origin.isEmpty()?"":" / "+origin);'''
new='''        if(error.errorCode==PlaybackException.ERROR_CODE_PARSING_CONTAINER_UNSUPPORTED)
            return "Format streama nije prepoznat. OK → Provjeri odgovor servera";
        return error.getErrorCodeName()+(origin.isEmpty()?"":" / "+origin);'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

b=Path('app/build.gradle')
t=b.read_text()
assert "versionCode 2" in t
assert "versionName '0.2.0-playback-diagnostics'" in t
t=t.replace("versionCode 2","versionCode 3")
# A GitHub-hosted debug build uses an ephemeral signing key; install v0.3 beside v0.2.
assert "applicationIdSuffix '.beta'" in t
t=t.replace("applicationIdSuffix '.beta'", "applicationIdSuffix '.gamma'")
t=t.replace("versionName '0.2.0-playback-diagnostics'","versionName '0.3.0-stream-probe'")
b.write_text(t)

ui=Path('app/src/main/java/com/keldin/iptv/ui/MainActivity.java')
content=ui.read_text()
content=content.replace('Ui.text(this,"K",32,0xff151428,true)', 'Ui.text(this,"K▶",22,0xff151428,true)',1)
content=content.replace('v0.1  •  Sve otključano','v0.3  •  Sve otključano',1)
ui.write_text(content)
print("v0.3 stream diagnostics and branding patch applied")
