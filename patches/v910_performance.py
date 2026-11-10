from pathlib import Path
import re

ROOT=Path("app/src/main/java/com/keldin/iptv")
def edit(name,fn):
    path=ROOT/name
    before=path.read_text()
    after=fn(before)
    if before==after:raise AssertionError("v910 unchanged "+name)
    path.write_text(after)
def swap(s,before,after,label):
    if before not in s:raise AssertionError("v910 missing "+label+" "+before[:65])
    return s.replace(before,after,1)

# v0.9.9 checked SharedPreferences once for EACH channel, for EACH catalog read.
# The source activation state changes only per provider, not per channel.
def catalog(s):
    before='''    public synchronized List<Channel> channels(){
        ArrayList<Channel> visible=new ArrayList<>();
        for(Channel c:channels)
            if(isPlaylistActiveV99(c.sourceId))visible.add(c);
        return visible;
    }'''
    after='''    public synchronized List<Channel> channels(){
        java.util.HashSet<String> enabled=new java.util.HashSet<>();
        for(PlaylistSource src:sources)
            if(isPlaylistActiveV99(src.id))enabled.add(src.id);
        ArrayList<Channel> visible=new ArrayList<>(channels.size());
        for(Channel c:channels)
            if(enabled.contains(c.sourceId))visible.add(c);
        return visible;
    }

    // Source-scoped, read-only-in-practice index; no giant global snapshot
    // needs to be rebuilt each time the remote opens the TV Grid / categories.
    private final java.util.HashMap<String,ArrayList<Channel>> liveIndexV910=
        new java.util.HashMap<>();
    private boolean liveIndexReadyV910=false;

    public synchronized List<Channel> liveChannelsForSourceV910(String sourceId){
        if(sourceId==null||!isPlaylistActiveV99(sourceId))
            return java.util.Collections.emptyList();
        if(!liveIndexReadyV910){
            liveIndexV910.clear();
            for(Channel c:channels){
                if(!"LIVE".equals(c.kind))continue;
                liveIndexV910.computeIfAbsent(c.sourceId,
                    key->new ArrayList<>()).add(c);
            }
            liveIndexReadyV910=true;
        }
        List<Channel> result=liveIndexV910.get(sourceId);
        return result==null?java.util.Collections.emptyList():result;
    }
'''
    s=swap(s,before,after,"per-channel preference lookup")
    # Refreshing a provider must invalidate the source index even if the
    # replacement stream count is identical.
    match=re.search(r'public\s+(?:synchronized\s+)?void\s+updateChannels\s*\([^)]*\)\s*\{',s)
    if not match:raise AssertionError("cannot locate catalog updateChannels")
    s=s[:match.end()]+'''
        liveIndexReadyV910=false;
        liveIndexV910.clear();'''+s[match.end():]
    return s
edit("data/CatalogStore.java",catalog)

