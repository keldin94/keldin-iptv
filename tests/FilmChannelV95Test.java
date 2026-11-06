import com.keldin.iptv.data.Channel;
import com.keldin.iptv.net.CategoryScanV61;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public final class FilmChannelV95Test {
    private static void require(boolean good,String label){
        if(!good)throw new IllegalStateException("FAILED "+label);
    }
    public static void main(String[] args)throws Exception{
        String group="EX-YU | Filmski";
        require("LIVE".equals(Channel.inferKind(group,"http://server.example/live/u/p/123.ts")),
            "HBO live URL and Filmski group");
        require("LIVE".equals(Channel.inferKind(group,"http://server.example/u/p/123")),
            "HBO bare live URL and Filmski group");
        require("LIVE".equals(Channel.inferKind("EX YU | FILMSKI HD","http://server.example/u/p/321")),
            "mixed case FILMSKI category");
        require("MOVIES".equals(Channel.inferKind("EX-YU | Filmski","http://server.example/movie/u/p/456.mp4")),
            "actual movie URL stays VOD");
        require("MOVIES".equals(Channel.inferKind("Filmovi 2026","http://server.example/movie/u/p/789.mp4")),
            "movie group");
        require("SERIES".equals(Channel.inferKind("EX-YU | Serije","http://server.example/series/u/p/1.mp4")),
            "series");
        require("RADIO".equals(Channel.inferKind("Radio BiH","http://server.example/radio/u/p/1.mp3")),
            "radio");
        Path file=Files.createTempFile("v95-filmski",".m3u");
        try{
            String m3u="#EXTM3U\n"+
                "#EXTINF:-1 group-title=\"EX-YU | Filmski\",BH: HBO HD\n"+
                "http://server.example/u/p/1.ts\n"+
                "#EXTINF:-1 group-title=\"EX-YU | Filmski\",BH: AXN\n"+
                "http://server.example/u/p/2.ts\n"+
                "#EXTINF:-1 group-title=\"Filmovi\",Film\n"+
                "http://server.example/movie/u/p/3.mp4\n";
            Files.writeString(file,m3u,StandardCharsets.UTF_8);
            CategoryScanV61 scan=CategoryScanV61.scan(file.toFile(),n->{});
            require(scan.liveGroups.getOrDefault(group,0)==2,"two filmski TV channels scanned");
            require(scan.kinds[0]==2 && scan.kinds[1]==1,"two live, one movie");
        }finally{Files.deleteIfExists(file);}
        System.out.println("PASS: EX-YU Filmski correctly imports as live TV, VOD and series unaffected");
    }
}
