package com.keldin.iptv.updates;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Independent of Android: version validation and ordering for published releases. */
public final class UpdateVersion {
    private static final Pattern PATTERN=Pattern.compile("^v?(\\d+)\\.(\\d+)\\.(\\d+)(?:[+-].*)?$");
    private UpdateVersion(){}

    public static int compare(String candidate,String installed){
        int[] a=parse(candidate),b=parse(installed);
        if(a==null || b==null)throw new IllegalArgumentException("Invalid version");
        for(int i=0;i<3;i++){
            int cmp=Integer.compare(a[i],b[i]);
            if(cmp!=0)return cmp;
        }
        return 0;
    }
    public static int[] parse(String value){
        if(value==null)return null;
        Matcher m=PATTERN.matcher(value.trim());
        if(!m.matches())return null;
        try{
            return new int[]{Integer.parseInt(m.group(1)),
                Integer.parseInt(m.group(2)),Integer.parseInt(m.group(3))};
        }catch(NumberFormatException e){return null;}
    }
}
