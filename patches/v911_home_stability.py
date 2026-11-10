from pathlib import Path
import re

BASE=Path("app/src/main/java/com/keldin/iptv")
def edit(relative,fn):
    p=BASE/relative
    before=p.read_text()
    after=fn(before)
    if before==after:raise AssertionError("v0.9.11 no change: "+relative)
    p.write_text(after)
def once(s,old,new,label):
    if old not in s:raise AssertionError("v0.9.11 missing "+label)
    return s.replace(old,new,1)

def main(s):
    anchor='''    private String selectedSourceV99="";'''
    fields='''    // The browse screen can hold 150k+ references through its adapters.
    // Detach them explicitly before building the lightweight Home dashboard.
    private RecyclerView activeGridV911;
    private RecyclerView activeCategoryListV911;
    private long navigationGenerationV911=0;

    private void releaseHeavyBrowseV911(){
        if(activeGridV911!=null){
            activeGridV911.setAdapter(null);
            activeGridV911=null;
        }
        if(activeCategoryListV911!=null){
            activeCategoryListV911.setAdapter(null);
            activeCategoryListV911=null;
        }
        browseCategoriesV93=null;
        browseGridV93=null;
    }
'''
    s=once(s,anchor,anchor+"\n"+fields,"explicit browse lifetime tracking")
    s=once(s,'''    private void navigate(String destination) {
        page=destination;searchQuery="";''',
    '''    private void navigate(String destination) {
        navigationGenerationV911++;
        page=destination;searchQuery="";''',"discard stale posted player return on navigation")
    s=once(s,'''    private void render() {
        if(content==null)return;
        content.removeAllViews();''',
    '''    private void render() {
        if(content==null)return;
        if("Početna".equals(page)){
            releaseHeavyBrowseV911();
            store.clearLiveIndexV911();
        }
        content.removeAllViews();''',"free channel adapters before Home rebuild")
    s=once(s,'''    @Override protected void onResume() {
        getWindow().getDecorView().post(()->{''',
    '''    @Override protected void onResume() {
        final long expectedNavigationV911=navigationGenerationV911;
        getWindow().getDecorView().post(()->{
            // If Home was opened while the callback was pending, do not
            // force a second full Live browse render on top of Home.
            if(expectedNavigationV911!=navigationGenerationV911)return;''',
    "prevent delayed playback return rendering over Home")
    s=once(s,'''        if(store!=null && content!=null && ("Početna".equals(page)||"Favoriti".equals(page)))render();''',
    '''        // Home has no changing content that needs a second onResume render.
        if(store!=null && content!=null && "Favoriti".equals(page))render();''',
    "avoid redundant Home render on every activity resume")
    begin=s.index("    private void showChannelGrid(boolean guideMode) {")
    end=s.index("    private ArrayList<Channel> filterSection(",begin)
    part=s[begin:end]
    part=once(part,
    '''        categories.setAdapter(listAdapter);''',
    '''        categories.setAdapter(listAdapter);
        activeCategoryListV911=categories;
        activeGridV911=grid;''',"track both browse RecyclerViews")
    s=s[:begin]+part+s[end:]
    return s
edit("ui/MainActivity.java",main)

def store(s):
    needle='''    private boolean liveIndexReadyV910=false;'''
    additional='''    private boolean liveIndexReadyV910=false;
    public synchronized void clearLiveIndexV911(){
        liveIndexV910.clear();
        liveIndexReadyV910=false;
    }'''
    return once(s,needle,additional,"release live-channel cache on Home")
edit("data/CatalogStore.java",store)

def logo(s):
    # Reduce retained bitmaps on low-memory TV boxes; keep logo loading lazy.
    return once(s,'''new LruCache<String,Bitmap>(12*1024)''',
                '''new LruCache<String,Bitmap>(6*1024)''',
                "reduce persistent artwork memory")
edit("ui/LogoLoader.java",logo)

gradle=Path("app/build.gradle")
s=gradle.read_text()
assert "versionCode 910" in s and "versionName '0.9.10'" in s
gradle.write_text(s.replace("versionCode 910","versionCode 911",1)
                   .replace("versionName '0.9.10'","versionName '0.9.11'",1))
print("PASS v0.9.11: Home detaches heavy grids, clears live cache, single resume render, skips stale callbacks; in-place update")
