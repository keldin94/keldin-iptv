from pathlib import Path
main=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=main.read_text()
def replace(old,new,name):
    global s
    if old not in s: raise RuntimeError("v0.6 main marker missing: "+name+" / "+old[:85])
    s=s.replace(old,new,1)

replace('''    private static final String[] PAGES = {"Početna","Uživo","Filmovi","Serije","Favoriti","TV vodič","Pretraga","Moje liste","Postavke"};''',
'''    private static final String[] PAGES = {"Početna","Uživo","Filmovi","Serije","Radio","Favoriti","TV vodič","Pretraga","Moje liste","Postavke"};''',"add radio")
replace('''    private static final String[] ICONS = {"⌂","◉","▣","▤","♡","▦","⌕","☷","⚙"};''',
'''    private static final String[] ICONS = {"⌂","◉","▣","▤","♫","♡","▦","⌕","☷","⚙"};''',"radio icon")
# English by default for visible strings, keeping stable internal keys.
s=s.replace('''    private String searchQuery = "";''','''    private String searchQuery = "";
    private boolean autoLaunched=false;
    private TextView settingsHelp;
    private final android.os.Handler mainHandler=new android.os.Handler(android.os.Looper.getMainLooper());
    private String tr(String key){return I18n.t(this,key);}
''',1)
start=s.index("    @Override protected void onCreate(Bundle savedInstanceState) {")
end=s.index("    @Override protected void onResume()",start)
s=s[:start]+'''    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN
            |View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        Ui.applyTheme(this);
        TextView loading=Ui.text(this,"KELDIN IPTV\\n\\nLoading your library…",22,Ui.WHITE,true);
        loading.setGravity(Gravity.CENTER);
        loading.setBackgroundColor(Ui.BG);
        setContentView(loading);
        // Parse the large persistent catalogue off the main/UI thread.
        new Thread(()->{
            try {
                CatalogStore prepared=CatalogStore.shared(getApplicationContext());
                runOnUiThread(()->{
                    if(isFinishing()||isDestroyed())return;
                    store=prepared;
                    sync=new PlaylistSync(this,store);
                    createShell();
                    render();
                    if(store.channels().isEmpty()&&!store.sources().isEmpty()){
                        // Explicitly show playlists to repair/refresh an empty cache.
                        navigate("Moje liste");
                    }else if(savedInstanceState==null&&store.openLastChannelAtStart()){
                        Channel last=store.lastLiveChannel();
                        if(last!=null&&!autoLaunched){
                            autoLaunched=true;
                            mainHandler.post(()->play(last));
                        }
                    }
                });
            } catch(Exception ex){
                runOnUiThread(()->{
                    new AlertDialog.Builder(this).setTitle("Keldin IPTV")
                        .setMessage("Cannot open local library. "+ex.getClass().getSimpleName())
                        .setPositiveButton("Close",(d,w)->finish()).show();
                });
            }
        },"KeldinLibraryLoader").start();
    }

'''+s[end:]
replace('''        LinearLayout root=Ui.horizontal(this);root.setGravity(Gravity.TOP);''',
'''        navItems.clear();
        LinearLayout root=Ui.horizontal(this);root.setGravity(Gravity.TOP);''',"clear nav")
# Title lines, navbar labels and date
replace('''            TextView item=Ui.text(this,ICONS[i]+"   "+target,14,Ui.MUTED,false);''',
'''            TextView item=Ui.text(this,ICONS[i]+"   "+displayPage(target),14,Ui.MUTED,false);''',"nav translation")
replace('''        TextView now=Ui.text(this,new SimpleDateFormat("EEE, d. MMM",new Locale("bs")).format(new java.util.Date()),13,Ui.MUTED,false);''',
'''        TextView now=Ui.text(this,new SimpleDateFormat("EEE, d MMM",Locale.getDefault()).format(new java.util.Date()),13,Ui.MUTED,false);''',"header date")
replace('''        TextView home=Ui.button(this,"⌂  Početna",()->navigate("Početna"),false);''',
'''        TextView home=Ui.button(this,"⌂  "+tr("home"),()->navigate("Početna"),false);''',"home label")
replace('''        TextView search=Ui.button(this,"⌕  Pretraga",()->navigate("Pretraga"),false);''',
'''        TextView search=Ui.button(this,"⌕  "+tr("search"),()->navigate("Pretraga"),false);''',"search label")
replace('''        TextView add=Ui.button(this,"☷  Liste",()->navigate("Moje liste"),false);''',
'''        TextView add=Ui.button(this,"☷  "+tr("lists"),()->navigate("Moje liste"),false);''',"lists label")
replace('''        page=destination;searchQuery="";selectedGroup="Sve kategorije";render();''',
'''        page=destination;searchQuery="";
        selectedGroup=getSharedPreferences("keldin_settings",MODE_PRIVATE)
            .getString("selected_group_"+page,"Sve kategorije");
        render();''',"remember category")
