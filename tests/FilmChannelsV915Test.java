import com.keldin.iptv.data.Channel;
import com.keldin.iptv.net.CategoryScanV61;
import com.keldin.iptv.net.M3uParser;
import java.io.File;
import java.io.StringReader;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class FilmChannelsV915Test {
    private static void require(boolean pass,String description){
        if(!pass)throw new AssertionError(description);
    }
    public static void main(String[] args)throws Exception{
        String group="EX YU | Filmovi & Serije";
        String[] names={
          "HBO HD","HBO L2","HBO 2 HD","HBO 2 L2","HBO 3 HD","HBO 3 L2",
          "CineStar 1 FHD","CineStar 1 HD","CineStar 2 FHD","CineStar 2 HD",
          "CineStar Premiere 1","CineStar Premiere 2","Cinemax HD","Cinemax 2 HD",
          "AMC HD","FilmBox HD","FilmBox Stars","FilmBox Premium","FilmBox Extra",
          "AXN HD","AXN Spin","STAR Movies","STAR Crime","STAR Life",
          "Epic Drama","Diva","TV 1000","Film4","Klasik TV"
        };
        StringBuilder m3u=new StringBuilder("#EXTM3U\n");
        for(int i=0;i<54;i++){
            String name=names[i%names.length]+" "+(i+1);
            m3u.append("#EXTINF:-1 tvg-name=\"").append(name)
                .append("\" group-title=\"").append(group)
                .append("\",").append(name).append("\n");
            m3u.append("http://iptv.example.com/u/p/").append(1200+i).append(".ts\n");
        }
        m3u.append("#EXTINF:-1 group-title=\"EX YU | Filmovi & Serije\",Real VOD\n");
        m3u.append("http://iptv.example.com/movie/u/p/500.mp4\n");
        m3u.append("#EXTINF:-1 group-title=\"EX YU | Serije\",Episode 1\n");
        m3u.append("http://iptv.example.com/series/u/p/501.mp4\n");
        File file=File.createTempFile("keldin-v915-exyu",".m3u");
        try{
            Files.writeString(file.toPath(),m3u.toString(),StandardCharsets.UTF_8);
            CategoryScanV61 scan=CategoryScanV61.scan(file,n->{});
            require(scan.liveGroups.containsKey(group),"Missing named Live TV category at import");
            require(scan.liveGroups.get(group)==54,"Must show all 54 live TV broadcasters at import");
            require(scan.kinds[0]==54&&scan.kinds[1]==1&&scan.kinds[2]==1,
                "Never mix real VOD with live broadcasters");
            M3uParser.Result parsed=M3uParser.parse(new StringReader(m3u.toString()),
                "demo","http://iptv.example.com/get.php",n->{},c->true);
            int live=0,movie=0,series=0;
            for(Channel c:parsed.channels){
                if("LIVE".equals(c.kind)&&group.equals(c.group))live++;
                if("MOVIES".equals(c.kind))movie++;
                if("SERIES".equals(c.kind))series++;
            }
            require(live==54&&movie==1&&series==1,
                "Scanner and importer must agree about all 54 live broadcasters");
            require(Channel.isLiveFilmGroup("EX-YU | Filmovi i Serije",
                "http://iptv.example.com/u/p/555.ts"),
                "Alternate category name must remain Live TV");
            System.out.println("PASS 54 EX YU Filmovi & Serije live channels and actual M3U importer");
        }finally{file.delete();}
    }
}
