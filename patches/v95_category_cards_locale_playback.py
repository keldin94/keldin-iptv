from pathlib import Path

def edit(path, changes):
    file=Path(path)
    s=file.read_text()
    for label,old,new in changes:
        if old not in s:
            raise AssertionError("v0.9.5 missing anchor "+label+" in "+path)
        s=s.replace(old,new,1)
    file.write_text(s)

base="app/src/main/java/com/keldin/iptv/"

edit(base+"data/Channel.java",[
 ("classify live-film category",
 '''    public static String inferKind(String group, String url) {
        String g = group.toLowerCase(Locale.ROOT);
        String u = url.toLowerCase(Locale.ROOT);''',
 '''    /** TV film CHANNEL categories are not VOD movies. */
    public static boolean isLiveFilmGroup(String group,String url){
        String g=(group==null?"":group).toLowerCase(Locale.ROOT)
            .replace('-', ' ').replace('_', ' ').replace('|',' ');
        String u=(url==null?"":url).toLowerCase(Locale.ROOT);
        if(u.contains("/movie/")||u.contains("/series/"))return false;
        // Ex-Yu cinematic broadcasters, including HBO, AXN and CineStar.
        return (g.contains("ex yu")||g.contains("exyu")||
                g.contains("ex jug")||g.contains("ex yug")) &&
               (g.contains("filmski")||g.contains("filmsk")||
                g.contains("movie channels")||g.contains("films channels"));
    }
    public static String inferKind(String group, String url) {
        String g = (group==null?"":group).toLowerCase(Locale.ROOT);
        String u = (url==null?"":url).toLowerCase(Locale.ROOT);
        if(u.contains("/live/")||isLiveFilmGroup(group,url)) return "LIVE";''')
])

edit(base+"net/CategoryScanV61.java",[
 ("scan classifier live priority",
 '''        String u=url.toLowerCase(Locale.ROOT);
        if(g.contains("radio")''',
 '''        String u=url.toLowerCase(Locale.ROOT);
        if(u.contains("/live/")||
           com.keldin.iptv.data.Channel.isLiveFilmGroup(group,url))return 0;
        if(g.contains("radio")''')
])

edit(base+"data/CatalogStore.java",[
 ("migrate existing cached category only",
 '''                    c.group=o.optString("group","Ostalo");
                    c.kind=o.optString("kind","LIVE");c.userAgent=o.optString("userAgent");
                    channels.add(c);''',
 '''                    c.group=o.optString("group","Ostalo");
                    c.kind=o.optString("kind","LIVE");c.userAgent=o.optString("userAgent");
                    if("MOVIES".equals(c.kind)&&Channel.isLiveFilmGroup(c.group,c.url))
                        c.kind="LIVE"; // Migrate already imported TV groups in memory.
                    channels.add(c);''')
])

edit(base+"ui/ChannelAdapter.java",[
 ("smaller channel card padding",
  'box.setPadding(Ui.dp(c,15),Ui.dp(c,15),Ui.dp(c,15),Ui.dp(c,12));',
  'box.setPadding(Ui.dp(c,11),Ui.dp(c,11),Ui.dp(c,11),Ui.dp(c,9));'),
 ("tight logo tile",
  'FrameLayout.LayoutParams imageLp=new FrameLayout.LayoutParams(Ui.dp(c,52),Ui.dp(c,52),Gravity.CENTER);',
  'FrameLayout.LayoutParams imageLp=new FrameLayout.LayoutParams(Ui.dp(c,47),Ui.dp(c,47),Gravity.CENTER);'),
 ("tight head",
  'head.addView(tile,Ui.lp(c,66,58));',
  'head.addView(tile,Ui.lp(c,53,52));'),
 ("two-line channel name",
  'TextView name=Ui.text(c,"",guideMode?17:16,Ui.WHITE,true);name.setMaxLines(1);name.setEllipsize(android.text.TextUtils.TruncateAt.END);',
  'TextView name=Ui.text(c,"",guideMode?15:14,Ui.WHITE,true);name.setMaxLines(2);name.setEllipsize(android.text.TextUtils.TruncateAt.END);'),
 ("remove category subtitle",
  'headText.addView(name); headText.addView(category);',
  'headText.addView(name); // The selected category is already shown in the left rail.'),
 ("shrink name left spacing",
  'ht.leftMargin=Ui.dp(c,10);',
  'ht.leftMargin=Ui.dp(c,5);'),
 ("shrink epg gap",
  'box.addView(Ui.space(c,guideMode?3:9));',
  'box.addView(Ui.space(c,guideMode?3:5));'),
 ("more readable epg",
  'program.setSingleLine(true); program.setEllipsize(android.text.TextUtils.TruncateAt.END);',
  'program.setMaxLines(2); program.setEllipsize(android.text.TextUtils.TruncateAt.END);'),
 ("epg layout",
  'box.addView(program,Ui.lp(c,-1,19));',
  'box.addView(program,Ui.lp(c,-1,32));'),
 ("remove redundant LIVE footer",
  'if(!guideMode)box.addView(footer,fp);',
  '// No LIVE dot, category or duplicate footer on individual channel cards.'),
 ("hide empty epg progress",
  'if(current!=null) {\n            h.program.setText(current.title);',
  'if(current!=null) {\n            h.progress.setVisibility(View.VISIBLE);\n            h.program.setText(current.title);'),
 ("localize no EPG and suppress fake bar",
  'h.program.setText("TV vodič nije dostupan");',
  'h.program.setText(I18n.t(h.itemView.getContext(),"guide_unavailable"));\n            h.progress.setVisibility(View.GONE);'),
 ("no duplicate category binding",
  'h.name.setText(ch.name);h.category.setText(ch.group);',
  'h.name.setText(ch.name); // Do not repeat the category on every card.')
])

