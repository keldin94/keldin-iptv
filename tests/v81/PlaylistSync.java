package com.keldin.iptv.net;
import java.io.IOException;
import java.io.InputStream;
import java.net.SocketTimeoutException;
/** Simulates the original 15-second network client timing out. */
public final class PlaylistSync {
    public static InputStream open(String u,String a,long size)throws IOException{
        throw new SocketTimeoutException("original attempt timed out (test)");
    }
}
