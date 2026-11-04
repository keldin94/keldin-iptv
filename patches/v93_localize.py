from pathlib import Path
loc=Path("app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java")
s=loc.read_text()
anchor='''        put("Connection failed","Povezivanje nije uspjelo","Povezava ni uspela","Verbindung fehlgeschlagen");'''
assert anchor in s
new='''        put("Manage / Hide","Upravljaj / Sakrij","Upravljaj / Skrij","Verwalten / Ausblenden");
        put("Choose categories to display","Izaberi vidljive kategorije","Izberi vidne kategorije","Sichtbare Kategorien wählen");
        put("No categories found.","Nema kategorija.","Ni kategorij.","Keine Kategorien gefunden.");
        put("Save","Sačuvaj","Shrani","Speichern");
        put("Show all","Prikaži sve","Prikaži vse","Alle anzeigen");
        put("Open seasons & episodes","Otvori sezone i epizode","Odpri sezone in epizode","Staffeln und Folgen öffnen");
        put("Hide series","Sakrij seriju","Skrij serijo","Serie ausblenden");
        put("Hide this title","Sakrij ovaj naslov","Skrij ta naslov","Diesen Titel ausblenden");
        put("Category","Kategorija","Kategorija","Kategorie");
        put("Hide adult content","Sakrij erotski sadržaj","Skrij vsebino za odrasle","Erwachseneninhalte ausblenden");
        put("Always filter explicit titles and categories in live TV, movies and series. On is the default. This setting is saved between updates.",
            "Uvijek sakrij erotske naslove i kategorije u TV-u, filmovima i serijama. Zadano je uključeno i ostaje sačuvano.",
            "Vedno skrij naslove in kategorije za odrasle pri TV, filmih in serijah. Privzeto je vklopljeno.",
            "Explizite Titel und Kategorien aus TV, Filmen und Serien ausblenden. Standardmäßig aktiv.");
        put("Manage movie categories","Upravljaj kategorijama filmova","Upravljaj kategorije filmov","Filmkategorien verwalten");
        put("Manage series categories","Upravljaj kategorijama serija","Upravljaj kategorije serij","Serienkategorien verwalten");
        put("Choose precisely which movie groups appear. Hidden groups remain in your source playlist and can be restored.",
            "Izaberi koje kategorije filmova želiš vidjeti. Skrivene grupe ostaju u listi i možeš ih vratiti.",
            "Izberi kategorije filmov. Skrite skupine ostanejo v seznamu in jih lahko obnoviš.",
            "Filmkategorien auswählen. Ausgeblendete Gruppen bleiben in der Playlist und können wiederhergestellt werden.");
        put("Choose precisely which series groups appear. Hidden groups can be re-enabled without downloading the playlist.",
            "Izaberi kategorije serija. Skrivene grupe možeš ponovo uključiti bez preuzimanja liste.",
            "Izberi kategorije serij. Skrite skupine lahko obnoviš brez ponovnega prenosa.",
            "Serienkategorien auswählen und später ohne erneuten Download wieder anzeigen.");
        put("Restore hidden movies and series","Vrati skrivene filmove i serije","Obnovi skrite filme in serije","Ausgeblendete Filme und Serien wiederherstellen");
        put("Reset hidden titles","Vrati skrivene naslove","Obnovi skrite naslove","Ausgeblendete Titel wiederherstellen");
        put("Restore individual movies and series you previously hid. Category exclusions are managed separately.",
            "Vrati pojedinačne filmove i serije koje si sakrio. Filter kategorija ostaje odvojen.",
            "Obnovi posamezne skrite filme in serije. Filtri kategorij ostanejo ločeni.",
            "Einzeln ausgeblendete Filme und Serien wiederherstellen. Kategorien bleiben separat gefiltert.");
'''
s=s.replace(anchor,anchor+"\n"+new,1)
loc.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
def repl(before,after,name):
 global s
 assert before in s, "v0.9.3 localization marker missing "+name
 s=s.replace(before,after,1)
repl('''"  ·  Manage / Hide"''',
''' "  ·  "+UiLocaleV9.translate(this,"Manage / Hide")''',"category shortcut")
repl('''            message("No categories found.");return;''',
'''            message(UiLocaleV9.translate(this,"No categories found."));return;''',"empty categories")
repl('''            .setTitle("Choose categories to display")''',
'''            .setTitle(UiLocaleV9.translate(this,"Choose categories to display"))''',"category manager title")
repl('''            .setPositiveButton("Save",(dialog,button)->{''',
'''            .setPositiveButton(UiLocaleV9.translate(this,"Save"),(dialog,button)->{''',"save category filter")
repl('''            .setNeutralButton("Show all",(dialog,button)->{''',
'''            .setNeutralButton(UiLocaleV9.translate(this,"Show all"),(dialog,button)->{''',"restore categories")
repl('''            String[] choices={"Open seasons & episodes","Hide series","Cancel"};''',
'''            String[] choices={
                UiLocaleV9.translate(this,"Open seasons & episodes"),
                UiLocaleV9.translate(this,"Hide series"),tr("cancel")};''',"series menu")
repl('''        String[] actions={tr("play"),tr("favorites"),"Hide this title",tr("cancel")};''',
'''        String[] actions={tr("play"),tr("favorites"),
            UiLocaleV9.translate(this,"Hide this title"),tr("cancel")};''',"film menu")
repl('''        String message="Category: "+media.group+''',
'''        String message=UiLocaleV9.translate(this,"Category")+": "+media.group+''',"media category")
p.write_text(s)
print("v0.9.3: English-default and Bosnian/Slovenian/German localized media filtering controls")