edit(base+"ui/MainActivity.java",[
 ("localize channel listing count",
  'count.setText(visible.size()+" items  •  OK to open");',
  'count.setText(visible.size()+" "+tr("items"));'),
 ("localize filtered count",
  'count.setText(filtered.size()+" items  •  "+group);',
  'count.setText(filtered.size()+" "+tr("items")+"  •  "+group);')
])

edit(base+"playback/PlayerActivity.java",[
 ("translate buffering state",
  'status.setText("Učitavanje streama...");',
  'status.setText(com.keldin.iptv.ui.UiLocaleV9.translate(PlayerActivity.this,"Buffering..."));'),
 ("translate buffering watchdog",
  'status.setText("Buffer stalled — reconnecting...");',
  'status.setText(com.keldin.iptv.ui.UiLocaleV9.translate(this,"Buffer stalled — reconnecting..."));'),
 ("translate ended live state",
  'status.setText("Prijenos je prekinut — pokušavam obnoviti vezu...");',
  'status.setText(com.keldin.iptv.ui.UiLocaleV9.translate(PlayerActivity.this,"Stream interrupted — reconnecting..."));'),
 ("translate ended nonlive state",
  'status.setText("Reprodukcija je završena.");',
  'status.setText(com.keldin.iptv.ui.UiLocaleV9.translate(PlayerActivity.this,"Playback ended."));'),
 ("translate empty channel group",
  'status.setText("No other channel in this category");',
  'status.setText(com.keldin.iptv.ui.UiLocaleV9.translate(this,"No other channel in this category"));'),
 ("safer live jitter rebuffer",
  'int rebufferMs=liveStream?3000:Math.min(1200,minBuffer);',
  'int rebufferMs=liveStream?Math.max(4500,Math.min(7000,minBuffer/2)):Math.min(1200,minBuffer);')
])

