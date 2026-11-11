from pathlib import Path
base=Path("app/src/main/java/com/keldin/iptv")
def edit(rel,fn):
 p=base/rel
 before=p.read_text()
 after=fn(before)
 if before==after:raise AssertionError("v917 no change "+rel)
 p.write_text(after)
def swap(s,old,new,label):
 if old not in s:raise AssertionError("v917 missing "+label+": "+old[:90])
 return s.replace(old,new,1)

def url(s):
 old='''            if(user==null||pass==null||user.isEmpty()||pass.isEmpty())return "";'''
 new='''            // Also accept Xtream's /get.php?username=...&password=...
            // links, common when a provider is added through an M3U URL.
            if(user==null||pass==null){
                String query=feed.getQuery();
                if(query!=null)for(String part:query.split("&")){
                    int eq=part.indexOf('=');
                    if(eq<=0)continue;
                    String key=java.net.URLDecoder.decode(part.substring(0,eq),"UTF-8")
                        .toLowerCase(java.util.Locale.ROOT);
                    String val=java.net.URLDecoder.decode(part.substring(eq+1),"UTF-8");
                    if("username".equals(key))user=val;
                    if("password".equals(key))pass=val;
                }
            }
            if(user==null||pass==null||user.isEmpty()||pass.isEmpty())return "";'''
 return swap(s,old,new,"detect XMLTV from M3U query credentials")
edit("data/PlaylistSource.java",url)

def parser(s):
 s=swap(s,
 '''        final StringBuilder text = new StringBuilder();''',
 '''        final StringBuilder text = new StringBuilder();
        // Providers often put a different XMLTV <channel id> in the guide
        // than in the M3U tvg-id. Resolve via the XMLTV display-name.
        final Map<String,String> aliases=new HashMap<>();
        final Map<String,String> knownNames=new HashMap<>();
        final StringBuilder channelNameText=new StringBuilder();
        String sourceChannelId="";
        boolean readingDisplayName=false;
        static String normal(String s){
            return s==null?"":s.toLowerCase(Locale.ROOT)
                .replaceAll("\\\\s+"," ").trim();
        }''',"add XMLTV display-name aliases")
 s=swap(s,
 '''        Handler(Set<String> wanted, long now) { this.wanted = new HashSet<>(wanted); this.now = now; }''',
 '''        Handler(Set<String> wanted, long now) {
            this.wanted = new HashSet<>(wanted);this.now=now;
            for(String w:wanted)if(w!=null&&!w.isEmpty())
                knownNames.putIfAbsent(normal(w),w);
        }''',"normalized exact-name lookup")
 s=swap(s,
 '''            if ("programme".equals(qName)) {
                channel = attr.getValue("channel");''',
 '''            if("channel".equals(qName)){
                sourceChannelId=attr.getValue("id");
                if(sourceChannelId==null)sourceChannelId="";
            }
            if("display-name".equals(qName)&&!sourceChannelId.isEmpty()){
                readingDisplayName=true;
                channelNameText.setLength(0);
            }
            if ("programme".equals(qName)) {
                String rawChannel=attr.getValue("channel");
                channel=rawChannel!=null&&wanted.contains(rawChannel)?
                    rawChannel:aliases.get(rawChannel);''',"read alias while parsing EPG channels")
 s=swap(s,
 '''            if (reading && !currentTag.isEmpty() && text.length() < 2000) text.append(ch, start, length);''',
 '''            if(readingDisplayName&&channelNameText.length()<400)
                channelNameText.append(ch,start,length);
            if (reading && !currentTag.isEmpty() && text.length() < 2000)
                text.append(ch,start,length);''',"read XMLTV channel display names")
 s=swap(s,
 '''        @Override public void endElement(String uri, String local, String qName) {
            if (reading && qName.equals(currentTag)) {''',
 '''        @Override public void endElement(String uri, String local, String qName) {
            if("display-name".equals(qName)&&readingDisplayName){
                readingDisplayName=false;
                String wantedName=knownNames.get(normal(channelNameText.toString()));
                if(wantedName!=null&&!sourceChannelId.isEmpty())
                    aliases.putIfAbsent(sourceChannelId,wantedName);
            }
            if("channel".equals(qName))sourceChannelId="";
            if (reading && qName.equals(currentTag)) {''',"use display names for fallback EPG matching")
 return s
