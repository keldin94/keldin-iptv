from pathlib import Path
import re

root=Path("app/src/main/java/com/keldin/iptv")
def modify(rel,action):
    p=root/rel
    old=p.read_text()
    new=action(old)
    if old==new:raise AssertionError("v918 unchanged "+rel)
    p.write_text(new)
def swap(s,a,b,label):
    if a not in s:raise AssertionError("v918 missing "+label+": "+a[:100])
    return s.replace(a,b,1)

def catalog(s):
    old='''    public boolean isPlaylistActiveV99(String id){
        return prefs.getBoolean("playlist_active_v99_"+id,true);
    }
    public void setPlaylistActiveV99(String id,boolean active){
        prefs.edit().putBoolean("playlist_active_v99_"+id,active).apply();
    }'''
    new='''    // Exactly ONE provider is loaded in RAM. The others remain on disk.
    // Migration retains the last selected, formerly enabled provider.
    private volatile String activePlaylistV918="";
    public boolean isPlaylistActiveV99(String id){
        return id!=null&&!id.isEmpty()&&id.equals(activePlaylistV918);
    }
    public synchronized String activePlaylistIdV918(){return activePlaylistV918;}
    private String initialActiveV918(){
        String saved=prefs.getString("active_playlist_v918","");
        if(sourceById(saved)!=null)return saved;
        String previous=prefs.getString("selected_source_Uživo","");
        if(sourceById(previous)!=null&&
            prefs.getBoolean("playlist_active_v99_"+previous,true))return previous;
        for(PlaylistSource src:sources)
            if(prefs.getBoolean("playlist_active_v99_"+src.id,true))return src.id;
        return sources.isEmpty()?"":sources.get(0).id;
    }
    public synchronized void setPlaylistActiveV99(String id,boolean active){
        if(!active||id==null||id.equals(activePlaylistV918))return;
        try{activatePlaylistV918(id);}
        catch(java.io.IOException problem){throw new IllegalStateException(
            "Could not load the selected playlist",problem);}
    }
    private ArrayList<Channel> readPlaylistV918(String sourceId)
            throws java.io.IOException{
        ArrayList<Channel> result=new ArrayList<>();
        if(sourceId==null||sourceId.isEmpty())return result;
        File src=new File(context.getFilesDir(),"catalog-v6.jsonl");
        if(!src.isFile())return result;
        java.util.HashMap<String,String> groups=new java.util.HashMap<>();
        java.util.HashMap<String,String> kinds=new java.util.HashMap<>();
        try(java.io.BufferedReader input=new java.io.BufferedReader(
                new java.io.InputStreamReader(new FileInputStream(src),
                StandardCharsets.UTF_8),65536)){
            String line;
            while((line=input.readLine())!=null){
                try{
                    // This is the only source instantiated, not the entire
                    // combined M3U catalogue.
                    JSONObject o=new JSONObject(line);
                    if(!sourceId.equals(o.optString("sourceId")))continue;
                    Channel c=new Channel();
                    c.id=o.optString("id");
                    c.sourceId=sourceId;
                    c.name=o.optString("name");c.url=o.optString("url");
                    c.tvgId=o.optString("tvgId");c.logo=o.optString("logo");
                    c.group=poolStringV912(o.optString("group","Ostalo"),groups);
                    c.kind=poolStringV912(o.optString("kind","LIVE"),kinds);
                    c.userAgent=o.optString("userAgent");
                    result.add(c);
                    if(result.size()>200000)
                        throw new java.io.IOException("Playlist exceeds safe memory limit");
                }catch(org.json.JSONException malformed){
                    throw new java.io.IOException("Damaged playlist catalog",malformed);
                }
            }
        }
        return result;
    }
    public synchronized void activatePlaylistV918(String id)
            throws java.io.IOException{
        if(sourceById(id)==null)
            throw new java.io.IOException("Playlist no longer exists");
        if(id.equals(activePlaylistV918))return;
        ArrayList<Channel> selected=readPlaylistV918(id);
        // Commit to UI only after the entire requested source was read.
        channels.clear();
        liveIndexReadyV910=false;
        liveIndexV910.clear();
        guide.clear();
        channels.addAll(selected);
        activePlaylistV918=id;
        prefs.edit().putString("active_playlist_v918",id).commit();
    }
    // Keep only one provider in RAM while the wizard parses a second list.
    // No channel data on disk is removed by this operation.
    public synchronized void suspendLibraryForImportV918(){
        channels.clear();
        liveIndexV910.clear();
        liveIndexReadyV910=false;
    }
    public synchronized void restoreLibraryAfterImportV918()
            throws java.io.IOException{
        if(!channels.isEmpty()||activePlaylistV918.isEmpty())return;
        channels.addAll(readPlaylistV918(activePlaylistV918));
        liveIndexV910.clear();
        liveIndexReadyV910=false;
    }
    private void persistSourceV918(String target,java.util.List<Channel> updated)
            throws java.io.IOException{
        File dest=new File(context.getFilesDir(),"catalog-v6.jsonl");
        File temp=new File(context.getFilesDir(),"catalog-v918.tmp");
        java.util.HashSet<String> valid=new java.util.HashSet<>();
        for(PlaylistSource p:sources)valid.add(p.id);
        try(java.io.BufferedWriter output=new java.io.BufferedWriter(
            new java.io.OutputStreamWriter(new FileOutputStream(temp),
                StandardCharsets.UTF_8),65536)){
            // Copy unchanged providers verbatim. Never deserialize inactive
            // channels into memory or overwrite their saved selections.
            if(dest.isFile())
                try(java.io.BufferedReader input=new java.io.BufferedReader(
                    new java.io.InputStreamReader(new FileInputStream(dest),
                        StandardCharsets.UTF_8),65536)){
                    String line;
                    while((line=input.readLine())!=null){
                        JSONObject o=new JSONObject(line);
                        String sid=o.optString("sourceId","");
                        if(valid.contains(sid)&&!target.equals(sid)){
                            output.write(line);
                            output.newLine();
                        }
                    }
                }catch(org.json.JSONException e){
                    throw new java.io.IOException("Catalog could not be read safely",e);
                }
            for(Channel c:updated){
                JSONObject o=new JSONObject();
                try{
                    o.put("id",c.id);o.put("sourceId",target);
                    o.put("name",c.name);o.put("url",c.url);
                    o.put("tvgId",c.tvgId);o.put("logo",c.logo);
                    o.put("group",c.group);o.put("kind",c.kind);
                    o.put("userAgent",c.userAgent);
                }catch(org.json.JSONException e){
                    throw new java.io.IOException("Could not serialize channel",e);
                }
                output.write(o.toString());output.newLine();
            }
        }catch(Exception e){
            temp.delete();
            if(e instanceof java.io.IOException)throw (java.io.IOException)e;
            throw new java.io.IOException("Could not persist playlist",e);
        }
        // Same-directory rename is atomic on Android's app-private storage.
        // On failure, leave the old valid catalogue in place.
        if(!temp.renameTo(dest)){
            temp.delete();
            throw new java.io.IOException("Not enough storage to save the playlist safely");
        }
        // Old combined binary cache must never restore every inactive source.
        new File(context.getFilesDir(),"catalog-v912.bin").delete();
        new File(context.getFilesDir(),"catalog.json").delete();
    }'''
    s=swap(s,old,new,"single-source preference and disk loading")
    old='''    public synchronized List<Channel> channels(){
        java.util.HashSet<String> enabled=new java.util.HashSet<>();
        for(PlaylistSource src:sources)
            if(isPlaylistActiveV99(src.id))enabled.add(src.id);
        ArrayList<Channel> visible=new ArrayList<>(channels.size());
        for(Channel c:channels)
            if(enabled.contains(c.sourceId))visible.add(c);
        return visible;
    }'''
    new='''    public synchronized List<Channel> channels(){
        // The resident catalogue already contains ONLY the active provider.
        return new ArrayList<>(channels);
    }'''
    s=swap(s,old,new,"no multi-source copies during TV browsing")
    old='''    public synchronized void updateChannels(String sourceId, List<Channel> updated) {
        liveIndexReadyV910=false;
        liveIndexV910.clear();
        channels.removeIf(c -> c.sourceId.equals(sourceId));
        channels.addAll(updated);
        saveChannels();
    }'''
    new='''    public synchronized void updateChannels(String sourceId,List<Channel> updated){
        try{
            // Write ALL providers safely: unchanged ones are copied on disk;
            // only the active source ever becomes a resident Java list.
            persistSourceV918(sourceId,updated);
        }catch(java.io.IOException problem){
            throw new IllegalStateException("Playlist save failed: "+problem.getMessage(),problem);
        }
        if(isPlaylistActiveV99(sourceId)){
            channels.clear();
            channels.addAll(updated);
            liveIndexReadyV910=false;
            liveIndexV910.clear();
        }
    }'''
    s=swap(s,old,new,"stream-safe non-destructive per-source updates")
    old='''    public synchronized void putSource(PlaylistSource src) {
        sources.removeIf(p -> p.id.equals(src.id)); sources.add(src); saveSources();
    }
    public synchronized void removeSource(String id) {
        sources.removeIf(p -> p.id.equals(id));
        channels.removeIf(p -> p.sourceId.equals(id));
        saveSources(); saveChannels();
    }'''
    new='''    public synchronized void putSource(PlaylistSource src){
        sources.removeIf(p->p.id.equals(src.id));
        sources.add(src);
        if(activePlaylistV918.isEmpty()){
            activePlaylistV918=src.id;
            prefs.edit().putString("active_playlist_v918",src.id).commit();
        }
        saveSources();
    }
    public synchronized void removeSource(String id){
        if(sourceById(id)==null)return;
        try{
            // Do not modify source metadata until the other catalogues
            // have been persisted successfully.
            persistSourceV918(id,java.util.Collections.emptyList());
        }catch(java.io.IOException problem){
            throw new IllegalStateException("Unable to remove playlist safely",problem);
        }
        sources.removeIf(p->p.id.equals(id));
        if(id.equals(activePlaylistV918)){
            channels.clear();
            liveIndexV910.clear();
            liveIndexReadyV910=false;
            guide.clear();
            activePlaylistV918=sources.isEmpty()?"":sources.get(0).id;
            prefs.edit().putString("active_playlist_v918",activePlaylistV918).commit();
            try{restoreLibraryAfterImportV918();}
            catch(java.io.IOException ignored){}
        }
        saveSources();
    }'''
    s=swap(s,old,new,"preserve inactive sources on removal")
    old='''        // Prefer the fast, versioned local snapshot if the source JSONL has not
        // changed. A failed or incomplete snapshot transparently falls back.
        File lines=new File(context.getFilesDir(),"catalog-v6.jsonl");
        if(lines.exists()&&loadFastV912(lines))return;'''
    new='''        // Migrate old multi-active installations before channel allocation.
        // Never read every registered IPTV source into this TV box's RAM.
        activePlaylistV918=initialActiveV918();
        prefs.edit().putString("active_playlist_v918",activePlaylistV918).commit();
        File lines=new File(context.getFilesDir(),"catalog-v6.jsonl");
        if(lines.exists()&&sources.size()==1&&loadFastV912(lines))return;'''
    s=swap(s,old,new,"single source startup, bypass old combined cache")
    old='''                    JSONObject o=new JSONObject(line);
                    Channel c=new Channel();'''
    new='''                    JSONObject o=new JSONObject(line);
                    if(!activePlaylistV918.equals(o.optString("sourceId")))continue;
                    Channel c=new Channel();'''
    s=swap(s,old,new,"only hydrate active source from JSONL")
    old='''            if(fullyLoaded){
                // First migration takes place after the app may show Home.'''
    new='''            if(fullyLoaded&&sources.size()==1){
                // A multi-source cache must not resurrect unloaded providers.'''
    s=swap(s,old,new,"do not create all-source binary cache")
    # Legacy JSON cache (for users upgrading from very old builds) may have
    # multiple sources. Limit its in-memory contents too.
    old='''                    JSONObject o = arr.getJSONObject(i);
                    Channel c = new Channel();'''
    new='''                    JSONObject o = arr.getJSONObject(i);
                    if(!activePlaylistV918.equals(o.optString("sourceId")))continue;
                    Channel c = new Channel();'''
    s=swap(s,old,new,"legacy JSON also loads one selected source")
    return s
