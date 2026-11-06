from pathlib import Path
import re

root=Path("app/src/main/java/com/keldin/iptv/")
def replace(path,old,new,label):
    p=root/path
    text=p.read_text()
    assert old in text, "v0.9.6 missing "+label+" in "+str(p)
    p.write_text(text.replace(old,new,1))

# The top shortcut is visible from Live TV, Movies, Series, Search and every other page.
replace("ui/MainActivity.java",
'''        toolbar.addView(search,sp);
        // Playlist administration lives in Settings -> Playlists.''',
'''        toolbar.addView(search,sp);
        TextView settingsShortcutV96=Ui.button(this,"⚙",
            ()->navigate("Postavke"),false);
        settingsShortcutV96.setContentDescription(tr("settings"));
        LinearLayout.LayoutParams settingsShortcutLp=Ui.lp(this,46,42);
        settingsShortcutLp.leftMargin=Ui.dp(this,9);
        toolbar.addView(settingsShortcutV96,settingsShortcutLp);
        // Playlist administration lives in Settings -> Playlists.''',
"top Settings button")

# Add a single target page argument; never clear/recreate playlists, settings or user data.
replace("ui/MainActivity.java",
'''                    createShell();
                    render();''',
'''                    createShell();
                    boolean openSettingsV96=getIntent()!=null &&
                        getIntent().getBooleanExtra("keldin_open_settings_v96",false);
                    if(openSettingsV96){
                        getIntent().removeExtra("keldin_open_settings_v96");
                        navigate("Postavke");
                    }else render();''',
"handle launch from player")
replace("ui/MainActivity.java",
'''                    if(store.channels().isEmpty()&&!store.sources().isEmpty()){''',
'''                    if(!openSettingsV96 && store.channels().isEmpty()&&!store.sources().isEmpty()){''',
"do not auto-open playlists when entering Settings")
replace("ui/MainActivity.java",
'''if(store.channels().isEmpty()&&!store.sources().isEmpty()){''',
'''if(!openSettingsV96 && store.channels().isEmpty()&&!store.sources().isEmpty()){''',
"skip missing-catalog redirect for Settings")
replace("ui/MainActivity.java",
'''                    }else if(savedInstanceState==null&&store.openLastChannelAtStart()){''',
'''                    }else if(!openSettingsV96&&savedInstanceState==null&&store.openLastChannelAtStart()){''',
"prevent auto-play when opening Settings")
replace("ui/MainActivity.java",
'''    private void createShell() {''',
'''    @Override protected void onNewIntent(android.content.Intent incoming){
        super.onNewIntent(incoming);
        setIntent(incoming);
        if(incoming!=null &&
            incoming.getBooleanExtra("keldin_open_settings_v96",false) &&
            store!=null){
            incoming.removeExtra("keldin_open_settings_v96");
            navigate("Postavke");
        }
    }
    private void createShell() {''',
"handle existing MainActivity Settings navigation")

# Eliminate stale Bosnian-only interface strings on all pages.
replace("ui/MainActivity.java",
'''TextView section=Ui.text(this,"BIBLIOTEKA",10,Ui.MUTED,true);''',
'''TextView section=Ui.text(this,UiLocaleV9.translate(this,"LIBRARY").toUpperCase(
            java.util.Locale.forLanguageTag(store.language())),10,Ui.MUTED,true);''',
"library heading")
replace("ui/MainActivity.java",
'''TextView version=Ui.text(this,"v0.4  •  Sve otključano",10,Ui.MUTED,false);''',
'''TextView version=Ui.text(this,"v"+com.keldin.iptv.BuildConfig.VERSION_NAME,
            10,Ui.MUTED,false);''',
"stale version and untranslated subtitle")
replace("ui/MainActivity.java",
'''new SimpleDateFormat("EEE, d MMM",Locale.getDefault())''',
'''new SimpleDateFormat("EEE, d MMM",
            java.util.Locale.forLanguageTag(store.language()))''',
"date uses selected language")

