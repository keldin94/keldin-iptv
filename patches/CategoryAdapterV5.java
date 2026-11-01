package com.keldin.iptv.ui;

import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;
import java.util.List;

public final class CategoryAdapter extends RecyclerView.Adapter<CategoryAdapter.Holder> {
    public interface Select { void onSelect(String group); }
    private final ArrayList<String> groups=new ArrayList<>();
    private final android.content.Context context;
    private final Select callback;
    private String active="Sve kategorije";

    public CategoryAdapter(android.content.Context context,List<String> source,String active,Select callback){
        this.context=context;groups.addAll(source);this.active=active;this.callback=callback;
    }
    @NonNull @Override public Holder onCreateViewHolder(@NonNull ViewGroup parent,int type){
        LinearLayout shell=Ui.vertical(context);
        shell.setGravity(Gravity.CENTER_VERTICAL);
        shell.setPadding(Ui.dp(context,15),0,Ui.dp(context,9),0);
        shell.setFocusable(true);
        shell.setClickable(true);
        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(context,52));
        lp.setMargins(0,Ui.dp(context,3),Ui.dp(context,4),Ui.dp(context,3));
        shell.setLayoutParams(lp);
        TextView label=Ui.text(context,"",14,Ui.WHITE,false);
        label.setMaxLines(1);
        label.setEllipsize(android.text.TextUtils.TruncateAt.END);
        shell.addView(label);
        return new Holder(shell,label);
    }
    @Override public void onBindViewHolder(@NonNull Holder h,int pos){
        String group=groups.get(pos);
        h.name.setText(group);
        h.itemView.setOnClickListener(v->choose(group));
        h.itemView.setOnFocusChangeListener((v,focus)->update(h,group,focus));
        update(h,group,h.itemView.hasFocus());
    }
    private void choose(String group){
        if(!active.equals(group)){
            String old=active;active=group;
            int previous=groups.indexOf(old),next=groups.indexOf(group);
            if(previous>=0)notifyItemChanged(previous);
            if(next>=0)notifyItemChanged(next);
        }
        callback.onSelect(group);
    }
    private void update(Holder h,String group,boolean focused){
        boolean selected=group.equals(active);
        h.name.setTypeface(Typeface.DEFAULT,selected?Typeface.BOLD:Typeface.NORMAL);
        h.name.setTextColor(selected?Ui.WHITE:focused?Ui.WHITE:Ui.MUTED);
        GradientDrawable bg=Ui.shape(selected?0xff195677:focused?0xff284c63:Ui.PANEL,10,context);
        if(focused)bg.setStroke(Ui.dp(context,2),Ui.ACCENT);
        h.itemView.setBackground(bg);
    }
    @Override public int getItemCount(){return groups.size();}
    static final class Holder extends RecyclerView.ViewHolder{
        final TextView name;
        Holder(View v,TextView name){super(v);this.name=name;}
    }
}