# Use the full 16-language order already defined in I18n. The four major locales
# retain existing settings translations; new player alerts are translated in all locales.
edit(base+"ui/UiLocaleV9.java",[
 ("localized 16 language runtime for new messages",
  '    private static final Map<String,String[]> TEXT=new HashMap<>();',
  '''    private static final Map<String,String[]> TEXT=new HashMap<>();
    private static final Map<String,String[]> FULL=new HashMap<>();
    private static void put16(String... items){
        if(items.length!=16)throw new IllegalArgumentException("16 translations required");
        FULL.put(items[0],items);
    }'''),
 ("16-language playback labels",
  '    static {\n        put("Accent color"',
  '''    static {
        put16("Buffering...","Učitavanje...","Medpomnjenje...","Almacenando en búfer...","Carregando buffer...","बफ़रिंग...","جارٍ التخزين المؤقت...","Mise en mémoire tampon...","Memuat buffer...","Puffern...","Arabelleğe alınıyor...","バッファリング中...","버퍼링 중...","正在缓冲...","Буферизация...","বাফারিং...");
        put16("Buffer stalled — reconnecting...","Učitavanje je zastalo — ponovo povezivanje...","Medpomnjenje je obstalo — ponovno povezovanje...","Búfer detenido — reconectando...","Buffer parou — reconectando...","बफ़र रुका — पुनः कनेक्ट हो रहा है...","توقف التخزين المؤقت — إعادة الاتصال...","Mise en mémoire bloquée — reconnexion...","Buffer berhenti — menyambung ulang...","Puffer angehalten – erneute Verbindung...","Tampon durdu — yeniden bağlanılıyor...","バッファが停止 — 再接続中...","버퍼 중단 — 다시 연결 중...","缓冲停滞，正在重连...","Буферизация остановлена — переподключение...","বাফার থেমেছে — পুনঃসংযোগ...");
        put16("Stream interrupted — reconnecting...","Prijenos prekinut — ponovo povezivanje...","Prenos prekinjen — ponovno povezovanje...","Transmisión interrumpida — reconectando...","Transmissão interrompida — reconectando...","स्ट्रीम रुकी — पुनः कनेक्ट हो रहा है...","انقطع البث — جارٍ إعادة الاتصال...","Flux interrompu — reconnexion...","Siaran terputus — menyambung ulang...","Stream unterbrochen – erneute Verbindung...","Yayın kesildi — yeniden bağlanılıyor...","配信が中断 — 再接続中...","스트림 중단 — 다시 연결 중...","播放中断，正在重连...","Трансляция прервана — переподключение...","স্ট্রিম বন্ধ — পুনঃসংযোগ...");
        put16("Playback ended.","Reprodukcija završena.","Predvajanje se je končalo.","La reproducción terminó.","A reprodução terminou.","प्लेबैक समाप्त हुआ।","انتهى التشغيل.","Lecture terminée.","Pemutaran selesai.","Wiedergabe beendet.","Oynatma bitti.","再生が終了しました。","재생이 종료되었습니다.","播放结束。","Воспроизведение завершено.","প্লেব্যাক শেষ।");
        put16("No other channel in this category","Nema drugih kanala u ovoj kategoriji","V tej kategoriji ni drugih kanalov","No hay más canales en esta categoría","Não há outros canais nesta categoria","इस श्रेणी में अन्य चैनल नहीं हैं","لا توجد قنوات أخرى في هذه الفئة","Aucune autre chaîne dans cette catégorie","Tidak ada saluran lain dalam kategori ini","Keine weiteren Sender in dieser Kategorie","Bu kategoride başka kanal yok","このカテゴリーに他のチャンネルはありません","이 카테고리에 다른 채널이 없습니다","此分类没有其他频道","В этой категории нет других каналов","এই বিভাগে আর কোনো চ্যানেল নেই");
        put("Accent color"'''),
 ("fallback add full map",
  '        String[] entry=TEXT.get(value);',
  '''        String[] full=FULL.get(value);
        if(full!=null)return full[I18n.selectedLanguage(context)];
        String[] entry=TEXT.get(value);''')
])

# Record localized, privacy-safe diagnoses instead of an unverifiable exact cause.
diag=Path(base+"playback/PlaybackDiagnosticsV91.java")
s=diag.read_text()
needle='''        return "Recent playback events (local times):\\n\\n"+events;'''
assert needle in s, "diagnostics report return missing"
s=s.replace(needle,'''        int buffering=events.split("BUFFERING started",-1).length-1;
        int drops=events.split("DROPPED FRAMES",-1).length-1;
        int errors=events.split("PLAYER ERROR",-1).length-1;
        String hint=buffering>drops?
            "Repeated buffering: check server throughput, Wi-Fi and playlist stream.":
            drops>0?"Dropped video frames: check decoder load and output format.":
            "No clear stutter cause in these events.";
        return "Playback review (not a definitive diagnosis):\\n"+
            "Buffering events: "+buffering+"  |  Dropped-frame events: "+drops+
            "  |  Player errors: "+errors+"\\n"+hint+
            "\\n\\nRecent playback events (local times):\\n\\n"+events;''',1)
diag.write_text(s)

# Reuse the exact permanent package identity and signing key.
gradle=Path("app/build.gradle")
s=gradle.read_text()
assert "versionCode 904" in s and "versionName '0.9.4'" in s
gradle.write_text(s.replace("versionCode 904","versionCode 905",1)
                   .replace("versionName '0.9.4'","versionName '0.9.5'",1))
print("Applied v0.9.5: EX-YU film broadcasters -> live, legacy cache migration, compact EPG cards, localized player and jitter tolerance")