# Playback Settings opens Settings in the existing main app and ends playback
# normally, avoiding a second player or duplicate MainActivity instances.
replace("playback/PlayerActivity.java",
'''    private void showOptions() {''',
'''    private void openAppSettingsV96(){
        handler.removeCallbacks(hideControls);
        android.content.Intent intent=new android.content.Intent(
            this,com.keldin.iptv.ui.MainActivity.class);
        intent.putExtra("keldin_open_settings_v96",true);
        intent.addFlags(android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP |
            android.content.Intent.FLAG_ACTIVITY_SINGLE_TOP);
        startActivity(intent);
    }

    private void showOptions() {''',
"Settings from player options")
replace("playback/PlayerActivity.java",
'''            "Probe HLS / TS server"};''',
'''            "Probe HLS / TS server",tr("settings")};''',
"thirteenth player option")
replace("playback/PlayerActivity.java",
'''                    case 11:diagnoseServer();break;''',
'''                    case 11:diagnoseServer();break;
                    case 12:openAppSettingsV96();break;''',
"Settings player menu action")

# Playback option sheet gets a fourth grouped 'APPLICATION' category.
replace("playback/TvPlaybackOptionsV94.java",
'''        "↻","▣","↗","ⓘ","♡","⊞","♫","CC","Ⅱ","❮","❯","⌕"''',
'''        "↻","▣","↗","ⓘ","♡","⊞","♫","CC","Ⅱ","❮","❯","⌕","⚙"''',
"Settings icon")
for which,label in [
    ("EN","Open application settings"),
    ("BS","Otvori postavke aplikacije"),
    ("SL","Odpri nastavitve aplikacije"),
    ("DE","App-Einstellungen öffnen")]:
    p=root/"playback/TvPlaybackOptionsV94.java"
    s=p.read_text()
    start=s.index("private static final String[] "+which+"={")
    end=s.index("};",start)
    block=s[start:end]
    anchor=block.rfind('"')
    assert anchor>0
    s=s[:start]+block[:anchor+1]+',\n        "'+label+'"'+s[end:]
    p.write_text(s)
replace("playback/TvPlaybackOptionsV94.java",
'''String[] en={"STREAM","PLAYBACK","CHANNEL"};''',
'''String[] en={"STREAM","PLAYBACK","CHANNEL","APPLICATION"};''',
"new option section English")
replace("playback/TvPlaybackOptionsV94.java",
'''String[] bs={"STREAM","REPRODUKCIJA","KANALI"};''',
'''String[] bs={"STREAM","REPRODUKCIJA","KANALI","APLIKACIJA"};''',
"new option section Bosnian")
replace("playback/TvPlaybackOptionsV94.java",
'''String[] sl={"PRENOS","PREDVAJANJE","KANALI"};''',
'''String[] sl={"PRENOS","PREDVAJANJE","KANALI","APLIKACIJA"};''',
"new option section Slovenian")
replace("playback/TvPlaybackOptionsV94.java",
'''String[] de={"STREAM","WIEDERGABE","SENDER"};''',
'''String[] de={"STREAM","WIEDERGABE","SENDER","ANWENDUNG"};''',
"new option section German")
replace("playback/TvPlaybackOptionsV94.java",
'''if(i==0||i==4||i==8){''',
'''if(i==0||i==4||i==8||i==12){''',
"fourth options section")

# Localize the exact user-facing dialog controls in the player and main
# without modifying server names, URLs, programme titles or any network data.
def translate_literal_dialogs(path,context):
    p=root/path
    s=p.read_text()
    s=re.sub(r'\.(setTitle|setMessage|setPositiveButton|setNegativeButton|setNeutralButton)\("([^"]+)"',
       lambda m:'.'+m.group(1)+'(com.keldin.iptv.ui.UiLocaleV9.translate('+context+',"'+m.group(2)+'")',s)
    p.write_text(s)

translate_literal_dialogs("playback/PlayerActivity.java","PlayerActivity.this")
translate_literal_dialogs("ui/MainActivity.java","MainActivity.this")

# Localize additional short, non-provider UI captions and error feedback.
p=root/"playback/PlayerActivity.java"
s=p.read_text()
substitutions={
 '"Provjeravam odgovor servera..."':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Checking server response...")',
 '"Provjera servera završena. OK → Opcije."':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Server check completed.")',
 '"Odgovor IPTV servera"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"IPTV server response")',
 '"Pokreni kao HLS"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Play as HLS")',
 '"Pokreni ponovo"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Play again")',
 '"Zatvori"':'com.keldin.iptv.ui.I18n.t(this,"close")',
 '"Automatski"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Automatic")',
 '"VLC identifikacija"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"VLC identification")',
 '"HLS + VLC identifikacija"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"HLS + VLC identification")',
 '"Stream nedostupan"':'com.keldin.iptv.ui.UiLocaleV9.translate(this,"Stream unavailable")'
}
for old,new in substitutions.items():
    # Only substitute unconverted forms; do not touch original IPTV data.
    if old in s:s=s.replace(old,new)
