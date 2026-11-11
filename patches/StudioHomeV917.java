package com.keldin.iptv.ui;

import android.app.Activity;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

/**
 * Original editorial TV hub drawing on broad streaming/OTT design patterns.
 * No external assets, branding or copyrighted interface resources are used.
 * Navigates existing KELDIN pages; never loads or modifies a playlist.
 */
public final class StudioHomeV917 {
    private StudioHomeV917(){}
    private static final int WHITE=0xfff4faf7;
    private static final int MUTED=0xffa4beb4;
    private static final int MINT=0xff8cdbb6;

    private static LinearLayout.LayoutParams padding(Activity a,int h,int margin){
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,Ui.dp(a,h));
        lp.bottomMargin=Ui.dp(a,margin);
        return lp;
    }
    private static GradientDrawable gradient(Activity a,int[] colors,int corner){
        GradientDrawable bg=new GradientDrawable(GradientDrawable.Orientation.TL_BR,colors);
        bg.setCornerRadius(Ui.dp(a,corner));
        bg.setStroke(Ui.dp(a,1),0xff395b4c);
        return bg;
    }
    private static void heading(Activity a,LinearLayout root,String title){
        TextView label=Ui.text(a,title,14,MUTED,true);
        label.setLetterSpacing(.10f);
        root.addView(label,new LinearLayout.LayoutParams(-1,-2));
        root.addView(Ui.space(a,10));
    }
    private static LinearLayout makeCard(Activity a,String symbol,String label,
            String detail,String route,ThemeV914.Navigation nav,boolean primary,int height){
        LinearLayout card=Ui.vertical(a);
        card.setGravity(Gravity.CENTER_VERTICAL);
        card.setPadding(Ui.dp(a,20),Ui.dp(a,14),Ui.dp(a,16),Ui.dp(a,14));
        GradientDrawable normal=gradient(a,primary?
            new int[]{0xff194032,0xff192d2a}:new int[]{0xff151c20,0xff1b2927},15);
        GradientDrawable focused=gradient(a,
            new int[]{0xff315c4d,0xff174837},15);
        card.setBackground(normal);
        TextView mark=Ui.text(a,symbol,25,MINT,true);
        TextView title=Ui.text(a,label,20,WHITE,true);
        title.setMaxLines(2);
        TextView hint=Ui.text(a,detail,12,MUTED,false);
        hint.setMaxLines(2);
        card.addView(mark);
        card.addView(Ui.space(a,5));
        card.addView(title);
        card.addView(Ui.space(a,4));
        card.addView(hint);
        card.setFocusable(true);
        card.setClickable(true);
        card.setContentDescription(label+", "+detail);
        card.setOnClickListener(v->nav.go(route));
        card.setOnFocusChangeListener((v,hasFocus)->{
            card.setBackground(hasFocus?focused:normal);
            title.setTextColor(hasFocus?0xffadf6cf:WHITE);
        });
        card.setMinimumHeight(Ui.dp(a,height));
        return card;
    }
    private static void addWeighted(Activity a,LinearLayout row,View item,float weight,int h){
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(
            0,Ui.dp(a,h),weight);
        lp.leftMargin=Ui.dp(a,5);
        lp.rightMargin=Ui.dp(a,5);
        row.addView(item,lp);
    }
    private static LinearLayout row(Activity a){
        LinearLayout line=Ui.horizontal(a);
        line.setClipChildren(false);
        line.setClipToPadding(false);
        return line;
    }
    private static LinearLayout feature(Activity a,ThemeV914.Navigation nav){
        LinearLayout hero=Ui.vertical(a);
        hero.setGravity(Gravity.CENTER_VERTICAL);
        hero.setPadding(Ui.dp(a,29),Ui.dp(a,22),Ui.dp(a,26),Ui.dp(a,20));
        hero.setBackground(gradient(a,new int[]{
            0xff102222,0xff1c4c37,0xff0c1b1e},19));
        TextView eyebrow=Ui.text(a,"KELDIN STUDIO    /    WATCH",13,MINT,true);
        eyebrow.setLetterSpacing(.08f);
        hero.addView(eyebrow);
        hero.addView(Ui.space(a,14));
        TextView headline=Ui.text(a,"Television, your way.",31,WHITE,true);
        headline.setMaxLines(2);
        hero.addView(headline);
        hero.addView(Ui.space(a,8));
        TextView sub=Ui.text(a,
            "Your channels, movies and shows in one elegant place.",
            14,0xffc6ded2,false);
        sub.setMaxLines(2);
        hero.addView(sub);
        hero.addView(Ui.space(a,20));
        LinearLayout links=row(a);
        TextView live=Ui.button(a,"▶  Watch Live TV",()->nav.go("Uživo"),true);
        TextView guide=Ui.button(a,"▦  Open TV Guide",()->nav.go("TV vodič"),false);
        links.addView(live,Ui.lp(a,175,49));
        LinearLayout.LayoutParams gp=Ui.lp(a,180,49);
        gp.leftMargin=Ui.dp(a,12);
        links.addView(guide,gp);
        hero.addView(links);
        return hero;
    }
    public static void populate(Activity a,LinearLayout body,ThemeV914.Navigation nav){
        heading(a,body,"FEATURED   /   LIVE TELEVISION");
        LinearLayout featured=row(a);
        addWeighted(a,featured,feature(a,nav),1.95f,260);
        LinearLayout right=Ui.vertical(a);
        LinearLayout.LayoutParams mp=new LinearLayout.LayoutParams(0,Ui.dp(a,260),1f);
        mp.leftMargin=Ui.dp(a,9);
        mp.rightMargin=Ui.dp(a,5);
        featured.addView(right,mp);
        right.addView(makeCard(a,"▣","Movies","Explore your library","Filmovi",
            nav,false,125),padding(a,125,10));
        right.addView(makeCard(a,"▤","Series","Discover episodes","Serije",
            nav,false,125),padding(a,125,0));
        body.addView(featured,padding(a,260,22));
        heading(a,body,"YOUR MEDIA");
        LinearLayout services=row(a);
        addWeighted(a,services,makeCard(a,"◉","Live TV","All channels","Uživo",
            nav,false,115),1f,115);
        addWeighted(a,services,makeCard(a,"♡","Favorites","Saved channels","Favoriti",
            nav,false,115),1f,115);
        addWeighted(a,services,makeCard(a,"♫","Radio","Your stations","Radio",
            nav,false,115),1f,115);
        addWeighted(a,services,makeCard(a,"⚙","Settings","Preferences","Postavke",
            nav,false,115),1f,115);
        body.addView(services,padding(a,115,8));
    }
}
