import com.keldin.iptv.data.Channel;
import com.keldin.iptv.net.CategoryScanV61;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public final class FilmAndPlaylistsV99Test {
    private static void check(boolean value,String label){
        if(!value)throw new AssertionError(label);
    }
    public static void main(String[] args)throws Exception{
        String group="EX YU | Filmovi & Serije";
        check("LIVE".equals(Channel.inferKind(group,
            "http://iptv.example.com/u/p/365.ts")),"HBO bare live URL");
        check("LIVE".equals(Channel.inferKind(group,
            "http://iptv.example.com/live/u/p/372")),"CineStar live URL");
        check("LIVE".equals(Channel.inferKind("EX-YU | Filmovi i Serije",
            "http://iptv.example.com/u/p/369")),"EX-YU alternate group");
        check("MOVIES".equals(Channel.inferKind(group,
            "http://iptv.example.com/movie/u/p/1.mp4")),"real VOD movie");
        check("SERIES".equals(Channel.inferKind(group,
            "http://iptv.example.com/series/u/p/2.mp4")),"real VOD series");
        Path file=Files.createTempFile("keldin-v99-film",".m3u");
        try{
            String m3u="#EXTM3U\n"+
              "#EXTINF:-1 group-title=\"EX YU | Filmovi & Serije\",HBO HD\n"+
              "http://iptv.example.com/u/p/365.ts\n"+
              "#EXTINF:-1 group-title=\"EX YU | Filmovi & Serije\",CineStar 1 HD\n"+
              "http://iptv.example.com/u/p/372.ts\n"+
              "#EXTINF:-1 group-title=\"EX YU | Filmovi & Serije\",Cinemax HD\n"+
              "http://iptv.example.com/u/p/399.ts\n"+
              "#EXTINF:-1 group-title=\"EX YU | Filmovi & Serije\",Actual VOD\n"+
              "http://iptv.example.com/movie/u/p/452.mp4\n"+
              "#EXTINF:-1 group-title=\"EX YU | Serije\",True series\n"+
              "http://iptv.example.com/series/u/p/3.mp4\n";
            Files.writeString(file,m3u,StandardCharsets.UTF_8);
            CategoryScanV61 scan=CategoryScanV61.scan(file.toFile(),n->{});
            check(scan.liveGroups.getOrDefault(group,0)==3,
                "3 broadcaster channels must be selectable at import");
            check(scan.kinds[0]==3&&scan.kinds[1]==1&&scan.kinds[2]==1,
                "Live, VOD movies and series properly separated");
        }finally{Files.deleteIfExists(file);}
        System.out.println("PASS Filmovi & Serije channel group, import selection and VOD preservation");
    }
}
