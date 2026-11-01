from pathlib import Path
p=Path('app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java')
s=p.read_text()
def change(a,b):
 global s
 if a not in s: raise RuntimeError('Patch marker missing: '+a[:95])
 s=s.replace(a,b,1)

change('import android.app.Activity;','import android.app.Activity;\nimport android.content.ActivityNotFoundException;\nimport android.content.Intent;')
change('import androidx.media3.datasource.DefaultHttpDataSource;', 'import androidx.media3.datasource.DefaultHttpDataSource;\nimport androidx.media3.datasource.HttpDataSource;')
change('    private boolean controlsVisible=true;', '    private boolean controlsVisible=true;\n    private int playbackMode=0;\n    private String lastError="Nema evidentirane greške.";')
change('''        String ua=!current.userAgent.isEmpty()?current.userAgent:(source==null?"KeldinIPTV/0.1":source.userAgent);
        if(ua==null||ua.isEmpty())ua="KeldinIPTV/0.1";''','''        String ua=!current.userAgent.isEmpty()?current.userAgent:(source==null?"KeldinIPTV/0.1":source.userAgent);
        if(ua==null||ua.isEmpty())ua="KeldinIPTV/0.1";
        // Some IPTV servers expect a known player User-Agent for live streams.
        if (playbackMode==1 || playbackMode==3) ua="VLC/3.0.21 LibVLC/3.0.21";
        qualityHint.setText("EXOPLAYER  •  " + playbackModeName());''')
change('''            @Override public void onPlayerError(PlaybackException error){
                status.setText("Greška streama ("+error.errorCode+")");
                scheduleRetry(error.getMessage());
            }''','''            @Override public void onPlayerError(PlaybackException error){
                String label=readableError(error);
                lastError=label;
                if(retryAttempt==0 && playbackMode==0) playbackMode=1;
                else if(retryAttempt==1 && "LIVE".equals(current.kind)) playbackMode=2;
                else if(retryAttempt==2 && "LIVE".equals(current.kind)) playbackMode=3;
                scheduleRetry(label);
            }''')
change('''        if(lower.contains(".m3u8")||lower.contains("format=m3u8")||lower.contains("output=hls"))
            media.setMimeType(MimeTypes.APPLICATION_M3U8);''','''        if(playbackMode==2 || playbackMode==3 || lower.contains(".m3u8")
            || lower.contains("format=m3u8") || lower.contains("output=hls"))
            media.setMimeType(MimeTypes.APPLICATION_M3U8);''')
change('''        player.prepare();player.play();setControls(true);scheduleHide();''','''        player.prepare();player.play();setControls(true);''')
change('''        if(!store.autoRetry()){status.setText("Stream nije dostupan. MENU → Pokušaj ponovo.");setControls(true);return;}''','''        if(!store.autoRetry()){status.setText("Greška: "+shortLabel(reason)+". MENU → Pokušaj ponovo.");setControls(true);return;}''')
change('''            status.setText("Nije moguće povezati se. MENU → Pokušaj ponovo.");''','''            status.setText("Neuspješno: "+shortLabel(reason)+". MENU → Način reprodukcije.");''')
change('''        status.setText("Veza je prekinuta. Novi pokušaj za "+delay+" s ("+retryAttempt+"/5)");''','''        status.setText(shortLabel(reason)+" · novi pokušaj za "+delay+" s ("+retryAttempt+"/5)");''')
change('''        retryAttempt=0;startStream();
    }
    private void updateInfo()''','''        retryAttempt=0;playbackMode=0;startStream();
    }
    private void updateInfo()''')
change('''        String[] actions={"Ponovo poveži stream","Dodaj/ukloni favorit","Promijeni format slike",
            "Audio zapisi","Titlovi","Pauza / Nastavi","Prethodni kanal","Sljedeći kanal"};''','''        String[] actions={"Ponovo poveži stream","Promijeni način reprodukcije",
            "Otvori u vanjskom playeru","Detalji greške","Dodaj/ukloni favorit",
            "Promijeni format slike","Audio zapisi","Titlovi",
            "Pauza / Nastavi","Prethodni kanal","Sljedeći kanal"};''')
