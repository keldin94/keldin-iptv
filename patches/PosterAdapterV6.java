package com.keldin.iptv.ui;

import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.keldin.iptv.data.Channel;
import java.util.ArrayList;
import java.util.List;

/** Poster grid: only visible images are loaded by RecyclerView; no full-list Bitmap allocations. */
public final class PosterAdapterV6 extends RecyclerView.Adapter<PosterAdapterV6.Holder>{
    public interface Open{void onOpen(Channel item);}
    private final ArrayList<Channel> items=new ArrayList<>();
    private final Open open;
    public PosterAdapterV6(List<Channel> values,Open open){
        items.addAll(values);this.open=open;setHasStableIds(true);
    }
    public void replace(List<Channel> values){items.clear();items.addAll(values);notifyDataSetChanged();}
    @Override public long getItemId(int p){return items.get(p).key().hashCode();}
    @Override public int getItemCount(){return items.size();}
    @NonNull @Override public Holder onCreateViewHolder(@NonNull ViewGroup parent,int type){
        Context c=parent.getContext();
        LinearLayout root=Ui.vertical(c);
        root.setFocusable(true);root.setClickable(true);
        root.setPadding(Ui.dp(c,8),Ui.dp(c,8),Ui.dp(c,8),Ui.dp(c,9));
        root.setBackground(Ui.shape(Ui.PANEL,15,c));
        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(c,295));
        lp.setMargins(Ui.dp(c,5),Ui.dp(c,5),Ui.dp(c,5),Ui.dp(c,5));
        root.setLayoutParams(lp);
        FrameLayout poster=new FrameLayout(c);
        ImageView picture=new ImageView(c);
        picture.setScaleType(ImageView.ScaleType.CENTER_CROP);
        poster.setClipToOutline(true);
        poster.setBackground(Ui.shape(Ui.SURFACE,12,c));
        poster.addView(picture,new FrameLayout.LayoutParams(-1,-1));
        TextView fallback=Ui.text(c,"▶",38,Ui.ACCENT,true);
        fallback.setGravity(Gravity.CENTER);
        poster.addView(fallback,new FrameLayout.LayoutParams(-1,-1));
        root.addView(poster,new LinearLayout.LayoutParams(-1,0,1));
        root.addView(Ui.space(c,10));
        TextView title=Ui.text(c,"",15,Ui.WHITE,true);
        title.setSingleLine(true);title.setEllipsize(TextUtils.TruncateAt.END);
        TextView subtitle=Ui.text(c,"",11,Ui.MUTED,false);
        subtitle.setSingleLine(true);subtitle.setEllipsize(TextUtils.TruncateAt.END);
        root.addView(title);root.addView(Ui.space(c,3));root.addView(subtitle);
        return new Holder(root,picture,fallback,title,subtitle);
    }
    @Override public void onBindViewHolder(@NonNull Holder holder,int pos){
        Channel item=items.get(pos);
        holder.title.setText(item.name);
        holder.subtitle.setText(item.group);
        holder.fallback.setVisibility(View.VISIBLE);
        // Uses existing bounded cache/network loader and recycled-view tag checks.
        LogoLoader.load(holder.picture,item.logo,loaded ->
            holder.fallback.setVisibility(loaded?View.GONE:View.VISIBLE));
        holder.itemView.setOnClickListener(v->open.onOpen(item));
        holder.itemView.setOnFocusChangeListener((v,has)->{
            GradientDrawable d=Ui.shape(has?Ui.SURFACE:Ui.PANEL,15,v.getContext());
            if(has)d.setStroke(Ui.dp(v.getContext(),2),Ui.ACCENT);
            v.setBackground(d);
            v.animate().scaleX(has?1.025f:1f).scaleY(has?1.025f:1f).setDuration(115).start();
        });
    }
    static final class Holder extends RecyclerView.ViewHolder{
        final ImageView picture;final TextView fallback,title,subtitle;
        Holder(View item,ImageView picture,TextView fallback,TextView title,TextView subtitle){
            super(item);this.picture=picture;this.fallback=fallback;this.title=title;this.subtitle=subtitle;
        }
    }
}
