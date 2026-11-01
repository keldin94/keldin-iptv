package com.keldin.iptv.playback;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.keldin.iptv.data.CatalogStore;
import com.keldin.iptv.data.Channel;
import com.keldin.iptv.data.GuideProgram;
import com.keldin.iptv.ui.Ui;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/**
 * Remote-controlled, non-modal overlay above the existing video.
 * Only a portion of the video is covered; no large View tree is created for huge M3U lists.
 */
public final class TvSidePanel {
    public interface Listener { void play(Channel channel); }
    public static final int HIDDEN=0, CHANNELS=1, CATEGORIES=2, GUIDE=3;
    private static final int CYAN=0xff55D9FB, WHITE=0xffF6FAFF, MUTED=0xffA5B6C9;

    private final Context ctx;
    private final FrameLayout host;
    private final CatalogStore store;
    private final Listener listener;
    private final ArrayList<RowData> rows=new ArrayList<>();
    private FrameLayout panel;
    private RecyclerView list;
    private RowAdapter adapter;
    private Channel current;
    private int mode=HIDDEN, selection=0;
    private String selectedCategory="Sve kategorije";

    public TvSidePanel(Context ctx, FrameLayout host, CatalogStore store, Listener listener) {
        this.ctx=ctx;this.host=host;this.store=store;this.listener=listener;
    }

    public boolean isOpen(){ return mode!=HIDDEN; }

    public void openChannels(Channel channel){
        if(channel==null)return;
        current=channel;
        mode=CHANNELS;
        refresh();
    }
    public void openGuide(Channel channel){
        if(channel==null)return;
        current=channel;
        mode=GUIDE;
        refresh();
    }
    public void left(){
        if(mode==CHANNELS){mode=CATEGORIES;refresh();}
        else if(mode==GUIDE){mode=CHANNELS;refresh();}
    }
    public void right(){
        if(mode==CATEGORIES){mode=CHANNELS;refresh();}
        else if(mode==CHANNELS){mode=GUIDE;refresh();}
    }
    public void move(int direction){
        if(rows.isEmpty())return;
        int next=Math.max(0,Math.min(rows.size()-1,selection+direction));
        if(next==selection)return;
        int before=selection;
        selection=next;
        if(adapter!=null){adapter.notifyItemChanged(before);adapter.notifyItemChanged(selection);}
        if(list!=null)list.scrollToPosition(selection);
    }
    public void select(){
        if(selection<0||selection>=rows.size())return;
        RowData r=rows.get(selection);
        if(mode==CHANNELS && r.channel!=null){
            Channel target=r.channel;
            hide();
            listener.play(target);
        } else if(mode==CATEGORIES && r.category!=null) {
            selectedCategory=r.category;
            mode=CHANNELS;
            refresh();
        } else if(mode==GUIDE && r.program!=null){
            new android.app.AlertDialog.Builder(ctx)
                .setTitle(r.program.title)
                .setMessage(r.program.description==null||r.program.description.isEmpty()?
                    "Nema dodatnog opisa emisije.":r.program.description)
                .setPositiveButton("Zatvori",null).show();
        }
    }
    public void hide(){
        mode=HIDDEN;
        if(panel!=null){host.removeView(panel);panel=null;}
        list=null;adapter=null;rows.clear();
    }

