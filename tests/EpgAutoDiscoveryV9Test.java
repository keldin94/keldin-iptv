import com.keldin.iptv.data.PlaylistSource;

public final class EpgAutoDiscoveryV9Test {
    static void test(boolean condition,String name){
        if(!condition)throw new AssertionError(name);
    }
    public static void main(String[] args){
        PlaylistSource src=new PlaylistSource();
        src.type="M3U";
        src.url="http://provider.example:2095/playlist/account/password/m3u_plus?output=hls";
        test(src.guideUrl().equals("http://provider.example:2095/xmltv.php?username=account&password=password"),"compatible M3U guide");
        src.epgUrl="https://epg.example/programs.xml";
        test(src.guideUrl().equals(src.epgUrl),"explicit XMLTV link overrides auto-detection");
        src.epgUrl="";
        src.url="https://provider.example/user/other.m3u";
        test(src.guideUrl().isEmpty(),"never guess from unrelated M3U address");
        src.type="XTREAM";src.server="https://provider.example:444";src.username="A";src.password="B";
        test(src.guideUrl().equals("https://provider.example:444/xmltv.php?username=A&password=B"),"XTREAM behavior unchanged");
        System.out.println("PASS: safe same-host XMLTV auto-detection and explicit EPG override");
    }
}
