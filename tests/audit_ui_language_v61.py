from pathlib import Path
import re
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
terms=re.compile(r'\b(?:Uživo|Filmovi|Serije|Početna|Kategorije|Dodaj|Sačuvaj|Osvježi|Učitaj|Potvrdi|Odustani|Uredi|Pretraga|Moje liste|Postavke|Gledaj|sadržaja|Nastavi|Prikaz|TV vodič|Dijagnostika|račun|greška|korisničko|Lozinka|Prikaz|nastavi|skraćeno|epizoda|kanala|datum|nema|nije|kako|lista|važi|Ukloni)\b',re.I)
print("=== REMAINING BOSNIAN-LIKE USER INTERFACE LINES (audit only) ===")
count=0
for i,line in enumerate(s.splitlines(),1):
    if not terms.search(line):continue
    if not ('Ui.text(' in line or 'Ui.button(' in line or '.setTitle(' in line or '.setMessage(' in line or '.setHint(' in line or 'TextView ' in line or 'addSetting(' in line):continue
    if count>=130:break
    print(str(i)+": "+line.strip()[:185])
    count+=1
print("TOTAL SHOWN:",count)