    private void refresh(){
        rows.clear();
        selection=0;
        if(mode==CHANNELS){
            List<Channel> channels=store.channels();
            for(Channel c:channels){
                if(!"LIVE".equals(c.kind)||!c.sourceId.equals(current.sourceId))continue;
                if(!"Sve kategorije".equals(selectedCategory)&&!selectedCategory.equals(c.group))continue;
                RowData r=new RowData();
                r.channel=c;
                r.title=c.name;
                r.subtitle=c.group+(store.favorite(c)?"  •  ♥":"");
                rows.add(r);
                if(c.key().equals(current.key()))selection=rows.size()-1;
            }
        }else if(mode==CATEGORIES){
            LinkedHashMap<String,Integer> groups=new LinkedHashMap<>();
            int total=0;
            for(Channel c:store.channels()){
                if("LIVE".equals(c.kind)&&c.sourceId.equals(current.sourceId)){
                    total++;
                    String group=(c.group==null||c.group.isEmpty())?"Ostalo":c.group;
                    groups.put(group,groups.getOrDefault(group,0)+1);
                }
            }
            RowData all=new RowData();all.category="Sve kategorije";
            all.title="Sve kategorije";all.subtitle=total+" kanala";rows.add(all);
            for(Map.Entry<String,Integer> g:groups.entrySet()){
                RowData r=new RowData();r.category=g.getKey();r.title=g.getKey();
                r.subtitle=g.getValue()+" kanala";rows.add(r);
                if(selectedCategory.equals(r.category))selection=rows.size()-1;
            }
        }else if(mode==GUIDE){
            List<GuideProgram> programs=store.schedule(current,System.currentTimeMillis());
            SimpleDateFormat clock=new SimpleDateFormat("HH:mm",Locale.getDefault());
            long time=System.currentTimeMillis();
            for(GuideProgram program:programs){
                if(program.end+store.guideOffsetHours()*3600_000L < time-30*60_000L)continue;
                RowData r=new RowData();
                r.program=program;
                r.title=clock.format(new Date(program.start+store.guideOffsetHours()*3600_000L))+
                    "  "+program.title;
                boolean now=program.start+store.guideOffsetHours()*3600_000L<=time
                    && program.end+store.guideOffsetHours()*3600_000L>time;
                r.subtitle=now?"● U TOKU":clock.format(new Date(program.end+store.guideOffsetHours()*3600_000L));
                if(now)selection=rows.size();
                rows.add(r);
                if(rows.size()>=60)break;
            }
            if(rows.isEmpty()){
                RowData empty=new RowData();
                empty.title="TV vodič nije dostupan";
                empty.subtitle="Dodaj XMLTV / EPG URL u postavkama liste.";
                rows.add(empty);
            }
        }
        rebuild();
    }

    private GradientDrawable rounded(int color,int radius) {
        GradientDrawable d=Ui.shape(color,radius,ctx);
        d.setStroke(Ui.dp(ctx,1),0xff36516b);
        return d;
    }

    private void rebuild(){
        if(panel!=null)host.removeView(panel);
        panel=new FrameLayout(ctx);
        int screenWidth=ctx.getResources().getDisplayMetrics().widthPixels;
        int panelWidth=Math.min((int)(screenWidth*.41f),Ui.dp(ctx,570));
        panelWidth=Math.min(panelWidth,screenWidth-Ui.dp(ctx,24));
        FrameLayout.LayoutParams frame=new FrameLayout.LayoutParams(panelWidth,-1,
            mode==GUIDE?Gravity.RIGHT:Gravity.LEFT);
        int margin=Ui.dp(ctx,16);
        frame.setMargins(margin,margin,margin,margin);
        panel.setBackground(rounded(0xf20e1c2f,19));
        panel.setElevation(Ui.dp(ctx,20));
        panel.setClipToOutline(true);
        host.addView(panel,frame);

        LinearLayout body=Ui.vertical(ctx);
        body.setPadding(Ui.dp(ctx,18),Ui.dp(ctx,19),Ui.dp(ctx,15),Ui.dp(ctx,13));
        panel.addView(body,new FrameLayout.LayoutParams(-1,-1));

        TextView eyebrow=Ui.text(ctx,"KELDIN IPTV   /   FULL",10,CYAN,true);
        eyebrow.setLetterSpacing(.12f);body.addView(eyebrow);
        body.addView(Ui.space(ctx,8));
        TextView title=Ui.text(ctx,
            mode==CHANNELS?"TV kanali":mode==CATEGORIES?"Kategorije":"TV vodič",
            26,WHITE,true);
        body.addView(title);
        TextView detail=Ui.text(ctx,mode==GUIDE?current.name:
            mode==CHANNELS?selectedCategory:"Odaberi kategoriju",12,MUTED,false);
        detail.setSingleLine(true);detail.setEllipsize(android.text.TextUtils.TruncateAt.END);
        body.addView(detail);
        body.addView(Ui.space(ctx,12));

        View line=new View(ctx);
        line.setBackgroundColor(0xff35516c);
        body.addView(line,new LinearLayout.LayoutParams(-1,Ui.dp(ctx,1)));
        body.addView(Ui.space(ctx,8));

        TextView count=Ui.text(ctx,rows.size()+" stavki",11,CYAN,true);
        body.addView(count);body.addView(Ui.space(ctx,5));

        list=new RecyclerView(ctx);
        list.setLayoutManager(new LinearLayoutManager(ctx));
        list.setOverScrollMode(View.OVER_SCROLL_NEVER);
        list.setVerticalScrollBarEnabled(false);
        list.setHasFixedSize(true);
        list.setItemAnimator(null);
        adapter=new RowAdapter();
        list.setAdapter(adapter);
        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        if(selection>0)list.scrollToPosition(selection);

        body.addView(Ui.space(ctx,8));
        View bottom=new View(ctx);bottom.setBackgroundColor(0xff36516b);
        body.addView(bottom,new LinearLayout.LayoutParams(-1,Ui.dp(ctx,1)));
        body.addView(Ui.space(ctx,10));
        TextView legend=Ui.text(ctx,
            mode==CATEGORIES?"→ Kanali   •   ↑↓ Odaberi   •   OK Otvori":
                mode==GUIDE?"← Kanali   •   BACK Zatvori   •   OK Detalji":
                    "← Kategorije   •   → EPG   •   OK Gledaj",11,MUTED,false);
        body.addView(legend);
    }

