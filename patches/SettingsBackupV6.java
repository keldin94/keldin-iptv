package com.keldin.iptv.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;
import org.json.JSONObject;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/** Backup deliberately excludes credentials, M3U/Xtream URLs, cached catalogue and parental PINs. */
public final class SettingsBackupV6 {
    private static final String[] INTS={"accent","font_scale","panel_opacity","buffer","guide_offset"};
    private static final String[] BOOLEANS={"startup_last","retry","remember"};
    private SettingsBackupV6(){}
    public static void write(Context ctx,Uri dest)throws Exception{
        SharedPreferences p=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE);
        JSONObject o=new JSONObject();
        o.put("schema","keldin-settings-v6");
        o.put("ui_lang",p.getString("ui_lang","en"));
        for(String k:INTS)o.put(k,p.getInt(k,0));
        for(String k:BOOLEANS)o.put(k,p.getBoolean(k,true));
        try(OutputStream stream=ctx.getContentResolver().openOutputStream(dest)){
            if(stream==null)throw new java.io.IOException("Destination unavailable");
            stream.write(o.toString(2).getBytes(StandardCharsets.UTF_8));
        }
    }
    public static void read(Context ctx,Uri source)throws Exception{
        byte[] raw=new byte[32768];
        int off=0;
        try(InputStream stream=ctx.getContentResolver().openInputStream(source)){
            if(stream==null)throw new java.io.IOException("File unavailable");
            while(off<raw.length){
                int n=stream.read(raw,off,raw.length-off);
                if(n<0)break;
                if(n==0)continue;
                off+=n;
            }
            if(off>=raw.length||stream.read()!=-1)
                throw new java.io.IOException("Invalid backup size");
        }
        JSONObject j=new JSONObject(new String(raw,0,off,StandardCharsets.UTF_8));
        if(!"keldin-settings-v6".equals(j.optString("schema")))
            throw new java.io.IOException("Not a compatible settings backup");
        SharedPreferences.Editor e=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE).edit();
        if(j.has("ui_lang"))e.putString("ui_lang",j.getString("ui_lang"));
        for(String k:INTS)if(j.has(k))e.putInt(k,j.getInt(k));
        for(String k:BOOLEANS)if(j.has(k))e.putBoolean(k,j.getBoolean(k));
        e.apply();
    }
}
