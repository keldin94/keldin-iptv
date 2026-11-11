from pathlib import Path
ROOT=Path("app/src/main/java/com/keldin/iptv")
def edit(rel,fn):
    p=ROOT/rel
    old=p.read_text()
    new=fn(old)
    if old==new:raise AssertionError("v913 unchanged "+rel)
    p.write_text(new)
def one(s,old,new,label):
    if old not in s:raise AssertionError("v913 missing "+label+" | "+old[:120])
    return s.replace(old,new,1)

def activity(s):
    # A playback -> application Settings intent is consumed by onNewIntent().
    # v0.9.8's deferred onResume callback mistakenly interpreted the old
    # return_live_pending flag as a request to navigate back to Live TV.
    # This can create a full 350k-channel browse screen over Settings.
    s=one(s,
        '''    private void navigate(String destination) {
        navigationGenerationV911++;
        page=destination;searchQuery="";''',
        '''    private void navigate(String destination) {
        navigationGenerationV911++;
        if("Postavke".equals(destination)||"Početna".equals(destination)){
            getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
                .putBoolean("return_live_pending_v98",false)
                .putBoolean("return_live_focus_v98",false).apply();
        }
        page=destination;searchQuery="";''',
        "explicit Home and Settings navigation consumes stale player return")

    s=one(s,
        '''            if(store==null || isFinishing() || isDestroyed())return;''',
        '''            if(store==null || isFinishing() || isDestroyed())return;
            if("Postavke".equals(page))return;''',
        "never override Settings via stale player return")
    # A delayed return from playback must also not override a Home selection.
    # navigate() already increments navigationGenerationV911 and clears the flag.

    # Remove the two full adapter detachments from an active RecyclerView
    # focus/key callback. Detach can throw while a layout is being computed.
    # The content view and all Activity references are cleared on render.
    s=one(s,
        '''        if(activeGridV911!=null){
            activeGridV911.setAdapter(null);
            activeGridV911=null;
        }
        if(activeCategoryListV911!=null){
            activeCategoryListV911.setAdapter(null);
            activeCategoryListV911=null;
        }''',
        '''        // Do not mutate RecyclerView adapters during a D-pad Back event:
        // it can still be computing layout, causing IllegalStateException.
        // The surrounding content is removed by render(), releasing the
        // detached view hierarchy without a costly synchronous adapter reset.
        activeGridV911=null;
        activeCategoryListV911=null;''',
        "remove re-entrant adapter mutation on Back")
    return s
edit("ui/MainActivity.java",activity)

def player(s):
    # Explicitly distinguish leaving the player via Back from opening the
    # main application's Settings screen, or backgrounding Android TV.
    s=one(s,'''    private void openAppSettingsV96(){
        handler.removeCallbacks(hideControls);''',
      '''    private boolean openingAppSettingsV913=false;
    private void openAppSettingsV96(){
        openingAppSettingsV913=true;
        // Settings is a destination, not a last-channel return request.
        getSharedPreferences("keldin_settings",MODE_PRIVATE).edit()
            .putBoolean("return_live_pending_v98",false)
            .putBoolean("return_live_focus_v98",false).apply();
        handler.removeCallbacks(hideControls);''',
      "mark Settings navigation before leaving player")
    s=one(s,
      '''    @Override protected void onPause(){
        rememberLiveReturnV98();
        super.onPause();
    }''',
      '''    @Override protected void onPause(){
        // Remember only when Back is actually finishing this player.
        // A HOME/Settings/app switch must never relaunch Live TV.
        if(!openingAppSettingsV913&&isFinishing())
            rememberLiveReturnV98();
        super.onPause();
    }
    @Override protected void onResume(){
        openingAppSettingsV913=false;
        super.onResume();
    }''',
      "prevent stale return flags after Settings or Android background")
    return s
edit("playback/PlayerActivity.java",player)

def panel(s):
    # Drop the expensive second RecyclerView with a 2-column logo grid.
    # Left once: one column of channels. Left twice: one column of categories.
    start=s.index('''        if(mode==CATEGORIES){
            LinearLayout splitV98=Ui.horizontal(ctx);''')
    end=s.index('''        if(selection>0)list.scrollToPosition(selection);''',start)
    block=s[start:end]
    if 'categoryLogoPreviewV98' not in block or 'GridLayoutManager(ctx,2)' not in block:
        raise AssertionError("two-column logo preview not found")
    s=s[:start]+'''        // A single, efficient column for either channels or categories.
        // No secondary RecyclerView, bitmap/logo requests or extra scrolling.
        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
'''+s[end:]
    # Prevent rebuilding the now-removed preview whenever focus changes.
    s=one(s,'''        if(list!=null)list.scrollToPosition(selection);
        updateCategoryLogoPreviewV98();''',
        '''        if(list!=null)list.scrollToPosition(selection);''',
        "no logo preview on D-pad selection")
    a=s.index('''    private void updateCategoryLogoPreviewV98(){''')
    b=s.index('''    private void refresh(){''',a)
    s=s[:a]+s[b:]
    # Delete stale preview refs, ensure category list keeps full width.
    s=s.replace('''    private RecyclerView categoryLogoPreviewV98;
''','',1)
    s=s.replace('''        categoryLogoPreviewV98=null;previewGroupV910="";
''','',1)
    s=s.replace('''        previewGroupV910="";
        categoryLogoPreviewV98=null;
''','',1)
    # Avoid retaining a stale RecyclerView when moving between categories.
    s=one(s,
        '''        if(panel!=null)host.removeView(panel);
        panel=new FrameLayout(ctx);''',
        '''        if(panel!=null){
            // Disconnect the old list before replacing the overlay; the old
            // RecyclerView may still hold dozens of logo-bearing view holders.
            if(list!=null&&!list.isComputingLayout())list.setAdapter(null);
            host.removeView(panel);
        }
        panel=new FrameLayout(ctx);''',
        "release old side panel list without mutating during layout")
    # Match narrower Apple-like overlay rather than a near-half-screen panel.
    import re
    match=re.search(r'        int panelWidth=[^\n]+;',s)
    if not match:raise AssertionError("panelWidth declaration not found")
    s=s[:match.start()]+'''        int panelWidth=mode==GUIDE
            ?Math.min((int)(screenWidth*.35f),Ui.dp(ctx,500))
            :Math.min((int)(screenWidth*.30f),Ui.dp(ctx,440));'''+s[match.end():]
    return s
edit("playback/TvSidePanel.java",panel)

p=Path("app/build.gradle")
v=p.read_text()
assert "versionCode 912" in v and "versionName '0.9.12'" in v
p.write_text(v.replace("versionCode 912","versionCode 913",1)
              .replace("versionName '0.9.12'","versionName '0.9.13'",1))
print("PASS v0.9.13: fix Settings return/navigation, D-pad Back recycling crash, one-column side panel")
