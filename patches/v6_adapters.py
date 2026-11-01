from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/CategoryAdapter.java")
s=p.read_text()
s=s.replace('''    private String active="Sve kategorije";''','''    private String active="Sve kategorije";
    private boolean condensed;
    private Runnable focusCallback;
    public void setCondensed(boolean enabled){condensed=enabled;notifyDataSetChanged();}
    public void setFocusCallback(Runnable callback){focusCallback=callback;}''',1)
s=s.replace('''        h.name.setText(group);''',
'''        h.name.setText(condensed?(group.equals("Sve kategorije")?"▦":
            group.isEmpty()?"•":group.substring(0,1).toUpperCase()):group);
        h.name.setGravity(condensed?Gravity.CENTER:Gravity.CENTER_VERTICAL);''',1)
s=s.replace('''        h.itemView.setOnFocusChangeListener((v,focus)->update(h,group,focus));''',
'''        h.itemView.setOnFocusChangeListener((v,focus)->{
            if(focus&&focusCallback!=null)focusCallback.run();
            update(h,group,focus);
        });''',1)
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/ui/PosterAdapterV6.java")
s=p.read_text()
s=s.replace('''    private final Open open;''',
'''    private final Open open;
    private Runnable focusCallback;
    public void setFocusCallback(Runnable listener){focusCallback=listener;}''',1)
s=s.replace('''        holder.itemView.setOnFocusChangeListener((v,has)->{
            GradientDrawable d''',
'''        holder.itemView.setOnFocusChangeListener((v,has)->{
            if(has&&focusCallback!=null)focusCallback.run();
            GradientDrawable d''',1)
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/data/CatalogStore.java")
s=p.read_text()
anchor='''    public boolean parentalLocked(){return !prefs.getString("parental_pin","").isEmpty();}'''
assert anchor in s
s=s.replace(anchor,'''    private transient boolean adultUnlocked;
    public boolean isContentUnlocked(){return adultUnlocked;}
    public void lockContent(){adultUnlocked=false;}
    public boolean unlockContent(String pin){
        adultUnlocked=checkPin(pin);
        return adultUnlocked;
    }
    public static boolean isAdultCategory(String group){
        if(group==null)return false;
        String g=group.toLowerCase(java.util.Locale.ROOT);
        return g.contains("adult")||g.contains("xxx")||g.contains("18+")||
            g.contains("porn")||g.contains("erotic")||g.contains("odrasli");
    }
'''+anchor,1)
# Avoid plaintext passwords/PINs in SharedPreferences.
s=s.replace('''    public boolean checkPin(String pin){return pin!=null&&pin.equals(prefs.getString("parental_pin",""));}''',
'''    public boolean checkPin(String pin){return pin!=null&&!pin.isEmpty() &&
        secureHash(pin).equals(prefs.getString("parental_pin",""));}
    private static String secureHash(String input){
        try{
            byte[] bytes=java.security.MessageDigest.getInstance("SHA-256")
                .digest(("KeldinV6:"+input).getBytes(StandardCharsets.UTF_8));
            StringBuilder out=new StringBuilder();
            for(byte v:bytes)out.append(String.format(java.util.Locale.ROOT,"%02x",v&255));
            return out.toString();
        }catch(Exception e){return "";}
    }''',1)
s=s.replace('''    public void setParentalPin(String pin){prefs.edit().putString("parental_pin",pin==null?"":pin).apply();}''',
'''    public void setParentalPin(String pin){
        prefs.edit().putString("parental_pin",pin==null||pin.isEmpty()?"":secureHash(pin)).apply();
        adultUnlocked=false;
    }''',1)
# Explicitly filter exclusions once when called, not once per record
s=s.replace('''        for(Channel c:channels)if(kind.equals(c.kind) && kindEnabled(c.kind)
            && !excludedGroups(c.sourceId).contains(c.group))filtered.add(c);''',
'''        HashMap<String,Set<String>> filterCache=new HashMap<>();
        for(Channel c:channels){
            if(!kind.equals(c.kind)||!kindEnabled(c.kind))continue;
            Set<String> excluded=filterCache.computeIfAbsent(c.sourceId,this::excludedGroups);
            if(!excluded.contains(c.group) && !excluded.contains("@kind:"+c.kind))filtered.add(c);
        }''',1)
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
s=s.replace('''        for(Channel ch:source){
            if(!kind.isEmpty()&&!kind.equals(ch.kind))continue;
            if(store.excludedGroups(ch.sourceId).contains(ch.group))continue;
            if(store.excludedGroups(ch.sourceId).contains("@kind:"+ch.kind))continue;''',
'''        java.util.HashMap<String,java.util.Set<String>> exclusions=new java.util.HashMap<>();
        for(Channel ch:source){
            if(!kind.isEmpty()&&!kind.equals(ch.kind))continue;
            java.util.Set<String> excluded=exclusions.computeIfAbsent(
                ch.sourceId,store::excludedGroups);
            if(excluded.contains(ch.group)||excluded.contains("@kind:"+ch.kind))continue;''',1)
s=s.replace('''            TextView refresh=Ui.button(this,"↻  Sync",()->new com.keldin.iptv.net.PlaylistWizardV6(
                this,store,src,(success,msg)->{notice.setText(msg);render();}).start(),false);''',
'''            TextView refresh=Ui.button(this,"↻  Sync",()->{
                if("FILE".equals(src.type)){refresh(src);return;}
                new com.keldin.iptv.net.PlaylistWizardV6(
                    this,store,src,(success,msg)->{notice.setText(msg);render();}).start();
            },false);''',1)
s=s.replace('''        addOptionV6(body,"Parental PIN",store.parentalLocked()?"Enabled":"Disabled",
            "Hide adult-labelled groups until you enter your PIN. This is a basic local parental control.",this::configurePinV6);''',
'''        addOptionV6(body,"Parental PIN",store.parentalLocked()?"Enabled":"Disabled",
            "Hide adult-labelled groups until you enter your PIN. This is a basic local parental control.",this::configurePinV6);
        if(store.parentalLocked())addOptionV6(body,"Unlock restricted categories",
            store.isContentUnlocked()?"Unlocked for this session":"Locked",
            "Enter PIN to show restricted channels until the app process closes.",()->{
                EditText pin=new EditText(this);
                pin.setInputType(InputType.TYPE_CLASS_NUMBER|InputType.TYPE_NUMBER_VARIATION_PASSWORD);
                pin.setHint("Parental PIN");
                new AlertDialog.Builder(this).setTitle("Unlock")
                    .setView(pin).setPositiveButton("Unlock",(d,w)->{
                        if(store.unlockContent(pin.getText().toString()))render();
                        else message("Incorrect PIN");
                    }).setNegativeButton("Cancel",null).show();
            });''',1)
p.write_text(s)
print("v0.6 adapters + parental control + category filtering optimization applied")