modify("data/CatalogStore.java",catalog)

def main(s):
    begin=s.index("    private void managePlaylistActivationV99(){")
    end=s.index("    private void showLists()",begin)
    methods='''    private void activatePlaylistV918(PlaylistSource source){
        if(source==null)return;
        if(store.isPlaylistActiveV99(source.id)){
            selectedSourceV99=source.id;
            navigate("Uživo");
            return;
        }
        AlertDialog loadingV918=new AlertDialog.Builder(this)
            .setTitle("Switching IPTV playlist")
            .setMessage("Loading only "+source.name+" into memory…")
            .setCancelable(false).create();
        loadingV918.show();
        new Thread(()->{
            String problem=null;
            try{store.activatePlaylistV918(source.id);}
            catch(Exception error){problem=error.getMessage();}
            final String result=problem;
            runOnUiThread(()->{
                if(isFinishing()||isDestroyed())return;
                loadingV918.dismiss();
                if(result!=null){
                    message("Playlist not loaded: "+result);
                    return;
                }
                selectedSourceV99=source.id;
                selectedGroup="Sve kategorije";
                getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                    .putString("selected_source_Uživo",source.id)
                    .putString("selected_group_Uživo","Sve kategorije")
                    .putString("selected_source_Filmovi",source.id)
                    .putString("selected_source_Serije",source.id)
                    .putString("selected_source_Radio",source.id).apply();
                navigate("Uživo");
                mainHandler.postDelayed(this::autoEpgV917,1000);
            });
        },"keldin-switch-single-playlist").start();
    }
    private void managePlaylistActivationV99(){
        List<PlaylistSource> sources=store.sources();
        if(sources.isEmpty()){message("No playlists found.");return;}
        String[] labels=new String[sources.size()];
        int selected=0;
        for(int i=0;i<sources.size();i++){
            PlaylistSource src=sources.get(i);
            labels[i]=src.name+(store.isPlaylistActiveV99(src.id)?"  •  ACTIVE":"");
            if(store.isPlaylistActiveV99(src.id))selected=i;
        }
        new AlertDialog.Builder(this)
            .setTitle("Choose active IPTV playlist  ·  One at a time")
            .setSingleChoiceItems(labels,selected,(dialog,index)->{
                dialog.dismiss();
                activatePlaylistV918(sources.get(index));
            })
            .setNegativeButton(tr("cancel"),null).show();
    }

'''
    s=s[:begin]+methods+s[end:]
    s=swap(s,
      '''            TextView activeLists=Ui.button(this,"☷  Active playlists  ·  Show / Hide",''',
      '''            TextView activeLists=Ui.button(this,"☷  Active IPTV playlist  ·  Choose",''',
      "choose single source wording")
    s=swap(s,
      '''            TextView details=Ui.text(this,type+"  •  "+(src.lastUpdated==0?localized("Not updated","Nije ažurirano"):''',
      '''            TextView details=Ui.text(this,
                (store.isPlaylistActiveV99(src.id)?"● ACTIVE  •  ":"Inactive (saved)  •  ")
                +type+"  •  "+(src.lastUpdated==0?localized("Not updated","Nije ažurirano"):''',
      "show active state per source")
    s=swap(s,
      '''            card.addView(refresh,Ui.lp(this,-2,40));''',
      '''            card.addView(refresh,Ui.lp(this,-2,40));
            if(!store.isPlaylistActiveV99(src.id)){
                TextView use=Ui.button(this,"▶  Use",
                    ()->activatePlaylistV918(src),true);
                LinearLayout.LayoutParams ap=Ui.lp(this,-2,40);
                ap.leftMargin=Ui.dp(this,8);
                card.addView(use,ap);
            }''',
      "one-click activation on playlist card")
    s=swap(s,
      '''        for(PlaylistSource entry:store.sources())
            bySource.put(entry.id,new LinkedHashMap<>());''',
      '''        for(PlaylistSource entry:store.sources())
            if(store.isPlaylistActiveV99(entry.id))
                bySource.put(entry.id,new LinkedHashMap<>());''',
      "browse only one active provider")
    s=swap(s,
      '''            this,store,store.sources(),bySource,selectedSourceV99,selectedGroup,''',
      '''            this,store,activeSourcesV918(),bySource,selectedSourceV99,selectedGroup,''',
      "only active source in category rail")
    anchor='''    private void showChannelGrid(boolean guideMode) {'''
    helper='''    private List<PlaylistSource> activeSourcesV918(){
        ArrayList<PlaylistSource> active=new ArrayList<>();
        for(PlaylistSource source:store.sources())
            if(store.isPlaylistActiveV99(source.id))active.add(source);
        return active;
    }
'''
    s=swap(s,anchor,helper+anchor,"fast active source category selector")
    return s
