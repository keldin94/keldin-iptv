from pathlib import Path

base=Path("app/src/main/java/com/keldin/iptv")
def edit(relative,transform):
    p=base/relative
    original=p.read_text()
    changed=transform(original)
    if original==changed:raise AssertionError("v920 no change "+relative)
    p.write_text(changed)
def one(s,old,new,label):
    if old not in s:raise AssertionError("v920 missing "+label+" : "+old[:140])
    return s.replace(old,new,1)

def store(s):
    s=one(s,
      '''                if(!"LIVE".equals(c.kind))continue;
                liveIndexV910.computeIfAbsent(c.sourceId,''',
      '''                if(!"LIVE".equals(c.kind)
                        &&!Channel.isLiveFilmGroup(c.group,c.url))continue;
                liveIndexV910.computeIfAbsent(c.sourceId,''',
      "include existing EX YU film broadcasters in fast TV index")
    return s
edit("data/CatalogStore.java",store)

def main(s):
    # On an enormous M3U this used to copy every VOD movie/series item,
    # classify it and construct two group indexes on the main thread
    # before displaying even the first TV channel. Use the already indexed
    # LIVE-only source, which is prewarmed by the background catalog loader.
    s=one(s,
      '''        List<Channel> source="Favoriti".equals(page)?store.favorites():store.channels();''',
      '''        List<Channel> source="Favoriti".equals(page)?store.favorites():
            "Uživo".equals(page)
                ?store.liveChannelsForSourceV910(store.activePlaylistIdV918())
                :store.channels();''',
      "show Live TV without scanning all Movies and Series")
    s=one(s,
      '''                    store=prepared;
                    sync=new PlaylistSync(this,store);''',
      '''                    store=prepared;
                    sync=new PlaylistSync(this,store);''',
      "verify background library init anchor")
    # Prewarm source-scoped live index before runOnUiThread, preserving
    # instantaneous Home and avoiding a first-time scan when opening Live.
    s=one(s,
      '''                CatalogStore prepared=CatalogStore.shared(getApplicationContext());
                runOnUiThread(()->{''',
      '''                CatalogStore prepared=CatalogStore.shared(getApplicationContext());
                prepared.liveChannelsForSourceV910(prepared.activePlaylistIdV918());
                runOnUiThread(()->{''',
      "index Live TV in background before Home displayed")
    s=one(s,
      '''        ChannelAdapter liveAdapter=null;
        PosterAdapterV6 posterAdapter=null;
        if(isPosters){
            posterAdapter=new PosterAdapterV6(visible,this::openMediaDetails);
            grid.setAdapter(posterAdapter);
        }else{
            liveAdapter=new ChannelAdapter(store,visible,this::play,guideMode);
            grid.setAdapter(liveAdapter);
        }''',
      '''        ChannelAdapter liveAdapter=null;
        PosterAdapterV6 posterAdapter=null;
        PagedLiveGridV920 pagedLiveV920=null;
        if(isPosters){
            posterAdapter=new PosterAdapterV6(visible,this::openMediaDetails);
            grid.setAdapter(posterAdapter);
        }else{
            liveAdapter=new ChannelAdapter(store,
                java.util.Collections.emptyList(),this::play,guideMode);
            grid.setAdapter(liveAdapter);
            pagedLiveV920=new PagedLiveGridV920(grid,liveAdapter,gridManager);
            pagedLiveV920.show(visible);
        }''',
      "bounded Live TV grid adapter window")
    s=one(s,
      '''        final ChannelAdapter channelCards=liveAdapter;
        final PosterAdapterV6 movieCards=posterAdapter;''',
      '''        final ChannelAdapter channelCards=liveAdapter;
        final PagedLiveGridV920 channelPagerV920=pagedLiveV920;
        final PosterAdapterV6 movieCards=posterAdapter;''',
      "retain pager for group selection and last-channel restore")
    s=one(s,
      '''                    if(channelCards!=null)channelCards.setItems(filtered);''',
      '''                    if(channelPagerV920!=null)channelPagerV920.show(filtered);''',
      "change categories without binding entire all-channel collection")
    s=one(s,
      '''                if(channelCards!=null)channelCards.setItems(restored);
                count.setText(restored.size()+" "+tr("items")+"  •  "+group);''',
      '''                count.setText(restored.size()+" "+tr("items")+"  •  "+group);''',
      "defer last-channel grid page selection")
    s=one(s,
      '''                final int focusIndex=found;
                grid.post(()->{
                    if(!"Uživo".equals(page))return;
                    grid.scrollToPosition(focusIndex);''',
      '''                final int focusIndex=found;
                if(channelPagerV920!=null)channelPagerV920.show(restored,focusIndex);
                grid.post(()->{
                    if(!"Uživo".equals(page))return;
                    grid.scrollToPosition(channelPagerV920==null?focusIndex:
                        channelPagerV920.localIndex(focusIndex));''',
      "restore far-away TV channel with bounded adapter window")
    s=one(s,
      '''                            grid.findViewHolderForAdapterPosition(focusIndex);
                        if(item!=null)item.itemView.requestFocus();''',
      '''                            grid.findViewHolderForAdapterPosition(
                                channelPagerV920==null?focusIndex:
                                channelPagerV920.localIndex(focusIndex));
                        if(item!=null)item.itemView.requestFocus();''',
      "restore focused item inside paged channel window")
    s=one(s,
      '''                final int position=i;
                grid.post(()->{
                    grid.scrollToPosition(position);''',
      '''                final int position=i;
                if(channelPagerV920!=null)channelPagerV920.show(visible,position);
                grid.post(()->{
                    grid.scrollToPosition(channelPagerV920==null?position:
                        channelPagerV920.localIndex(position));''',
      "Back focus selects visible page without building huge adapter")
    s=one(s,
      '''                            grid.findViewHolderForAdapterPosition(position);
                        if(row!=null)row.itemView.requestFocus();''',
      '''                            grid.findViewHolderForAdapterPosition(
                                channelPagerV920==null?position:
                                channelPagerV920.localIndex(position));
                        if(row!=null)row.itemView.requestFocus();''',
      "Back focus item relative to paged window")
    # Java errors are caught before Activity termination; OutOfMemoryError is
    # avoided by the bounded UI but should not be swallowed.
    s=one(s,
      '''        render();
    }
    private void render() {''',
      '''        if("Uživo".equals(destination)){
            try{render();}
            catch(RuntimeException error){
                android.util.Log.e("KeldinLiveTv","Live TV screen failed",error);
                page="Moje liste";
                if(content!=null){
                    content.removeAllViews();
                    showLists();
                }
                message("Live TV could not open. Select a playlist in Playlists.");
            }
        }else render();
    }
    private void render() {''',
      "graceful fallback to saved playlists when UI throws runtime error")
    return s
