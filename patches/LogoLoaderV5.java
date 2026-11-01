package com.keldin.iptv.ui;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.util.LruCache;
import android.widget.ImageView;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashSet;
import java.util.ArrayDeque;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class LogoLoader {
    public interface Result { void onLoaded(boolean loaded); }
    private static final ExecutorService pool=Executors.newFixedThreadPool(3);
    private static final Handler ui=new Handler(Looper.getMainLooper());
    private static final LruCache<String,Bitmap> cache = new LruCache<String,Bitmap>(12*1024) {
        @Override protected int sizeOf(String key,Bitmap b) { return Math.max(1,b.getByteCount()/1024); }
    };
    private static final HashSet<String> pending=new HashSet<>();
    private LogoLoader() {}

    public static void load(ImageView image,String url,Result onLoad) {
        image.setTag(url);image.setImageDrawable(null);
        if(url==null||!(url.startsWith("https://")||url.startsWith("http://"))) {
            if(onLoad!=null)onLoad.onLoaded(false);
            return;
        }
        Bitmap existing=cache.get(url);
        if(existing!=null){image.setImageBitmap(existing);if(onLoad!=null)onLoad.onLoaded(true);return;}
        // A recycled row should not briefly display initials behind transparent pixels.
        if(onLoad!=null)onLoad.onLoaded(false);
        synchronized(pending) {
            if(pending.size()>96)return; // no unbounded requests when scrolling 60k items
        }
        pool.execute(()->{
            HttpURLConnection conn=null;
            try {
                conn=(HttpURLConnection)new URL(url).openConnection();
                conn.setConnectTimeout(4000);conn.setReadTimeout(5000);
                conn.setInstanceFollowRedirects(true);
                if(conn.getResponseCode()!=200 || conn.getContentLengthLong()>2_000_000)return;
                ByteArrayOutputStream out=new ByteArrayOutputStream();
                try(InputStream in=conn.getInputStream()){
                    byte[] buf=new byte[4096];int n;
                    while((n=in.read(buf))!=-1){
                        if(out.size()+n>2_000_000)return;
                        out.write(buf,0,n);
                    }
                }
                byte[] data=out.toByteArray();
                BitmapFactory.Options options=new BitmapFactory.Options();
                options.inJustDecodeBounds=true;
                BitmapFactory.decodeByteArray(data,0,data.length,options);
                int largest=Math.max(options.outWidth,options.outHeight);
                options.inSampleSize=1;
                while(largest/options.inSampleSize>240)options.inSampleSize*=2;
                options.inJustDecodeBounds=false;
                options.inPreferredConfig=Bitmap.Config.ARGB_8888;
                Bitmap bitmap=BitmapFactory.decodeByteArray(data,0,data.length,options);
                if(bitmap==null)return;
                bitmap=removeFlatBorderBackground(bitmap);
                cache.put(url,bitmap);
                Bitmap ready=bitmap;
                ui.post(()->{
                    if(url.equals(image.getTag())){
                        image.setImageBitmap(ready);
                        if(onLoad!=null)onLoad.onLoaded(true);
                    }
                });
            }catch(Exception ignored){}
            finally {if(conn!=null)conn.disconnect();}
        });
    }
    /** Remove only a reasonably uniform corner-connected background baked into a channel-logo image.
        Avoid touching logos that already have transparent edges or complex backgrounds. */
    private static Bitmap removeFlatBorderBackground(Bitmap bitmap){
        int w=bitmap.getWidth(),h=bitmap.getHeight();
        if(w<20||h<20||w*h>100000)return bitmap;
        int tl=bitmap.getPixel(0,0),tr=bitmap.getPixel(w-1,0);
        int bl=bitmap.getPixel(0,h-1),br=bitmap.getPixel(w-1,h-1);
        if(Color.alpha(tl)<245||Color.alpha(tr)<245||Color.alpha(bl)<245||Color.alpha(br)<245)return bitmap;
        if(distance(tl,tr)>55||distance(tl,bl)>55||distance(tl,br)>55)return bitmap;
        int bg=average(tl,tr,bl,br);
        int[] pixels=new int[w*h];
        bitmap.getPixels(pixels,0,w,0,0,w,h);
        boolean[] seen=new boolean[pixels.length];
        ArrayDeque<Integer> queue=new ArrayDeque<>();
        for(int x=0;x<w;x++){
            include(x,0,w,h,pixels,seen,queue,bg);
            include(x,h-1,w,h,pixels,seen,queue,bg);
        }
        for(int y=0;y<h;y++){
            include(0,y,w,h,pixels,seen,queue,bg);
            include(w-1,y,w,h,pixels,seen,queue,bg);
        }
        int affected=0;
        while(!queue.isEmpty()){
            int id=queue.removeFirst();affected++;
            int x=id%w,y=id/w;
            if(x>0)include(x-1,y,w,h,pixels,seen,queue,bg);
            if(x<w-1)include(x+1,y,w,h,pixels,seen,queue,bg);
            if(y>0)include(x,y-1,w,h,pixels,seen,queue,bg);
            if(y<h-1)include(x,y+1,w,h,pixels,seen,queue,bg);
        }
        // Do not erase a whole-square photograph, or a nearly uniform brand symbol.
        if(affected<w*h/12||affected> w*h*4/5)return bitmap;
        for(int i=0;i<pixels.length;i++)if(seen[i])pixels[i]&=0x00ffffff;
        Bitmap result=Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888);
        result.setPixels(pixels,0,w,0,0,w,h);
        return result;
    }
    private static void include(int x,int y,int w,int h,int[] p,boolean[] seen,
                                ArrayDeque<Integer> queue,int bg){
        int i=y*w+x;
        if(!seen[i] && distance(p[i],bg)<58 && Color.alpha(p[i])>225){
            seen[i]=true;queue.add(i);
        }
    }
    private static int distance(int a,int b){
        int dr=Color.red(a)-Color.red(b),dg=Color.green(a)-Color.green(b),db=Color.blue(a)-Color.blue(b);
        return (int)Math.sqrt(dr*dr+dg*dg+db*db);
    }
    private static int average(int a,int b,int c,int d){
        return Color.rgb((Color.red(a)+Color.red(b)+Color.red(c)+Color.red(d))/4,
            (Color.green(a)+Color.green(b)+Color.green(c)+Color.green(d))/4,
            (Color.blue(a)+Color.blue(b)+Color.blue(c)+Color.blue(d))/4);
    }
}
