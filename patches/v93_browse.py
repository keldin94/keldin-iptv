from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
def sub(a,b,name):
 global s
 assert a in s,"v0.9.3 media browser patch missing "+name
 s=s.replace(a,b,1)
sub('''    private void showChannelGrid(boolean guideMode) {''','''    private RecyclerView browseCategoriesV93,browseGridV93;
    private boolean tvChildV93(View child,View parent){
        while(child!=null){
            if(child==parent)return true;
            android.view.ViewParent next=child.getParent();
            child=next instanceof View?(View)next:null;
        }
        return false;
    }
    private void focusBrowseV93(RecyclerView view){
        if(view==null||view.getLayoutManager()==null)return;
        view.scrollToPosition(0);
        view.post(()->{
            if(view.getLayoutManager()==null)return;
            View item=view.getLayoutManager().findViewByPosition(0);
            if(item!=null)item.requestFocus();
            else view.requestFocus();
        });
    }
    @Override public boolean dispatchKeyEvent(android.view.KeyEvent event){
        if(event.getAction()==android.view.KeyEvent.ACTION_DOWN &&
                ("Filmovi".equals(page)||"Serije".equals(page))&&
                browseCategoriesV93!=null&&browseGridV93!=null){
            View focused=getCurrentFocus();
            if(focused!=null){
                if(event.getKeyCode()==android.view.KeyEvent.KEYCODE_DPAD_LEFT &&
                        tvChildV93(focused,browseGridV93)){
                    RecyclerView.ViewHolder row=browseGridV93.findContainingViewHolder(focused);
                    int position=row==null?0:row.getBindingAdapterPosition();
                    int columns=((GridLayoutManager)browseGridV93.getLayoutManager()).getSpanCount();
                    if(position<0||position%Math.max(1,columns)==0){
                        focusBrowseV93(browseCategoriesV93);
                        return true;
                    }
                }
                if(event.getKeyCode()==android.view.KeyEvent.KEYCODE_DPAD_RIGHT &&
                        tvChildV93(focused,browseCategoriesV93)){
                    focusBrowseV93(browseGridV93);
                    return true;
                }
            }
        }
        return super.dispatchKeyEvent(event);
    }
    private void showChannelGrid(boolean guideMode) {''',"explicit movie/series D-pad navigation")
sub('''        java.util.HashMap<String,java.util.Set<String>> exclusions=new java.util.HashMap<>();
        for(Channel ch:source){''','''        java.util.HashMap<String,java.util.Set<String>> exclusions=new java.util.HashMap<>();
        android.content.SharedPreferences viewingPrefs=
            getSharedPreferences("keldin_settings",MODE_PRIVATE);
        boolean hideExplicit=viewingPrefs.getBoolean("hide_adult_content_v93",true);
        java.util.Set<String> hiddenTitles=viewingPrefs.getStringSet(
            "hidden_media_items_v93",java.util.Collections.emptySet());
        java.util.Set<String> hiddenSeries=viewingPrefs.getStringSet(
            "hidden_series_v93",java.util.Collections.emptySet());
        for(Channel ch:source){''',"default explicit filter and individual exclusions")
sub('''            if(store.parentalLocked()&&!store.isContentUnlocked()&&CatalogStore.isAdultCategory(ch.group))continue;
            section.add(ch);''','''            if(hiddenTitles.contains(com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.key())))
                continue;
            if("SERIES".equals(ch.kind)&&hiddenSeries.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.sourceId+"|"+
                    ch.group+"|"+SeriesBrowserV6.seriesBase(ch))))continue;
            if((hideExplicit||(store.parentalLocked()&&!store.isContentUnlocked())) &&
                    com.keldin.iptv.data.ContentFilterV93.isExplicit(ch.group,ch.name))
                continue;
            section.add(ch);''',"filter adult by group AND title")
sub('''        if(!groups.contains(selectedGroup))selectedGroup="Sve kategorije";''','''        if("MOVIES".equals(kind)||"SERIES".equals(kind)){
            // M3U has no reliable added-at date. Latest entries in the source
            // are placed first, without inventing a timestamp.
            java.util.Collections.reverse(section);
        }
        if(!groups.contains(selectedGroup))selectedGroup="Sve kategorije";''',"newest playlist entries first")
sub('''        RecyclerView categories=new RecyclerView(this);
        categories.setLayoutManager''','''        RecyclerView categories=new RecyclerView(this);
        categories.setId(View.generateViewId());
        categories.setLayoutManager''',"category rail view ID")
sub('''        RecyclerView grid=new RecyclerView(this);
        boolean isPosters''','''        RecyclerView grid=new RecyclerView(this);
        grid.setId(View.generateViewId());
        boolean isPosters''',"media grid view ID")
sub('''        browsing.addView(count);browsing.addView(Ui.space(this,8));''',
'''        browsing.addView(count);browsing.addView(Ui.space(this,8));
        if("MOVIES".equals(kind)||"SERIES".equals(kind)){
            TextView categoryManager=Ui.button(this,"⚙  "+tr("categories")+
                "  ·  Manage / Hide",()->manageContentCategoriesV93(kind),false);
            browsing.addView(categoryManager,Ui.lp(this,-1,48));
            browsing.addView(Ui.space(this,8));
        }''',"user-facing category hide option")
start=s.index('''        if(isPosters){
            final boolean[] narrow={false};''')