replace('''        title.setText("Početna".equals(page)?"KELDIN IPTV":page);''',
'''        title.setText("Početna".equals(page)?"KELDIN IPTV":displayPage(page));''',"title translation")
replace('''        subtitle.setText("Početna".equals(page)?
            "TV uživo, filmovi i serije na jednom mjestu":
            "Keldin IPTV   •   "+store.sources().size()+" aktivnih lista");''',
'''        subtitle.setText("Početna".equals(page)?
            tr("choose"):
            "Keldin IPTV   •   "+store.sources().size()+" playlists");''',"subtitle")
replace('''        if(store.sources().isEmpty() && !page.equals("Moje liste")&&!page.equals("Postavke")) {''',
'''        if(store.sources().isEmpty() && !page.equals("Moje liste")
            && !page.equals("Postavke")&&!page.equals("Početna")) {''',"empty home")
replace('''            case "Uživo": case "Filmovi": case "Serije": case "Favoriti": showChannelGrid(false);break;''',
'''            case "Uživo": case "Filmovi": case "Serije": case "Radio": case "Favoriti": showChannelGrid(false);break;''',"radio grid")
replace('''            case "Postavke":showSettings();break;''',
'''            case "Postavke":showSettingsV6();break;''',"new settings")
# v0.5 home to 5 equal large tiles
start=s.index("    private void showHome() {")
end=s.index("    private void landingTile(",start)
s=s[:start]+'''    private String displayPage(String name){
        switch(name){
            case "Početna":return tr("home");
            case "Uživo":return tr("live");
            case "Filmovi":return tr("movies");
            case "Serije":return tr("series");
            case "Radio":return tr("radio");
            case "Favoriti":return tr("favorites");
            case "TV vodič":return tr("guide");
            case "Pretraga":return tr("search");
            case "Moje liste":return tr("lists");
            case "Postavke":return tr("settings");
            default:return name;
        }
    }
    private void refreshAppearance(){
        Ui.applyTheme(this);
        createShell();
        render();
    }
    private void showHome() {
        ScrollView scroll=new ScrollView(this);
        scroll.setFillViewport(true);scroll.setVerticalScrollBarEnabled(false);
        LinearLayout body=Ui.vertical(this);
        body.setPadding(Ui.dp(this,4),Ui.dp(this,9),Ui.dp(this,4),Ui.dp(this,10));
        scroll.addView(body);
        TextView label=Ui.text(this,tr("choose"),21,Ui.WHITE,true);
        body.addView(label);body.addView(Ui.space(this,19));
        LinearLayout cards=Ui.horizontal(this);
        landingTile(cards,"▣",tr("live"),tr("guide"),"Uživo");
        landingTile(cards,"▷",tr("movies"),tr("categories"),"Filmovi");
        landingTile(cards,"▤",tr("series"),tr("categories"),"Serije");
        landingTile(cards,"♫",tr("radio"),tr("favorites"),"Radio");
        landingTile(cards,"⚙",tr("settings"),tr("appearance"),"Postavke");
        body.addView(cards,Ui.lp(this,-1,183));
        body.addView(Ui.space(this,30));
        List<Channel> recent=store.recentChannels();
        if(!recent.isEmpty()){
            body.addView(Ui.text(this,tr("continue"),18,Ui.WHITE,true));
            body.addView(Ui.space(this,14));
            addHorizontalCards(body,recent,8);
        }
        if(store.sources().isEmpty()){
            body.addView(Ui.space(this,18));
            TextView add=Ui.button(this,"＋  "+tr("add"),()->editSource(null,"M3U"),true);
            body.addView(add,Ui.lp(this,310,52));
        }
        content.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
    }

'''+s[end:]
# v0.5 category browser replace with responsive split and poster grids
start=s.index("    private void showChannelGrid(boolean guideMode) {")
end=s.index("    private void showGuide() {",start)
s=s[:start]+'''    private void showChannelGrid(boolean guideMode) {
        String kind=page.equals("Filmovi")?"MOVIES":page.equals("Serije")?"SERIES":
            page.equals("Uživo")?"LIVE":page.equals("Radio")?"RADIO":"";
        List<Channel> source="Favoriti".equals(page)?store.favorites():store.channels();
        ArrayList<Channel> section=new ArrayList<>();
        LinkedHashSet<String> groups=new LinkedHashSet<>();
        groups.add("Sve kategorije");
        for(Channel ch:source){
            if(!kind.isEmpty()&&!kind.equals(ch.kind))continue;
            if(store.excludedGroups(ch.sourceId).contains(ch.group))continue;
            if(store.excludedGroups(ch.sourceId).contains("@kind:"+ch.kind))continue;
            if(store.parentalLocked()&&!store.isContentUnlocked()&&CatalogStore.isAdultCategory(ch.group))continue;
            section.add(ch);
            groups.add(ch.group==null||ch.group.isEmpty()?"Ostalo":ch.group);
        }
        if(!groups.contains(selectedGroup))selectedGroup="Sve kategorije";
        LinearLayout main=Ui.horizontal(this);
        main.setGravity(Gravity.TOP);
        LinearLayout categoryBox=Ui.vertical(this);
        categoryBox.setPadding(Ui.dp(this,10),Ui.dp(this,12),Ui.dp(this,9),Ui.dp(this,8));
        categoryBox.setBackground(Ui.shape(Ui.PANEL,14,this));
        TextView categoryLabel=Ui.text(this,tr("categories").toUpperCase(Locale.ROOT),11,Ui.ACCENT,true);
        categoryBox.addView(categoryLabel);
        categoryBox.addView(Ui.space(this,12));
        RecyclerView categories=new RecyclerView(this);
        categories.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));
        categories.setItemAnimator(null);
        categories.setHasFixedSize(true);
        categoryBox.addView(categories,new LinearLayout.LayoutParams(-1,0,1));
        LinearLayout.LayoutParams catParams=Ui.lp(this,220,-1);
        catParams.rightMargin=Ui.dp(this,15);
        main.addView(categoryBox,catParams);
        LinearLayout browsing=Ui.vertical(this);
        TextView count=Ui.text(this,"",13,Ui.MUTED,false);
        browsing.addView(count);browsing.addView(Ui.space(this,8));
        RecyclerView grid=new RecyclerView(this);
        boolean isPosters="MOVIES".equals(kind)||"SERIES".equals(kind);
        GridLayoutManager gridManager=new GridLayoutManager(this,isPosters?4:4);
        grid.setLayoutManager(gridManager);
        grid.setHasFixedSize(true);
        grid.setItemAnimator(null);
        grid.setClipToPadding(false);
        ArrayList<Channel> visible=filterSection(section,selectedGroup);
        final Runnable[] openPane={()->{}};
        ChannelAdapter channelAdapter=null;
        PosterAdapterV6 posterAdapter=null;
        if(isPosters){
            posterAdapter=new PosterAdapterV6(visible,this::openMediaDetails);
            grid.setAdapter(posterAdapter);
        }else{
            channelAdapter=new ChannelAdapter(store,visible,this::play,guideMode);
            grid.setAdapter(channelAdapter);
        }
        count.setText(visible.size()+" items  •  OK to open");
        browsing.addView(grid,new LinearLayout.LayoutParams(-1,0,1));
        main.addView(browsing,new LinearLayout.LayoutParams(0,-1,1));
        final ChannelAdapter liveAdapter=channelAdapter;
        final PosterAdapterV6 mediaAdapter=posterAdapter;
        CategoryAdapter categoryAdapter=new CategoryAdapter(this,new ArrayList<>(groups),selectedGroup,group->{
            selectedGroup=group;
            getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                .putString("selected_group_"+page,group).apply();
            ArrayList<Channel> filtered=filterSection(section,group);
            if(mediaAdapter!=null)mediaAdapter.replace(filtered);
            if(liveAdapter!=null)liveAdapter.setItems(filtered);
            count.setText(filtered.size()+" items  •  "+group);
            grid.scrollToPosition(0);
        });
        categories.setAdapter(categoryAdapter);
        if(isPosters){
            final boolean[] narrow={false};
            final int wide=220,slim=83;
            mediaAdapter.setFocusCallback(()->{
                if(!narrow[0]){
                    narrow[0]=true;
                    catParams.width=Ui.dp(this,slim);
                    categoryBox.setLayoutParams(catParams);
                    categoryAdapter.setCondensed(true);
                    gridManager.setSpanCount(5);
                }
            });
            categoryAdapter.setFocusCallback(()->{
                if(narrow[0]){
                    narrow[0]=false;
                    catParams.width=Ui.dp(this,wide);
                    categoryBox.setLayoutParams(catParams);
                    categoryAdapter.setCondensed(false);
                    gridManager.setSpanCount(4);
                }
            });
        }
        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));
    }
    private ArrayList<Channel> filterSection(List<Channel> section,String group){
        ArrayList<Channel> filtered=new ArrayList<>();
        for(Channel c:section)
            if("Sve kategorije".equals(group)||group.equals(c.group))filtered.add(c);
        return filtered;
    }
    private void openMediaDetails(Channel media){
        String name=media.name;
        String message="Category: "+media.group+"\\n"+
            ("SERIES".equals(media.kind)?
            "Episodes and seasons are shown if supplied by the playlist.":"Resume playback is saved automatically.");
        new AlertDialog.Builder(this).setTitle(name).setMessage(message)
            .setPositiveButton(tr("play"),(d,w)->play(media))
            .setNeutralButton(tr("favorites"),(d,w)->{store.toggleFavorite(media);render();})
            .setNegativeButton(tr("cancel"),null).show();
    }
'''+s[end:]

