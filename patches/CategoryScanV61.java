package com.keldin.iptv.net;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * Memory-bounded first pass. No Channel objects are stored; only category counts.
 * The actual playlist is parsed from the same local temp file AFTER selection.
 */
public final class CategoryScanV61 {
    public interface Progress { void update(long entries); }
    public final LinkedHashMap<String,Integer> liveGroups=new LinkedHashMap<>();
    public final int[] kinds=new int[4]; // LIVE, MOVIES, SERIES, RADIO
    public long total;

    private CategoryScanV61(){}
    private static int classify(String group,String url){
        String g=group.toLowerCase(Locale.ROOT);
        String u=url.toLowerCase(Locale.ROOT);
        if(g.contains("radio")||g.contains("radij")||g.contains("fm stanice")||
           u.contains("/radio/")||u.endsWith(".mp3")||u.contains(".mp3?")||
           u.endsWith(".aac")||u.contains(".aac?"))return 3;
        if(u.contains("/series/")||g.contains("series")||g.contains("serij")||
           g.contains("tv show")||g.contains("episode"))return 2;
        if(u.contains("/movie/")||g.contains("film")||g.contains("movie")||
           g.contains("vod")||g.contains("kino"))return 1;
        return 0;
    }
    private static String group(String extinf){
        String lower=extinf.toLowerCase(Locale.ROOT);
        int index=lower.indexOf("group-title=");
        if(index<0)return "Uncategorized";
        int begin=index+"group-title=".length();
        if(begin>=extinf.length())return "Uncategorized";
        char delimiter=extinf.charAt(begin);
        if(delimiter=='"'||delimiter=='\''){
            int end=extinf.indexOf(delimiter,begin+1);
            if(end>begin+1)return extinf.substring(begin+1,end).trim();
        }
        int end=begin;
        while(end<extinf.length()&&!Character.isWhitespace(extinf.charAt(end)))end++;
        String raw=extinf.substring(begin,end).trim();
        return raw.isEmpty()?"Uncategorized":raw;
    }
    public static CategoryScanV61 scan(File file,Progress progress)throws IOException{
        CategoryScanV61 result=new CategoryScanV61();
        try(BufferedReader input=new BufferedReader(new InputStreamReader(
                new FileInputStream(file),StandardCharsets.UTF_8),65536)){
            String line,group="Uncategorized";
            boolean pending=false;
            while((line=input.readLine())!=null){
                if(line.startsWith("#EXTINF")){
                    group=group(line);
                    pending=true;
                }else if(pending&&!line.isEmpty()&&!line.startsWith("#")){
                    int kind=classify(group,line.trim());
                    result.kinds[kind]++;
                    result.total++;
                    if(kind==0)result.liveGroups.merge(group,1,Integer::sum);
                    if(progress!=null&&result.total%1000==0)progress.update(result.total);
                    pending=false;
                }
            }
        }
        if(progress!=null)progress.update(result.total);
        return result;
    }
}
