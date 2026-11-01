from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java")
s=p.read_text()
marker='''    public void start(){'''
assert marker in s
s=s.replace(marker,'''    private String msg(String english,String bosnian){
        return "bs".equals(store.language())?bosnian:english;
    }
'''+marker,1)
replacements=[
("1/3 · Povezivanje sa serverom","1/3 · Connecting to server"),
("Provjeravam adresu i dostupnost liste...","Checking playlist URL and server..."),
("2/3 · Preuzimanje i analiza","2/3 · Downloading and parsing"),
("Brojim kanale i prepoznajem kategorije...","Discovering content and categories..."),
("Preuzeto: %.1f MB   ·   Prepoznato: %,d stavki","Downloaded: %.1f MB   ·   Items found: %,d"),
("Nema podržanih kanala. Provjeri M3U adresu.","No compatible streams found. Check your M3U URL."),
("KELDIN IPTV · Uvoz liste","KELDIN IPTV · Import"),
("Priprema...","Preparing..."),
("TV uživo","Live TV"),
("Filmovi","Movies"),
("Serije","Series"),
("3/3 · Odaberi šta želiš učitati","3/3 · Choose content to keep"),
("Isključi države i kategorije koje ne gledaš. ","Uncheck countries and categories you do not watch. "),
("Neizabrani sadržaj neće biti upisan u lokalnu biblioteku. ","Excluded items will not be saved in the local library. "),
("Izbor možeš naknadno promijeniti u postavkama.","You can change this later in playlist settings."),
("Odustani","Cancel"),
("Uvoz otkazan.","Import cancelled."),
("Sačuvaj odabrano","Save selected"),
("3/3 · Spremanje odabranog sadržaja","3/3 · Saving selected content"),
("Optimiziram lokalnu biblioteku...","Optimizing your local library..."),
("Nema odabranih stavki.","No content selected."),
("Učitano: ","Imported: "),
(" · Filmovi "," · Movies "),
(" · Serije "," · Series "),
(" · Radio "," · Radio "),
("Neuspješno spremanje","Unable to save the library"),
("Lista je spremna","Playlist is ready"),
("Uvoz nije završen","Import failed"),
("U redu","OK")
]
for a,b in replacements:s=s.replace(a,b)
# Preserve Bosnian when selected at least for major steps and names.
s=s.replace('''setPhase("1/3 · Connecting to server","Checking playlist URL and server...");''',
'''setPhase(msg("1/3 · Connecting to server","1/3 · Povezivanje"),
            msg("Checking playlist URL and server...","Provjeravam server i adresu liste..."));''')
s=s.replace('''setPhase("2/3 · Downloading and parsing","Discovering content and categories...");''',
'''setPhase(msg("2/3 · Downloading and parsing","2/3 · Preuzimanje i analiza"),
            msg("Discovering content and categories...","Prepoznajem sadržaj i kategorije..."));''')
s=s.replace('''setPhase("3/3 · Saving selected content","Optimizing your local library...");''',
'''setPhase(msg("3/3 · Saving selected content","3/3 · Spremanje"),
            msg("Optimizing your local library...","Optimizacija biblioteke..."));''')
s=s.replace('''String[] kindLabels={"Live TV","Movies","Series","Radio"};''',
'''String[] kindLabels={"Live TV","Movies","Series","Radio"};
        if("bs".equals(store.language()))
            kindLabels=new String[]{"TV uživo","Filmovi","Serije","Radio"};''')
p.write_text(s)

# Avoid exporting default buffer 0 or opacity 0 when preferences are unset.
p=Path("app/src/main/java/com/keldin/iptv/ui/SettingsBackupV6.java")
s=p.read_text()
s=s.replace('''for(String k:INTS)o.put(k,p.getInt(k,0));''',
'''for(String k:INTS){
            int defaultValue="buffer".equals(k)?3:
                "font_scale".equals(k)?1:"panel_opacity".equals(k)?84:0;
            o.put(k,p.getInt(k,defaultValue));
        }''',1)
p.write_text(s)
print("English-first import wizard, Bosnian major stages and sensible backup defaults")
