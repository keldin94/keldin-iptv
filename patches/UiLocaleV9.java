package com.keldin.iptv.ui;

import android.content.Context;
import java.util.HashMap;
import java.util.Map;

/** Localizes authored UI labels. IPTV provider titles are intentionally unchanged. */
public final class UiLocaleV9 {
    private static final Map<String,String[]> TEXT=new HashMap<>();
    private UiLocaleV9(){}
    private static void put(String en,String bs,String sl,String de){
        String[] values={en,bs,sl,de};
        TEXT.put(en,values);
        TEXT.put(bs,values);
    }
    static {
        put("Accent color","Boja naglaska","Poudarjena barva","Akzentfarbe");
        put("Text size","Veličina teksta","Velikost besedila","Textgröße");
        put("Panel transparency","Prozirnost menija","Prosojnost menijev","Menütransparenz");
        put("Playback & startup","Reprodukcija i pokretanje","Predvajanje in zagon","Wiedergabe und Start");
        put("Home screen","Početni ekran","Začetni zaslon","Startbildschirm");
        put("Last live channel","Posljednji TV kanal","Zadnji TV-kanal","Letzter TV-Sender");
        put("Buffer","Međuspremnik","Medpomnilnik","Puffer");
        put("Automatic reconnect","Automatsko ponovno povezivanje","Samodejna ponovna povezava","Automatisch neu verbinden");
        put("Remember last channel","Zapamti posljednji kanal","Zapomni si zadnji kanal","Letzten Sender merken");
        put("Playlists and country filters","Liste i filteri država","Seznami in filtri držav","Playlists und Länderfilter");
        put("EPG time offset","Vremenski pomak EPG-a","Časovni zamik EPG","EPG-Zeitversatz");
        put("Parental PIN","Roditeljski PIN","Starševski PIN","Jugendschutz-PIN");
        put("Settings backup","Sigurnosna kopija postavki","Varnostna kopija nastavitev","Einstellungen sichern");
        put("Crash diagnostics","Dijagnostika grešaka","Diagnostika napak","Fehlerdiagnose");
        put("Check for updates","Provjeri ažuriranja","Preveri posodobitve","Nach Updates suchen");
        put("Automatic update checks","Automatska provjera ažuriranja","Samodejno preverjanje posodobitev","Automatische Updateprüfung");
        put("Overlay auto-hide","Automatsko skrivanje menija","Samodejno skrivanje menijev","Menüs automatisch ausblenden");
        put("Preferred audio language","Željeni jezik zvuka","Prednostni jezik zvoka","Bevorzugte Audiosprache");
        put("Playlist connection timeout","Vrijeme čekanja na server","Časovna omejitev povezave","Verbindungszeitlimit");
        put("Select the app language. English is the default; playlist titles are unchanged.",
            "Odaberi jezik aplikacije. Engleski je početni; nazivi iz liste ostaju isti.",
            "Izberi jezik aplikacije. Privzet je angleški; nazivi v seznamih se ne spreminjajo.",
            "App-Sprache wählen. Standard ist Englisch; Playlist-Titel bleiben unverändert.");
        put("Change only the selected-item and icon accent; the dark interface stays consistent.",
            "Promijeni boju odabranih stavki i ikona; tamna tema ostaje ista.",
            "Spremeni barvo izbranih elementov in ikon; temna tema ostane enaka.",
            "Farbe der Auswahl und Symbole ändern; das dunkle Design bleibt.");
        put("Adjust interface text size for different TV sizes and viewing distances.",
            "Prilagodi veličinu teksta televizoru i udaljenosti gledanja.",
            "Prilagodi velikost besedila zaslonu in razdalji gledanja.",
            "Textgröße an TV und Betrachtungsabstand anpassen.");
        put("Adjust transparency of channel lists and the EPG over the playing video.",
            "Podesi prozirnost liste kanala i EPG-a preko videa.",
            "Nastavi prosojnost seznama kanalov in EPG nad videom.",
            "Transparenz der Senderlisten und des EPG über dem Video einstellen.");
        put("Open the last watched live channel when the playlist is available, or show the home menu.",
            "Pokreni posljednji gledani kanal ili prikaži početni ekran.",
            "Odpri zadnji gledani kanal ali prikaži začetni zaslon.",
            "Letzten TV-Sender öffnen oder Startbildschirm anzeigen.");
        put("A smaller buffer reduces delay; a larger buffer may improve stability.",
            "Manji međuspremnik smanjuje kašnjenje; veći poboljšava stabilnost.",
            "Manjši medpomnilnik zmanjša zamik, večji lahko izboljša stabilnost.",
            "Kleiner Puffer senkt Verzögerung, größerer erhöht Stabilität.");
        put("Reconnect interrupted live streams automatically, using the working player mode.",
            "Automatski ponovo poveži prekinute kanale.",
            "Samodejno ponovno poveži prekinjene prenose.",
            "Unterbrochene Streams automatisch neu verbinden.");
        put("Save the most recently watched content and playback progress.",
            "Pamti posljednji gledani sadržaj i napredak.",
            "Shrani nazadnje gledano vsebino in napredek.",
            "Zuletzt gesehene Inhalte und Fortschritt merken.");
        put("Reopen an existing playlist to include or exclude countries. No URL needs to be typed again.",
            "Ponovo otvori listu i uključi ili isključi države bez novog unosa adrese.",
            "Znova odpri seznam in izberi države brez ponovnega vnosa naslova.",
            "Playlist erneut öffnen und Länder ohne neue URL wählen.");
        put("Correct the timezone offset of the TV guide relative to local time.",
            "Podesi vremenski pomak rasporeda prema lokalnom vremenu.",
            "Prilagodi časovni zamik sporeda glede na lokalni čas.",
            "Zeitzonenversatz des Programmführers korrigieren.");
        put("Hide adult-labelled groups until you enter your PIN. This is a basic local parental control.",
            "Sakrij kategorije za odrasle uz PIN zaštitu.",
            "Skrij kategorije za odrasle s kodo PIN.",
            "Erwachsenenkategorien mit PIN schützen.");
        put("Save or restore appearance and player settings only. Playlists and access credentials are excluded.",
            "Sačuvaj ili vrati izgled i postavke. Liste i pristupni podaci se ne izvoze.",
            "Shrani ali obnovi nastavitve. Seznami in prijavni podatki niso vključeni.",
            "Darstellung und Player-Einstellungen sichern, ohne Playlists oder Zugangsdaten.");
        put("Show the last recorded fatal Java crash without exposing playlist addresses or passwords.",
            "Prikaži zadnju grešku bez otkrivanja adresa i lozinki.",
            "Prikaži zadnjo napako brez razkrivanja URL-jev ali gesel.",
            "Letzten Absturz ohne Freigabe von URLs oder Passwörtern anzeigen.");
        put("Checks the latest signed public GitHub release. Verifies APK checksum and asks for Android installation confirmation. Playlists remain saved.",
            "Provjerava potpisana izdanja, integritet APK-a i traži potvrdu instalacije. Liste ostaju sačuvane.",
            "Preveri podpisane različice, celovitost APK in zahteva potrditev. Seznami ostanejo shranjeni.",
            "Prüft signierte Versionen und APK-Prüfsumme. Android bestätigt die Installation; Playlists bleiben.");
        put("Checks once per day while Keldin IPTV is in use. Downloads or installation never happen without your confirmation.",
            "Provjerava jednom dnevno. Preuzimanje i instalaciju uvijek potvrđuješ.",
            "Preverja enkrat na dan. Prenos in namestitev vedno potrdiš.",
            "Prüft täglich. Download und Installation benötigen immer deine Zustimmung.");
        put("Hide channel and EPG menus automatically after inactivity. Each remote key press restarts the timer.",
            "Sakrij listu kanala i EPG nakon neaktivnosti. Svaka tipka resetuje vrijeme.",
            "Samodejno skrij menije po nedejavnosti. Vsak pritisk tipke ponastavi časovnik.",
            "Sender- und EPG-Menüs nach Inaktivität ausblenden; jede Taste setzt den Timer zurück.");
        put("Prefer this audio track when the stream offers multiple languages. Auto uses the stream default.",
            "Koristi izabrani jezik zvuka ako je dostupan. Automatski koristi zadani zvuk.",
            "Prednost ima izbrani jezik, če je na voljo. Samodejno uporabi privzetega.",
            "Gewünschte Audiosprache bevorzugen, sofern verfügbar. Auto verwendet Standard.");
        put("Timeout for additional download attempts if the IPTV server initially fails to connect.",
            "Vrijeme čekanja pri ponovnom pokušaju povezivanja s IPTV serverom.",
            "Časovna omejitev dodatnih poskusov povezave s strežnikom IPTV.",
            "Zeitlimit für erneute IPTV-Verbindungsversuche.");
        put("On","Uključeno","Vklopljeno","Ein");
        put("Off","Isključeno","Izklopljeno","Aus");
        put("Never","Nikad","Nikoli","Nie");
        put("Auto","Automatski","Samodejno","Automatisch");
        put("Compact","Kompaktno","Kompaktno","Kompakt");
        put("Standard","Standardno","Standardno","Standard");
        put("Large","Veliko","Veliko","Groß");
        put("Installed ","Instalirano ","Nameščeno ","Installiert ");
        put("Reconnect stream","Ponovo poveži kanal","Znova poveži tok","Stream neu verbinden");
        put("Change playback mode","Promijeni način reprodukcije","Spremeni način predvajanja","Wiedergabemodus wechseln");
        put("Open in external player","Otvori u vanjskom playeru","Odpri v zunanjem predvajalniku","Externen Player öffnen");
        put("Error details","Detalji greške","Podrobnosti napake","Fehlerdetails");
        put("Toggle favorite","Dodaj/ukloni favorit","Preklopi priljubljeno","Favorit umschalten");
        put("Change aspect ratio","Promijeni format slike","Spremeni razmerje slike","Bildformat ändern");
        put("Audio tracks","Audio zapisi","Zvočne sledi","Audiospuren");
        put("Subtitles","Titlovi","Podnapisi","Untertitel");
        put("Pause / Resume","Pauza / Nastavi","Premor / Nadaljuj","Pause / Fortsetzen");
        put("Previous channel","Prethodni kanal","Prejšnji kanal","Vorheriger Sender");
        put("Next channel","Sljedeći kanal","Naslednji kanal","Nächster Sender");
        put("Probe HLS / TS server","Provjeri odgovor servera (HLS / TS)","Preveri odziv strežnika (HLS / TS)","Serverantwort prüfen (HLS / TS)");
        put("Options","Opcije","Možnosti","Optionen");
        put("Connecting...","Povezivanje...","Povezovanje...","Verbinden...");
        put("No available tracks.","Nema dostupnih zapisa.","Ni razpoložljivih sledi.","Keine Spuren verfügbar.");
        put("No errors recorded.","Nema evidentirane greške.","Ni zabeleženih napak.","Keine Fehler erfasst.");
        put("Connection failed","Povezivanje nije uspjelo","Povezava ni uspela","Verbindung fehlgeschlagen");
    }
    public static String translate(Context context,String value){
        if(value==null)return "";
        String lang=context.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getString("ui_lang","en");
        String[] entry=TEXT.get(value);
        if(entry==null)return value;
        switch(lang){
            case "bs":return entry[1];
            case "sl":return entry[2];
            case "de":return entry[3];
            default:return entry[0];
        }
    }
}
