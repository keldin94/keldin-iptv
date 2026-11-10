package com.keldin.iptv.ui;

import android.content.Context;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.keldin.iptv.data.CatalogStore;
import com.keldin.iptv.data.PlaylistSource;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** One continuous list: playlist header, then only that playlist's categories. */
public final class PlaylistGroupAdapterV99
        extends RecyclerView.Adapter<PlaylistGroupAdapterV99.Holder> {
    public interface Select {
        void onSelect(String sourceId, String group);
        void onActivationChanged();
    }
    public static final String ALL = "Sve kategorije";
    private static final class Entry {
        String sourceId, group, title;
        int count;
        boolean header;
        Entry(String id,String group,String title,int count,boolean header){
            this.sourceId=id;this.group=group;this.title=title;
            this.count=count;this.header=header;
        }
    }
    private final Context context;
    private final CatalogStore store;
    private final Select select;
    private final List<PlaylistSource> sources;
    private final LinkedHashMap<String,LinkedHashMap<String,Integer>> groups;
    private final ArrayList<Entry> entries=new ArrayList<>();
    private String selectedSource,selectedGroup;

    public PlaylistGroupAdapterV99(Context context,CatalogStore store,
            List<PlaylistSource> sources,
            LinkedHashMap<String,LinkedHashMap<String,Integer>> groups,
            String selectedSource,String selectedGroup,Select select){
        this.context=context;this.store=store;this.sources=sources;
        this.groups=groups;this.selectedSource=selectedSource;
        this.selectedGroup=selectedGroup;this.select=select;
        rebuild();
    }

    private void rebuild(){
        entries.clear();
        for(PlaylistSource src:sources){
            boolean active=store.isPlaylistActiveV99(src.id);
            LinkedHashMap<String,Integer> categories=groups.get(src.id);
            int count=0;
            if(categories!=null)
                for(Integer value:categories.values())count+=value;
            entries.add(new Entry(src.id,null,src.name,count,true));
            if(!active||store.isPlaylistCollapsedV99(src.id))continue;
            entries.add(new Entry(src.id,ALL,"All channels",count,false));
            if(categories!=null)for(Map.Entry<String,Integer> item:categories.entrySet())
                entries.add(new Entry(src.id,item.getKey(),item.getKey(),item.getValue(),false));
        }
    }

    @NonNull @Override public Holder onCreateViewHolder(@NonNull ViewGroup parent,int viewType){
        LinearLayout view=Ui.vertical(context);
        view.setGravity(Gravity.CENTER_VERTICAL);
        view.setFocusable(true);view.setClickable(true);
        view.setMinimumHeight(Ui.dp(context,56));
        view.setPadding(Ui.dp(context,12),Ui.dp(context,8),
            Ui.dp(context,10),Ui.dp(context,8));
        RecyclerView.LayoutParams params=new RecyclerView.LayoutParams(
            -1,ViewGroup.LayoutParams.WRAP_CONTENT);
        params.bottomMargin=Ui.dp(context,3);
        view.setLayoutParams(params);
        TextView name=Ui.text(context,"",13,Ui.WHITE,false);
        name.setMaxLines(2);
        name.setEllipsize(TextUtils.TruncateAt.END);
        TextView details=Ui.text(context,"",10,Ui.MUTED,false);
        details.setSingleLine(true);
        details.setEllipsize(TextUtils.TruncateAt.END);
        view.addView(name);
        view.addView(details);
        return new Holder(view,name,details);
    }

    @Override public void onBindViewHolder(@NonNull Holder h,int position){
        Entry item=entries.get(position);
        boolean active=store.isPlaylistActiveV99(item.sourceId);
        boolean collapsed=store.isPlaylistCollapsedV99(item.sourceId);
        boolean selected=!item.header && item.sourceId.equals(selectedSource)
            && item.group.equals(selectedGroup);
        boolean focused=h.itemView.hasFocus();
        if(item.header){
            h.title.setText((collapsed||!active?"▸  ":"▾  ")+item.title);
            h.details.setText(active?
                (item.count+" channels · click to collapse/expand"):
                "Inactive · click to enable");
            h.title.setTypeface(Typeface.DEFAULT,Typeface.BOLD);
            h.title.setTextColor(active?Ui.WHITE:Ui.MUTED);
        }else{
            h.title.setText("   "+item.title);
            h.details.setText("   "+item.count+" channels");
            h.title.setTypeface(Typeface.DEFAULT,
                selected?Typeface.BOLD:Typeface.NORMAL);
            h.title.setTextColor(selected?Ui.WHITE:Ui.MUTED);
        }
        GradientDrawable bg=Ui.shape(item.header?0xff203448:
            selected?0xff195677:focused?0xff284c63:Ui.PANEL,10,context);
        if(focused||selected)bg.setStroke(Ui.dp(context,focused?2:1),
            focused?Ui.ACCENT:0xff3c7194);
        h.itemView.setBackground(bg);
        h.itemView.setContentDescription(item.header?
            item.title+(active?(collapsed?", collapsed":", expanded"):", inactive"):
            item.title+", "+item.count+" channels");
        h.itemView.setOnClickListener(v->{
            if(item.header){
                if(!store.isPlaylistActiveV99(item.sourceId)){
                    store.setPlaylistActiveV99(item.sourceId,true);
                    select.onActivationChanged();
                }else{
                    store.setPlaylistCollapsedV99(item.sourceId,
                        !store.isPlaylistCollapsedV99(item.sourceId));
                    rebuild();notifyDataSetChanged();
                }
            }else{
                selectedSource=item.sourceId;selectedGroup=item.group;
                notifyDataSetChanged();
                select.onSelect(item.sourceId,item.group);
            }
        });
        h.itemView.setOnFocusChangeListener((v,hasFocus)->{
            GradientDrawable focusBg=Ui.shape(item.header?0xff203448:
                selected?0xff195677:hasFocus?0xff284c63:Ui.PANEL,10,context);
            if(hasFocus||selected)focusBg.setStroke(Ui.dp(context,hasFocus?2:1),
                hasFocus?Ui.ACCENT:0xff3c7194);
            v.setBackground(focusBg);
        });
    }
    @Override public int getItemCount(){return entries.size();}
    static final class Holder extends RecyclerView.ViewHolder{
        final TextView title,details;
        Holder(View root,TextView title,TextView details){
            super(root);this.title=title;this.details=details;
        }
    }
}
