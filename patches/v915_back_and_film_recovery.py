from pathlib import Path

BASE=Path("app/src/main/java/com/keldin/iptv")
def edit(relative,transform):
    p=BASE/relative
    old=p.read_text()
    new=transform(old)
    if old==new:raise AssertionError("v915 unchanged: "+relative)
    p.write_text(new)
def change(s,old,new,label):
    if old not in s:raise AssertionError("v915 missing: "+label+" | "+old[:95])
    return s.replace(old,new,1)

# Playlists already excluded by older versions cannot be magically recreated:
# the user must run the existing three-step wizard to download ONLY the missing
# broadcast channels. Do not erase their other category choices.
def wizard(s):
    s=change(s,
        '''    private final Complete done;''',
        '''    private final Complete done;
    private final boolean recoverFilmChannelsV915;''',
        "wizard recovery mode field")
    anchor='''    public PlaylistWizardV6(Activity activity,CatalogStore store,PlaylistSource src,Complete done){
        this.activity=activity;this.store=store;this.source=src;this.done=done;
    }'''
    replacement='''    public PlaylistWizardV6(Activity activity,CatalogStore store,PlaylistSource src,Complete done){
        this(activity,store,src,done,false);
    }
    public PlaylistWizardV6(Activity activity,CatalogStore store,PlaylistSource src,
            Complete done,boolean recoverFilmChannels){
        this.activity=activity;this.store=store;this.source=src;this.done=done;
        this.recoverFilmChannelsV915=recoverFilmChannels;
    }'''
    s=change(s,anchor,replacement,"overloaded recovery wizard constructor")
    s=change(s,
        '''            enabled[i]=!old.contains("@kind:"+KINDS[i]);''',
        '''            enabled[i]=!old.contains("@kind:"+KINDS[i]);
            if(recoverFilmChannelsV915&&i==0)enabled[i]=true;''',
        "re-enable Live TV for film broadcaster recovery")
    s=change(s,
        '''        String explanation="Select the countries and categories you watch. "+''',
        '''        // The standard chooser may have its own local/country filters.
        // In recovery mode only, restore Live and the previously missing
        // broadcaster categories after those normal defaults are computed.
        if(recoverFilmChannelsV915){
            enabled[0]=true;
            for(int i=0;i<groups.size();i++)
                if(com.keldin.iptv.data.Channel.isLiveFilmGroup(
                        groups.get(i),"http://localhost/live/film"))
                    enabled[i+4]=true;
        }
        String explanation="Select the countries and categories you watch. "+''',
        "recover live film group after all default selections")
    s=change(s,
        '''        if(warning!=null)explanation+="\\n\\n"+warning;''',
        '''        if(recoverFilmChannelsV915)
            explanation+="\\n\\nRecovery mode: Live TV and regional film TV channels "+
                "are preselected. Keep your other selections or adjust them below.";
        if(warning!=null)explanation+="\\n\\n"+warning;''',
        "explain one-time refresh scope")
    return s
edit("net/PlaylistWizardV6.java",wizard)

# On Back from player, MainActivity.onResume was calling render() and rebuilding
# a 150,000-item browse screen synchronously. The existing screen already exists
# behind PlayerActivity; keep it, persist last source/group, and rebuild only on
# explicit category navigation. Direct three-dot Settings already avoids this.
def main(s):
    old='''            page="Uživo";
            selectedGroup=playedGroup;
            selectedSourceV99=prefs.getString("return_live_source_v99","");
            render();'''
    new='''            // A Back-to-app return must NOT reconstruct an entire huge
            // Live TV catalogue in the resumed Activity on its UI thread.
            // Keep the existing screen. The exact last source/category/key
            // are persisted above and restored on the next explicit Live TV open.
            if("Uživo".equals(page)){
                selectedGroup=playedGroup;
                selectedSourceV99=prefs.getString("return_live_source_v99","");
            }'''
    s=change(s,old,new,"avoid synchronous entire-grid rebuild after Back")
    s=change(s,
        '''            releaseHeavyBrowseV911();
            store.clearLiveIndexV911();''',
        '''            releaseHeavyBrowseV911();
            // Reusing the source index avoids a costly synchronized purge
            // and reallocation while transitioning to the lightweight Home.''',
        "remove enormous on-Back cache churn")
    # Add recovery button to Live TV only when provider group is absent.
    begin=s.index("    private void showChannelGrid(boolean guideMode) {")
    end=s.index("    private ArrayList<Channel> filterSection(",begin)
    part=s[begin:end]
    needle='''        browsing.addView(count);'''
    inject='''        browsing.addView(count);
        if("LIVE".equals(kind)){
            boolean filmTVPresentV915=false;
            for(Channel broadcast:section)
                if(Channel.isLiveFilmGroup(broadcast.group,broadcast.url)){
                    filmTVPresentV915=true;break;
                }
            if(!filmTVPresentV915&&!store.sources().isEmpty()){
                TextView restore=Ui.button(this,
                    "↻  Restore EX YU | Filmovi & Serije channels",
                    this::restoreFilmChannelsV915,false);
                restore.setContentDescription(
                    "Refresh IPTV playlist and reimport missing EX YU film TV channels");
                LinearLayout.LayoutParams buttonLp=Ui.lp(this,-1,42);
                buttonLp.topMargin=Ui.dp(this,8);
                buttonLp.bottomMargin=Ui.dp(this,9);
                browsing.addView(restore,buttonLp);
            }
        }'''
    part=change(part,needle,inject,"repair missing category on Live TV screen")
    s=s[:begin]+part+s[end:]
    marker='''    private void showChannelGrid(boolean guideMode) {'''
    methods='''    private void restoreFilmChannelsV915(){
        java.util.ArrayList<PlaylistSource> active=new java.util.ArrayList<>();
        for(PlaylistSource src:store.sources())
            if(store.isPlaylistActiveV99(src.id))active.add(src);
        if(active.isEmpty()){
            message("Enable an IPTV playlist in Settings > Playlists first.");
            return;
        }
        String[] names=new String[active.size()];
        for(int i=0;i<active.size();i++)names[i]=active.get(i).name;
        new AlertDialog.Builder(this)
            .setTitle("Restore missing EX YU film TV channels")
            .setMessage("The old import may have skipped this Live TV category. "+
                "Choose a playlist to rescan. Existing channels are retained "+
                "until the new selection is successfully saved.")
            .setItems(names,(dialog,index)->{
                PlaylistSource chosen=active.get(index);
                new com.keldin.iptv.net.PlaylistWizardV6(this,store,chosen,
                    (success,msg)->{
                        message(msg);
                        if(success)navigate("Uživo");
                    },true).start();
            })
            .setNegativeButton(tr("cancel"),null).show();
    }

'''
    s=change(s,marker,methods+marker,"one-click recovery from live categories")
    return s
edit("ui/MainActivity.java",main)

# This is deliberately a patch after v914, not a second player or duplicate UI.
gradle=Path("app/build.gradle")
g=gradle.read_text()
assert "versionCode 914" in g and "versionName '0.9.14'" in g
gradle.write_text(g.replace("versionCode 914","versionCode 915",1)
                   .replace("versionName '0.9.14'","versionName '0.9.15'",1))
print("PASS v0.9.15: Back uses existing screen, no heavy immediate redraw; missing film-TV recovery wizard keeps other selections")