change('''                    case 1:store.toggleFavorite(current);updateInfo();break;
                    case 2:toggleAspect();break;
                    case 3:chooseTrack(C.TRACK_TYPE_AUDIO);break;
                    case 4:chooseTrack(C.TRACK_TYPE_TEXT);break;
                    case 5:if(player!=null){if(player.isPlaying())player.pause();else player.play();}break;
                    case 6:changeChannel(-1);break;
                    case 7:changeChannel(1);break;''','''                    case 1:playbackMode=(playbackMode+1)%4;retryAttempt=0;
                        Toast.makeText(this,playbackModeName(),Toast.LENGTH_SHORT).show();startStream();break;
                    case 2:openExternalPlayer();break;
                    case 3:new AlertDialog.Builder(this).setTitle("Dijagnostika streama")
                        .setMessage(lastError+"\\nNačin: "+playbackModeName()+
                            "\\nAko sve aplikacije prekidaju, provjeri IPTV server i broj aktivnih veza.")
                        .setPositiveButton("U redu",null).show();break;
                    case 4:store.toggleFavorite(current);updateInfo();break;
                    case 5:toggleAspect();break;
                    case 6:chooseTrack(C.TRACK_TYPE_AUDIO);break;
                    case 7:chooseTrack(C.TRACK_TYPE_TEXT);break;
                    case 8:if(player!=null){if(player.isPlaying())player.pause();else player.play();}break;
                    case 9:changeChannel(-1);break;
                    case 10:changeChannel(1);break;''')
anchor='''    private void toggleAspect() {'''
add='''    private String playbackModeName() {
        switch(playbackMode){
            case 1:return "VLC identifikacija";
            case 2:return "HLS";
            case 3:return "HLS + VLC identifikacija";
            default:return "Automatski";
        }
    }
    private String shortLabel(String description) {
        if(description==null||description.isEmpty())return "Stream nedostupan";
        return description.length()>100 ? description.substring(0,100) : description;
    }
    private String readableError(PlaybackException error) {
        int httpCode=-1;
        Throwable cause=error;
        String origin="";
        while(cause!=null){
            if(cause instanceof HttpDataSource.InvalidResponseCodeException){
                httpCode=((HttpDataSource.InvalidResponseCodeException)cause).responseCode;
                break;
            }
            if(cause.getCause()==null)origin=cause.getClass().getSimpleName();
            cause=cause.getCause();
        }
        if(httpCode>0){
            if(httpCode==401 || httpCode==403)return "HTTP "+httpCode+" – pristup streamu odbijen";
            if(httpCode==404)return "HTTP 404 – stream nije pronađen";
            if(httpCode==429)return "HTTP 429 – ograničenje servera";
            return "HTTP "+httpCode+" – greška servera";
        }
        return error.getErrorCodeName()+(origin.isEmpty()?"":" / "+origin);
    }
    private void openExternalPlayer() {
        if(current==null)return;
        try {
            Intent intent=new Intent(Intent.ACTION_VIEW);
            intent.setDataAndType(Uri.parse(current.url),"video/*");
            intent.addCategory(Intent.CATEGORY_DEFAULT);
            startActivity(Intent.createChooser(intent,"Otvori stream u playeru"));
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this,"Instaliraj VLC ili drugi video player.",Toast.LENGTH_LONG).show();
        }
    }
'''
change(anchor,add+anchor)
change('''        if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){showControls();return true;}''',
       '''        if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){showOptions();return true;}''')
change('''OK  Info     MENU  Opcije''','''OK  Opcije     MENU  Opcije''')
p.write_text(s)
print('Player fix applied',len(s),'characters')

b=Path('app/build.gradle')
t=b.read_text()
assert "versionCode 1" in t and "versionName '0.1.0-full-preview'" in t
assert "applicationIdSuffix '.debug'" in t
t=t.replace('versionCode 1','versionCode 2').replace("versionName '0.1.0-full-preview'","versionName '0.2.0-playback-diagnostics'").replace("applicationIdSuffix '.debug'", "applicationIdSuffix '.beta'")
b.write_text(t)
print('Version and separate beta package applied')
