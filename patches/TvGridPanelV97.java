package com.keldin.iptv.playback;

import android.content.Context;
import android.graphics.Gravity;
import android.graphics.drawable.GradientDrawable;
import android.text.TextUtils;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.keldin.iptv.data.CatalogStore;
import com.keldin.iptv.data.Channel;
import com.keldin.iptv.data.ContentFilterV93;
import com.keldin.iptv.ui.I18n;
import com.keldin.iptv.ui.LogoLoader;
import com.keldin.iptv.ui.Ui;
import com.keldin.iptv.ui.UiLocaleV9;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Set;

/** Responsive TV-grid overlay: the same ExoPlayer continues behind the grid.
 * No additional stream/player or per-channel thumbnail View trees are created.
 */
public final class TvGridPanelV97 {
    public interface Choose { void onChannel(Channel selected); }

    private final Context ctx;
    private final FrameLayout host;
    private final CatalogStore store;
    private final Choose choose;
    private final ArrayList<Channel> channels=new ArrayList<>();
    private FrameLayout scrim;
    private RecyclerView grid;
    private GridAdapter adapter;
    private int selection=0, columns=4;

    public TvGridPanelV97(Context context,FrameLayout root,
                          CatalogStore catalog,Choose listener){
        ctx=context;host=root;store=catalog;choose=listener;
    }
    public boolean isOpen(){return scrim!=null;}

    public void open(Channel active){
        hide();
        if(active==null)return;
        final boolean hideAdult=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getBoolean("hide_adult_content_v93",true);
        final Set<String> excluded=store.excludedGroups(active.sourceId);
        int chosen=0;
        for(Channel ch:store.channels()){
            if(!"LIVE".equals(ch.kind)||!active.sourceId.equals(ch.sourceId))continue;
            if(excluded.contains(ch.group)||excluded.contains("@kind:LIVE"))continue;
            if((hideAdult||(store.parentalLocked()&&!store.isContentUnlocked()))
                && ContentFilterV93.isExplicit(ch.group,ch.name))continue;
            if(ch.key().equals(active.key()))chosen=channels.size();
            channels.add(ch);
        }
        if(channels.isEmpty())return;
        selection=Math.max(0,Math.min(channels.size()-1,chosen));
        int width=ctx.getResources().getDisplayMetrics().widthPixels;
        int height=ctx.getResources().getDisplayMetrics().heightPixels;
        float density=ctx.getResources().getDisplayMetrics().density;
        float availableDp=width/Math.max(1f,density);
        columns=availableDp>1050?6:availableDp>760?5:availableDp>520?4:3;

        scrim=new FrameLayout(ctx);
        scrim.setBackgroundColor(0x4e080d16);
        host.addView(scrim,new FrameLayout.LayoutParams(-1,-1));

        LinearLayout pane=Ui.vertical(ctx);
        pane.setPadding(Ui.dp(ctx,19),Ui.dp(ctx,14),Ui.dp(ctx,19),Ui.dp(ctx,13));
        GradientDrawable shape=Ui.shape(0xf5151f2d,21,ctx);
        shape.setStroke(Ui.dp(ctx,1),0xff41556d);
        pane.setBackground(shape);
        pane.setElevation(Ui.dp(ctx,18));
        int panelHeight=Math.max(Ui.dp(ctx,245),
            Math.min(Ui.dp(ctx,510),(int)(height*.69f)));
        FrameLayout.LayoutParams panelLp=new FrameLayout.LayoutParams(
            -1,panelHeight,Gravity.BOTTOM);
        panelLp.setMargins(Ui.dp(ctx,22),0,Ui.dp(ctx,22),Ui.dp(ctx,18));
        scrim.addView(pane,panelLp);

        LinearLayout header=Ui.horizontal(ctx);
        header.setGravity(Gravity.CENTER_VERTICAL);
        TextView title=Ui.text(ctx,UiLocaleV9.translate(ctx,"TV Grid"),22,Ui.WHITE,true);
        title.setMaxLines(2);
        header.addView(title,new LinearLayout.LayoutParams(0,-2,1));
        TextView count=Ui.text(ctx,channels.size()+" "+I18n.t(ctx,"channels_count"),
            12,Ui.MUTED,false);
        header.addView(count,Ui.lp(ctx,-2,-2));
        pane.addView(header);
        pane.addView(Ui.space(ctx,5));
        TextView instruction=Ui.text(ctx,
            "← → ↑ ↓   •   OK   •   BACK",11,Ui.MUTED,false);
        instruction.setMaxLines(2);
        pane.addView(instruction);
        pane.addView(Ui.space(ctx,8));

        grid=new RecyclerView(ctx);
        grid.setOverScrollMode(View.OVER_SCROLL_NEVER);
        grid.setVerticalScrollBarEnabled(false);
        grid.setItemAnimator(null);
        grid.setHasFixedSize(true);
        grid.setLayoutManager(new GridLayoutManager(ctx,columns));
        adapter=new GridAdapter();
        grid.setAdapter(adapter);
        pane.addView(grid,new LinearLayout.LayoutParams(-1,0,1));
        grid.scrollToPosition(selection);
        scrim.setFocusableInTouchMode(true);
        scrim.requestFocus();
    }

