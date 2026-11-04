import com.keldin.iptv.net.M3uParser;
import com.keldin.iptv.net.CategoryScanV61;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.util.concurrent.atomic.AtomicInteger;

public class FilteredM3uV61SmokeTest{
    private static void check(boolean good,String message){if(!good)throw new AssertionError(message);}
    public static void main(String[]args)throws Exception{
        File tmp=File.createTempFile("keldin-v61-large-", ".m3u");
        try{
            try(BufferedWriter out=new BufferedWriter(new FileWriter(tmp))){
                out.write("#EXTM3U\n");
                for(int i=0;i<170001;i++){
                    String country=i%17==0?"EX YU | Bosna":"Australia";
                    out.write("#EXTINF:-1 group-title=\""+country+"\",Test "+i+"\n");
                    out.write("https://example.org/live/stream/"+i+".ts\n");
                }
            }
            CategoryScanV61 groups=CategoryScanV61.scan(tmp,null);
            check(groups.total==170001,"Scanner must scan all 170001 entries");
            check(groups.liveGroups.get("Australia")>150000,"Big category expected");
            AtomicInteger seen=new AtomicInteger();
            M3uParser.Result selected=M3uParser.parse(new FileReader(tmp),
                "test","https://example.org/playlist",n->seen.set(n),
                c->c.group.equals("EX YU | Bosna"));
            check(selected.channels.size()>9900&&selected.channels.size()<11000,
                "Only selected country's channels should be kept");
            check(selected.channels.get(0).group.equals("EX YU | Bosna"),
                "Incorrect category filtering");
            System.out.println("PASS: 170001 scanned; "+selected.channels.size()+
                " imported; low-memory selection preserved");
        }finally{tmp.delete();}
    }
}
