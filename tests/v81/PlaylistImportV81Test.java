import com.keldin.iptv.net.PlaylistImportHttpV81;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class PlaylistImportV81Test {
    static void require(boolean yes,String name){
        if(!yes)throw new AssertionError(name);
    }
    static String fetch(String url)throws Exception{
        try(InputStream stream=PlaylistImportHttpV81.open(url,"KeldinTest/1.0",1024*1024)){
            return new String(stream.readAllBytes(),StandardCharsets.UTF_8);
        }
    }
    public static void main(String[] args)throws Exception {
        HttpServer server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
        server.createContext("/m3u",exchange->{
            byte[] bytes="#EXTM3U\n#EXTINF:-1,Test Channel\nhttp://example.test/live.ts\n"
                .getBytes(StandardCharsets.UTF_8);
            require("KeldinTest/1.0".equals(exchange.getRequestHeaders().getFirst("User-Agent")),
                "original user agent preserved on first retry");
            exchange.sendResponseHeaders(200,bytes.length);
            try(java.io.OutputStream output=exchange.getResponseBody()){output.write(bytes);}
        });
        server.createContext("/redirect",exchange->{
            exchange.getResponseHeaders().set("Location","/m3u");
            exchange.sendResponseHeaders(302,-1);
            exchange.close();
        });
        server.createContext("/forbidden",exchange->{
            exchange.sendResponseHeaders(403,-1);
            exchange.close();
        });
        server.start();
        String base="http://127.0.0.1:"+server.getAddress().getPort();
        try{
            require(fetch(base+"/m3u").contains("Test Channel"),"recover from original 15s timeout");
            require(fetch(base+"/redirect").contains("Test Channel"),"redirect followed");
            try{
                fetch(base+"/forbidden");
                throw new AssertionError("HTTP 403 must be surfaced");
            }catch(java.io.IOException expected){
                require(expected.getMessage().contains("403"),"HTTP response captured");
            }
            System.out.println("PASS: recoverable timeout, redirect, and HTTP 403");
        }finally{
            server.stop(0);
        }
    }
}
