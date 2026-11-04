from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
needle='''    private void showSearch() {'''
assert needle in s,"search UI not found"
method='''    private List<Channel> filteredChannelsSafeV93(String query){
        List<Channel> matched=filteredChannels(query);
        java.util.ArrayList<Channel> visible=new java.util.ArrayList<>();
        android.content.SharedPreferences prefs=getSharedPreferences("keldin_settings",MODE_PRIVATE);
        boolean hideAdult=prefs.getBoolean("hide_adult_content_v93",true);
        java.util.Set<String> hidden=prefs.getStringSet(
            "hidden_media_items_v93",java.util.Collections.emptySet());
        java.util.Set<String> hiddenSeries=prefs.getStringSet(
            "hidden_series_v93",java.util.Collections.emptySet());
        java.util.HashMap<String,java.util.Set<String>> excluded=new java.util.HashMap<>();
        for(Channel ch:matched){
            java.util.Set<String> groups=excluded.computeIfAbsent(
                ch.sourceId,store::excludedGroups);
            if(groups.contains(ch.group)||groups.contains("@kind:"+ch.kind))continue;
            if(hidden.contains(com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.key())))continue;
            if("SERIES".equals(ch.kind)&&hiddenSeries.contains(
                com.keldin.iptv.data.ContentFilterV93.fingerprint(ch.sourceId+"|"+
                    ch.group+"|"+SeriesBrowserV6.seriesBase(ch))))continue;
            if((hideAdult||(store.parentalLocked()&&!store.isContentUnlocked()))&&
                com.keldin.iptv.data.ContentFilterV93.isExplicit(ch.group,ch.name))
                continue;
            visible.add(ch);
        }
        return visible;
    }
'''
s=s.replace(needle,method+needle,1)
start=s.index(needle)
end=s.index('''    private void showLists()''',start)
fragment=s[start:end]
assert fragment.count('filteredChannels(searchQuery)')==2
fragment=fragment.replace('filteredChannels(searchQuery)','filteredChannelsSafeV93(searchQuery)')
s=s[:start]+fragment+s[end:]
p.write_text(s)
print("v0.9.3: filtered search results respect adult category/title, hidden groups and hidden movies/series")