modify("ui/MainActivity.java",main)

def wizard(s):
    # Import of another huge provider can temporarily need a second 150k
    # channel array. Release the already-saved resident provider before parse,
    # restoring it safely if the operation fails.
    old='''            try(BufferedReader reader=new BufferedReader(new InputStreamReader(
                    new FileInputStream(requireStagingV917()),StandardCharsets.UTF_8),65536)){'''
    new='''            store.suspendLibraryForImportV918();
            try(BufferedReader reader=new BufferedReader(new InputStreamReader(
                    new FileInputStream(requireStagingV917()),StandardCharsets.UTF_8),65536)){'''
    s=swap(s,old,new,"release resident channels while importing second provider")
    old='''            }catch(Exception e){
                String err=e.getMessage()==null?"Failed to save playlist.":e.getMessage();'''
    new='''            }catch(Exception e){
                String err=e.getMessage()==null?"Failed to save playlist.":e.getMessage();'''
    # Recovery also happens if parsing fails, without deleting either source.
    needle='''            }
        });
    }
    /**
     * Some low-storage TV boxes may still lose a staging file'''
    # Earlier v917 recovery method may be positioned differently; patch
    # finally on save() method only.
    saveStart=s.index("    private void save(CategoryScanV61 scan,Set<String> excluded){")
    saveEnd=s.index("    private File requireStagingV917()",saveStart) if "    private File requireStagingV917()" in s[saveStart:] else s.index("    private void fail(String message)",saveStart)
    block=s[saveStart:saveEnd]
    if 'store.suspendLibraryForImportV918();' not in block:raise AssertionError("save suspended missing")
    if '''        });
    }''' not in block:raise AssertionError("save end missing")
    # Always recover active from the persisted catalogue after save; success
    # of active source already holds chosen channels so no extra read.
    block=block.replace('''        });
    }''','''            finally{
                try{store.restoreLibraryAfterImportV918();}
                catch(Exception ignored){}
            }
        });
    }''',1)
    s=s[:saveStart]+block+s[saveEnd:]
    s=swap(s,
      '''                if(!source.guideUrl().isEmpty()){''',
      '''                if(store.isPlaylistActiveV99(source.id)&&
                        !source.guideUrl().isEmpty()){''',
      "inactive source does not load EPG")
    return s
modify("net/PlaylistWizardV6.java",wizard)

p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 917" in g and "versionName '0.9.17'" in g
p.write_text(g.replace("versionCode 917","versionCode 918",1)
              .replace("versionName '0.9.17'","versionName '0.9.18'",1))
print("PASS v0.9.18 one active playlist in memory, others preserved on disk, safe switching and importer memory recovery")
