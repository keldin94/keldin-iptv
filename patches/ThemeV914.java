package com.keldin.iptv.ui;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.keldin.iptv.data.CatalogStore;

/**
 * Five distinct TV layouts. All use the same channel catalogue, player,
 * updates, source selections, favorites and D-pad navigation.
 * Theme changes never trigger network requests or mutate catalogue data.
 */
public final class ThemeV914 {
    public static final int CLASSIC=0, CINEMA=1, GUIDE=2, GLASS=3, COMPACT=4;
    public static final String KEY="interface_layout_v914";
    private static final String[] LABELS={
        "KELDIN Classic","KELDIN Cinema","KELDIN TV Guide",
        "KELDIN Glass","KELDIN Compact"
    };
    private static final String[] DESCRIPTIONS={
        "Modern dashboard, prominent TV and streaming sections.",
        "Cinematic featured screen and horizontal movie categories.",
        "TV-first navigation, quick EPG access and wider channel lists.",
        "Floating translucent panels and spacious cards.",
        "Dense dashboard with more channels visible at once."
    };
    public interface Navigation { void go(String target); }
    private ThemeV914(){}

    public static int current(Context ctx){
        int saved=ctx.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
            .getInt(KEY,CLASSIC);
        return Math.max(CLASSIC,Math.min(COMPACT,saved));
    }
    public static String label(Context ctx){return LABELS[current(ctx)];}
    public static int railWidth(int theme){
        switch(theme){
            case CINEMA:return 175;
            case GUIDE:return 282;
            case GLASS:return 224;
            case COMPACT:return 184;
            default:return 232;
        }
    }
    public static int gridColumns(int theme,boolean posters){
        switch(theme){
            case CINEMA:return posters?5:3;
            case GUIDE:return posters?4:3;
            case GLASS:return posters?4:3;
            case COMPACT:return posters?6:5;
            default:return 4;
        }
    }
    public static void styleBrowse(Context ctx,LinearLayout categories,
                                   TextView section,int theme){
        int bg=theme==GLASS?0x9b25354a:
            theme==CINEMA?0xff18202e:
            theme==GUIDE?0xff1c3040:
            theme==COMPACT?0xff181f2b:Ui.PANEL;
        int round=theme==COMPACT?8:theme==GLASS?24:16;
        GradientDrawable shape=Ui.shape(bg,round,ctx);
        if(theme==GLASS)shape.setStroke(Ui.dp(ctx,1),0x886abadd);
        categories.setBackground(shape);
        categories.setPadding(Ui.dp(ctx,theme==COMPACT?6:12),
            Ui.dp(ctx,theme==COMPACT?6:12),
            Ui.dp(ctx,theme==COMPACT?6:10),Ui.dp(ctx,9));
        if(theme==GUIDE)section.setTextSize(14);
        else if(theme==COMPACT)section.setTextSize(10);
    }

