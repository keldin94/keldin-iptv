from pathlib import Path
import re

ROOT=Path("app/src/main/java/com/keldin/iptv")
def edit(path,fn):
    p=ROOT/path
    old=p.read_text()
    new=fn(old)
    if old==new:raise AssertionError("v914 no change "+path)
    p.write_text(new)
def one(s,old,new,label):
    if old not in s:raise AssertionError("v914 missing "+label+" => "+old[:150])
    return s.replace(old,new,1)

def main(s):
    # One shared library/player. Rebuild only the lightweight Home view for
    # the selected skin: never re-import M3U or invalidate channel caches.
    start=s.index("    private void showHome() {")
    end=s.index("    private void landingTile(",start)
    s=s[:start]+'''    private void showHome() {
        ThemeV914.showHome(this,content,store,
            destination->navigate(destination),()->editSource(null,"M3U"));
    }

'''+s[end:]

    start=s.index("    private void showSettingsV6(){")
    end=s.index("    private void headingV6(",start)
    settings=s[start:end]
    anchor='''        if(selectedSettingsTab==5){'''
    gallery='''        if(selectedSettingsTab==4){
            headingV6(body,"INTERFACE THEMES");
            addOptionV6(body,"Theme gallery",ThemeV914.label(this),
                "Five distinct layouts: KELDIN Classic, Cinema, TV Guide, Glass and Compact. "+
                "Changes the home, categories and player without reloading playlists.",
                ()->ThemeV914.showGallery(this,()->{
                    createShell();
                    render();
                }));
        }
'''
    settings=one(settings,anchor,gallery+anchor,"Appearance theme picker before Updates section")
    s=s[:start]+settings+s[end:]

    start=s.index("    private void showChannelGrid(boolean guideMode) {")
    end=s.index("    private ArrayList<Channel> filterSection(",start)
    browser=s[start:end]
    browser=one(browser,
        '''        LinearLayout main=Ui.horizontal(this);''',
        '''        int skinV914=ThemeV914.current(this);
        // Cinema uses a horizontal category ribbon above movies and series;
        // the other four themes use different source rails beside the grid.
        LinearLayout main=(skinV914==ThemeV914.CINEMA&&isPosters)
            ?Ui.vertical(this):Ui.horizontal(this);''',
        "theme-dependent media browser structure")
    browser=one(browser,
        '''        categoryBox.addView(categoryLabel);''',
        '''        ThemeV914.styleBrowse(this,categoryBox,categoryLabel,skinV914);
        categoryBox.addView(categoryLabel);''',
        "theme-dependent category rail styling")
    browser=one(browser,
        '''        categories.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));''',
        '''        categories.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(
            this,(skinV914==ThemeV914.CINEMA&&isPosters)
            ?androidx.recyclerview.widget.LinearLayoutManager.HORIZONTAL
            :androidx.recyclerview.widget.LinearLayoutManager.VERTICAL,false));''',
        "cinema horizontal category ribbon")
    browser=one(browser,
        '''        LinearLayout.LayoutParams rail=Ui.lp(this,215,-1);
        rail.rightMargin=Ui.dp(this,9);''',
        '''        LinearLayout.LayoutParams rail=(skinV914==ThemeV914.CINEMA&&isPosters)
            ?Ui.lp(this,-1,88)
            :Ui.lp(this,ThemeV914.railWidth(skinV914),-1);
        rail.rightMargin=Ui.dp(this,9);
        rail.bottomMargin=Ui.dp(this,skinV914==ThemeV914.CINEMA&&isPosters?7:0);''',
        "five category rail dimensions")
    browser=one(browser,
        '''        GridLayoutManager gridManager=new GridLayoutManager(this,4);''',
        '''        GridLayoutManager gridManager=new GridLayoutManager(
            this,ThemeV914.gridColumns(skinV914,isPosters));''',
        "five browse densities")
    browser=one(browser,
        '''        main.addView(browsing,new LinearLayout.LayoutParams(0,-1,1));''',
        '''        if(skinV914==ThemeV914.CINEMA&&isPosters)
            main.addView(browsing,new LinearLayout.LayoutParams(-1,0,1));
        else main.addView(browsing,new LinearLayout.LayoutParams(0,-1,1));''',
        "cinema ribbon layout weight")
    s=s[:start]+browser+s[end:]
    return s
edit("ui/MainActivity.java",main)

