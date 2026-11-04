package com.keldin.iptv.playback;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.ColorDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.keldin.iptv.ui.Ui;

/** Fully D-pad accessible TV options sheet; no native one-line AlertDialog list. */
public final class TvPlaybackOptionsV94 {
    public interface Choice { void onSelected(android.content.DialogInterface dialog,int action); }

    private TvPlaybackOptionsV94() {}
    private static final String[] SYMBOLS={
        "↻","▣","↗","ⓘ","♡","⊞","♫","CC","Ⅱ","❮","❯","⌕"
    };
    private static final String[] EN={
        "Reconnect the current broadcast",
        "Try another stream transport",
        "Use an installed external player",
        "Review player errors and diagnostics",
        "Add or remove this channel",
        "Change video scaling to fit the screen",
        "Choose an available sound track",
        "Select available subtitle tracks",
        "Pause or resume the broadcast",
        "Switch to the previous channel",
        "Switch to the next channel",
        "Inspect the server response"
    };
    private static final String[] BS={
        "Ponovo poveži trenutni kanal",
        "Isprobaj drugi način reprodukcije",
        "Otvori u vanjskom playeru",
        "Provjeri greške i dijagnostiku",
        "Dodaj ili ukloni kanal iz favorita",
        "Promijeni format slike",
        "Izaberi dostupan audio zapis",
        "Izaberi dostupne titlove",
        "Pauziraj ili nastavi reprodukciju",
        "Prebaci na prethodni kanal",
        "Prebaci na sljedeći kanal",
        "Provjeri odgovor servera"
    };
    private static final String[] SL={
        "Ponovno poveži trenutni kanal",
        "Preizkusi drug način predvajanja",
        "Odpri v zunanjem predvajalniku",
        "Preveri napake in diagnostiko",
        "Dodaj ali odstrani iz priljubljenih",
        "Spremeni razmerje slike",
        "Izberi razpoložljiv zvočni zapis",
        "Izberi razpoložljive podnapise",
        "Začasno ustavi ali nadaljuj predvajanje",
        "Preklopi na prejšnji kanal",
        "Preklopi na naslednji kanal",
        "Preveri odgovor strežnika"
    };
    private static final String[] DE={
        "Aktuellen Sender neu verbinden",
        "Anderen Wiedergabemodus verwenden",
        "In externem Player öffnen",
        "Fehler und Diagnosen anzeigen",
        "Sender zu Favoriten hinzufügen oder entfernen",
        "Bildformat anpassen",
        "Verfügbare Audiospur wählen",
        "Verfügbare Untertitel wählen",
        "Wiedergabe pausieren oder fortsetzen",
        "Zum vorherigen Sender wechseln",
        "Zum nächsten Sender wechseln",
        "Serverantwort überprüfen"
    };

    private static String[] descriptions(Activity activity){
        String lang=activity.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getString("ui_lang","en");
        switch(lang){
            case "bs":return BS;
            case "sl":return SL;
            case "de":return DE;
            default:return EN;
        }
    }
    private static String group(Activity activity,int position){
        String lang=activity.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getString("ui_lang","en");
        String[] en={"STREAM","PLAYBACK","CHANNEL"};
        String[] bs={"STREAM","REPRODUKCIJA","KANALI"};
        String[] sl={"PRENOS","PREDVAJANJE","KANALI"};
        String[] de={"STREAM","WIEDERGABE","SENDER"};
        String[] words="bs".equals(lang)?bs:"sl".equals(lang)?sl:"de".equals(lang)?de:en;
        return words[position];
    }

