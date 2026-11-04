package com.keldin.iptv.updates;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import androidx.core.content.FileProvider;
import com.keldin.iptv.BuildConfig;
import com.keldin.iptv.ui.Ui;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Self-updater for APKs distributed directly from GitHub.
 * Only published non-prerelease versions of keldin94/keldin-iptv are considered.
 * Requires SAME applicationId and SAME release signing certificate across updates.
 * The operating system always asks the viewer to confirm installation.
 */
public final class AppUpdateManager {
    private static final String API="https://api.github.com/repos/keldin94/keldin-iptv/releases/latest";
    private static final String APK_NAME="keldin-iptv.apk";
    private static final long MAX_BYTES=150L*1024L*1024L;
    private static final long CHECK_INTERVAL=24L*60L*60L*1000L;
    private static final ExecutorService POOL=Executors.newSingleThreadExecutor();
    private static final Handler MAIN=new Handler(Looper.getMainLooper());
    private static final AtomicBoolean ACTIVE=new AtomicBoolean(false);
    private static final String PREFERENCES="keldin_updater";
    private AppUpdateManager(){}

    private static SharedPreferences prefs(Context ctx){
        return ctx.getApplicationContext().getSharedPreferences(PREFERENCES,Context.MODE_PRIVATE);
    }
    public static boolean automaticChecks(Context ctx){
        return prefs(ctx).getBoolean("auto_check",true);
    }
    public static void setAutomaticChecks(Context ctx,boolean enabled){
        prefs(ctx).edit().putBoolean("auto_check",enabled).apply();
    }
    public static void check(Activity activity,boolean manual){
        if(activity==null||activity.isFinishing()||activity.isDestroyed())return;
        if(BuildConfig.APPLICATION_ID.endsWith(".updatepreview")){
            if(manual)showMessage(activity,"Updater preview",
                "This is a test build. In-place updates require the signed stable app. "+
                "The stable app will preserve your playlists on future updates.");
            return;
        }
        if(!manual&&!automaticChecks(activity))return;
        long now=System.currentTimeMillis();
        if(!manual&&now-prefs(activity).getLong("last_check",0)<CHECK_INTERVAL)return;
        if(!ACTIVE.compareAndSet(false,true))return;
        prefs(activity).edit().putLong("last_check",now).apply();
        POOL.execute(()->{
            try{
                HttpURLConnection conn=openApi(API);
                int code=conn.getResponseCode();
                if(code==404){
                    if(manual)showMessage(activity,"No public updates",
                        "No signed public version is available yet. Test builds are not eligible for automatic updates.");
                    conn.disconnect();
                    return;
                }
                if(code!=200)throw new java.io.IOException("GitHub returned HTTP "+code);
                byte[] data=readLimited(conn.getInputStream(),256*1024);
                conn.disconnect();
                JSONObject release=new JSONObject(new String(data,StandardCharsets.UTF_8));
                if(release.optBoolean("draft",false)||release.optBoolean("prerelease",false)){
                    if(manual)showMessage(activity,"No public updates","Only stable signed versions can update this app.");
                    return;
                }
                String tag=release.optString("tag_name","");
                String version=tag.startsWith("v")?tag.substring(1):tag;
                if(UpdateVersion.parse(version)==null){
                    throw new java.io.IOException("Unrecognized release version");
                }
                if(UpdateVersion.compare(version,BuildConfig.VERSION_NAME)<=0){
                    if(manual)showMessage(activity,"Up to date",
                        "Keldin IPTV "+BuildConfig.VERSION_NAME+" is already the latest public version.");
                    return;
                }
                JSONArray assets=release.optJSONArray("assets");
                JSONObject target=null;
                if(assets!=null){
                    for(int i=0;i<assets.length();i++){
                        JSONObject asset=assets.optJSONObject(i);
                        if(asset!=null&&APK_NAME.equals(asset.optString("name"))){
                            target=asset;break;
                        }
                    }
                }
                if(target==null)throw new java.io.IOException("The release contains no signed APK");
                final String uri=target.optString("browser_download_url","");
                final String digest=target.optString("digest","");
                final long size=target.optLong("size",-1);
                final String notes=release.optString("body","").trim();
                if(!uri.startsWith("https://github.com/keldin94/keldin-iptv/releases/download/"))
                    throw new java.io.IOException("Untrusted update location");
                if(!digest.matches("sha256:[0-9a-fA-F]{64}")||size<1024||size>MAX_BYTES)
                    throw new java.io.IOException("Missing or invalid update checksum/size");
                if(!manual&&version.equals(prefs(activity).getString("dismissed_version","")))return;
                MAIN.post(()->{
                    if(activity.isFinishing()||activity.isDestroyed())return;
                    String intro="Version "+version+" is available.\n\nYour playlists, favorites and settings stay on this device.";
                    String excerpt=notes.isEmpty()?"":("\n\nWhat's new:\n"+
                        notes.substring(0,Math.min(notes.length(),900)));
                    new AlertDialog.Builder(activity)
                        .setTitle("Keldin IPTV update")
                        .setMessage(intro+excerpt)
                        .setPositiveButton("Download & install",(dialog,which)->
                            download(activity,version,uri,digest.substring(7),size))
                        .setNegativeButton("Later",(dialog,which)->
                            prefs(activity).edit().putString("dismissed_version",version).apply())
                        .show();
                });
            }catch(Exception e){
                if(manual){
                    String label=e.getMessage()==null?e.getClass().getSimpleName():e.getMessage();
                    showMessage(activity,"Update check failed",
                        label+"\n\nCheck your network connection and try again.");
                }
            }finally{
                ACTIVE.set(false);
            }
        });
    }
    private static void download(Activity activity,String version,String url,
                                 String sha256,long expectedSize){
        AtomicBoolean cancelled=new AtomicBoolean(false);
        LinearLayout layout=Ui.vertical(activity);
        layout.setPadding(Ui.dp(activity,24),Ui.dp(activity,14),
            Ui.dp(activity,24),Ui.dp(activity,20));
        TextView title=Ui.text(activity,"Downloading "+version,19,Ui.WHITE,true);
        ProgressBar bar=new ProgressBar(activity,null,android.R.attr.progressBarStyleHorizontal);
        bar.setMax(100);
        TextView label=Ui.text(activity,"Preparing secure download…",13,Ui.MUTED,false);
        layout.addView(title);
        layout.addView(Ui.space(activity,13));
        layout.addView(bar,Ui.lp(activity,-1,7));
        layout.addView(Ui.space(activity,11));
        layout.addView(label);
        AlertDialog dialog=new AlertDialog.Builder(activity)
            .setTitle("Software update")
            .setView(layout)
            .setNegativeButton("Cancel",(d,w)->cancelled.set(true))
            .setCancelable(false).create();
        dialog.show();
        POOL.execute(()->{
            File output=null;
            try{
                File directory=new File(activity.getCacheDir(),"updates");
                if(!directory.exists()&&!directory.mkdirs())
                    throw new java.io.IOException("Cannot create update directory");
                output=new File(directory,"keldin-update.apk");
                if(output.exists()&&!output.delete())
                    throw new java.io.IOException("Cannot replace old update file");
                URL trusted=new URL(url);
                if(!"https".equalsIgnoreCase(trusted.getProtocol())||
                    !"github.com".equalsIgnoreCase(trusted.getHost()))
                    throw new java.io.IOException("Update URL is not trusted");
                HttpURLConnection connection=(HttpURLConnection)trusted.openConnection();
                connection.setRequestProperty("User-Agent","KeldinIPTV-AndroidTV-Updater");
                connection.setConnectTimeout(15000);
                connection.setReadTimeout(30000);
                connection.setInstanceFollowRedirects(true);
                if(connection.getResponseCode()!=200){
                    int error=connection.getResponseCode();connection.disconnect();
                    throw new java.io.IOException("Download failed: HTTP "+error);
                }
                MessageDigest sha=MessageDigest.getInstance("SHA-256");
                long copied=0,lastUpdate=0;
                try(InputStream input=new BufferedInputStream(connection.getInputStream());
                    FileOutputStream stream=new FileOutputStream(output)){
                    byte[] bytes=new byte[32768];
                    int n;
                    while((n=input.read(bytes))!=-1){
                        if(cancelled.get())throw new java.io.IOException("Download cancelled");
                        copied+=n;
                        if(copied>MAX_BYTES||copied>expectedSize)
                            throw new java.io.IOException("Update exceeds expected size");
                        sha.update(bytes,0,n);
                        stream.write(bytes,0,n);
                        long current=System.currentTimeMillis();
                        if(current-lastUpdate>350){
                            int percentage=(int)(100*copied/Math.max(1,expectedSize));
                            long downloaded=copied;
                            MAIN.post(()->{
                                if(!activity.isFinishing()){
                                    bar.setProgress(percentage);
                                    label.setText(String.format(Locale.ROOT,
                                        "%d%%   ·   %.1f / %.1f MB",percentage,
                                        downloaded/1048576.0,expectedSize/1048576.0));
                                }
                            });
                            lastUpdate=current;
                        }
                    }
                    stream.getFD().sync();
                }finally{connection.disconnect();}
                if(copied!=expectedSize)
                    throw new java.io.IOException("Incomplete download. Please retry.");
                StringBuilder calculated=new StringBuilder();
                for(byte b:sha.digest())calculated.append(String.format(Locale.ROOT,"%02x",b&255));
                if(!sha256.equalsIgnoreCase(calculated.toString()))
                    throw new java.io.IOException("Update checksum mismatch");
                PackageManager pm=activity.getPackageManager();
                PackageInfo archive=pm.getPackageArchiveInfo(output.getAbsolutePath(),0);
                if(archive==null||!activity.getPackageName().equals(archive.packageName))
                    throw new java.io.IOException("APK package differs from installed app");
                if(UpdateVersion.compare(archive.versionName,BuildConfig.VERSION_NAME)<=0)
                    throw new java.io.IOException("Update version is not newer");
                File installedFile=output;
                MAIN.post(()->{
                    dialog.dismiss();
                    if(!cancelled.get()&&!activity.isFinishing()&&!activity.isDestroyed())
                        requestInstall(activity,installedFile);
                });
            }catch(Exception e){
                if(output!=null)output.delete();
                String message=e.getMessage()==null?e.getClass().getSimpleName():e.getMessage();
                MAIN.post(()->{
                    dialog.dismiss();
                    if(!cancelled.get())showMessage(activity,"Update failed",message);
                });
            }
        });
    }
    private static void requestInstall(Activity activity,File apk){
        if(Build.VERSION.SDK_INT>=Build.VERSION_CODES.O &&
            !activity.getPackageManager().canRequestPackageInstalls()){
            new AlertDialog.Builder(activity)
                .setTitle("Installation permission")
                .setMessage("Allow Keldin IPTV to install updates in Android settings. "+
                    "Then return to Keldin IPTV and choose Check for updates again.")
                .setPositiveButton("Open Android settings",(d,w)->{
                    try{
                        Intent settings=new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                            Uri.parse("package:"+activity.getPackageName()));
                        activity.startActivity(settings);
                    }catch(ActivityNotFoundException ex){
                        showMessage(activity,"Installation permission","Enable Install unknown apps for Keldin IPTV in Android settings.");
                    }
                }).setNegativeButton("Not now",null).show();
            return;
        }
        try{
            Uri file=FileProvider.getUriForFile(activity,
                activity.getPackageName()+".updateprovider",apk);
            Intent install=new Intent(Intent.ACTION_VIEW);
            install.setDataAndType(file,"application/vnd.android.package-archive");
            install.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            activity.startActivity(install);
        }catch(Exception error){
            showMessage(activity,"Cannot open Android installer",
                "Please enable app installation permissions and try again.");
        }
    }
    private static HttpURLConnection openApi(String uri)throws Exception{
        HttpURLConnection c=(HttpURLConnection)new URL(uri).openConnection();
        c.setRequestProperty("Accept","application/vnd.github+json");
        c.setRequestProperty("User-Agent","KeldinIPTV-AndroidTV-Updater");
        c.setConnectTimeout(12000);
        c.setReadTimeout(12000);
        return c;
    }
    private static byte[] readLimited(InputStream input,int limit)throws Exception{
        try(InputStream in=input;ByteArrayOutputStream out=new ByteArrayOutputStream()){
            byte[] buffer=new byte[4096];int n;
            while((n=in.read(buffer))!=-1){
                if(out.size()+n>limit)throw new java.io.IOException("Update response too large");
                out.write(buffer,0,n);
            }
            return out.toByteArray();
        }
    }
    private static void showMessage(Activity activity,String title,String message){
        MAIN.post(()->{
            if(activity.isFinishing()||activity.isDestroyed())return;
            new AlertDialog.Builder(activity).setTitle(title).setMessage(message)
                .setPositiveButton("OK",null).show();
        });
    }
}
