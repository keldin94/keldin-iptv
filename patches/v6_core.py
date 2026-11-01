from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/data/Channel.java")
s=p.read_text()
needle='''        if (u.contains("/series/")'''
assert needle in s
s=s.replace(needle,'''        if (g.contains("radio") || g.contains("radijski") || g.contains("radijske") ||
            g.contains("fm stanice") || g.contains("radiostanice") ||
            u.contains("/radio/") || u.contains("/radios/")) return "RADIO";
        if (u.endsWith(".mp3") || u.contains(".mp3?") || u.endsWith(".aac") ||
            u.contains(".aac?")) return "RADIO";
        if (u.contains("/series/")''',1)
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/net/M3uParser.java")
s=p.read_text()
s=s.replace("public static final int MAX_CHANNELS = 60000;","public static final int MAX_CHANNELS = 150000;")
needle="    public static Result parse(Reader input, String sourceId, String baseUrl) throws IOException {"
assert needle in s
s=s.replace(needle,'''    public interface ProgressListener { void onItemsParsed(int count); }

    public static Result parse(Reader input, String sourceId, String baseUrl) throws IOException {
        return parse(input,sourceId,baseUrl,null);
    }
    public static Result parse(Reader input, String sourceId, String baseUrl, ProgressListener progress) throws IOException {''',1)
needle='''                    result.channels.add(pending);
                    if (result.channels.size() >= MAX_CHANNELS) break;'''
assert needle in s
s=s.replace(needle,'''                    result.channels.add(pending);
                    if (progress!=null && result.channels.size()%500==0)
                        progress.onItemsParsed(result.channels.size());
                    if (result.channels.size() >= MAX_CHANNELS)
                        throw new IOException("Lista prelazi granicu od "+MAX_CHANNELS+" stavki. Uvezi manje kategorija ili drugu listu.");''',1)
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/data/CatalogStore.java")
s=p.read_text()
needle='''    public synchronized List<PlaylistSource> sources()'''
assert needle in s
s=s.replace(needle,'''    public boolean openLastChannelAtStart() {
        return prefs.getBoolean("startup_last",true);
    }
    public void setOpenLastChannelAtStart(boolean enabled) {
        prefs.edit().putBoolean("startup_last",enabled).apply();
    }
    public boolean hasSources(){return !sources.isEmpty();}
    public synchronized Channel lastLiveChannel(){
        for(String key:recent)
            for(Channel c:channels)
                if(c.key().equals(key)&&"LIVE".equals(c.kind)&&sourceById(c.sourceId)!=null)
                    return c;
        return null;
    }
    public Set<String> excludedGroups(String sourceId){
        HashSet<String> result=new HashSet<>();
        try{
            JSONArray groups=new JSONArray(prefs.getString("exclusions_"+sourceId,"[]"));
            for(int i=0;i<groups.length();i++)result.add(groups.getString(i));
        }catch(Exception ignored){}
        return result;
    }
    public void setExcludedGroups(String sourceId,Set<String> names){
        prefs.edit().putString("exclusions_"+sourceId,new JSONArray(names).toString()).apply();
    }
    public boolean kindEnabled(String kind){
        return prefs.getBoolean("kind_"+kind,true);
    }
    public void setKindEnabled(String kind,boolean enabled){
        prefs.edit().putBoolean("kind_"+kind,enabled).apply();
    }
    public String language(){
        return prefs.getString("ui_lang","en");
    }
    public void setLanguage(String language){prefs.edit().putString("ui_lang",language).apply();}
    public int accentIndex(){return prefs.getInt("accent",0);}
    public void setAccentIndex(int index){prefs.edit().putInt("accent",index).apply();}
    public int panelOpacity(){return prefs.getInt("panel_opacity",84);}
    public void setPanelOpacity(int opacity){prefs.edit().putInt("panel_opacity",Math.max(45,Math.min(98,opacity))).apply();}
    public int fontScaleIndex(){return prefs.getInt("font_scale",1);}
    public void setFontScaleIndex(int index){prefs.edit().putInt("font_scale",Math.max(0,Math.min(2,index))).apply();}
    public boolean parentalLocked(){return !prefs.getString("parental_pin","").isEmpty();}
    public boolean checkPin(String pin){return pin!=null&&pin.equals(prefs.getString("parental_pin",""));}
    public void setParentalPin(String pin){prefs.edit().putString("parental_pin",pin==null?"":pin).apply();}

'''+needle,1)
# Disable present groups on page display, without deleting the imported catalog
needle='''    public synchronized List<Channel> channels() { return new ArrayList<>(channels); }'''
assert needle in s
# Still allow settings to re-enable by refetch without retyping URL.
s=s.replace(needle,'''    public synchronized List<Channel> channels() { return new ArrayList<>(channels); }
    public synchronized List<Channel> channelsForKind(String kind) {
        ArrayList<Channel> filtered=new ArrayList<>();
        for(Channel c:channels)if(kind.equals(c.kind) && kindEnabled(c.kind)
            && !excludedGroups(c.sourceId).contains(c.group))filtered.add(c);
        return filtered;
    }''',1)