    public static void show(Activity activity,String channelName,String[] actions,Choice callback,Runnable onClose){
        if(activity.isFinishing()||activity.isDestroyed())return;
        final Dialog dialog=new Dialog(activity);
        final LinearLayout panel=Ui.vertical(activity);
        panel.setPadding(Ui.dp(activity,27),Ui.dp(activity,20),
            Ui.dp(activity,27),Ui.dp(activity,21));
        GradientDrawable backdrop=Ui.shape(0xff101e31,24,activity);
        backdrop.setStroke(Ui.dp(activity,1),0xff496783);
        panel.setBackground(backdrop);
        panel.setClipToPadding(false);
        panel.setClipChildren(false);

        TextView eyebrow=Ui.text(activity,"KELDIN IPTV  /  PLAYER",11,Ui.ACCENT,true);
        eyebrow.setLetterSpacing(.13f);
        panel.addView(eyebrow);
        panel.addView(Ui.space(activity,6));
        TextView heading=Ui.text(activity,"Playback options",24,Ui.WHITE,true);
        String lang=activity.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getString("ui_lang","en");
        if("bs".equals(lang))heading.setText("Opcije reprodukcije");
        else if("sl".equals(lang))heading.setText("Možnosti predvajanja");
        else if("de".equals(lang))heading.setText("Wiedergabeoptionen");
        panel.addView(heading);
        TextView subtitle=Ui.text(activity,channelName==null?"":channelName,13,Ui.MUTED,false);
        subtitle.setSingleLine(true);
        subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);
        panel.addView(subtitle);
        panel.addView(Ui.space(activity,12));
        View line=new View(activity);line.setBackgroundColor(0xff38536d);
        panel.addView(line,new LinearLayout.LayoutParams(-1,Ui.dp(activity,1)));
        panel.addView(Ui.space(activity,9));

        ScrollView scroll=new ScrollView(activity);
        scroll.setVerticalScrollBarEnabled(false);
        scroll.setFillViewport(false);
        scroll.setClipToPadding(false);
        LinearLayout list=Ui.vertical(activity);
        list.setClipChildren(false);
        list.setClipToPadding(false);
        scroll.addView(list);
        String[] details=descriptions(activity);
        for(int i=0;i<actions.length&&i<SYMBOLS.length;i++){
            if(i==0||i==4||i==8){
                TextView category=Ui.text(activity,group(activity,i/4),10,Ui.ACCENT,true);
                category.setLetterSpacing(.14f);
                category.setPadding(Ui.dp(activity,5),Ui.dp(activity,10),0,Ui.dp(activity,5));
                list.addView(category);
            }
            final int index=i;
            LinearLayout item=Ui.horizontal(activity);
            item.setGravity(Gravity.CENTER_VERTICAL);
            item.setPadding(Ui.dp(activity,15),Ui.dp(activity,9),
                Ui.dp(activity,14),Ui.dp(activity,9));
            item.setFocusable(true);
            item.setClickable(true);
            item.setBackground(Ui.shape(0xff192a40,13,activity));
            TextView symbol=Ui.text(activity,SYMBOLS[i],24,Ui.ACCENT,true);
            symbol.setGravity(Gravity.CENTER);
            item.addView(symbol,Ui.lp(activity,51,48));
            LinearLayout info=Ui.vertical(activity);
            info.setPadding(Ui.dp(activity,12),0,0,0);
            TextView name=Ui.text(activity,actions[i],17,Ui.WHITE,true);
            TextView detail=Ui.text(activity,details[i],12,Ui.MUTED,false);
            info.addView(name);
            info.addView(Ui.space(activity,2));
            info.addView(detail);
            item.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
            item.setOnFocusChangeListener((v,focused)->{
                GradientDrawable bg=Ui.shape(focused?0xff28465f:0xff192a40,13,activity);
                if(focused)bg.setStroke(Ui.dp(activity,2),Ui.ACCENT);
                item.setBackground(bg);
                name.setTextColor(focused?Ui.ACCENT:Ui.WHITE);
            });
            item.setOnClickListener(v->{
                dialog.dismiss();
                callback.onSelected(dialog,index);
            });
            LinearLayout.LayoutParams cell=Ui.lp(activity,-1,64);
            cell.bottomMargin=Ui.dp(activity,5);
            list.addView(item,cell);
        }
        panel.addView(scroll,new LinearLayout.LayoutParams(-1,0,1f));
        dialog.setContentView(panel);
        dialog.setCanceledOnTouchOutside(true);
        dialog.setOnDismissListener(d->{
            if(onClose!=null)onClose.run();
        });
        dialog.setOnShowListener(d->{
            if(list.getChildCount()>1){
                View firstItem=list.getChildAt(1);
                if(firstItem!=null)firstItem.requestFocus();
            }
        });
        dialog.show();
        Window w=dialog.getWindow();
        if(w!=null){
            w.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
            w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
            w.setDimAmount(.61f);
            int sw=activity.getResources().getDisplayMetrics().widthPixels;
            int sh=activity.getResources().getDisplayMetrics().heightPixels;
            w.setLayout(Math.min((int)(sw*.64f),Ui.dp(activity,810)),
                Math.min((int)(sh*.81f),Ui.dp(activity,700)));
            w.setGravity(Gravity.CENTER);
        }
    }
}
