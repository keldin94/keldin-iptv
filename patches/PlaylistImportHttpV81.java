package com.keldin.iptv.net;

import java.io.FilterInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.NoRouteToHostException;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.net.URLConnection;
import java.util.Locale;
import java.util.zip.GZIPInputStream;

/**
 * First use the existing downloader (preserves compatibility with playlists
 * already working), then retry transport/connect failures with longer timeouts.
 * Never rewrite provider URLs or put credentials into diagnostics.
 */
public final class PlaylistImportHttpV81 {
    private PlaylistImportHttpV81(){}

    public static InputStream open(String playlistUrl,String userAgent,long maxBytes)throws IOException {
        IOException original;
        try {
            return PlaylistSync.open(playlistUrl,userAgent,maxBytes);
        }catch(IOException e){
            if(!retryable(e))throw e;
            original=e;
        }
        IOException last=original;
        for(int attempt=0;attempt<2;attempt++){
            try {
                int timeout=attempt==0?30000:45000;
                String agent=attempt==0?userAgent:"Mozilla/5.0 (Linux; Android 11; Android TV) KeldinIPTV/0.8.1";
                return connect(playlistUrl,agent,timeout,60000,maxBytes);
            }catch(IOException e){
                last=e;
                if(!retryable(e))throw e;
            }
        }
        throw new IOException("IPTV server connection timed out after retries. "
            +"Check whether the provider allows a fresh playlist download from this device. "
            +"The playlist address has not been changed.",last);
    }

    private static boolean retryable(IOException error){
        if(error instanceof SocketTimeoutException ||
           error instanceof ConnectException ||
           error instanceof NoRouteToHostException ||
           error instanceof SocketException) return true;
        Throwable cause=error.getCause();
        while(cause!=null){
            if(cause instanceof SocketTimeoutException ||
               cause instanceof ConnectException ||
               cause instanceof NoRouteToHostException ||
               cause instanceof SocketException)return true;
            cause=cause.getCause();
        }
        String message=error.getMessage();
        if(message==null)return false;
        String lower=message.toLowerCase(Locale.ROOT);
        return lower.contains("timed out") ||
               lower.contains("failed to connect") ||
               lower.contains("connection reset") ||
               lower.contains("network unreachable");
    }

    private static InputStream connect(String raw,String agent,int connectMs,int readMs,long maxBytes)
            throws IOException {
        URL url=new URL(raw);
        for(int hops=0;hops<5;hops++){
            String scheme=url.getProtocol().toLowerCase(Locale.ROOT);
            if(!"http".equals(scheme)&&!"https".equals(scheme))
                throw new IOException("Only HTTP or HTTPS playlist URLs are supported.");
            URLConnection rawConn=url.openConnection();
            if(!(rawConn instanceof HttpURLConnection))
                throw new IOException("Unexpected IPTV protocol.");
            HttpURLConnection conn=(HttpURLConnection)rawConn;
            conn.setInstanceFollowRedirects(false);
            conn.setConnectTimeout(connectMs);
            conn.setReadTimeout(readMs);
            conn.setUseCaches(false);
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept","*/*");
            conn.setRequestProperty("Accept-Encoding","gzip");
            conn.setRequestProperty("Connection","close");
            conn.setRequestProperty("User-Agent",
                agent==null||agent.trim().isEmpty()?
                "Mozilla/5.0 (Linux; Android TV) KeldinIPTV/0.8.1":agent);
            int code;
            try{
                code=conn.getResponseCode();
            }catch(IOException e){
                conn.disconnect();
                throw e;
            }
            if(code==301||code==302||code==303||code==307||code==308){
                String location=conn.getHeaderField("Location");
                conn.disconnect();
                if(location==null||location.isEmpty())
                    throw new IOException("IPTV server redirected without a destination.");
                url=new URL(url,location);
                continue;
            }
            if(code!=200){
                conn.disconnect();
                throw new IOException("IPTV server returned HTTP "+code+
                    ". Verify that the playlist URL is active.");
            }
            long length=conn.getContentLengthLong();
            if(length>maxBytes){
                conn.disconnect();
                throw new IOException("Playlist exceeds permitted download size.");
            }
            InputStream body;
            try{
                body=conn.getInputStream();
                if("gzip".equalsIgnoreCase(conn.getContentEncoding()))
                    body=new GZIPInputStream(body);
            }catch(IOException e){
                conn.disconnect();
                throw e;
            }
            final HttpURLConnection owned=conn;
            return new FilterInputStream(body){
                @Override public void close()throws IOException{
                    try{super.close();}finally{owned.disconnect();}
                }
            };
        }
        throw new IOException("IPTV server redirected too many times.");
    }
}
