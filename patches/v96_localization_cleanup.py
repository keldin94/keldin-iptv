from pathlib import Path
import re

root=Path("app/src/main/java/com/keldin/iptv/")
def replace(path,old,new,label):
    p=root/path
    text=p.read_text()
    assert old in text, "v0.9.6 missing "+label+" in "+str(p)
    p.write_text(text.replace(old,new,1))

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

print("PASS: v0.9.6 localized fixed UI labels, toolbar date and authored player dialogs")
