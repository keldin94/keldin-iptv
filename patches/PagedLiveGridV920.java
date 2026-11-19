package com.keldin.iptv.ui;

import android.view.View;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.keldin.iptv.data.Channel;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Bounded TV-channel adapter window. RecyclerView already recycles views;
 * this additionally avoids keeping a second 100k+ channel array in its
 * adapter, keeps focus restoration possible and loads additional rows
 * only as the viewer scrolls.
 */
public final class PagedLiveGridV920 {
    private static final int PAGE=96;
    private static final int MAX_DISPLAYED=384;
    private static final int EDGE=30;
    private final RecyclerView grid;
    private final ChannelAdapter adapter;
    private final GridLayoutManager layout;
    private List<Channel> all=Collections.emptyList();
    private int first=0,end=0,revision=0;
    private boolean pending=false;

    public PagedLiveGridV920(RecyclerView grid,ChannelAdapter adapter,
                             GridLayoutManager layout){
        this.grid=grid;this.adapter=adapter;this.layout=layout;
        grid.addOnScrollListener(new RecyclerView.OnScrollListener(){
            @Override public void onScrolled(RecyclerView view,int dx,int dy){
                if(dy!=0)requestMore(dy>0);
            }
            @Override public void onScrollStateChanged(RecyclerView view,int state){
                if(state==RecyclerView.SCROLL_STATE_IDLE)requestMore(true);
            }
        });
    }
    public void show(List<Channel> channels){show(channels,0);}
    public void show(List<Channel> channels,int focus){
        revision++;
        pending=false;
        all=channels==null?Collections.emptyList():channels;
        int n=all.size();
        int selected=n==0?0:Math.max(0,Math.min(n-1,focus));
        first=Math.min(Math.max(0,selected-PAGE/3),
            Math.max(0,n-MAX_DISPLAYED));
        end=Math.min(n,first+MAX_DISPLAYED);
        adapter.setItems(new ArrayList<>(all.subList(first,end)));
        grid.scrollToPosition(Math.max(0,selected-first));
    }
    public int localIndex(int absolute){
        return Math.max(0,Math.min(Math.max(0,end-first-1),absolute-first));
    }
    public int total(){return all.size();}
    public int inMemoryCards(){return end-first;}

    private void requestMore(boolean downward){
        if(pending||all.isEmpty())return;
        int visible=downward?layout.findLastVisibleItemPosition():
            layout.findFirstVisibleItemPosition();
        if(visible==RecyclerView.NO_POSITION)return;
        if(downward && (visible<end-first-EDGE || end>=all.size()))return;
        if(!downward && (visible>EDGE || first==0))return;
        pending=true;
        final int expected=revision;
        grid.post(()->{
            pending=false;
            if(expected!=revision||grid.getParent()==null)return;
            int oldStart=first;
            int anchor=downward?layout.findFirstVisibleItemPosition():
                layout.findLastVisibleItemPosition();
            int absolute=Math.max(oldStart,oldStart+Math.max(0,anchor));
            if(downward){
                end=Math.min(all.size(),end+PAGE);
                first=Math.max(0,end-MAX_DISPLAYED);
            }else{
                first=Math.max(0,first-PAGE);
                end=Math.min(all.size(),first+MAX_DISPLAYED);
            }
            if(first==oldStart && end-first==adapter.getItemCount())return;
            adapter.setItems(new ArrayList<>(all.subList(first,end)));
            grid.scrollToPosition(Math.max(0,Math.min(end-first-1,absolute-first)));
        });
    }
}
