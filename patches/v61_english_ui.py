from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
anchor='''    private String tr(String key){return I18n.t(this,key);}'''
assert anchor in s, "translation helper missing"
s=s.replace(anchor, anchor+'''
    private String localized(String english,String bosnian){
        return store!=null && "bs".equals(store.language())?bosnian:english;
    }''',1)

subs=[
('Ui.button(this,"+  Dodaj M3U listu",',
 'Ui.button(this,localized("＋  Add M3U playlist","+  Dodaj M3U listu"),'),
('Ui.text(this,"Bez ugrađenih TV kanala. Aplikacija reprodukuje liste koje sam dodaš.",',
 'Ui.text(this,localized("No built-in channels. Add your own playlist to start watching.","Bez ugrađenih TV kanala. Aplikacija reprodukuje liste koje sam dodaš."),'),
('field.setHint("Pretraži kanale, filmove i serije...");',
 'field.setHint(localized("Search channels, movies and series...","Pretraži kanale, filmove i serije..."));'),
('src.lastUpdated==0?"Nije ažurirano":',
 'src.lastUpdated==0?localized("Not updated","Nije ažurirano"):'),
('addSetting(body,"Automatsko pamćenje kanala",store.rememberLast()?"Uključeno":"Isključeno"',
 'addSetting(body,localized("Remember last channel","Automatsko pamćenje kanala"),store.rememberLast()?localized("On","Uključeno"):localized("Off","Isključeno")'),
('addSetting(body,"Dijagnostika zatvaranja",',
 'addSetting(body,localized("Crash diagnostics","Dijagnostika zatvaranja"),'),
('setTitle("Dijagnostika")',
 'setTitle(localized("Diagnostics","Dijagnostika"))'),
('setTitle(existing==null?"Dodaj " + (xtream?"Xtream nalog":"M3U listu"):"Uredi listu")',
 'setTitle(existing==null?localized("Add ","Dodaj ") + (xtream?localized("Xtream account","Xtream nalog"):localized("M3U playlist","M3U listu")):localized("Edit playlist","Uredi listu"))'),
('setTitle("Ukloni listu?").setMessage(src.name+" i njeni kanali bit će uklonjeni s uređaja.")',
 'setTitle(localized("Remove playlist?","Ukloni listu?")).setMessage(src.name+localized(" and its channels will be removed from this device."," i njeni kanali bit će uklonjeni s uređaja."))'),
]
for old,new in subs:
    if old not in s:
        print("WARNING missing:",old[:100])
    else:
        s=s.replace(old,new)
        print("Localized:",old[:57])

# Use English on default during remaining user-facing empty states.
extras=[
 ('"Nema aktivnih kanala."','localized("No active channels.","Nema aktivnih kanala.")'),
 ('"Nema sadržaja"','localized("No content","Nema sadržaja")'),
 ('"Svi kanali"','localized("All channels","Svi kanali")'),
 ('"Svi filmovi"','localized("All movies","Svi filmovi")'),
 ('"Sve serije"','localized("All series","Sve serije")'),
 ('"Lista nije ažurirana"','localized("Playlist is not updated","Lista nije ažurirana")')
]
for old,new in extras:
    if old in s:s=s.replace(old,new)
p.write_text(s)
print("Completed language hotfix on MainActivity")