    public boolean handleKey(KeyEvent e){
        if(!isOpen())return false;
        int key=e.getKeyCode();
        boolean relevant=key==KeyEvent.KEYCODE_BACK||key==KeyEvent.KEYCODE_ESCAPE
            ||key==KeyEvent.KEYCODE_DPAD_LEFT||key==KeyEvent.KEYCODE_DPAD_RIGHT
            ||key==KeyEvent.KEYCODE_DPAD_UP||key==KeyEvent.KEYCODE_DPAD_DOWN
            ||key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER
            ||key==KeyEvent.KEYCODE_CHANNEL_UP||key==KeyEvent.KEYCODE_CHANNEL_DOWN;
        if(!relevant)return false;
        if(e.getAction()!=KeyEvent.ACTION_DOWN)return true;
        if(e.getRepeatCount()>0)return true;
        if(key==KeyEvent.KEYCODE_BACK||key==KeyEvent.KEYCODE_ESCAPE){hide();return true;}
        if(key==KeyEvent.KEYCODE_DPAD_CENTER||key==KeyEvent.KEYCODE_ENTER){
            select();return true;
        }
        int step=key==KeyEvent.KEYCODE_DPAD_LEFT?-1:
            key==KeyEvent.KEYCODE_DPAD_RIGHT?1:
            key==KeyEvent.KEYCODE_DPAD_UP||key==KeyEvent.KEYCODE_CHANNEL_UP?
                -columns:columns;
        move(step);
        return true;
    }

    private void move(int amount){
        if(channels.isEmpty())return;
        int next=Math.max(0,Math.min(channels.size()-1,selection+amount));
        if(next==selection)return;
        int old=selection;
        selection=next;
        if(adapter!=null){
            adapter.notifyItemChanged(old);
            adapter.notifyItemChanged(selection);
        }
        if(grid!=null)grid.scrollToPosition(selection);
    }

    private void select(){
        if(selection<0||selection>=channels.size())return;
        Channel selected=channels.get(selection);
        hide();
        choose.onChannel(selected);
    }
    public void hide(){
        if(scrim!=null){host.removeView(scrim);scrim=null;}
        grid=null;adapter=null;channels.clear();
    }

    private final class GridAdapter extends RecyclerView.Adapter<GridAdapter.Holder>{
        @Override public int getItemCount(){return channels.size();}
        @NonNull @Override public Holder onCreateViewHolder(@NonNull ViewGroup parent,int type){
            LinearLayout card=Ui.vertical(ctx);
            card.setPadding(Ui.dp(ctx,8),Ui.dp(ctx,7),
                Ui.dp(ctx,8),Ui.dp(ctx,7));
            card.setGravity(Gravity.CENTER);
            card.setMinimumHeight(Ui.dp(ctx,99));
            card.setClickable(true);
            card.setFocusable(false); // PlayerActivity handles D-pad consistently.
            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,-2);
            lp.setMargins(Ui.dp(ctx,4),Ui.dp(ctx,4),
                Ui.dp(ctx,4),Ui.dp(ctx,4));
            card.setLayoutParams(lp);
            FrameLayout logoFrame=new FrameLayout(ctx);
            ImageView image=new ImageView(ctx);
            image.setScaleType(ImageView.ScaleType.FIT_CENTER);
            TextView fallback=Ui.text(ctx,"TV",14,Ui.ACCENT,true);
            fallback.setGravity(Gravity.CENTER);
            logoFrame.addView(fallback,new FrameLayout.LayoutParams(-1,-1));
            logoFrame.addView(image,new FrameLayout.LayoutParams(-1,-1));
            card.addView(logoFrame,Ui.lp(ctx,-1,45));
            card.addView(Ui.space(ctx,5));
            TextView label=Ui.text(ctx,"",12,Ui.WHITE,true);
            label.setGravity(Gravity.CENTER);
            label.setMaxLines(2);
            label.setEllipsize(TextUtils.TruncateAt.END);
            card.addView(label,new LinearLayout.LayoutParams(-1,-2));
            return new Holder(card,image,fallback,label);
        }
        @Override public void onBindViewHolder(@NonNull Holder h,int pos){
            Channel channel=channels.get(pos);
            h.title.setText(channel.name);
            h.icon.setImageDrawable(null);
            h.fallback.setVisibility(View.VISIBLE);
            LogoLoader.load(h.icon,channel.logo,ok->
                h.fallback.setVisibility(ok?View.GONE:View.VISIBLE));
            boolean focused=pos==selection;
            GradientDrawable bg=Ui.shape(focused?0xff24486a:0xee1e2b3c,12,ctx);
            bg.setStroke(Ui.dp(ctx,focused?2:1),
                focused?Ui.ACCENT:0xff304154);
            h.itemView.setBackground(bg);
            h.title.setTextColor(focused?Ui.WHITE:Ui.MUTED);
            h.itemView.setContentDescription(channel.name);
            h.itemView.setOnClickListener(v->{
                int target=h.getBindingAdapterPosition();
                if(target==RecyclerView.NO_POSITION)return;
                selection=target;select();
            });
        }
        final class Holder extends RecyclerView.ViewHolder{
            final ImageView icon;
            final TextView fallback,title;
            Holder(View view,ImageView image,TextView fallback,TextView title){
                super(view);icon=image;this.fallback=fallback;this.title=title;
            }
        }
    }
}
