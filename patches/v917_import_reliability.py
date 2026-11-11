from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java")
s=p.read_text()
old='''                tempFile=File.createTempFile("keldin-import-", ".m3u",activity.getCacheDir());'''
new='''                // Android can evict getCacheDir() while the import chooser is open.
                // Its file must survive steps 1/2 -> 3 before it is explicitly removed.
                File staging=new File(activity.getFilesDir(),"keldin-import-staging");
                if(!staging.exists()&&!staging.mkdirs())
                    throw new IOException("Cannot prepare private import storage");
                File[] leftovers=staging.listFiles();
                if(leftovers!=null)for(File candidate:leftovers)
                    if(candidate.isFile()&&candidate.getName().startsWith("keldin-import-")&&
                       System.currentTimeMillis()-candidate.lastModified()>86_400_000L)
                        candidate.delete();
                tempFile=File.createTempFile("keldin-import-", ".m3u",staging);'''
assert old in s,"v917 missing cache temp file creation"
s=s.replace(old,new,1)
old='''                    new FileInputStream(tempFile),StandardCharsets.UTF_8),65536)){'''
new='''                    new FileInputStream(requireStagingV917()),StandardCharsets.UTF_8),65536)){'''
assert old in s,"v917 missing M3U parsing from temp"
s=s.replace(old,new,1)
needle='''    private void fail(String message){ui.post(()->complete(false,message));}'''
methods='''    /**
     * Some low-storage TV boxes may still lose a staging file after the
     * category chooser has been displayed. Safely redownload it on the
     * existing background executor rather than showing a raw ENOENT.
     * Never clear existing channels unless parsing and saving succeeds.
     */
    private File requireStagingV917()throws IOException{
        if(tempFile!=null&&tempFile.isFile()&&tempFile.length()>0)return tempFile;
        setPhase("Reconnecting playlist",
            "The temporary import file disappeared. Downloading a fresh copy…");
        if("FILE".equals(source.type))
            throw new IOException("The selected local M3U file is unavailable. Re-select it.");
        File staging=new File(activity.getFilesDir(),"keldin-import-staging");
        if(!staging.exists()&&!staging.mkdirs())
            throw new IOException("Not enough private storage for playlist import");
        long free=staging.getUsableSpace();
        if(free<16_000_000L)throw new IOException("Not enough space to refresh playlist");
        File fresh=File.createTempFile("keldin-import-", ".m3u",staging);
        boolean valid=false;
        try(InputStream in=com.keldin.iptv.net.PlaylistImportHttpV81.open(
                 source.playlistUrl(),source.userAgent,MAX_BYTES,
                 activity.getSharedPreferences("keldin_settings",
                     android.content.Context.MODE_PRIVATE)
                     .getInt("playlist_timeout_seconds",45));
            FileOutputStream output=new FileOutputStream(fresh)){
            byte[] buffer=new byte[32768];
            long downloaded=0;int n;
            while((n=in.read(buffer))!=-1){
                downloaded+=n;
                if(downloaded>MAX_BYTES||downloaded>free-8_000_000L)
                    throw new IOException("Playlist is too large for available storage");
                output.write(buffer,0,n);
            }
            valid=downloaded>0;
        }finally{if(!valid)fresh.delete();}
        if(!valid)throw new IOException("Playlist download returned no data");
        tempFile=fresh;
        return fresh;
    }

'''
assert needle in s,"v917 recovery insertion marker"
s=s.replace(needle,methods+needle,1)
p.write_text(s)
print("PASS import staging stays outside evictable Android cache and safely retries missing files")
