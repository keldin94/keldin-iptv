from pathlib import Path

BASE=Path("app/src/main/java/com/keldin/iptv")
def edit(relative,transform):
    p=BASE/relative
    before=p.read_text()
    after=transform(before)
    if after==before:raise AssertionError("v99 unchanged "+relative)
    p.write_text(after)
def change(s,a,b,label):
    if a not in s:raise AssertionError("v99 missing "+label+" : "+a[:90])
    return s.replace(a,b,1)

# IMPORTANT: EX YU | Filmovi & Serije (HBO, CineStar, Cinemax)
# is a LIVE-TV broadcaster group, not a VOD series or film group.
def channel(s):
    a=s.index("    public static boolean isLiveFilmGroup(String group,String url){")
    b=s.index("    public static String inferKind(",a)
    new='''    public static boolean isLiveFilmGroup(String group,String url){
        String g=(group==null?"":group).toLowerCase(Locale.ROOT)
            .replace('-', ' ').replace('_', ' ').replace('|',' ')
            .replaceAll("\\\\s+"," ").trim();
        String u=(url==null?"":url).toLowerCase(Locale.ROOT);
        if(u.contains("/movie/")||u.contains("/series/"))return false;
        boolean region=g.contains("ex yu")||g.contains("exyu")||
            g.contains("ex jug")||g.contains("ex yug")||
            g.contains("balkan")||g.contains("regional");
        boolean filmSeries=g.contains("filmovi") &&
            (g.contains("serije")||g.contains("serija"));
        boolean filmChannels=g.contains("filmski")||g.contains("filmsk")||
            g.contains("film channels")||g.contains("movie channels")||
            g.contains("cinema channels")||g.contains("kino kanali");
        return (region&&(filmSeries||filmChannels))||
            filmChannels&&(g.equals("filmski")||
                g.equals("filmski kanali")||g.equals("film channels"));
    }

'''
    return s[:a]+new+s[b:]
edit("data/Channel.java",channel)

# Selection and expansion are local display preferences, never delete catalogue.
def store(s):
    anchor='''    public boolean openLastChannelAtStart() {'''
    addition='''    public boolean isPlaylistActiveV99(String id){
        return prefs.getBoolean("playlist_active_v99_"+id,true);
    }
    public void setPlaylistActiveV99(String id,boolean active){
        prefs.edit().putBoolean("playlist_active_v99_"+id,active).apply();
    }
    public boolean isPlaylistCollapsedV99(String id){
        return prefs.getBoolean("playlist_collapsed_v99_"+id,false);
    }
    public void setPlaylistCollapsedV99(String id,boolean collapsed){
        prefs.edit().putBoolean("playlist_collapsed_v99_"+id,collapsed).apply();
    }

'''
    return change(s,anchor,addition+anchor,"catalog settings API")
edit("data/CatalogStore.java",store)

# Remember source with the channel, not only group: two providers may use same title.
def player(s):
    return change(s,'''            .putString("return_live_key_v98",current.key())''',
      '''            .putString("return_live_source_v99",current.sourceId)
            .putString("return_live_key_v98",current.key())''',
      "remember actual playback source")
edit("playback/PlayerActivity.java",player)

