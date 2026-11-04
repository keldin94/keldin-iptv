from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistImportHttpV81.java")
s=p.read_text()
needle='''    public static InputStream open(String playlistUrl,String userAgent,long maxBytes)throws IOException {
        IOException original;'''
replacement='''    public static InputStream open(String playlistUrl,String userAgent,long maxBytes)throws IOException {
        return open(playlistUrl,userAgent,maxBytes,45);
    }
    public static InputStream open(String playlistUrl,String userAgent,long maxBytes,
                                   int preferredTimeoutSeconds)throws IOException {
        preferredTimeoutSeconds=Math.max(15,Math.min(90,preferredTimeoutSeconds));
        IOException original;'''
assert needle in s
s=s.replace(needle,replacement,1)
assert 'int timeout=attempt==0?30000:45000;' in s
s=s.replace('int timeout=attempt==0?30000:45000;',
            'int timeout=attempt==0?Math.max(20000,preferredTimeoutSeconds*750):preferredTimeoutSeconds*1000;',1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java")
s=p.read_text()
old='''PlaylistImportHttpV81.open(source.playlistUrl(),source.userAgent,MAX_BYTES)'''
new='''PlaylistImportHttpV81.open(source.playlistUrl(),source.userAgent,MAX_BYTES,
                    activity.getSharedPreferences("keldin_settings",android.content.Context.MODE_PRIVATE)
                        .getInt("playlist_timeout_seconds",45))'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print("v0.9: retry connection timeout is user configurable in Network tab")
