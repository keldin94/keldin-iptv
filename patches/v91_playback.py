from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def replace_once(old,new,label):
    global s
    assert old in s, "v0.9.1 playback patch marker missing: "+label
    s=s.replace(old,new,1)

replace_once('''        int secs=store.bufferSeconds();
        int minBuffer=Math.max(1300,secs*1000),maxBuffer=Math.max(9000,minBuffer*5);
        DefaultLoadControl load=new DefaultLoadControl.Builder()
            .setBufferDurationsMs(minBuffer,maxBuffer,Math.min(1200,minBuffer),Math.min(1200,minBuffer))
            .build();''',
'''        int secs=store.bufferSeconds();
        // Live IPTV benefits from a deeper jitter buffer than VOD. The old
        // default could allow only ~3 seconds buffered ahead of playback.
        boolean liveStream="LIVE".equals(current.kind);
        int minBuffer=liveStream?Math.max(8000,secs*1000):Math.max(1300,secs*1000);
        int maxBuffer=liveStream?Math.max(30000,minBuffer*4):Math.max(9000,minBuffer*5);
        int startMs=liveStream?2500:Math.min(1200,minBuffer);
        int rebufferMs=liveStream?3000:Math.min(1200,minBuffer);
        DefaultLoadControl load=new DefaultLoadControl.Builder()
            .setBufferDurationsMs(minBuffer,maxBuffer,startMs,rebufferMs)
            .build();''',"live rebuffer safety")
replace_once('''        player.addListener(new Player.Listener(){''',
'''        PlaybackDiagnosticsV91.watch(this,player);
        player.addListener(new Player.Listener(){''',"instrument player states, seeks and dropped frames")
replace_once('''        handler.postDelayed(bufferingCheck,22000);''',
'''        int timeout=getSharedPreferences("keldin_settings",MODE_PRIVATE)
            .getInt("playback_stall_seconds",60);
        if(timeout>0)
            handler.postDelayed(bufferingCheck,Math.max(30,Math.min(timeout,120))*1000L);''',"replace aggressive 22s watchdog")
replace_once('''            status.setText("Veza je zastala — ponovno povezivanje...");
            scheduleRetry("Buffer traje predugo");''',
'''            PlaybackDiagnosticsV91.record(this,"WATCHDOG timeout: automatic stream reconnect");
            status.setText("Buffer stalled — reconnecting...");
            scheduleRetry("Buffer stalled");''',"watchdog action log")
replace_once('''    private void scheduleRetry(String reason) {
        handler.removeCallbacks(bufferingCheck);handler.removeCallbacks(retry);''',
'''    private void scheduleRetry(String reason) {
        PlaybackDiagnosticsV91.record(this,"AUTO RETRY requested");
        handler.removeCallbacks(bufferingCheck);handler.removeCallbacks(retry);''',"retry log")
# Make existing player menu's diagnostics show playback states. Do not include URL,
# title, provider credentials or raw network exceptions in the report.
needle='''.setMessage(lastError+"\\nNačin: "+playbackModeName()+'''
assert needle in s,"playback diagnostics menu marker missing"
s=s.replace(needle,'''.setMessage("Player mode: "+playbackModeName()+"\\nLast error: "+lastError+
                            "\\n\\n"+PlaybackDiagnosticsV91.report(this)+''',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
needle='''        addOptionV6(body,"Overlay auto-hide",'''
assert needle in s,"Video tab marker missing"
s=s.replace(needle,'''        addOptionV6(body,"Buffer stall recovery",
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("playback_stall_seconds",60)==0?"Never":
            getSharedPreferences("keldin_settings",MODE_PRIVATE)
                .getInt("playback_stall_seconds",60)+" s",
            "Reconnect only after a live stream remains buffering for the selected interval. "+
            "Longer intervals help prevent premature restarts; Off disables this watchdog.",()->{
                String[] options={"30 s","45 s","60 s","90 s","120 s","Never"};
                int[] seconds={30,45,60,90,120,0};
                new AlertDialog.Builder(this).setTitle("Buffer stall recovery")
                    .setItems(options,(d,index)->{
                        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                            .putInt("playback_stall_seconds",seconds[index]).apply();
                        render();
                    }).show();
            });
'''+needle,1)
needle='''        headingV6(body,"Troubleshooting");'''
assert needle in s,"System tab marker missing"
s=s.replace(needle,'''        headingV6(body,"Troubleshooting");
        addOptionV6(body,"Playback diagnostics","Buffering / jumps / dropped frames",
            "Shows a local, time-stamped record of player buffering, position jumps, "+
            "decoder dropped frames and retry attempts, without playlist passwords.",()->{
                new AlertDialog.Builder(this).setTitle("Playback diagnostics")
                    .setMessage(com.keldin.iptv.playback.PlaybackDiagnosticsV91.report(this))
                    .setPositiveButton("OK",null).show();
            });''',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java")
s=p.read_text()
needle='''        put("Connected  •  Playing","Povezano  •  Reprodukcija","Povezano  •  Predvajanje","Verbunden  •  Wiedergabe");'''
assert needle in s
s=s.replace(needle,needle+'''
        put("Buffer stall recovery","Oporavak nakon zastoja","Obnovitev po zastoju","Neustart bei Pufferstillstand");
        put("Playback diagnostics","Dijagnostika reprodukcije","Diagnostika predvajanja","Wiedergabediagnose");
        put("Buffering / jumps / dropped frames","Učitavanje / preskakanje / izgubljeni kadrovi",
            "Medpomnjenje / preskoki / izgubljeni okvirji","Pufferung / Sprünge / ausgelassene Bilder");
''',1)
p.write_text(s)
print("v0.9.1: 60s adjustable watchdog, deeper live buffer, private playback state telemetry")
