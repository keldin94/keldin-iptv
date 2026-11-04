import com.keldin.iptv.net.M3uParser;
import com.keldin.iptv.net.CategoryScanV61;
import java.io.*;
import java.util.concurrent.atomic.AtomicInteger;

/** Regression for the real-world 183,104 item import that previously failed at 150,000. */
public class LargeFullPlaylistV8Test {
    private static void ok(boolean test,String name){
        if(!test)throw new AssertionError(name);
    }
    public static void main(String[] args)throws Exception {
        final int expected=183104;
        File playlist=File.createTempFile("keldin-v8-183104",".m3u");
        try {
            try(BufferedWriter output=new BufferedWriter(new FileWriter(playlist))){
                output.write("#EXTM3U\n");
                for(int i=0;i<expected;i++){
                    String category=i%5==0?"Bosnia":i%5==1?"Croatia":
                        i%5==2?"Germany":i%5==3?"Spain":"Slovenia";
                    output.write("#EXTINF:-1 group-title=\""+category+"\",Channel "+i+"\n");
                    output.write("https://example.com/live/"+i+".ts\n");
                }
            }
            CategoryScanV61 groups=CategoryScanV61.scan(playlist,null);
            ok(groups.total==expected,"all source entries counted");
            ok(groups.liveGroups.size()==5,"all five countries discovered");
            AtomicInteger last=new AtomicInteger();
            M3uParser.Result full=M3uParser.parse(new FileReader(playlist),
                "v8","https://example.com/playlist",last::set,ch->true);
            ok(full.channels.size()==expected,"full 183104-item catalogue imported");
            System.out.println("PASS: "+expected+" playlist entries parsed and retained");
        }finally{playlist.delete();}
    }
}
