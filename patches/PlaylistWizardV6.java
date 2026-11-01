package com.keldin.iptv.net;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Handler;
import android.os.Looper;
import android.text.TextUtils;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import com.keldin.iptv.data.CatalogStore;
import com.keldin.iptv.data.Channel;
import com.keldin.iptv.data.PlaylistSource;
import com.keldin.iptv.ui.Ui;
import java.io.BufferedReader;
import java.io.FilterInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Three-stage import: download/parse -> choose included countries -> save.
 * All blocking I/O, large catalog serialization and filtering run off the UI thread.
 * Actual percentage is deliberately not invented for chunked or gzipped streams.
 */
public final class PlaylistWizardV6 {
    public interface Complete { void finished(boolean success,String message); }
    private static final String[] KINDS={"LIVE","MOVIES","SERIES","RADIO"};
    private final Activity activity;
    private final CatalogStore store;
    private final PlaylistSource source;
    private final Complete done;
    private final Handler ui=new Handler(Looper.getMainLooper());
    private final ExecutorService executor=Executors.newSingleThreadExecutor();
    private AlertDialog progress;
    private TextView phase,details;
    private ProgressBar bar;
    private long lastProgress;
    private volatile int parsed;
    private volatile long bytes;

    public PlaylistWizardV6(Activity activity,CatalogStore store,PlaylistSource src,Complete done){
        this.activity=activity;this.store=store;this.source=src;this.done=done;
    }