    private static final class RowData {
        String title="",subtitle="",category;
        Channel channel;
        GuideProgram program;
    }
    private final class RowAdapter extends RecyclerView.Adapter<RowAdapter.Holder>{
        @Override public Holder onCreateViewHolder(ViewGroup parent,int type){
            LinearLayout row=Ui.horizontal(ctx);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(Ui.dp(ctx,13),Ui.dp(ctx,11),Ui.dp(ctx,10),Ui.dp(ctx,11));
            LinearLayout text=Ui.vertical(ctx);
            TextView title=Ui.text(ctx,"",15,WHITE,true);
            title.setSingleLine(true);
            title.setEllipsize(android.text.TextUtils.TruncateAt.END);
            TextView subtitle=Ui.text(ctx,"",11,MUTED,false);
            subtitle.setSingleLine(true);
            subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);
            text.addView(title);
            text.addView(Ui.space(ctx,3));
            text.addView(subtitle);
            row.addView(text,new LinearLayout.LayoutParams(0,-2,1));
            TextView arrow=Ui.text(ctx,"›",20,CYAN,true);
            arrow.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);
            row.addView(arrow,Ui.lp(ctx,20,-1));
            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(ctx,69));
            lp.bottomMargin=Ui.dp(ctx,5);
            row.setLayoutParams(lp);
            return new Holder(row,title,subtitle,arrow);
        }
        @Override public void onBindViewHolder(Holder holder,int pos){
            RowData r=rows.get(pos);
            holder.title.setText(r.title);
            holder.subtitle.setText(r.subtitle);
            boolean selected=(pos==selection);
            holder.title.setTextColor(selected?Color.WHITE:WHITE);
            holder.subtitle.setTextColor(selected?0xffDAEDFA:MUTED);
            holder.arrow.setVisibility(selected?View.VISIBLE:View.INVISIBLE);
            GradientDrawable bg=rounded(selected?0xff1e5d78:0x80203248,11);
            if(selected)bg.setStroke(Ui.dp(ctx,2),CYAN);
            holder.itemView.setBackground(bg);
            holder.itemView.setOnClickListener(v->{int previous=selection;selection=holder.getBindingAdapterPosition();
                if(previous>=0&&previous<rows.size())notifyItemChanged(previous);
                if(selection>=0&&selection<rows.size()){notifyItemChanged(selection);select();}
            });
        }
        @Override public int getItemCount(){return rows.size();}
        final class Holder extends RecyclerView.ViewHolder{
            final TextView title,subtitle,arrow;
            Holder(View item,TextView t,TextView s,TextView a){super(item);title=t;subtitle=s;arrow=a;}
        }
    }
}