edit("net/EpgParser.java",parser)

def main(s):
 # Add nonblocking background EPG downloads. Do not render the whole 150k
 # catalogue again when a new guide arrives.
 s=swap(s,'''    private PlaylistSync sync;''',
 '''    private PlaylistSync sync;
    private final java.util.ArrayDeque<PlaylistSource> epgQueueV917=
        new java.util.ArrayDeque<>();
    private boolean epgLoadingV917=false;
    private RecyclerView guideViewV917;
    private void autoEpgV917(){
        if(store==null||sync==null||isFinishing()||isDestroyed()||epgLoadingV917)return;
        epgQueueV917.clear();
        for(PlaylistSource source:store.sources())
            if(store.isPlaylistActiveV99(source.id)&&
                    !source.guideUrl().isEmpty())
                epgQueueV917.addLast(source);
        epgLoadingV917=true;
        nextEpgV917();
    }
    private void nextEpgV917(){
        if(isFinishing()||isDestroyed()){epgLoadingV917=false;return;}
        PlaylistSource source=epgQueueV917.pollFirst();
        if(source==null){epgLoadingV917=false;return;}
        sync.refreshEpg(source,(count,status,error)->{
            if(isFinishing()||isDestroyed())return;
            if(status!=null&&status.startsWith("EPG:"))
                redrawGuideCardsV917();
            nextEpgV917();
        });
    }
    private void redrawGuideCardsV917(){
        RecyclerView target="TV vodič".equals(page)?guideViewV917:activeGridV911;
        if(target==null||target.getParent()==null)return;
        target.post(()->{
            if(target.getParent()==null||target.isComputingLayout())return;
            RecyclerView.Adapter<?> adapter=target.getAdapter();
            if(adapter!=null)adapter.notifyDataSetChanged();
        });
    }
''',"EPG lifecycle and visible-card refresh")
 s=swap(s,
 '''                    sync=new PlaylistSync(this,store);
                    createShell();''',
 '''                    sync=new PlaylistSync(this,store);
                    createShell();
                    // EPG is fetched after Home is visible and never blocks
                    // Loading your library or channel playback.
                    mainHandler.postDelayed(this::autoEpgV917,2500);''',"start EPG automatically after library loaded")
 s=swap(s,
 '''        guide.setAdapter(new GuideAdapter(store,live,this::play));''',
 '''        guide.setAdapter(new GuideAdapter(store,live,this::play));
        guideViewV917=guide;''',"track guide RecyclerView for EPG result refresh")
 s=swap(s,
 '''    @Override protected void onDestroy(){if(sync!=null)sync.shutdown();super.onDestroy();}''',
 '''    @Override protected void onDestroy(){
        epgQueueV917.clear();
        guideViewV917=null;
        if(sync!=null)sync.shutdown();
        super.onDestroy();
    }''',"clean guide tasks when exiting")
 return s
edit("ui/MainActivity.java",main)

def wizard(s):
 marker='''                ui.post(()->complete(true,message));'''
 addition='''                // M3U playlists and Xtream accounts should begin downloading
                // their programme schedule automatically after a successful
                // import, rather than waiting for the user to open TV Guide.
                if(!source.guideUrl().isEmpty()){
                    final PlaylistSync backgroundGuideV917=
                        new PlaylistSync(activity.getApplicationContext(),store);
                    backgroundGuideV917.refreshEpg(source,(n,status,error)->
                        backgroundGuideV917.shutdown());
                }
                ui.post(()->complete(true,message));'''
 return swap(s,marker,addition,"auto EPG after successful import")
edit("net/PlaylistWizardV6.java",wizard)

p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 916" in g and "versionName '0.9.16'" in g
p.write_text(g.replace("versionCode 916","versionCode 917",1)
              .replace("versionName '0.9.16'","versionName '0.9.17'",1))
print("PASS v0.9.17: EPG autoload, Xtream M3U query discovery, XMLTV display-name matching, UI refresh and preserved data")
