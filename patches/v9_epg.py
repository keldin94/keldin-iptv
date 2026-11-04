from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/data/PlaylistSource.java")
s=p.read_text()
old='''        if (!"XTREAM".equals(type)) return "";
        return server.trim().replaceAll("/+$", "") + "/xmltv.php?username=" + encode(username)
            + "&password=" + encode(password);'''
new='''        if ("XTREAM".equals(type))
            return server.trim().replaceAll("/+$", "") + "/xmltv.php?username=" + encode(username)
                + "&password=" + encode(password);
        // Some providers expose an Xtream-compatible playlist as an M3U URL
        // with /playlist/user/pass/m3u_plus. Derive XMLTV from that SAME origin.
        // Never log, display, upload or redirect playlist credentials.
        if (!"M3U".equals(type)) return "";
        try {
            java.net.URL feed=new java.net.URL(url.trim());
            String protocol=feed.getProtocol().toLowerCase(java.util.Locale.ROOT);
            if(!protocol.equals("http")&&!protocol.equals("https"))return "";
            String[] parts=feed.getPath().split("/");
            String user=null,pass=null;
            for(int i=0;i+3<parts.length;i++){
                if("playlist".equalsIgnoreCase(parts[i])&&
                    parts[i+3].toLowerCase(java.util.Locale.ROOT).contains("m3u")){
                    user=java.net.URLDecoder.decode(parts[i+1],"UTF-8");
                    pass=java.net.URLDecoder.decode(parts[i+2],"UTF-8");
                    break;
                }
            }
            if(user==null||pass==null||user.isEmpty()||pass.isEmpty())return "";
            return new java.net.URL(protocol,feed.getHost(),feed.getPort(),
                "/xmltv.php?username="+encode(user)+"&password="+encode(pass)).toString();
        }catch(Exception ignored){return "";}'''
assert old in s,"v0.9 PlaylistSource guideUrl marker missing"
s=s.replace(old,new,1)
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
old='''            if(status!=null && status.startsWith("EPG nije dostupan"))
                Toast.makeText(this,tr("epg_load_error"),Toast.LENGTH_SHORT).show();'''
new='''            if(status!=null && status.startsWith("EPG nije dostupan")){
                requestedGuides.remove(src.id);
                Toast.makeText(this,tr("epg_load_error"),Toast.LENGTH_SHORT).show();
            }'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print("v0.9: auto-detect matching same-host XMLTV for Xtream-style M3U playlist URLs")