p.write_text(s)

# Expand the existing UI dictionary for screens and dialogs, keeping en default.
p=root/"ui/UiLocaleV9.java"
s=p.read_text()
needle='''        put("Accent color","Boja naglaska","Poudarjena barva","Akzentfarbe");'''
extra='''        put("LIBRARY","BIBLIOTEKA","KNJIŽNICA","BIBLIOTHEK");
        put("Application settings","Postavke aplikacije","Nastavitve aplikacije","App-Einstellungen");
        put("Settings","Postavke","Nastavitve","Einstellungen");
        put("Playback options","Opcije reprodukcije","Možnosti predvajanja","Wiedergabeoptionen");
        put("Close","Zatvori","Zapri","Schließen");
        put("OK","U redu","V redu","OK");
        put("Cancel","Odustani","Prekliči","Abbrechen");
        put("Home","Početna","Domov","Startseite");
        put("Continue watching","Nastavi gledati","Nadaljuj ogled","Weitersehen");
        put("Exit","Izađi","Izhod","Beenden");
        put("Stream diagnostics","Dijagnostika streama","Diagnostika prenosa","Stream-Diagnose");
        put("Player mode","Način reprodukcije","Način predvajanja","Wiedergabemodus");
        put("Last error","Posljednja greška","Zadnja napaka","Letzter Fehler");
        put("Checking server response...","Provjeravam odgovor servera...","Preverjam odziv strežnika...","Prüfe Serverantwort...");
        put("Server check completed.","Provjera servera završena.","Preverjanje strežnika zaključeno.","Serverprüfung abgeschlossen.");
        put("IPTV server response","Odgovor IPTV servera","Odziv strežnika IPTV","IPTV-Serverantwort");
        put("Play as HLS","Pokreni kao HLS","Predvajaj kot HLS","Als HLS abspielen");
        put("Play again","Pokreni ponovo","Predvajaj znova","Erneut abspielen");
        put("Automatic","Automatski","Samodejno","Automatisch");
        put("VLC identification","VLC identifikacija","Identifikacija VLC","VLC-Kennung");
        put("HLS + VLC identification","HLS + VLC identifikacija","Identifikacija HLS + VLC","HLS- + VLC-Kennung");
        put("Stream unavailable","Stream nedostupan","Prenos ni na voljo","Stream nicht verfügbar");
        put("Open in external player","Otvori u vanjskom playeru","Odpri v zunanjem predvajalniku","In externem Player öffnen");
        put("No channels in this category","Nema kanala u ovoj kategoriji","V tej kategoriji ni kanalov","Keine Sender in dieser Kategorie");
        put("Playback buffer","Buffer reprodukcije","Medpomnilnik predvajanja","Wiedergabepuffer");
        put("Buffer stall recovery","Oporavak buffera","Obnovitev po zastoju","Pufferwiederherstellung");
        put("Show all","Prikaži sve","Prikaži vse","Alle anzeigen");
        put("Save","Sačuvaj","Shrani","Speichern");
        put("Restore","Vrati","Obnovi","Wiederherstellen");
        put("Edit","Uredi","Uredi","Bearbeiten");
        put("Remove","Ukloni","Odstrani","Entfernen");
        put("Search","Pretraga","Iskanje","Suche");
'''
assert needle in s
p.write_text(s.replace(needle,extra+needle,1))

# v0.9.6 remains a signed in-place update, not a new app.
p=Path("app/build.gradle");s=p.read_text()
assert "versionCode 905" in s and "versionName '0.9.5'" in s
p.write_text(s.replace("versionCode 905","versionCode 906",1).replace("versionName '0.9.5'","versionName '0.9.6'",1))
print("v0.9.6 prepared: global Settings shortcut, player dialog Settings, localized UI entry points, persistent package")