edit("ui/MainActivity.java",main)

def card(s):
    s=one(s,
      '''        if(current!=null) {
            h.progress.setVisibility(View.VISIBLE);''',
      '''        if(current!=null&&current.end>current.start) {
            h.progress.setVisibility(View.VISIBLE);''',
      "ignore zero-duration or invalid XMLTV programmes")
    s=one(s,
      '''(int)(100L*(now-current.start)/(current.end-current.start))''',
      '''(int)(100L*(now-current.start)/Math.max(1L,current.end-current.start))''',
      "EPG progress denominator cannot be zero")
    return s
edit("ui/ChannelAdapter.java",card)

def grid(s):
    s=one(s,
      '''            if(!"LIVE".equals(ch.kind)||!active.sourceId.equals(ch.sourceId))continue;''',
      '''            if((!"LIVE".equals(ch.kind)&&
                !Channel.isLiveFilmGroup(ch.group,ch.url))||
                !active.sourceId.equals(ch.sourceId))continue;''',
      "fullscreen TV Grid also recognizes broadcaster groups")
    return s
edit("playback/TvGridPanelV97.java",grid)

p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 919" in g and "versionName '0.9.19'" in g
p.write_text(g.replace("versionCode 919","versionCode 920",1)
              .replace("versionName '0.9.19'","versionName '0.9.20'",1))
print("PASS v0.9.20: indexed Live TV, bounded grid cards, EPG guard, fallback, player TV Grid broadcaster safety")