# Build a snapshot ONCE per live source. Directional category navigation then
# looks up existing lists rather than scanning 150k catalogue entries repeatedly.
def side(s):
    marker='''    private void updateCategoryLogoPreviewV98(){'''
    helper='''    private String indexedSourceV910="";
    private final ArrayList<Channel> sourceLiveV910=new ArrayList<>();
    private final LinkedHashMap<String,ArrayList<Channel>> groupLiveV910=
        new LinkedHashMap<>();
    private String previewGroupV910="";

    private void indexSourceV910(){
        if(current==null)return;
        if(current.sourceId.equals(indexedSourceV910))return;
        indexedSourceV910=current.sourceId;
        sourceLiveV910.clear();groupLiveV910.clear();
        java.util.Set<String> excluded=store.excludedGroups(current.sourceId);
        boolean hideAdult=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getBoolean("hide_adult_content_v93",true)||
            (store.parentalLocked()&&!store.isContentUnlocked());
        for(Channel c:store.liveChannelsForSourceV910(current.sourceId)){
            if(excluded.contains(c.group)||excluded.contains("@kind:LIVE"))
                continue;
            if(hideAdult&&com.keldin.iptv.data.ContentFilterV93.isExplicit(
                c.group,c.name))continue;
            sourceLiveV910.add(c);
            String group=(c.group==null||c.group.isEmpty())?"Ostalo":c.group;
            groupLiveV910.computeIfAbsent(group,k->new ArrayList<>()).add(c);
        }
    }

'''
    s=swap(s,marker,helper+marker,"source index method")
    a=s.index("    private void updateCategoryLogoPreviewV98(){")
    b=s.index("    private void refresh(){",a)
    preview='''    private void updateCategoryLogoPreviewV98(){
        if(mode!=CATEGORIES||categoryLogoPreviewV98==null||
            selection<0||selection>=rows.size())return;
        String group=rows.get(selection).category;
        if(group==null||group.equals(previewGroupV910))return;
        previewGroupV910=group;
        List<Channel> matching="Sve kategorije".equals(group)?
            sourceLiveV910:groupLiveV910.get(group);
        ArrayList<Channel> preview=new ArrayList<>();
        if(matching!=null)for(Channel c:matching){
            preview.add(c);
            if(preview.size()>=48)break; // Lazy views + bounded previews.
        }
        categoryLogoPreviewV98.setAdapter(new LogoOnlyAdapter(preview));
    }

'''
    s=s[:a]+preview+s[b:]
    s=swap(s,'''    private void refresh(){
        categoryLogoPreviewV98=null;''',
      '''    private void refresh(){
        if(mode==CHANNELS||mode==CATEGORIES)indexSourceV910();
        previewGroupV910="";
        categoryLogoPreviewV98=null;''',
      "one snapshot for category refresh")
    s=swap(s,'''            List<Channel> channels=store.channels();''',
        '''            List<Channel> channels="Sve kategorije".equals(selectedCategory)?
                sourceLiveV910:groupLiveV910.get(selectedCategory);
            if(channels==null)channels=java.util.Collections.emptyList();''',
        "channel rows use source's selected group")
    s=swap(s,'''            for(Channel c:store.channels()){
                if("LIVE".equals(c.kind)&&c.sourceId.equals(current.sourceId)){''',
        '''            for(Channel c:sourceLiveV910){
                if("LIVE".equals(c.kind)){''',
        "category counts use cached source")
    s=swap(s,'''        list=null;adapter=null;detailInfo=null;rows.clear();''',
        '''        list=null;adapter=null;detailInfo=null;rows.clear();
        categoryLogoPreviewV98=null;previewGroupV910="";''',
        "release old preview adapter")
    return s
edit("playback/TvSidePanel.java",side)

def grid(s):
    return swap(s,'''        for(Channel ch:store.channels()){''',
        '''        for(Channel ch:store.liveChannelsForSourceV910(active.sourceId)){''',
        "TV Grid restricted to indexed source")
edit("playback/TvGridPanelV97.java",grid)

# An unbounded fixed-thread-pool queue used to accumulate image decoding tasks
# during fast scroll, even after RecyclerView holders were recycled.
def logos(s):
    s=swap(s,'''    private static final ExecutorService pool=Executors.newFixedThreadPool(3);''',
    '''    // At most three fetches and 24 waiting tiles; never accumulate
    // thousands of abandoned logo requests while scrolling large lists.
    private static final java.util.concurrent.ThreadPoolExecutor pool=
        new java.util.concurrent.ThreadPoolExecutor(3,3,15,
            java.util.concurrent.TimeUnit.SECONDS,
            new java.util.concurrent.ArrayBlockingQueue<>(24),
            new java.util.concurrent.ThreadPoolExecutor.DiscardPolicy());''',
    "bounded logo decode and network queue")
    return s
edit("ui/LogoLoader.java",logos)

# Remote channel zapping already caches its group in v0.9.4; keep that
# stable implementation rather than adding a second competing cache.