end=s.index('''        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));''',start)
old=s[start:end]
assert "categoryAdapter.setCondensed(true);" in old
s=s[:start]+'''        if(isPosters){
            // Never mutate the category adapter during a focus callback:
            // notifyDataSetChanged there previously dropped D-pad selection.
            browseCategoriesV93=categories;
            browseGridV93=grid;
            categories.setNextFocusRightId(grid.getId());
            grid.setNextFocusLeftId(categories.getId());
        }else{
            browseCategoriesV93=null;
            browseGridV93=null;
        }
'''+s[end:]
sub('''        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));
    }
    private ArrayList<Channel> filterSection''',
'''        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));
        if(isPosters)
            categories.post(()->{
                if("Filmovi".equals(page)||"Serije".equals(page))
                    focusBrowseV93(categories);
            });
    }
    private ArrayList<Channel> filterSection''',"focus movie categories on opening")
# Settings category management across every source; preserve filters from other content types.
anchor='''    private void openMediaDetails(Channel media){'''
assert anchor in s
newMethods='''    private void manageContentCategoriesV93(String kind){
        java.util.LinkedHashMap<String,String[]> groups=new java.util.LinkedHashMap<>();
        for(Channel ch:store.channels()){
            if(!kind.equals(ch.kind))continue;
            String group=ch.group==null?"":ch.group;
            String key=ch.sourceId+"\\\\u0001"+group;
            if(!groups.containsKey(key)){
                com.keldin.iptv.data.PlaylistSource src=store.sourceById(ch.sourceId);
                String label=(group.isEmpty()?"Other":group)+
                    (store.sources().size()>1&&src!=null?"   •   "+src.name:"");
                groups.put(key,new String[]{ch.sourceId,group,label});
            }
        }
        if(groups.isEmpty()){
            message("No categories found.");return;
        }
        java.util.ArrayList<String[]> records=new java.util.ArrayList<>(groups.values());
        String[] names=new String[records.size()];
        boolean[] enabled=new boolean[records.size()];
        java.util.HashMap<String,java.util.Set<String>> existing=new java.util.HashMap<>();
        for(int i=0;i<records.size();i++){
            String[] item=records.get(i);
            names[i]=item[2];
            java.util.Set<String> disabled=existing.computeIfAbsent(item[0],store::excludedGroups);
            enabled[i]=!disabled.contains(item[1]);
        }
        new AlertDialog.Builder(this)
            .setTitle("Choose categories to display")
            .setMultiChoiceItems(names,enabled,(dialog,index,on)->enabled[index]=on)
            .setPositiveButton("Save",(dialog,button)->{
                for(int i=0;i<records.size();i++){
                    String[] item=records.get(i);
                    java.util.Set<String> disabled=existing.get(item[0]);
                    if(enabled[i])disabled.remove(item[1]);
                    else disabled.add(item[1]);
                }
                for(java.util.Map.Entry<String,java.util.Set<String>> entry:existing.entrySet())
                    store.setExcludedGroups(entry.getKey(),entry.getValue());
                selectedGroup="Sve kategorije";
                render();
            })
            .setNeutralButton("Show all",(dialog,button)->{
                for(String[] item:records)
                    existing.get(item[0]).remove(item[1]);
                for(java.util.Map.Entry<String,java.util.Set<String>> entry:existing.entrySet())
                    store.setExcludedGroups(entry.getKey(),entry.getValue());
                selectedGroup="Sve kategorije";
                render();
            })
            .setNegativeButton(tr("cancel"),null).show();
    }
    private void hideMediaItemV93(Channel media){
        android.content.SharedPreferences prefs=
            getSharedPreferences("keldin_settings",MODE_PRIVATE);
        java.util.HashSet<String> hidden=new java.util.HashSet<>(prefs.getStringSet(
            "hidden_media_items_v93",java.util.Collections.emptySet()));
        hidden.add(com.keldin.iptv.data.ContentFilterV93.fingerprint(media.key()));
        android.content.SharedPreferences.Editor editor=prefs.edit()
            .putStringSet("hidden_media_items_v93",hidden);
        if("SERIES".equals(media.kind)){
            java.util.HashSet<String> series=new java.util.HashSet<>(prefs.getStringSet(
                "hidden_series_v93",java.util.Collections.emptySet()));
            series.add(com.keldin.iptv.data.ContentFilterV93.fingerprint(media.sourceId+"|"+
                media.group+"|"+SeriesBrowserV6.seriesBase(media)));
            editor.putStringSet("hidden_series_v93",series);
        }
        editor.apply();
        render();
    }
'''
s=s.replace(anchor,newMethods+anchor,1)
sub('''        if("SERIES".equals(media.kind)){
            SeriesBrowserV6.open(this,store.channels(),media,this::play);
            return;
        }''',
'''        if("SERIES".equals(media.kind)){
            String[] choices={"Open seasons & episodes","Hide series","Cancel"};
            new AlertDialog.Builder(this).setTitle(media.name)
                .setItems(choices,(dialog,which)->{
                    if(which==0)SeriesBrowserV6.open(this,store.channels(),media,this::play);
                    if(which==1)hideMediaItemV93(media);
                }).show();
            return;
        }''',"series hide option")
sub('''        new AlertDialog.Builder(this).setTitle(name).setMessage(message)
            .setPositiveButton(tr("play"),(d,w)->play(media))
            .setNeutralButton(tr("favorites"),(d,w)->{store.toggleFavorite(media);render();})
            .setNegativeButton(tr("cancel"),null).show();''',
'''        String[] actions={tr("play"),tr("favorites"),"Hide this title",tr("cancel")};
        new AlertDialog.Builder(this).setTitle(name).setMessage(message)
            .setItems(actions,(dialog,which)->{
                if(which==0)play(media);
                else if(which==1){store.toggleFavorite(media);render();}
                else if(which==2)hideMediaItemV93(media);
            }).show();''',"hide movie title without deleting playlist")
p.write_text(s)
print("v0.9.3: selectable TV category rail, persistent title/category hiding, default adult suppression, playlist-reverse movies/series")
