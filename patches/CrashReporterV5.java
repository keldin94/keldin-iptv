package com.keldin.iptv.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Process;
import java.util.Locale;

/** Local crash summary; does not upload user data or store IPTV URLs or passwords. */
public final class CrashReporter {
    private static volatile boolean installed;
    private static final String PREFS="keldin_diagnostics";
    private static final String KEY="last_crash";
    private CrashReporter(){}

    public static synchronized void install(Context context){
        if(installed)return;
        installed=true;
        Context app=context.getApplicationContext();
        Thread.UncaughtExceptionHandler prior=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,error)->{
            try{
                String type=error.getClass().getSimpleName();
                String place="nepoznato";
                StackTraceElement[] stack=error.getStackTrace();
                if(stack!=null&&stack.length>0){
                    StackTraceElement first=stack[0];
                    place=first.getClassName()+"."+first.getMethodName()+":"+first.getLineNumber();
                }
                // Never store exception.message: URLs may carry IPTV credentials.
                app.getSharedPreferences(PREFS,Context.MODE_PRIVATE).edit()
                    .putString(KEY,type+" | "+place)
                    .putLong("last_crash_time",System.currentTimeMillis())
                    .commit();
            }catch(Throwable ignored){}
            if(prior!=null){prior.uncaughtException(thread,error);}
            else {Process.killProcess(Process.myPid());System.exit(10);}
        });
    }
    public static String summary(Context ctx){
        String r=ctx.getSharedPreferences(PREFS,Context.MODE_PRIVATE).getString(KEY,"");
        return r.isEmpty()?"Nije zabilježena programska greška":"Posljednja greška je zabilježena";
    }
    public static String details(Context ctx){
        SharedPreferences p=ctx.getSharedPreferences(PREFS,Context.MODE_PRIVATE);
        String event=p.getString(KEY,"");
        if(event.isEmpty())return "Nema evidentirane fatalne Java greške u ovoj verziji. Ako Android sam ugasi aplikaciju zbog nedostatka memorije ili je proces prinudno zaustavljen, možda neće biti zapisa. Za pouzdan uzrok potreban je Android logcat.";
        long time=p.getLong("last_crash_time",0);
        return "Zadnje iznenadno zatvaranje:\\n"+event+
            "\\n\\nVrijeme: "+(time>0?new java.text.SimpleDateFormat("dd.MM.yyyy HH:mm",Locale.getDefault()).format(new java.util.Date(time)):"nepoznato")+
            "\\n\\nNema snimanja M3U URL-a ili pristupnih podataka. Ako se aplikacija samo zatvara bez ove greške, provjeri slobodnu memoriju uređaja ili pošalji logcat.";
    }
}