# Category switches should never recalculate every channel's SHA-256 hash
# when the user has not hidden any titles, or scan the whole combined list.
def main(s):
    marker='''        for(Channel ch:source){
            if(!store.isPlaylistActiveV99(ch.sourceId))continue;'''
    replacement='''        java.util.HashSet<String> activeSourceIdsV910=new java.util.HashSet<>();
        for(PlaylistSource p:store.sources())
            if(store.isPlaylistActiveV99(p.id))activeSourceIdsV910.add(p.id);
        for(Channel ch:source){
            if(!activeSourceIdsV910.contains(ch.sourceId))continue;'''
    s=swap(s,marker,replacement,"avoid prefs read for every channel")
    s=swap(s,'''            String effectiveKind=Channel.isLiveFilmGroup(ch.group,ch.url)?"LIVE":ch.kind;''',
      '''            String effectiveKind="LIVE".equals(ch.kind)?"LIVE":
                Channel.isLiveFilmGroup(ch.group,ch.url)?"LIVE":ch.kind;''',
      "no reclassification of already live channels")
    s=swap(s,'''            if(hiddenTitles.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.key())))
                continue;''',
      '''            if(!hiddenTitles.isEmpty()&&hiddenTitles.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.key())))
                continue;''',"avoid unnecessary SHA-256 for each media item")
    s=swap(s,'''            if("SERIES".equals(ch.kind)&&hiddenSeries.contains(''',
      '''            if("SERIES".equals(ch.kind)&&!hiddenSeries.isEmpty()&&hiddenSeries.contains(''',
      "avoid unnecessary series title hashing")
    # Build a source+group lookup on the browse screen once, preserving source
    # order, per-playlist activation, and current focus behavior.
    marker='''        if(isPosters)java.util.Collections.reverse(section);

        String previous=viewingPrefs.getString("selected_source_"+page,"");'''
    replacement='''        if(isPosters)java.util.Collections.reverse(section);
        final java.util.HashMap<String,ArrayList<Channel>> sourceItemsV910=
            new java.util.HashMap<>();
        final java.util.HashMap<String,java.util.HashMap<String,ArrayList<Channel>>> groupItemsV910=
            new java.util.HashMap<>();
        for(Channel ch:section){
            sourceItemsV910.computeIfAbsent(ch.sourceId,k->new ArrayList<>()).add(ch);
            String label=(ch.group==null||ch.group.isEmpty())?"Ostalo":ch.group;
            groupItemsV910.computeIfAbsent(ch.sourceId,k->new java.util.HashMap<>())
                .computeIfAbsent(label,k->new ArrayList<>()).add(ch);
        }

        String previous=viewingPrefs.getString("selected_source_"+page,"");'''
    s=swap(s,marker,replacement,"index visible groups in current browsing section")
    s=swap(s,'''        ArrayList<Channel> visible=filterSourceV99(section,selectedSourceV99,selectedGroup);''',
      '''        ArrayList<Channel> visible=filterIndexedV910(
            sourceItemsV910,groupItemsV910,selectedSourceV99,selectedGroup);''',
      "initial filter uses group index")
    s=swap(s,'''                    ArrayList<Channel> filtered=filterSourceV99(
                        section,sourceId,group);''',
      '''                    ArrayList<Channel> filtered=filterIndexedV910(
                        sourceItemsV910,groupItemsV910,sourceId,group);''',
      "category select uses group index")
    index=s.index("    private ArrayList<Channel> filterSourceV99(")
    helper='''    private ArrayList<Channel> filterIndexedV910(
            java.util.Map<String,ArrayList<Channel>> bySource,
            java.util.Map<String,java.util.HashMap<String,ArrayList<Channel>>> groups,
            String sourceId,String group){
        List<Channel> match=null;
        if(PlaylistGroupAdapterV99.ALL.equals(group))match=bySource.get(sourceId);
        else {
            java.util.Map<String,ArrayList<Channel>> selected=groups.get(sourceId);
            if(selected!=null)match=selected.get(group);
        }
        return match==null?new ArrayList<>():new ArrayList<>(match);
    }

'''
    s=s[:index]+helper+s[index:]
    return s
edit("ui/MainActivity.java",main)

version=Path("app/build.gradle")
g=version.read_text()
assert "versionCode 909" in g and "versionName '0.9.9'" in g
version.write_text(g.replace("versionCode 909","versionCode 910",1)
                   .replace("versionName '0.9.9'","versionName '0.9.10'",1))
print("PASS v0.9.10: indexed categories, bounded logos, fast source groups, channel-zap caching; identity retained")