# Save only after successful preview/selection; don't auto refresh without feedback
replace('''            store.putSource(src);dialog.dismiss();navigate("Moje liste");refresh(src);''',
'''            dialog.dismiss();
            new com.keldin.iptv.net.PlaylistWizardV6(this,store,src,(success,msg)->{
                notice.setText(msg);
                navigate(success?"Moje liste":"Početna");
            }).start();''',"wizard entry point")
# List manager: add category manage + use wizard when refreshing (also prevents silent 2 min wait)
replace('''            TextView refresh=Ui.button(this,"↻  Osvježi",()->refresh(src),false);''',
'''            TextView refresh=Ui.button(this,"↻  Sync",()->new com.keldin.iptv.net.PlaylistWizardV6(
                this,store,src,(success,msg)->{notice.setText(msg);render();}).start(),false);''',"refresh wizard")
needle='''            if(!src.type.equals("FILE")) {
                TextView edit=Ui.button(this,"Uredi",()->editSource(src,src.type),false);'''
assert needle in s
s=s.replace(needle,'''            if(!src.type.equals("FILE")) {
                TextView edit=Ui.button(this,"Edit",()->editSource(src,src.type),false);''',1)
# Show names instead of full list count during app start
s=s.replace('''        TextView settingsNote=Ui.text(this,"POSTAVKE REPRODUKCIJE",12,Ui.ACCENT,true);''',
'''        TextView settingsNote=Ui.text(this,"PLAYBACK SETTINGS",12,Ui.ACCENT,true);''',1)
# On first launch when no lists, edited welcome has top button; home still accessible
main.write_text(s)
print("v0.6 main UI, startup, 5 sections, responsive poster rails, live grouping and import integrated")

