import com.keldin.iptv.data.Channel;
import com.keldin.iptv.net.M3uParser;
import java.io.StringReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

/** Pure-Java smoke test: 60K+ entries, classification, country groups, parsing progress. */
public class ParserV6SmokeTest {
  private static void check(boolean condition,String message){
    if(!condition)throw new AssertionError(message);
  }
  public static void main(String[] args)throws Exception{
    String text="#EXTM3U x-tvg-url=\"https://example.org/guide.xml\"\n"+
        "#EXTINF:-1 group-title=\"EX YU | Bosna\" tvg-id=\"BHT\" tvg-logo=\"https://example.org/bht.png\",BHT FHD\n"+
        "http://example.org/live/bht.ts\n"+
        "#EXTINF:-1 group-title=\"EX YU | Austrija\",Austria One\n"+
        "http://example.org/live/at.ts\n"+
        "#EXTINF:-1 group-title=\"Radio | Balkanske stanice\",Radio Sarajevo\n"+
        "http://example.org/stream/live\n"+
        "#EXTINF:-1 group-title=\"Drama Movies\",Drama movie\n"+
        "http://example.org/movie/1.mp4\n"+
        "#EXTINF:-1 group-title=\"My Series\",Great Series S01E02\n"+
        "http://example.org/series/1.mp4\n";
    ArrayList<Integer> updates=new ArrayList<>();
    M3uParser.Result parsed=M3uParser.parse(new StringReader(text),"test",
        "http://example.org/all.m3u",updates::add);
    check(parsed.channels.size()==5,"Five channels required");
    check(parsed.channels.get(0).name.equals("BHT FHD"),"Name preserved");
    check(parsed.channels.get(0).group.equals("EX YU | Bosna"),"Country preserved");
    check(parsed.channels.get(2).kind.equals("RADIO"),"Radio classified");
    check(parsed.channels.get(3).kind.equals("MOVIES"),"Movie classified");
    check(parsed.channels.get(4).kind.equals("SERIES"),"Series classified");
    check(parsed.epgUrl.contains("guide.xml"),"Guide source parsed");
    HashSet<String> disabled=new HashSet<>(); disabled.add("EX YU | Austrija");
    int included=0;for(Channel ch:parsed.channels)if(!disabled.contains(ch.group))included++;
    check(included==4,"Country selection");
    StringBuilder big=new StringBuilder("#EXTM3U\n");
    final int n=61050;
    for(int i=0;i<n;i++){
      big.append("#EXTINF:-1 group-title=\"EX YU | Bosna\",Channel ")
         .append(i).append('\n').append("https://example.org/stream/")
         .append(i).append(".ts\n");
    }
    M3uParser.Result huge=M3uParser.parse(new StringReader(big.toString()),
        "large","https://example.org/playlist",updates::add);
    check(huge.channels.size()==n,"Must not truncate at 60000");
    check(!updates.isEmpty(),"Progress updates received");
    check(updates.get(updates.size()-1)>60000,"Progress reaches 60K");
    System.out.println("v0.6 PASS: classification, country filters, guide, 61,050 channels, progress");
  }
}