    private static String tr(Activity a,String key){return I18n.t(a,key);}
    private static GradientDrawable surface(Activity a,int theme,boolean focused,int emphasis){
        int base=theme==GLASS?0xa62b405b:
            theme==CINEMA?0xff202734:
            theme==GUIDE?0xff183447:
            theme==COMPACT?0xff1a2533:Ui.PANEL;
        if(emphasis==1)base=theme==CINEMA?0xff343448:
            theme==GUIDE?0xff18546d:
            theme==GLASS?0xb4345070:0xff253e59;
        GradientDrawable bg=Ui.shape(focused?0xff355877:base,
            theme==GLASS?25:theme==COMPACT?10:18,a);
        bg.setStroke(Ui.dp(a,focused?3:1),
            focused?Ui.ACCENT:theme==GLASS?0x8877c6e7:0x77576b87);
        return bg;
    }
    private static LinearLayout tile(Activity a,int theme,String icon,String text,
            String subtitle,String target,Navigation nav,int emphasis,int height){
        LinearLayout box=Ui.vertical(a);
        box.setGravity(Gravity.CENTER_VERTICAL);
        int inset=theme==COMPACT?11:17;
        box.setPadding(Ui.dp(a,inset),Ui.dp(a,9),Ui.dp(a,inset),Ui.dp(a,9));
        box.setBackground(surface(a,theme,false,emphasis));
        box.setFocusable(true);
        box.setClickable(true);
        box.setClipChildren(false);
        box.setContentDescription(text+" — "+subtitle);
        TextView symbol=Ui.text(a,icon,theme==COMPACT?22:31,Ui.ACCENT,true);
        symbol.setMaxLines(1);
        TextView title=Ui.text(a,text,theme==COMPACT?16:23,Ui.WHITE,true);
        title.setMaxLines(2);title.setEllipsize(android.text.TextUtils.TruncateAt.END);
        TextView hint=Ui.text(a,subtitle,theme==COMPACT?10:12,Ui.MUTED,false);
        hint.setMaxLines(2);hint.setEllipsize(android.text.TextUtils.TruncateAt.END);
        if(theme!=COMPACT){
            box.addView(symbol);box.addView(Ui.space(a,theme==CINEMA?15:8));
        }else{
            LinearLayout headline=Ui.horizontal(a);
            headline.setGravity(Gravity.CENTER_VERTICAL);
            headline.addView(symbol,Ui.lp(a,36,-2));
            headline.addView(title,new LinearLayout.LayoutParams(0,-2,1f));
            box.addView(headline);
        }
        if(theme!=COMPACT)box.addView(title);
        box.addView(Ui.space(a,5));box.addView(hint);
        box.setMinimumHeight(Ui.dp(a,height));
        box.setOnClickListener(v->nav.go(target));
        box.setOnFocusChangeListener((v,focus)->{
            box.setBackground(surface(a,theme,focus,emphasis));
            title.setTextColor(focus?Ui.ACCENT:Ui.WHITE);
        });
        return box;
    }
    private static void weighted(Activity a,LinearLayout row,View v,int h){
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,
            h<=0?-1:Ui.dp(a,h),1f);
        lp.leftMargin=Ui.dp(a,5);lp.rightMargin=Ui.dp(a,5);
        row.addView(v,lp);
    }
    private static void fixed(Activity a,LinearLayout column,View v,int h,int margin){
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,
            h<=0?-2:Ui.dp(a,h));
        lp.bottomMargin=Ui.dp(a,margin);
        column.addView(v,lp);
    }
    private static void caption(Activity a,LinearLayout body,String text,int size){
        TextView heading=Ui.text(a,text,size,Ui.WHITE,true);
        heading.setMaxLines(2);
        body.addView(heading);
        body.addView(Ui.space(a,10));
    }
    private static LinearLayout row(Activity a){
        LinearLayout r=Ui.horizontal(a);
        r.setGravity(Gravity.CENTER_VERTICAL);r.setClipChildren(false);
        r.setClipToPadding(false);return r;
    }
    private static void add(Activity a,int theme,LinearLayout body,String icon,
            String title,String subtitle,String target,Navigation nav,int height){
        fixed(a,body,tile(a,theme,icon,title,subtitle,target,nav,0,height),height,9);
    }

    public static void showHome(Activity a,LinearLayout content,CatalogStore store,
            Navigation nav,Runnable onAdd){
        int theme=current(a);
        ScrollView scroller=new ScrollView(a);
        scroller.setFillViewport(true);
        scroller.setVerticalScrollBarEnabled(false);
        scroller.setClipToPadding(false);
        LinearLayout body=Ui.vertical(a);
        body.setPadding(Ui.dp(a,theme==COMPACT?7:14),Ui.dp(a,8),
            Ui.dp(a,theme==COMPACT?7:14),Ui.dp(a,13));
        scroller.addView(body);
        if(theme==CLASSIC){
            caption(a,body,"DISCOVER  /  "+tr(a,"choose"),19);
            LinearLayout hero=row(a);
            weighted(a,hero,tile(a,theme,"▣",tr(a,"live"),"Live channels","Uživo",nav,1,198),198);
            weighted(a,hero,tile(a,theme,"▶",tr(a,"movies"),"Discover movies","Filmovi",nav,0,198),198);
            weighted(a,hero,tile(a,theme,"▤",tr(a,"series"),"Browse TV series","Serije",nav,0,198),198);
            weighted(a,hero,tile(a,theme,"♫",tr(a,"radio"),"Radio stations","Radio",nav,0,198),198);
            fixed(a,body,hero,198,15);
            LinearLayout shortcuts=row(a);
            weighted(a,shortcuts,tile(a,theme,"▦",tr(a,"guide"),"Programme schedule","TV vodič",nav,0,86),86);
            weighted(a,shortcuts,tile(a,theme,"⚙",tr(a,"settings"),"Customize your experience","Postavke",nav,0,86),86);
            fixed(a,body,shortcuts,86,8);
        }else if(theme==CINEMA){
            caption(a,body,"KELDIN CINEMA  /  FILMS & ENTERTAINMENT",18);
            LinearLayout top=row(a);
            LinearLayout featured=tile(a,theme,"▶","THE CINEMA",
                "Explore movies in a cinematic library","Filmovi",nav,1,232);
            LinearLayout.LayoutParams featureLp=new LinearLayout.LayoutParams(
                0,Ui.dp(a,232),1.9f);
            featureLp.leftMargin=Ui.dp(a,5);featureLp.rightMargin=Ui.dp(a,7);
            top.addView(featured,featureLp);
            LinearLayout second=Ui.vertical(a);
            fixed(a,second,tile(a,theme,"▤",tr(a,"series"),"Series collection","Serije",nav,0,107),107,12);
            fixed(a,second,tile(a,theme,"▣",tr(a,"live"),"Watch TV now","Uživo",nav,0,113),113,0);
            LinearLayout.LayoutParams right=new LinearLayout.LayoutParams(0,Ui.dp(a,232),1f);
            right.leftMargin=Ui.dp(a,5);right.rightMargin=Ui.dp(a,5);
            top.addView(second,right);
            fixed(a,body,top,232,14);
            caption(a,body,"QUICK ACCESS",14);
            LinearLayout navrow=row(a);
            weighted(a,navrow,tile(a,theme,"▦",tr(a,"guide"),"Schedule","TV vodič",nav,0,98),98);
            weighted(a,navrow,tile(a,theme,"♫",tr(a,"radio"),"Listen","Radio",nav,0,98),98);
            weighted(a,navrow,tile(a,theme,"⚙",tr(a,"settings"),"Preferences","Postavke",nav,0,98),98);
            fixed(a,body,navrow,98,4);
        }else if(theme==GUIDE){
            caption(a,body,"KELDIN TV GUIDE  /  LIVE FIRST",18);
            LinearLayout split=row(a);
            LinearLayout commands=Ui.vertical(a);
            fixed(a,commands,tile(a,theme,"▣",tr(a,"live"),"All channels","Uživo",nav,0,94),94,10);
            fixed(a,commands,tile(a,theme,"♡",tr(a,"favorites"),"Your channels","Favoriti",nav,0,94),94,10);
            fixed(a,commands,tile(a,theme,"♫",tr(a,"radio"),"Stations","Radio",nav,0,94),94,0);
            LinearLayout.LayoutParams cmd=new LinearLayout.LayoutParams(0,Ui.dp(a,302),.8f);
            cmd.leftMargin=Ui.dp(a,4);cmd.rightMargin=Ui.dp(a,8);
            split.addView(commands,cmd);
            LinearLayout schedule=tile(a,theme,"▦","TV GUIDE",
                "Open the full programme timeline and switch between channels",
                "TV vodič",nav,1,300);
            LinearLayout.LayoutParams sched=new LinearLayout.LayoutParams(0,Ui.dp(a,302),1.75f);
            sched.leftMargin=Ui.dp(a,5);sched.rightMargin=Ui.dp(a,5);
            split.addView(schedule,sched);
            fixed(a,body,split,302,12);
            LinearLayout extra=row(a);
            weighted(a,extra,tile(a,theme,"▶",tr(a,"movies"),"Movies","Filmovi",nav,0,82),82);
            weighted(a,extra,tile(a,theme,"▤",tr(a,"series"),"TV series","Serije",nav,0,82),82);
            weighted(a,extra,tile(a,theme,"⚙",tr(a,"settings"),"Settings","Postavke",nav,0,82),82);
            fixed(a,body,extra,82,4);
        }else if(theme==GLASS){
            caption(a,body,"KELDIN GLASS  /  FLOATING INTERFACE",18);
            LinearLayout split=row(a);
            LinearLayout live=tile(a,theme,"◉",tr(a,"live"),
                "Explore your television world","Uživo",nav,1,231);
            LinearLayout.LayoutParams lv=new LinearLayout.LayoutParams(0,Ui.dp(a,231),1.35f);
            lv.leftMargin=Ui.dp(a,7);lv.rightMargin=Ui.dp(a,9);
            split.addView(live,lv);
            LinearLayout other=Ui.vertical(a);
            fixed(a,other,tile(a,theme,"▶",tr(a,"movies"),"Films","Filmovi",nav,0,109),109,11);
            fixed(a,other,tile(a,theme,"▤",tr(a,"series"),"Series","Serije",nav,0,111),111,0);
            LinearLayout.LayoutParams oth=new LinearLayout.LayoutParams(0,Ui.dp(a,231),1f);
            oth.leftMargin=Ui.dp(a,5);oth.rightMargin=Ui.dp(a,5);
            split.addView(other,oth);
            fixed(a,body,split,231,17);
            LinearLayout lower=row(a);
            weighted(a,lower,tile(a,theme,"▦",tr(a,"guide"),"EPG","TV vodič",nav,0,100),100);
            weighted(a,lower,tile(a,theme,"♫",tr(a,"radio"),"Radio","Radio",nav,0,100),100);
            weighted(a,lower,tile(a,theme,"⚙",tr(a,"settings"),"Preferences","Postavke",nav,0,100),100);
            fixed(a,body,lower,100,5);
        }else{
            caption(a,body,"KELDIN COMPACT   •   "+tr(a,"choose"),17);
            LinearLayout first=row(a);
            weighted(a,first,tile(a,theme,"▣",tr(a,"live"),"TV","Uživo",nav,1,99),99);
            weighted(a,first,tile(a,theme,"▶",tr(a,"movies"),"Films","Filmovi",nav,0,99),99);
            weighted(a,first,tile(a,theme,"▤",tr(a,"series"),"Series","Serije",nav,0,99),99);
            fixed(a,body,first,99,8);
            LinearLayout second=row(a);
            weighted(a,second,tile(a,theme,"▦",tr(a,"guide"),"EPG","TV vodič",nav,0,99),99);
            weighted(a,second,tile(a,theme,"♫",tr(a,"radio"),"Radio","Radio",nav,0,99),99);
            weighted(a,second,tile(a,theme,"♡",tr(a,"favorites"),"Saved","Favoriti",nav,0,99),99);
            fixed(a,body,second,99,8);
            add(a,theme,body,"⚙",tr(a,"settings"),"Playlists and configuration",
                "Postavke",nav,75);
        }
        if(store.sources().isEmpty()){
            TextView add=Ui.button(a,"＋  "+tr(a,"add"),onAdd,true);
            LinearLayout.LayoutParams lp=Ui.lp(a,-1,50);
            lp.topMargin=Ui.dp(a,14);
            body.addView(add,lp);
        }
        content.addView(scroller,new LinearLayout.LayoutParams(-1,0,1f));
    }

    public static void stylePlayer(Activity a,LinearLayout panel){
        int theme=current(a);
        int sw=a.getResources().getDisplayMetrics().widthPixels;
        int width=theme==CINEMA?(int)(sw*.93f):
            theme==GUIDE?(int)(sw*.86f):
            theme==GLASS?(int)(sw*.75f):
            theme==COMPACT?(int)(sw*.70f):(int)(sw*.85f);
        int max=Ui.dp(a,theme==CINEMA?1350:theme==COMPACT?920:1100);
        width=Math.max(Ui.dp(a,420),Math.min(width,max));
        ViewGroup.LayoutParams lp=panel.getLayoutParams();
        if(lp instanceof FrameLayout.LayoutParams){
            FrameLayout.LayoutParams frame=(FrameLayout.LayoutParams)lp;
            frame.width=Math.min(sw-Ui.dp(a,24),width);
            frame.gravity=Gravity.BOTTOM|
                (theme==COMPACT?Gravity.LEFT:Gravity.CENTER_HORIZONTAL);
            frame.bottomMargin=Ui.dp(a,theme==GLASS?24:theme==CINEMA?9:16);
            frame.leftMargin=Ui.dp(a,theme==COMPACT?18:0);
            panel.setLayoutParams(frame);
        }
        GradientDrawable bg=Ui.shape(
            theme==GLASS?0xb922374d:
            theme==CINEMA?0xf51b202c:
            theme==GUIDE?0xee102e42:
            theme==COMPACT?0xf2101824:0xf20d1b2b,
            theme==COMPACT?12:theme==GLASS?25:18,a);
        bg.setStroke(Ui.dp(a,1),
            theme==GLASS?0x99a5daf3:0x886385a1);
        panel.setBackground(bg);
    }

    private static void fakePreview(Activity a,LinearLayout holder,int theme){
        LinearLayout preview=Ui.vertical(a);
        preview.setPadding(Ui.dp(a,8),Ui.dp(a,7),Ui.dp(a,8),Ui.dp(a,7));
        preview.setBackground(Ui.shape(0xff121d2b,9,a));
        int[][] widths=theme==CLASSIC?new int[][]{{1,1,1,1},{1,1}}:
            theme==CINEMA?new int[][]{{3,1},{1,1,1}}:
            theme==GUIDE?new int[][]{{1,4},{1,1,1}}:
            theme==GLASS?new int[][]{{2,1},{1,1,1}}:
            new int[][]{{1,1,1},{1,1,1}};
        for(int[] rowWeights:widths){
            LinearLayout row=Ui.horizontal(a);
            for(int w:rowWeights){
                TextView item=Ui.text(a,"",9,Ui.MUTED,false);
                item.setBackground(Ui.shape(theme==GLASS?0x88669ab8:
                    theme==CINEMA?0xff4b4965:
                    theme==GUIDE?0xff315b69:0xff365069,5,a));
                LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,Ui.dp(a,11),w);
                lp.setMargins(Ui.dp(a,2),Ui.dp(a,2),Ui.dp(a,2),Ui.dp(a,2));
                row.addView(item,lp);
            }
            preview.addView(row);
        }
        holder.addView(preview,Ui.lp(a,133,-2));
    }

    /** D-pad-friendly theme gallery with five miniature layout previews. */
    public static void showGallery(Activity a,Runnable changed){
        ScrollView scroll=new ScrollView(a);
        LinearLayout body=Ui.vertical(a);
        body.setPadding(Ui.dp(a,15),Ui.dp(a,12),Ui.dp(a,15),Ui.dp(a,13));
        scroll.addView(body);
        int old=current(a);
        AlertDialog dialog=new AlertDialog.Builder(a)
            .setTitle("Interface themes")
            .setView(scroll)
            .setNegativeButton("Cancel",null)
            .create();
        for(int i=0;i<LABELS.length;i++){
            final int choice=i;
            LinearLayout card=Ui.horizontal(a);
            card.setGravity(Gravity.CENTER_VERTICAL);
            card.setPadding(Ui.dp(a,12),Ui.dp(a,8),Ui.dp(a,12),Ui.dp(a,8));
            card.setFocusable(true);card.setClickable(true);
            card.setBackground(surface(a,i,false,i==old?1:0));
            fakePreview(a,card,i);
            LinearLayout info=Ui.vertical(a);
            info.setPadding(Ui.dp(a,14),0,0,0);
            TextView name=Ui.text(a,LABELS[i]+(i==old?"   ✓":""),16,Ui.WHITE,true);
            TextView desc=Ui.text(a,DESCRIPTIONS[i],11,Ui.MUTED,false);
            name.setMaxLines(2);desc.setMaxLines(2);
            info.addView(name);info.addView(Ui.space(a,4));info.addView(desc);
            card.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
            card.setContentDescription(LABELS[i]+". "+DESCRIPTIONS[i]);
            card.setOnFocusChangeListener((v,focus)->
                card.setBackground(surface(a,choice,focus,choice==old?1:0)));
            card.setOnClickListener(v->{
                a.getSharedPreferences("keldin_settings",Context.MODE_PRIVATE)
                    .edit().putInt(KEY,choice).apply();
                dialog.dismiss();
                changed.run();
            });
            LinearLayout.LayoutParams lp=Ui.lp(a,-1,-2);
            lp.bottomMargin=Ui.dp(a,8);
            body.addView(card,lp);
        }
        dialog.setOnShowListener(d->{
            android.view.Window window=dialog.getWindow();
            if(window!=null){
                int sw=a.getResources().getDisplayMetrics().widthPixels;
                int sh=a.getResources().getDisplayMetrics().heightPixels;
                window.setLayout(Math.min((int)(sw*.70f),Ui.dp(a,820)),
                    Math.min((int)(sh*.84f),Ui.dp(a,660)));
            }
            if(body.getChildCount()>old)body.getChildAt(old).requestFocus();
        });
        dialog.show();
    }
}
