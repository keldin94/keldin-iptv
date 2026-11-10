from pathlib import Path
import re

ROOT=Path("app/src/main/java/com/keldin/iptv")
def edit(rel,func):
    p=ROOT/rel
    old=p.read_text()
    new=func(old)
    if old==new: raise AssertionError("v0.9.8 no change: "+rel)
    p.write_text(new)

def replace_once(s,old,new,label):
    if old not in s: raise AssertionError("v0.9.8 missing "+label)
    return s.replace(old,new,1)

# A film-broadcaster group must remain a LIVE group, not a VOD/series shelf.
# Preserve genuine movie/series URLs and all other provider group titles.
def classify(s):
    start=s.index("    public static boolean isLiveFilmGroup(String group,String url){")
    end=s.index("    public static String inferKind(",start)
    new='''    public static boolean isLiveFilmGroup(String group,String url){
        String g=(group==null?"":group).toLowerCase(Locale.ROOT)
            .replace('-', ' ').replace('_', ' ').replace('|',' ')
            .replaceAll("\\\\s+"," ").trim();
        String u=(url==null?"":url).toLowerCase(Locale.ROOT);
        if(u.contains("/movie/")||u.contains("/series/"))return false;
        boolean cinematic=g.contains("filmski")||g.contains("filmsk")||
            g.contains("film channels")||g.contains("movie channels")||
            g.contains("cinema channels")||g.contains("kino kanali");
        boolean regional=g.contains("ex yu")||g.contains("exyu")||
            g.contains("ex jug")||g.contains("ex yug")||
            g.contains("balkan")||g.contains("regional");
        // EX-YU/Balkan film *channels* are not on-demand titles.
        return cinematic && (regional||g.equals("filmski")||
            g.equals("filmski kanali")||g.equals("film channels"));
    }

'''
    return s[:start]+new+s[end:]
edit("data/Channel.java",classify)

def cache(s):
    return replace_once(s,'''if("MOVIES".equals(c.kind)&&Channel.isLiveFilmGroup(c.group,c.url))''',
       '''if(!"LIVE".equals(c.kind)&&Channel.isLiveFilmGroup(c.group,c.url))''',
       "legacy cache upgrade")
edit("data/CatalogStore.java",cache)

def main(s):
    s=replace_once(s,'''rightPanel.setPadding(Ui.dp(this,18),Ui.dp(this,10),Ui.dp(this,16),Ui.dp(this,9));''',
      '''// Extra TV-safe area keeps Search and Settings clear of display overscan.
        rightPanel.setPadding(Ui.dp(this,22),Ui.dp(this,10),Ui.dp(this,48),Ui.dp(this,9));''',
      "top toolbar safe area")
    s=replace_once(s,
       '''            if(!kind.isEmpty()&&!kind.equals(ch.kind))continue;''',
       '''            boolean liveFilmV98=Channel.isLiveFilmGroup(ch.group,ch.url);
            String effectiveKindV98=liveFilmV98?"LIVE":ch.kind;
            if(!kind.isEmpty()&&!kind.equals(effectiveKindV98))continue;''',
       "display live films even from previously cached VOD classification")
    # Relocate existing content setting to the END of its own tab.
    start=s.index('''        addOptionV6(body,"Hide adult content",''')
    end=s.index('''        addOptionV6(body,"Manage movie categories"''',start)
    block=s[start:end]
    s=s[:start]+s[end:]
    block=block.replace('"Hide adult content"','"Adult channels & content"')
    block=block.replace('?\"On\":\"Off\"','?"Hidden":"Visible"')
    block=block.replace('Always filter explicit titles and categories in live TV, movies and series. On is the default. This setting is saved between updates.',
            'Hidden by default. Show or hide adult channels, movies and series. Your selection is saved.')
    tab=s.index("        if(selectedSettingsTab==3){")
    brace=s.index("{",tab)
    level=1
    i=brace+1
    # Scan curly braces, ignoring braces inside Java string literals.
    quote=False; escaped=False
    while i<len(s) and level:
        c=s[i]
        if quote:
            if escaped:escaped=False
            elif c=="\\":escaped=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=="{":level+=1
        elif c=="}":level-=1
        i+=1
    if level:raise AssertionError("unbalanced Settings section")
    insertion=i-1
    s=s[:insertion]+"\n        // Keep adult visibility at the bottom of the Content tab.\n"+block+s[insertion:]
    # When playback closes, display its ACTUAL live group, not the launch-time one.
    method=re.search(r'@Override\s+protected\s+void\s+onResume\s*\(\s*\)\s*\{',s)
    if not method:raise AssertionError("onResume not found")
    injection='''\n        getWindow().getDecorView().post(()->{
            if(store==null || isFinishing() || isDestroyed())return;
            if(getIntent()!=null &&
                getIntent().getBooleanExtra("keldin_open_settings_v96",false))return;
            android.content.SharedPreferences prefs=
                getSharedPreferences("keldin_settings",MODE_PRIVATE);
            if(!prefs.getBoolean("return_live_pending_v98",false))return;
            String playedGroup=prefs.getString("return_live_group_v98","Sve kategorije");
            prefs.edit().putBoolean("return_live_pending_v98",false)
                .putString("selected_group_Uživo",playedGroup).apply();
            page="Uživo";
            selectedGroup=playedGroup;
            render();
        });'''
    s=s[:method.end()]+injection+s[method.end():]
    return s
