package com.keldin.iptv.net;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Handler;
import android.os.Looper;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import com.keldin.iptv.data.CatalogStore;
import com.keldin.iptv.data.Channel;
import com.keldin.iptv.data.PlaylistSource;
import com.keldin.iptv.ui.Ui;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FilterInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * v0.6.1 two-pass, one-download import:
 * 1) stream the server response to a bounded local temp file,
 * 2) scan categories without allocating a Channel per item,
 * 3) let the viewer exclude countries,
 * 4) parse and persist ONLY selected streams.
 * Explicit limits protect low-memory TV boxes without rejecting lists solely due to total item count.
 */
public final class PlaylistWizardV6 {
    public interface Complete { void finished(boolean success,String message); }
    private static final String[] KINDS={"LIVE","MOVIES","SERIES","RADIO"};
    private static final int MAX_SELECTED=150000;
    private static final long MAX_BYTES=200_000_000L;
    private final Activity activity;
    private final CatalogStore store;
    private final PlaylistSource source;
    private final Complete done;
    private final Handler ui=new Handler(Looper.getMainLooper());
    private final ExecutorService executor=Executors.newSingleThreadExecutor();
    private AlertDialog progress;
    private TextView phase,details;
    private ProgressBar bar;
    private File tempFile;
    private long lastTick;
    private volatile long bytes;
    private volatile long processed;