# New streaming catalogue persists >60,000 items without building a huge JSONArray string.
marker='''        try {
            File f = new File(context.getFilesDir(), "catalog.json");'''
assert marker in s
new='''        // v0.6 streaming cache, avoiding the huge JSONArray used by older versions.
        File lines=new File(context.getFilesDir(),"catalog-v6.jsonl");
        if(lines.exists()){
            try(java.io.BufferedReader input=new java.io.BufferedReader(
                    new java.io.InputStreamReader(new FileInputStream(lines),StandardCharsets.UTF_8))){
                String line;
                while((line=input.readLine())!=null && channels.size()<150000){
                    JSONObject o=new JSONObject(line);
                    Channel c=new Channel();
                    c.id=o.optString("id"); c.sourceId=o.optString("sourceId");
                    c.name=o.optString("name"); c.url=o.optString("url");
                    c.tvgId=o.optString("tvgId");c.logo=o.optString("logo");
                    c.group=o.optString("group","Ostalo");
                    c.kind=o.optString("kind","LIVE");c.userAgent=o.optString("userAgent");
                    channels.add(c);
                }
            }catch(Exception ignored){}
            return;
        }
'''
s=s.replace(marker,new+marker,1)
start=s.index('''    private void saveChannels() {''')
assert s.rstrip().endswith("}")
# last method until final brace
s=s[:start]+'''    private void saveChannels() {
        File temp=new File(context.getFilesDir(),"catalog-v6.tmp");
        File dest=new File(context.getFilesDir(),"catalog-v6.jsonl");
        try(java.io.BufferedWriter output=new java.io.BufferedWriter(
                new java.io.OutputStreamWriter(new FileOutputStream(temp),StandardCharsets.UTF_8))){
            for(Channel c:channels){
                JSONObject o=new JSONObject();
                o.put("id",c.id);o.put("sourceId",c.sourceId);
                o.put("name",c.name);o.put("url",c.url);
                o.put("tvgId",c.tvgId);o.put("logo",c.logo);
                o.put("group",c.group);o.put("kind",c.kind);
                o.put("userAgent",c.userAgent);
                output.write(o.toString());output.newLine();
            }
        }catch(Exception ex){temp.delete();return;}
        if(!temp.renameTo(dest)) {
            try(java.io.InputStream in=new FileInputStream(temp);
                java.io.OutputStream out=new FileOutputStream(dest)){
                byte[] buf=new byte[8192];int n;
                while((n=in.read(buf))>0)out.write(buf,0,n);
            }catch(Exception ignored){return;}
            temp.delete();
        }
        new File(context.getFilesDir(),"catalog.json").delete();
    }
}
'''
p.write_text(s)
print("v0.6 core: radio + progressive parser + filters + compact persistent catalogue")