edit("ui/MainActivity.java",main)

def player(s):
    needle='''    @Override protected void onStop(){'''
    if needle not in s:raise AssertionError("player onStop anchor")
    persist='''    private void rememberLiveReturnV98(){
        if(current==null||!"LIVE".equals(current.kind))return;
        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
            .putString("return_live_group_v98",
                current.group==null||current.group.isEmpty()?
                    "Ostalo":current.group)
            .putString("return_live_key_v98",current.key())
            .putBoolean("return_live_pending_v98",true).apply();
    }
    @Override protected void onPause(){
        rememberLiveReturnV98();
        super.onPause();
    }

'''
    return replace_once(s,needle,persist+needle,"save actual channel before returning")
edit("playback/PlayerActivity.java",player)

def side(s):
    s=replace_once(s,'''    private RecyclerView list;''',
       '''    private RecyclerView list;
    private RecyclerView categoryLogoPreviewV98;''',"logo preview holder")
    s=replace_once(s,'''        current=channel;
        mode=CHANNELS;
        refresh();''',
       '''        current=channel;
        selectedCategory=channel.group==null||channel.group.isEmpty()?
            "Ostalo":channel.group;
        mode=CHANNELS;
        refresh();''',"match active channel category")
    s=replace_once(s,'''        if(list!=null)list.scrollToPosition(selection);''',
       '''        if(list!=null)list.scrollToPosition(selection);
        updateCategoryLogoPreviewV98();''',"refresh preview for highlighted category")
    s=replace_once(s,'''    private void refresh(){
        rows.clear();''',
       '''    private void updateCategoryLogoPreviewV98(){
        if(mode!=CATEGORIES||categoryLogoPreviewV98==null||
            selection<0||selection>=rows.size())return;
        String group=rows.get(selection).category;
        if(group==null)return;
        ArrayList<Channel> matching=new ArrayList<>();
        for(Channel c:store.channels()){
            if(!"LIVE".equals(c.kind)||
                !c.sourceId.equals(current.sourceId))continue;
            if(!"Sve kategorije".equals(group)&&!group.equals(c.group))continue;
            matching.add(c);
            if(matching.size()>=80)break; // Bounded on large playlists.
        }
        categoryLogoPreviewV98.setAdapter(new LogoOnlyAdapter(matching));
    }

    private void refresh(){
        categoryLogoPreviewV98=null;
        rows.clear();''',"category-specific logos")
    s=replace_once(s,
       '''        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));''',
       '''        if(mode==CATEGORIES){
            LinearLayout splitV98=Ui.horizontal(ctx);
            splitV98.addView(list,new LinearLayout.LayoutParams(0,-1,1));
            categoryLogoPreviewV98=new RecyclerView(ctx);
            categoryLogoPreviewV98.setLayoutManager(
                new androidx.recyclerview.widget.GridLayoutManager(ctx,2));
            categoryLogoPreviewV98.setItemAnimator(null);
            categoryLogoPreviewV98.setOverScrollMode(View.OVER_SCROLL_NEVER);
            categoryLogoPreviewV98.setVerticalScrollBarEnabled(false);
            LinearLayout.LayoutParams logosV98=Ui.lp(ctx,124,-1);
            logosV98.leftMargin=Ui.dp(ctx,8);
            splitV98.addView(categoryLogoPreviewV98,logosV98);
            body.addView(splitV98,new LinearLayout.LayoutParams(-1,0,1));
            updateCategoryLogoPreviewV98();
        }else{
            body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        }''',
        "live synchronized logo preview in Categories")
    return s
edit("playback/TvSidePanel.java",side)

gradle=Path("app/build.gradle")
s=gradle.read_text()
assert "versionCode 907" in s and "versionName '0.9.7'" in s
gradle.write_text(s.replace("versionCode 907","versionCode 908",1)
                   .replace("versionName '0.9.7'","versionName '0.9.8'",1))
print("PASS: v0.9.8 safe toolbar, film channels, live return state, adult visibility, category-linked logos")