    public PlaylistWizardV6(Activity activity,CatalogStore store,PlaylistSource src,Complete done){
        this.activity=activity;this.store=store;this.source=src;this.done=done;
    }
    private String t(String en,String bs){
        return "bs".equals(store.language())?bs:en;
    }
    public void start(){
        showProgress();
        setPhase(t("1/3 · Downloading playlist","1/3 · Preuzimanje liste"),
            t("Connecting to the server…","Povezivanje sa serverom…"));
        executor.execute(()->{
            try{
                tempFile=File.createTempFile("keldin-import-", ".m3u",activity.getCacheDir());
                long free=activity.getCacheDir().getUsableSpace();
                if(free<16_000_000L)throw new IOException("Not enough free storage. Clear the Android TV cache.");
                try(InputStream in=PlaylistSync.open(source.playlistUrl(),source.userAgent,MAX_BYTES);
                    FileOutputStream output=new FileOutputStream(tempFile)){
                    byte[] buffer=new byte[32768];
                    int count;
                    while((count=in.read(buffer))!=-1){
                        bytes+=count;
                        if(bytes>MAX_BYTES || bytes>free-8_000_000L)
                            throw new IOException("Playlist exceeds safe device storage. Free space or use a smaller playlist.");
                        output.write(buffer,0,count);
                        tick("Downloading",bytes,0);
                    }
                }
                setPhase(t("2/3 · Discovering categories","2/3 · Prepoznavanje kategorija"),
                    t("Scanning TV, movies, series and radio…","Prepoznajem TV, filmove, serije i radio…"));
                CategoryScanV61 categories=CategoryScanV61.scan(tempFile,n->{
                    processed=n;
                    tick("Scanning",bytes,n);
                });
                if(categories.total==0)
                    throw new IOException("No valid M3U items found. Check the URL or playlist format.");
                ui.post(()->choose(categories,null));
            }catch(Exception e){
                fail(e.getMessage()==null?"Import failed. Check the M3U URL and network.":e.getMessage());
            }
        });
    }
    private void tick(String stage,long amount,long entries){
        long time=System.currentTimeMillis();
        if(time-lastTick<500)return;
        lastTick=time;
        ui.post(()->{
            if(progress==null||!progress.isShowing())return;
            if("Downloading".equals(stage))
                details.setText(String.format(Locale.ROOT,"Downloaded: %.1f MB",amount/1048576.0));
            else details.setText(String.format(Locale.ROOT,
                "Scanned: %,d entries  ·  File: %.1f MB",entries,amount/1048576.0));
        });
    }
    private void showProgress(){
        if(activity.isFinishing()||activity.isDestroyed())return;
        LinearLayout content=Ui.vertical(activity);
        content.setPadding(Ui.dp(activity,24),Ui.dp(activity,18),
            Ui.dp(activity,24),Ui.dp(activity,20));
        phase=Ui.text(activity,"Preparing…",19,Ui.WHITE,true);
        details=Ui.text(activity,"",13,Ui.MUTED,false);
        bar=new ProgressBar(activity,null,android.R.attr.progressBarStyleHorizontal);
        bar.setIndeterminate(true);
        content.addView(phase);
        content.addView(Ui.space(activity,12));
        content.addView(bar,Ui.lp(activity,-1,6));
        content.addView(Ui.space(activity,14));
        content.addView(details);
        progress=new AlertDialog.Builder(activity)
            .setTitle("KELDIN IPTV · Playlist import")
            .setCancelable(false).setView(content).create();
        progress.show();
    }
    private void setPhase(String headline,String info){
        ui.post(()->{
            if(progress!=null&&progress.isShowing()){
                phase.setText(headline);details.setText(info);
            }
        });
    }
    private void closeProgress(){
        if(progress!=null&&progress.isShowing())progress.dismiss();
        progress=null;
    }
    private void choose(CategoryScanV61 scan,String warning){
        if(activity.isFinishing()||activity.isDestroyed()){cleanup();return;}
        closeProgress();
        List<String> groups=new ArrayList<>(scan.liveGroups.keySet());
        Collections.sort(groups,String.CASE_INSENSITIVE_ORDER);
        Set<String> old=store.excludedGroups(source.id);
        String[] kindNames={"Live TV","Movies","Series","Radio"};
        String[] labels=new String[4+groups.size()];
        boolean[] enabled=new boolean[labels.length];
        for(int i=0;i<4;i++){
            labels[i]=kindNames[i]+"  ("+scan.kinds[i]+")";
            enabled[i]=!old.contains("@kind:"+KINDS[i]);
        }
        boolean huge=scan.total>MAX_SELECTED;
        for(int i=0;i<groups.size();i++){
            String name=groups.get(i);
            labels[i+4]=name+"  ("+scan.liveGroups.get(name)+")";
            boolean local=name.toLowerCase(Locale.ROOT).matches(".*(ex.?yu|bosn|bih|hrvatsk|srbija|serbia|crna gora|montenegro|sloveni|sport).*");
            // When huge, avoid importing every foreign live country by default.
            enabled[i+4]=old.isEmpty() ? (!huge||local) : !old.contains(name);
            if(CatalogStore.isAdultCategory(name) && old.isEmpty())enabled[i+4]=false;
        }
        String explanation="Select the countries and categories you watch. "+
            "Only selected content is saved to the device. You can change this later in playlist settings.";
        if(huge)explanation+="\n\nLarge playlist ("+scan.total+" entries). Non-local TV groups are unchecked by default to reduce memory use.";
        if(warning!=null)explanation+="\n\n"+warning;
        new AlertDialog.Builder(activity)
            .setTitle("3/3 · Choose countries and content")
            .setMessage(explanation)
            .setMultiChoiceItems(labels,enabled,(dialog,index,checked)->enabled[index]=checked)
            .setPositiveButton("Save selected",(dialog,which)->{
                Set<String> excluded=new HashSet<>();
                for(int i=0;i<4;i++)if(!enabled[i])excluded.add("@kind:"+KINDS[i]);
                for(int i=0;i<groups.size();i++)if(!enabled[4+i])excluded.add(groups.get(i));
                long estimated=0;
                for(int i=0;i<4;i++)if(enabled[i])estimated+=scan.kinds[i];
                for(int i=0;i<groups.size();i++)
                    if(!enabled[4+i]&&enabled[0])estimated-=scan.liveGroups.get(groups.get(i));
                if(estimated>MAX_SELECTED){
                    choose(scan,"Selected "+estimated+" items, but this TV can import at most "+
                        MAX_SELECTED+" at once. Disable additional countries or media sections.");
                    return;
                }
                if(estimated<=0){
                    choose(scan,"Select at least one category or country.");
                    return;
                }
                save(scan,excluded);
            })
            .setNegativeButton("Cancel",(dialog,which)->complete(false,"Import cancelled."))
            .setCancelable(false).show();
    }
    private void save(CategoryScanV61 scan,Set<String> excluded){
        showProgress();
        setPhase(t("3/3 · Saving selected channels","3/3 · Spremanje odabranih kanala"),
            t("Filtering content and saving your local library…",
                "Filtriram sadržaj i spremam lokalnu biblioteku…"));
        executor.execute(()->{
            try(BufferedReader reader=new BufferedReader(new InputStreamReader(
                    new FileInputStream(tempFile),StandardCharsets.UTF_8),65536)){
                M3uParser.Result chosen=M3uParser.parse(reader,source.id,source.playlistUrl(),
                    n->{processed=n;tick("Scanning",bytes,n);},channel->
                        !excluded.contains("@kind:"+channel.kind) &&
                        (!"LIVE".equals(channel.kind)||!excluded.contains(channel.group)));
                if(chosen.channels.isEmpty())throw new IOException("No items match the selected categories.");
                if(chosen.channels.size()>MAX_SELECTED)
                    throw new IOException("Too many selected streams; exclude additional categories.");
                // Save the list and category preference only after a successful parse.
                source.lastUpdated=System.currentTimeMillis();
                if(source.epgUrl.isEmpty()&&!chosen.epgUrl.isEmpty())source.epgUrl=chosen.epgUrl;
                store.updateChannels(source.id,chosen.channels);
                store.putSource(source);
                store.setExcludedGroups(source.id,excluded);
                int[] count={0,0,0,0};
                for(Channel c:chosen.channels){
                    for(int j=0;j<KINDS.length;j++)
                        if(KINDS[j].equals(c.kind)){count[j]++;break;}
                }
                String message="Imported "+chosen.channels.size()+" items: "+
                    count[0]+" TV, "+count[1]+" movies, "+count[2]+" series, "+count[3]+" radio.";
                ui.post(()->complete(true,message));
            }catch(Exception e){
                String err=e.getMessage()==null?"Failed to save playlist.":e.getMessage();
                if(err.contains("Too many") || err.contains("selected"))
                    ui.post(()->choose(scan,err));
                else fail(err);
            }
        });
    }
    private void fail(String message){ui.post(()->complete(false,message));}
    private void cleanup(){
        if(tempFile!=null){tempFile.delete();tempFile=null;}
        executor.shutdown();
    }
    private void complete(boolean success,String text){
        closeProgress();
        cleanup();
        if(activity.isFinishing()||activity.isDestroyed())return;
        new AlertDialog.Builder(activity)
            .setTitle(success?"Playlist imported":"Import failed")
            .setMessage(text)
            .setPositiveButton("OK",(dialog,which)->done.finished(success,text))
            .show();
    }
}