    public void start(){
        showProgress();
        setPhase("1/3 · Povezivanje sa serverom","Provjeravam adresu i dostupnost liste...");
        executor.execute(()->{
            try(InputStream in=PlaylistSync.open(source.playlistUrl(),source.userAgent,70_000_000L)){
                setPhase("2/3 · Preuzimanje i analiza","Brojim kanale i prepoznajem kategorije...");
                FilterInputStream counting=new FilterInputStream(in){
                    @Override public int read() throws IOException {
                        int value=super.read();if(value>=0)onBytes(1);return value;
                    }
                    @Override public int read(byte[] out,int offset,int len)throws IOException{
                        int n=super.read(out,offset,len);if(n>0)onBytes(n);return n;
                    }
                };
                M3uParser.Result parsedList=M3uParser.parse(
                    new InputStreamReader(counting,StandardCharsets.UTF_8),source.id,source.playlistUrl(),
                    n->{parsed=n;progressTick();});
                if(parsedList.channels.isEmpty())throw new IOException("Nema podržanih kanala. Provjeri M3U adresu.");
                ui.post(()->chooseCategories(parsedList));
            }catch(Exception e){
                String msg=e.getMessage()==null?"Lista nije učitana.":e.getMessage();
                fail(msg);
            }
        });
    }
    private void onBytes(int count){bytes+=count;progressTick();}
    private void progressTick(){
        long now=System.currentTimeMillis();
        if(now-lastProgress<450)return;
        lastProgress=now;
        long b=bytes;int n=parsed;
        ui.post(()->{
            if(progress!=null&&progress.isShowing()){
                details.setText(String.format(java.util.Locale.ROOT,
                    "Preuzeto: %.1f MB   ·   Prepoznato: %,d stavki",
                    b/(1024.0*1024.0),n));
            }
        });
    }
    private void showProgress(){
        LinearLayout block=Ui.vertical(activity);
        block.setPadding(Ui.dp(activity,27),Ui.dp(activity,20),
            Ui.dp(activity,27),Ui.dp(activity,20));
        phase=Ui.text(activity,"Priprema...",20,Ui.WHITE,true);
        details=Ui.text(activity,"",13,Ui.MUTED,false);
        bar=new ProgressBar(activity,null,android.R.attr.progressBarStyleHorizontal);
        bar.setIndeterminate(true);
        block.addView(phase);
        block.addView(Ui.space(activity,13));
        block.addView(bar,Ui.lp(activity,-1,5));
        block.addView(Ui.space(activity,15));
        block.addView(details);
        progress=new AlertDialog.Builder(activity)
            .setTitle("KELDIN IPTV · Uvoz liste")
            .setView(block)
            .setCancelable(false).create();
        progress.show();
    }
    private void setPhase(String a,String b){
        ui.post(()->{
            if(progress!=null&&progress.isShowing()){
                phase.setText(a);details.setText(b);
            }
        });
    }
    private void chooseCategories(M3uParser.Result result){
        if(activity.isFinishing())return;
        dismissProgress();
        LinkedHashMap<String,Integer> counts=new LinkedHashMap<>();
        int[] total={0,0,0,0};
        for(Channel channel:result.channels){
            int index=kindIndex(channel.kind);
            if(index<0)continue;
            total[index]++;
            if(index==0)counts.merge(channel.group,1,Integer::sum);
        }
        ArrayList<String> groups=new ArrayList<>(counts.keySet());
        Collections.sort(groups,String.CASE_INSENSITIVE_ORDER);

        Set<String> priorExcluded=store.excludedGroups(source.id);
        String[] choices=new String[KINDS.length+groups.size()];
        boolean[] checked=new boolean[choices.length];
        String[] kindLabels={"TV uživo","Filmovi","Serije","Radio"};
        for(int i=0;i<KINDS.length;i++){
            choices[i]=kindLabels[i]+"  ("+total[i]+")";
            checked[i]=!priorExcluded.contains("@kind:"+KINDS[i]);
        }
        for(int i=0;i<groups.size();i++){
            String group=groups.get(i);
            choices[4+i]="TV · "+group+"  ("+counts.get(group)+")";
            checked[4+i]=!priorExcluded.contains(group);
        }
        new AlertDialog.Builder(activity)
            .setTitle("3/3 · Odaberi šta želiš učitati")
            .setMessage("Isključi države i kategorije koje ne gledaš. "+
                "Neizabrani sadržaj neće biti upisan u lokalnu biblioteku. "+
                "Izbor možeš naknadno promijeniti u postavkama.")
            .setMultiChoiceItems(choices,checked,(dialog,index,selected)->checked[index]=selected)
            .setNegativeButton("Odustani",(d,w)->finish(false,"Uvoz otkazan."))
            .setPositiveButton("Sačuvaj odabrano",(d,w)->{
                Set<String> disabled=new HashSet<>();
                for(int i=0;i<4;i++)if(!checked[i])disabled.add("@kind:"+KINDS[i]);
                for(int i=0;i<groups.size();i++)if(!checked[i+4])disabled.add(groups.get(i));
                save(result,disabled);
            }).show();
    }
    private void save(M3uParser.Result result,Set<String> disabled){
        showProgress();
        setPhase("3/3 · Spremanje odabranog sadržaja","Optimiziram lokalnu biblioteku...");
        executor.execute(()->{
            try{
                ArrayList<Channel> included=new ArrayList<>();
                int[] kinds=new int[4];
                for(Channel c:result.channels){
                    if(disabled.contains("@kind:"+c.kind) || ("LIVE".equals(c.kind)&&disabled.contains(c.group)))continue;
                    included.add(c);
                    int i=kindIndex(c.kind);if(i>=0)kinds[i]++;
                }
                if(included.isEmpty())throw new IOException("Nema odabranih stavki.");
                store.setExcludedGroups(source.id,disabled);
                source.lastUpdated=System.currentTimeMillis();
                if(source.epgUrl.isEmpty()&&!result.epgUrl.isEmpty())
                    source.epgUrl=result.epgUrl;
                store.updateChannels(source.id,included);
                store.putSource(source);
                String summary="Učitano: "+included.size()+" · TV "+kinds[0]+
                    " · Filmovi "+kinds[1]+" · Serije "+kinds[2]+" · Radio "+kinds[3];
                ui.post(()->finish(true,summary));
            }catch(Exception e){fail(e.getMessage()==null?"Neuspješno spremanje":e.getMessage());}
        });
    }
    private void fail(String reason){ui.post(()->finish(false,"Greška: "+reason));}
    private void finish(boolean ok,String message){
        dismissProgress();
        executor.shutdown();
        if(activity.isFinishing())return;
        new AlertDialog.Builder(activity)
            .setTitle(ok?"Lista je spremna":"Uvoz nije završen")
            .setMessage(message)
            .setPositiveButton("U redu",(d,w)->done.finished(ok,message))
            .show();
    }
    private void dismissProgress(){
        if(progress!=null&&progress.isShowing())progress.dismiss();
    }
    private static int kindIndex(String kind){
        for(int i=0;i<KINDS.length;i++)if(KINDS[i].equals(kind))return i;
        return -1;
    }
}