ui=Path("app/src/main/java/com/keldin/iptv/ui/Ui.java")
s=ui.read_text()
s=s.replace("public static final int ACCENT = Color.rgb(77,211,244);",
'''public static int ACCENT = Color.rgb(77,211,244);
    private static float textScale=1f;
    private static android.graphics.Typeface inter;
    public static void applyTheme(Context context){
        int i=context.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE).getInt("accent",0);
        int[] palette={0xff4dd3f4,0xff9896fc,0xff50d8aa,0xffffb45f,0xffe1eaf3};
        ACCENT=palette[Math.max(0,Math.min(palette.length-1,i))];
        int size=context.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE).getInt("font_scale",1);
        textScale=size==0?.91f:size==2?1.12f:1f;
    }''')
assert "public static void applyTheme(Context context)" in s
s=s.replace('''        t.setText(title); t.setTextSize(sp); t.setTextColor(color);
        if (bold) t.setTypeface(Typeface.DEFAULT,Typeface.BOLD);''',
'''        t.setText(title); t.setTextSize(sp*textScale); t.setTextColor(color);
        if(inter==null)try{ inter=Typeface.createFromAsset(ctx.getAssets(),"inter_regular.ttf"); }
            catch(Exception ignored){ inter=Typeface.create("sans-serif",Typeface.NORMAL); }
        t.setTypeface(Typeface.create(inter,bold?Typeface.BOLD:Typeface.NORMAL));''')
ui.write_text(s)
p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 5" in g and "applicationIdSuffix '.epsilon'" in g
g=g.replace("versionCode 5","versionCode 6")
g=g.replace("versionName '0.5.0-navigation'","versionName '0.6.0-editorial'")
g=g.replace("applicationIdSuffix '.epsilon'","applicationIdSuffix '.zeta'")
p.write_text(g)
print("v0.6 themed typography and separate beta package ready")
