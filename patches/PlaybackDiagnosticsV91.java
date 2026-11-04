package com.keldin.iptv.playback;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.SystemClock;
import androidx.media3.common.Player;
import androidx.media3.common.PlaybackException;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.analytics.AnalyticsListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/** Local-only diagnostics. Never stores stream URLs, playlist credentials or tokens. */
public final class PlaybackDiagnosticsV91 {
    private static final String PREFS="keldin_playback_diagnostics";
    private static final String KEY="events";
    private PlaybackDiagnosticsV91(){}

    public static synchronized void record(Context ctx,String event){
        if(ctx==null)return;
        String safe=event==null?"Unknown":event
            .replaceAll("(?i)https?://\\S+","[URL redacted]")
            .replaceAll("(?i)(password|username|token)=[^&\\s]+","$1=[redacted]");
        String time=new SimpleDateFormat("HH:mm:ss",Locale.ROOT).format(new Date());
        SharedPreferences prefs=ctx.getApplicationContext().getSharedPreferences(PREFS,Context.MODE_PRIVATE);
        String previous=prefs.getString(KEY,"");
        String history=previous+(time+"  "+safe+"\n");
        if(history.length()>8000){
            int index=history.indexOf('\n',history.length()-8000);
            history=history.substring(index>=0?index+1:history.length()-8000);
        }
        prefs.edit().putString(KEY,history).apply();
    }

    public static void watch(Context context,ExoPlayer player){
        final Context ctx=context.getApplicationContext();
        record(ctx,"New player session");
        player.addListener(new Player.Listener(){
            long bufferingSince=0;
            @Override public void onPlaybackStateChanged(int state){
                if(state==Player.STATE_BUFFERING){
                    bufferingSince=SystemClock.elapsedRealtime();
                    record(ctx,"BUFFERING started");
                }else if(state==Player.STATE_READY){
                    if(bufferingSince>0){
                        long delta=SystemClock.elapsedRealtime()-bufferingSince;
                        record(ctx,"READY after "+delta+" ms buffering");
                        bufferingSince=0;
                    }else record(ctx,"READY");
                }else if(state==Player.STATE_ENDED){
                    record(ctx,"Playback ended");
                }else if(state==Player.STATE_IDLE){
                    record(ctx,"Player idle");
                }
            }
            @Override public void onPlayerError(PlaybackException error){
                record(ctx,"PLAYER ERROR "+error.getErrorCodeName());
            }
            @Override public void onPositionDiscontinuity(
                Player.PositionInfo oldPosition,Player.PositionInfo newPosition,int reason){
                long delta=newPosition.positionMs-oldPosition.positionMs;
                record(ctx,"POSITION JUMP "+delta+" ms, reason="+reason);
            }
        });
        player.addAnalyticsListener(new AnalyticsListener(){
            @Override public void onDroppedVideoFrames(
                AnalyticsListener.EventTime eventTime,int frames,long elapsedMs){
                if(frames>=4)record(ctx,"DROPPED FRAMES "+frames+" in "+elapsedMs+" ms");
            }
        });
    }

    public static synchronized String report(Context ctx){
        String events=ctx.getApplicationContext().getSharedPreferences(PREFS,Context.MODE_PRIVATE)
            .getString(KEY,"");
        if(events==null||events.trim().isEmpty())
            return "No playback events recorded yet. Play a live channel, then check again.";
        return "Recent playback events (local times):\n\n"+events;
    }
}
