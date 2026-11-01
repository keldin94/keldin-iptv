package com.keldin.iptv.ui;

import android.app.Activity;
import android.app.AlertDialog;
import com.keldin.iptv.data.Channel;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.function.Consumer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Detects conventional S01E02 / 1x02 episode markers when supplied by the IPTV playlist. */
public final class SeriesBrowserV6 {
    private SeriesBrowserV6(){}
    private static final Pattern S_E=Pattern.compile("(?i)(?:^|[ ._\\-])s(\\d{1,2})[ ._\\-]*e(\\d{1,3})\\b");
    private static final Pattern X=Pattern.compile("(?i)(?:^|[ ._\\-])(\\d{1,2})x(\\d{1,3})\\b");

    private static Matcher marker(String name){
        Matcher first=S_E.matcher(name);
        if(first.find())return first;
        Matcher other=X.matcher(name);
        return other.find()?other:null;
    }
    private static int season(Channel item){
        Matcher m=marker(item.name);
        return m==null?0:Integer.parseInt(m.group(1));
    }
    private static int episode(Channel item){
        Matcher m=marker(item.name);
        return m==null?0:Integer.parseInt(m.group(2));
    }
    private static String base(Channel item){
        Matcher marker=marker(item.name);
        return marker==null?item.name:item.name.substring(0,marker.start()).trim();
    }
    public static List<Channel> unique(List<Channel> episodes){
        LinkedHashMap<String,Channel> map=new LinkedHashMap<>();
        for(Channel c:episodes){
            String key=c.sourceId+"|"+c.group+"|"+base(c).toLowerCase(Locale.ROOT);
            map.putIfAbsent(key,c);
        }
        return new ArrayList<>(map.values());
    }
    public static void open(Activity activity, List<Channel> catalog,
                            Channel selected, Consumer<Channel> start){
        String title=base(selected);
        ArrayList<Channel> matches=new ArrayList<>();
        for(Channel c:catalog)if("SERIES".equals(c.kind)&&c.sourceId.equals(selected.sourceId)
            && c.group.equals(selected.group)&&base(c).equalsIgnoreCase(title))
            matches.add(c);
        if(matches.size()<2){start.accept(selected);return;}
        matches.sort(Comparator.comparingInt(SeriesBrowserV6::season)
            .thenComparingInt(SeriesBrowserV6::episode));
        Map<Integer,List<Channel>> seasons=new LinkedHashMap<>();
        for(Channel c:matches)
            seasons.computeIfAbsent(season(c),x->new ArrayList<>()).add(c);
        String[] names=new String[seasons.size()];
        int i=0;
        for(Map.Entry<Integer,List<Channel>> e:seasons.entrySet())
            names[i++]=e.getKey()==0?"Episodes ("+e.getValue().size()+")":
                "Season "+e.getKey()+" · "+e.getValue().size()+" episodes";
        final ArrayList<List<Channel>> options=new ArrayList<>(seasons.values());
        new AlertDialog.Builder(activity).setTitle(title).setItems(names,(d,chosen)->{
            List<Channel> entries=options.get(chosen);
            String[] labels=new String[entries.size()];
            for(int j=0;j<entries.size();j++){
                Channel c=entries.get(j);
                labels[j]=episode(c)>0?"Episode "+episode(c)+" · "+c.name:c.name;
            }
            new AlertDialog.Builder(activity).setTitle(title).setItems(labels,
                (dd,selection)->start.accept(entries.get(selection)))
                .setNegativeButton("Back",null).show();
        }).setNegativeButton("Close",null).show();
    }
}