def main(s):
    s=change(s,'''    private RecyclerView browseCategoriesV93,browseGridV93;''',
      '''    private RecyclerView browseCategoriesV93,browseGridV93;
    private String selectedSourceV99="";''',"selected source state")
    s=change(s,'''                .putString("selected_group_Uživo",playedGroup)
                .putBoolean("return_live_focus_v98",true).apply();
            page="Uživo";
            selectedGroup=playedGroup;''',
      '''                .putString("selected_group_Uživo",playedGroup)
                .putString("selected_source_Uživo",
                    prefs.getString("return_live_source_v99",""))
                .putBoolean("return_live_focus_v98",true).apply();
            page="Uživo";
            selectedGroup=playedGroup;
            selectedSourceV99=prefs.getString("return_live_source_v99","");''',
      "Back restores provider identity")

    # All browse sections have the same grouped source/category navigation.
    start=s.index("    private void showChannelGrid(boolean guideMode) {")
    end=s.index("    private ArrayList<Channel> filterSection(",start)
    method='''    private ArrayList<Channel> filterSourceV99(List<Channel> source,
            String selectedSource,String group){
        ArrayList<Channel> out=new ArrayList<>();
        for(Channel c:source){
            if(!c.sourceId.equals(selectedSource))continue;
            String label=(c.group==null||c.group.isEmpty())?"Ostalo":c.group;
            if(PlaylistGroupAdapterV99.ALL.equals(group)||group.equals(label))
                out.add(c);
        }
        return out;
    }
    private void showChannelGrid(boolean guideMode) {
        String kind=page.equals("Filmovi")?"MOVIES":page.equals("Serije")?"SERIES":
            page.equals("Uživo")?"LIVE":page.equals("Radio")?"RADIO":"";
        List<Channel> source="Favoriti".equals(page)?store.favorites():store.channels();
        ArrayList<Channel> section=new ArrayList<>();
        LinkedHashMap<String,LinkedHashMap<String,Integer>> bySource=new LinkedHashMap<>();
        for(PlaylistSource entry:store.sources())
            bySource.put(entry.id,new LinkedHashMap<>());
        android.content.SharedPreferences viewingPrefs=
            getSharedPreferences("keldin_settings",MODE_PRIVATE);
        boolean hideAdult=viewingPrefs.getBoolean("hide_adult_content_v93",true);
        java.util.Set<String> hiddenTitles=viewingPrefs.getStringSet(
            "hidden_media_items_v93",java.util.Collections.emptySet());
        java.util.Set<String> hiddenSeries=viewingPrefs.getStringSet(
            "hidden_series_v93",java.util.Collections.emptySet());
        java.util.HashMap<String,java.util.Set<String>> exclusions=new java.util.HashMap<>();
        for(Channel ch:source){
            if(!store.isPlaylistActiveV99(ch.sourceId))continue;
            String effectiveKind=Channel.isLiveFilmGroup(ch.group,ch.url)?"LIVE":ch.kind;
            if(!kind.isEmpty()&&!kind.equals(effectiveKind))continue;
            java.util.Set<String> excluded=exclusions.computeIfAbsent(
                ch.sourceId,store::excludedGroups);
            if(excluded.contains(ch.group)||excluded.contains("@kind:"+effectiveKind))
                continue;
            if(hiddenTitles.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.key())))
                continue;
            if("SERIES".equals(ch.kind)&&hiddenSeries.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(
                    ch.sourceId+"|"+ch.group+"|"+SeriesBrowserV6.seriesBase(ch))))
                continue;
            if((hideAdult||(store.parentalLocked()&&!store.isContentUnlocked()))&&
                com.keldin.iptv.data.ContentFilterV93.isExplicit(ch.group,ch.name))
                continue;
            section.add(ch);
            String label=(ch.group==null||ch.group.isEmpty())?"Ostalo":ch.group;
            LinkedHashMap<String,Integer> groups=bySource.get(ch.sourceId);
            if(groups!=null)groups.put(label,groups.getOrDefault(label,0)+1);
        }
        boolean isPosters="MOVIES".equals(kind)||"SERIES".equals(kind);
        if(isPosters)java.util.Collections.reverse(section);

        String previous=viewingPrefs.getString("selected_source_"+page,"");
        if(!previous.isEmpty())selectedSourceV99=previous;
        if(selectedSourceV99.isEmpty()||
            !store.isPlaylistActiveV99(selectedSourceV99)||
            !bySource.containsKey(selectedSourceV99)){
            selectedSourceV99="";
            for(PlaylistSource entry:store.sources())
                if(store.isPlaylistActiveV99(entry.id)){
                    selectedSourceV99=entry.id;break;
                }
        }
        if(selectedSourceV99.isEmpty())selectedGroup=PlaylistGroupAdapterV99.ALL;
        else {
            LinkedHashMap<String,Integer> available=bySource.get(selectedSourceV99);
            if(available==null||(!PlaylistGroupAdapterV99.ALL.equals(selectedGroup)
                &&!available.containsKey(selectedGroup)))
                selectedGroup=PlaylistGroupAdapterV99.ALL;
        }

        LinearLayout main=Ui.horizontal(this);
        main.setGravity(Gravity.TOP);
        LinearLayout categoryBox=Ui.vertical(this);
        categoryBox.setPadding(Ui.dp(this,8),Ui.dp(this,9),Ui.dp(this,7),Ui.dp(this,7));
        categoryBox.setBackground(Ui.shape(Ui.PANEL,14,this));
        TextView categoryLabel=Ui.text(this,tr("categories").toUpperCase(Locale.ROOT),
            11,Ui.ACCENT,true);
        categoryBox.addView(categoryLabel);
        categoryBox.addView(Ui.space(this,6));
        RecyclerView categories=new RecyclerView(this);
        categories.setId(View.generateViewId());
        categories.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));
        categories.setItemAnimator(null);
        categories.setHasFixedSize(false);
        categoryBox.addView(categories,new LinearLayout.LayoutParams(-1,0,1));
        LinearLayout.LayoutParams rail=Ui.lp(this,215,-1);
        rail.rightMargin=Ui.dp(this,9);
        main.addView(categoryBox,rail);

        LinearLayout browsing=Ui.vertical(this);
        TextView count=Ui.text(this,"",13,Ui.MUTED,false);
        browsing.addView(count);
        browsing.addView(Ui.space(this,5));
        if(isPosters){
            TextView manage=Ui.button(this,"⚙  "+tr("categories")+"  ·  Manage / Hide",
                ()->manageContentCategoriesV93(kind),false);
            browsing.addView(manage,Ui.lp(this,-1,42));
            browsing.addView(Ui.space(this,5));
        }
        RecyclerView grid=new RecyclerView(this);
        grid.setId(View.generateViewId());
        GridLayoutManager gridManager=new GridLayoutManager(this,4);
        grid.setLayoutManager(gridManager);
        grid.setHasFixedSize(false);
        grid.setItemAnimator(null);
        grid.setClipToPadding(false);
        ArrayList<Channel> visible=filterSourceV99(section,selectedSourceV99,selectedGroup);
        ChannelAdapter liveAdapter=null;
        PosterAdapterV6 posterAdapter=null;
        if(isPosters){
            posterAdapter=new PosterAdapterV6(visible,this::openMediaDetails);
            grid.setAdapter(posterAdapter);
        }else{
            liveAdapter=new ChannelAdapter(store,visible,this::play,guideMode);
            grid.setAdapter(liveAdapter);
        }
        count.setText(visible.size()+" "+tr("items")+"  •  "+
            (selectedSourceV99.isEmpty()?"No active playlist":selectedGroup));
        browsing.addView(grid,new LinearLayout.LayoutParams(-1,0,1));
        main.addView(browsing,new LinearLayout.LayoutParams(0,-1,1));
        final ChannelAdapter channelCards=liveAdapter;
        final PosterAdapterV6 movieCards=posterAdapter;
        PlaylistGroupAdapterV99 listAdapter=new PlaylistGroupAdapterV99(
            this,store,store.sources(),bySource,selectedSourceV99,selectedGroup,
            new PlaylistGroupAdapterV99.Select(){
                @Override public void onSelect(String sourceId,String group){
                    selectedSourceV99=sourceId;
                    selectedGroup=group;
                    viewingPrefs.edit()
                        .putString("selected_source_"+page,sourceId)
                        .putString("selected_group_"+page,group).apply();
                    ArrayList<Channel> filtered=filterSourceV99(
                        section,sourceId,group);
                    if(movieCards!=null)movieCards.replace(filtered);
                    if(channelCards!=null)channelCards.setItems(filtered);
                    count.setText(filtered.size()+" "+tr("items")+"  •  "+group);
                    grid.scrollToPosition(0);
                }
                @Override public void onActivationChanged(){
                    render();
                }
            });
        categories.setAdapter(listAdapter);
        if(isPosters){
            browseCategoriesV93=categories;
            browseGridV93=grid;
            categories.setNextFocusRightId(grid.getId());
            grid.setNextFocusLeftId(categories.getId());
        }else{
            browseCategoriesV93=null;
            browseGridV93=null;
        }
        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));
        if(isPosters)
            categories.post(()->{
                if("Filmovi".equals(page)||"Serije".equals(page))
                    focusBrowseV93(categories);
            });
        if("LIVE".equals(kind) &&
            viewingPrefs.getBoolean("return_live_focus_v98",false)){
            viewingPrefs.edit().putBoolean("return_live_focus_v98",false).apply();
            String key=viewingPrefs.getString("return_live_key_v98","");
            for(int i=0;i<visible.size();i++){
                if(!visible.get(i).key().equals(key))continue;
                final int position=i;
                grid.post(()->{
                    grid.scrollToPosition(position);
                    grid.post(()->{
                        RecyclerView.ViewHolder row=
                            grid.findViewHolderForAdapterPosition(position);
                        if(row!=null)row.itemView.requestFocus();
                    });
                });
                break;
            }
        }
    }
'''
    s=s[:start]+method+s[end:]
    # Explicit per-playlist controls live at the top of the existing list manager.
    index=s.index("    private void showLists()")
    opening=s.index("{",index)
    depth=1;cursor=opening+1
    quote=False;escaped=False
    while depth and cursor<len(s):
        v=s[cursor]
        if quote:
            if escaped:escaped=False
            elif v=="\\\\":escaped=True
            elif v=='"':quote=False
        elif v=='"':quote=True
        elif v=="{":depth+=1
        elif v=="}":depth-=1
        cursor+=1
    if depth:raise AssertionError("showLists method brace mismatch")
    injection='''        if(!store.sources().isEmpty()){
            TextView activeLists=Ui.button(this,"☷  Active playlists  ·  Show / Hide",
                this::managePlaylistActivationV99,false);
            LinearLayout.LayoutParams toggleBar=Ui.lp(this,-1,49);
            toggleBar.bottomMargin=Ui.dp(this,8);
            content.addView(activeLists,0,toggleBar);
        }
'''
    s=s[:cursor-1]+injection+s[cursor-1:]
    anchor="    private void showLists()"
    methods='''    private void managePlaylistActivationV99(){
        List<PlaylistSource> sources=store.sources();
        if(sources.isEmpty()){message("No playlists found.");return;}
        String[] labels=new String[sources.size()];
        boolean[] enabled=new boolean[sources.size()];
        for(int i=0;i<sources.size();i++){
            PlaylistSource src=sources.get(i);
            labels[i]=src.name;
            enabled[i]=store.isPlaylistActiveV99(src.id);
        }
        new AlertDialog.Builder(this)
            .setTitle("Active playlists")
            .setMessage("Select which playlists appear in Live TV, Movies, Series and Search. Disabled playlists remain saved.")
            .setMultiChoiceItems(labels,enabled,
                (dialog,which,checked)->enabled[which]=checked)
            .setPositiveButton("Save",(dialog,which)->{
                for(int i=0;i<sources.size();i++)
                    store.setPlaylistActiveV99(sources.get(i).id,enabled[i]);
                selectedSourceV99="";
                render();
            })
            .setNeutralButton("Enable all",(dialog,which)->{
                for(PlaylistSource src:sources)
                    store.setPlaylistActiveV99(src.id,true);
                selectedSourceV99="";
                render();
            })
            .setNegativeButton(tr("cancel"),null).show();
    }

'''
    s=change(s,anchor,methods+anchor,"list activation dialog")
    return s
edit("ui/MainActivity.java",main)

# No reset of app identity or existing user data; signed in-place upgrade.
gradle=Path("app/build.gradle")
v=gradle.read_text()
assert "versionCode 908" in v and "versionName '0.9.8'" in v
gradle.write_text(v.replace("versionCode 908","versionCode 909",1)
                   .replace("versionName '0.9.8'","versionName '0.9.9'",1))
print("PASS v0.9.9: EX YU | Filmovi & Serije as Live TV, grouped source categories, persisted list activation and collapse, provider-aware Back")
