import com.keldin.iptv.data.PlaylistSource;
import com.keldin.iptv.data.GuideProgram;
import com.keldin.iptv.net.EpgParser;
import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class EpgAutoV917Test {
    static void require(boolean pass,String name){
        if(!pass)throw new AssertionError(name);
    }
    public static void main(String[] args)throws Exception {
        PlaylistSource source=new PlaylistSource();
        source.type="M3U";
        source.url="https://example.com:2095/get.php?username=viewer&password=secret&type=m3u_plus";
        require(source.guideUrl().equals(
            "https://example.com:2095/xmltv.php?username=viewer&password=secret"),
            "Xtream get.php query should automatically resolve XMLTV");
        source.url="http://example.org/playlist/viewer/secret/m3u_plus?output=hls";
        require(source.guideUrl().equals(
            "http://example.org/xmltv.php?username=viewer&password=secret"),
            "path-based M3U XMLTV discovery remains intact");
        source.epgUrl="https://epg.example.org/schedule.xml.gz";
        require(source.guideUrl().equals(source.epgUrl),"explicit EPG overrides guesses");
        source.epgUrl="";
        source.url="https://example.org/other/list.m3u";
        require(source.guideUrl().isEmpty(),"unrelated playlist must not invent EPG");

        long now=System.currentTimeMillis();
        java.text.SimpleDateFormat date=new java.text.SimpleDateFormat("yyyyMMddHHmmss Z",java.util.Locale.US);
        date.setTimeZone(java.util.TimeZone.getTimeZone("UTC"));
        String start=date.format(new java.util.Date(now-1_800_000L));
        String stop=date.format(new java.util.Date(now+1_800_000L));
        String xml="<?xml version=\"1.0\"?><tv>"+
            "<channel id=\"stream.328\"><display-name>HBO HD</display-name></channel>"+
            "<channel id=\"stream.329\"><display-name>CineStar 1 HD</display-name></channel>"+
            "<programme channel=\"stream.328\" start=\""+start+"\" stop=\""+stop+"\">"+
            "<title>Featured Film</title><desc>Evening cinema</desc></programme>"+
            "<programme channel=\"stream.329\" start=\""+start+"\" stop=\""+stop+"\">"+
            "<title>Another Film</title></programme></tv>";
        Set<String> wanted=new HashSet<>();
        wanted.add("HBO HD");wanted.add("CineStar 1 HD");
        Map<String,List<GuideProgram>> result=EpgParser.parse(
            new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)),wanted,now);
        require(result.containsKey("HBO HD")&&result.get("HBO HD").size()==1,
            "XMLTV id->display-name matching for HBO HD");
        require(result.containsKey("CineStar 1 HD")&&result.get("CineStar 1 HD").size()==1,
            "XMLTV id->display-name matching for CineStar");
        require("Featured Film".equals(result.get("HBO HD").get(0).title),
            "correct live programme in channel adapter");
        System.out.println("PASS auto EPG URL and XMLTV channel-name matching");
    }
}
