from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/LogoLoader.java")
s=p.read_text()
needle='''    private static final HashSet<String> pending=new HashSet<>();'''
assert needle in s
s=s.replace(needle,'''    // Limit both active transfers and queued work; default executor queues are unbounded.
    private static final java.util.concurrent.atomic.AtomicInteger inFlight=
        new java.util.concurrent.atomic.AtomicInteger();''',1)
needle='''        synchronized(pending) {
            if(pending.size()>96)return; // no unbounded requests when scrolling 60k items
        }
        pool.execute(()->{'''
assert needle in s
s=s.replace(needle,'''        if(inFlight.incrementAndGet()>28){
            inFlight.decrementAndGet();
            return;
        }
        pool.execute(()->{''',1)
needle='''            finally {if(conn!=null)conn.disconnect();}
        });'''
assert needle in s
s=s.replace(needle,'''            finally {
                if(conn!=null)conn.disconnect();
                inFlight.decrementAndGet();
            }
        });''',1)
needle='''        int w=bitmap.getWidth(),h=bitmap.getHeight();'''
assert needle in s
s=s.replace(needle,'''        int w=bitmap.getWidth(),h=bitmap.getHeight();
        // Portrait artwork is a movie poster, not a channel logo.
        if(h>w*1.22f)return bitmap;''',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
needle='''        Ui.applyTheme(this);
        TextView loading=Ui.text(this,''';
assert needle in s
s=s.replace(needle,'''        Ui.applyTheme(this);
        CrashReporter.install(this);
        TextView loading=Ui.text(this,''',1)
# Group separate episode URLs into a single series tile.
needle='''        ArrayList<Channel> visible=filterSection(section,selectedGroup);'''
assert needle in s
s=s.replace(needle,'''        ArrayList<Channel> visible=filterSection(section,selectedGroup);
        if("SERIES".equals(kind))visible=new ArrayList<>(SeriesBrowserV6.unique(visible));''',1)
needle='''            ArrayList<Channel> filtered=filterSection(section,group);
            if(mediaAdapter!=null)mediaAdapter.replace(filtered);'''
assert needle in s
s=s.replace(needle,'''            ArrayList<Channel> filtered=filterSection(section,group);
            if("SERIES".equals(kind))
                filtered=new ArrayList<>(SeriesBrowserV6.unique(filtered));
            if(mediaAdapter!=null)mediaAdapter.replace(filtered);''',1)
needle='''    private void openMediaDetails(Channel media){
        String name=media.name;'''
assert needle in s
s=s.replace(needle,'''    private void openMediaDetails(Channel media){
        if("SERIES".equals(media.kind)){
            SeriesBrowserV6.open(this,store.channels(),media,this::play);
            return;
        }
        String name=media.name;''',1)
# English-first labels on primary screens.
s=s.replace('"Nijedna lista nije dodana."','"No playlists added."')
s=s.replace('"+  Nova M3U lista"','"＋  Add M3U playlist"')
s=s.replace('"+  Xtream nalog"','"＋  Xtream login"')
s=s.replace('"Uvezi .m3u datoteku"','"Import .m3u file"')
s=s.replace('"Osvježi"','"Sync"')
s=s.replace('"Uredi"','"Edit"')
s=s.replace('"Ukloni"','"Remove"')
s=s.replace('"TV vodič nije dostupan"','"No TV guide"')
s=s.replace('"Dodaj M3U listu ili Xtream nalog za početak gledanja."',
''' "Add an M3U playlist or Xtream account to start watching."'''.strip())
# "Welcome" no more stuck within first-run flow
s=s.replace('"Dobro došao u Keldin IPTV"','"Welcome to Keldin IPTV"')
p.write_text(s)
print("v0.6 logo loading bounded, crash reporting enabled, series grouped by seasons")