def group_adapter(s):
    # Horizontal mode must show multiple playlist/category entries, not one
    # MATCH_PARENT entry that fills the entire ribbon.
    return one(s,
    '''        RecyclerView.LayoutParams params=new RecyclerView.LayoutParams(
            -1,ViewGroup.LayoutParams.WRAP_CONTENT);''',
    '''        RecyclerView.LayoutManager manager=((RecyclerView)parent).getLayoutManager();
        boolean horizontal=manager instanceof androidx.recyclerview.widget.LinearLayoutManager
            &&((androidx.recyclerview.widget.LinearLayoutManager)manager).getOrientation()
              ==androidx.recyclerview.widget.RecyclerView.HORIZONTAL;
        RecyclerView.LayoutParams params=new RecyclerView.LayoutParams(
            horizontal?Ui.dp(context,200):-1,ViewGroup.LayoutParams.WRAP_CONTENT);''',
    "horizontal Cinema category cards")
edit("ui/PlaylistGroupAdapterV99.java",group_adapter)

def player(s):
    # Built-in, checksum-checked installer already exists. Link its public
    # entry point directly to the player three-dot menu.
    s=one(s,
    '''"Probe HLS / TS server",tr("settings")};''',
    '''"Probe HLS / TS server",tr("settings"),
            "Check for updates"};''',
    "update action in three-dot menu")
    s=one(s,
    '''                    case 12:openAppSettingsV96();break;''',
    '''                    case 12:openAppSettingsV96();break;
                    case 13:com.keldin.iptv.updates.AppUpdateManager.check(this,true);break;''',
    "direct signed updater action on player")

    marker=re.search(r'private\s+void\s+setControls\s*\(\s*boolean\s+visible\s*\)\s*\{',s)
    if not marker:raise AssertionError("player setControls(boolean) not found")
    addition='''
        // Skins affect player chrome only; never reinitialize ExoPlayer.
        if(visible&&overlay!=null)
            com.keldin.iptv.ui.ThemeV914.stylePlayer(this,overlay);'''
    s=s[:marker.end()]+addition+s[marker.end():]
    s=one(s,
    '''        buttons.setGravity(Gravity.CENTER_VERTICAL);''',
    '''        buttons.setGravity(Gravity.CENTER_VERTICAL);
        buttons.setClipChildren(false);
        buttons.setClipToPadding(false);''',
    "prevent mini-player action focus borders from being cropped")
    return s
edit("playback/PlayerActivity.java",player)

def options(s):
    # Existing action order groups 0..3 Stream, 4..7 Playback,
    # 8..11 Channel, 12..13 Application.
    s=one(s,'''        "↻","▣","↗","ⓘ","♡","⊞","♫","CC","Ⅱ","❮","❯","⌕","⚙"''',
        '''        "↻","▣","↗","ⓘ","♡","⊞","♫","CC","Ⅱ","❮","❯","⌕","⚙","⬇"''',
        "new update icon")
    for description in (
      '"Open application settings"',
      '"Otvori postavke aplikacije"',
      '"Odpri nastavitve aplikacije"',
      '"App-Einstellungen öffnen"'
    ):
        if description not in s:raise AssertionError("missing description: "+description)
    translations={
      '"Open application settings"':'"Open application settings",\n        "Check for a newer signed application version"',
      '"Otvori postavke aplikacije"':'"Otvori postavke aplikacije",\n        "Provjeri i instaliraj novu verziju aplikacije"',
      '"Odpri nastavitve aplikacije"':'"Odpri nastavitve aplikacije",\n        "Preveri in namesti novejšo različico aplikacije"',
      '"App-Einstellungen öffnen"':'"App-Einstellungen öffnen",\n        "Neue signierte App-Version suchen und installieren"'
    }
    for old,new in translations.items():s=one(s,old,new,"update action localized description")
    # Allow full icon and two lines of text in the options sheet.
    s=one(s,'''            item.setMinimumHeight(Ui.dp(activity,65));''',
        '''            item.setMinimumHeight(Ui.dp(activity,72));''',
        "avoid 2-line options clipping")
    return s
edit("playback/TvPlaybackOptionsV94.java",options)

p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 913" in g and "versionName '0.9.13'" in g
p.write_text(g.replace("versionCode 913","versionCode 914",1)
              .replace("versionName '0.9.13'","versionName '0.9.14'",1))
print("PASS v0.9.14: five distinct themes, gallery, browser layouts, player chrome, update action")
