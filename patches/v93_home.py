from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
def sub(before,after,label):
 global s
 assert before in s, "v0.9.3 home layout marker missing: "+label
 s=s.replace(before,after,1)
sub('''        TextView add=Ui.button(this,"☷  "+tr("lists"),()->navigate("Moje liste"),false);
        LinearLayout.LayoutParams addLp=Ui.lp(this,-2,42);addLp.leftMargin=Ui.dp(this,9);
        toolbar.addView(add,addLp);''','''        // Playlist administration lives in Settings -> Playlists.
        // Keep the top toolbar minimal: Home and Search only.''',"unnecessary top Playlists button")
needle='''        title.setText("Početna".equals(page)?"KELDIN IPTV":displayPage(page));'''
sub(needle,needle+'''
        // Existing vector brand mark, not a new image or external font.
        android.graphics.drawable.Drawable brand=getDrawable(com.keldin.iptv.R.drawable.keldin_icon);
        if(brand!=null){
            brand.setBounds(0,0,Ui.dp(this,39),Ui.dp(this,39));
            title.setCompoundDrawables(brand,null,null,null);
            title.setCompoundDrawablePadding(Ui.dp(this,9));
        }''',"app brand icon beside title")

start=s.index("    private void showHome() {")
end=s.index("    private void landingTile(",start)
home='''    private void homeTileV93(LinearLayout row,String glyph,String label,
                            String summary,String target){
        LinearLayout tile=Ui.vertical(this);
        tile.setPadding(Ui.dp(this,20),Ui.dp(this,19),Ui.dp(this,14),Ui.dp(this,17));
        tile.setGravity(Gravity.CENTER);
        tile.setFocusable(true);tile.setClickable(true);
        tile.setClipChildren(false);tile.setClipToPadding(false);
        android.graphics.drawable.GradientDrawable normal=Ui.shape(Ui.PANEL,20,this);
        normal.setStroke(Ui.dp(this,1),0x665580a1);
        tile.setBackground(normal);
        TextView mark=Ui.text(this,glyph,43,Ui.ACCENT,true);
        mark.setGravity(Gravity.CENTER);
        TextView name=Ui.text(this,label,25,Ui.WHITE,true);
        name.setGravity(Gravity.CENTER);
        name.setMaxLines(1);
        TextView detail=Ui.text(this,summary,12,Ui.MUTED,false);
        detail.setGravity(Gravity.CENTER);
        detail.setMaxLines(2);
        tile.addView(mark);
        tile.addView(Ui.space(this,20));
        tile.addView(name);
        tile.addView(Ui.space(this,8));
        tile.addView(detail);
        tile.setOnClickListener(v->navigate(target));
        tile.setOnFocusChangeListener((v,focus)->{
            android.graphics.drawable.GradientDrawable backdrop=
                Ui.shape(focus?Ui.SURFACE:Ui.PANEL,20,this);
            backdrop.setStroke(Ui.dp(this,focus?3:1),
                focus?Ui.ACCENT:0x665580a1);
            tile.setBackground(backdrop);
            name.setTextColor(focus?Ui.ACCENT:Ui.WHITE);
            // No focus scaling, so the full tile border stays visible.
        });
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-1,1);
        lp.leftMargin=Ui.dp(this,5);
        lp.rightMargin=Ui.dp(this,5);
        row.addView(tile,lp);
    }
    private void showHome() {
        ScrollView scroller=new ScrollView(this);
        scroller.setFillViewport(true);
        scroller.setVerticalScrollBarEnabled(false);
        LinearLayout body=Ui.vertical(this);
        body.setPadding(Ui.dp(this,13),Ui.dp(this,4),
            Ui.dp(this,13),Ui.dp(this,16));
        scroller.addView(body);
        TextView label=Ui.text(this,tr("choose"),18,Ui.WHITE,true);
        body.addView(label);body.addView(Ui.space(this,14));
        LinearLayout primary=Ui.horizontal(this);
        primary.setClipChildren(false);
        primary.setClipToPadding(false);
        homeTileV93(primary,"▣",tr("live"),tr("guide"),"Uživo");
        homeTileV93(primary,"▶",tr("movies"),tr("categories"),"Filmovi");
        homeTileV93(primary,"▤",tr("series"),tr("categories"),"Serije");
        homeTileV93(primary,"♫",tr("radio"),tr("categories"),"Radio");
        int screenHeight=getResources().getDisplayMetrics().heightPixels;
        int heroHeight=Math.max(Ui.dp(this,220),
            Math.min(Ui.dp(this,345),(int)(screenHeight*.47f)));
        body.addView(primary,new LinearLayout.LayoutParams(-1,heroHeight));
        body.addView(Ui.space(this,20));

        LinearLayout secondary=Ui.horizontal(this);
        secondary.setGravity(Gravity.CENTER_VERTICAL);
        secondary.setFocusable(true);secondary.setClickable(true);
        secondary.setPadding(Ui.dp(this,24),Ui.dp(this,10),
            Ui.dp(this,23),Ui.dp(this,10));
        secondary.setBackground(Ui.shape(Ui.PANEL,15,this));
        TextView gear=Ui.text(this,"⚙",24,Ui.ACCENT,true);
        secondary.addView(gear,Ui.lp(this,46,-2));
        TextView settingName=Ui.text(this,tr("settings"),20,Ui.WHITE,true);
        secondary.addView(settingName,new LinearLayout.LayoutParams(0,-2,1));
        TextView hint=Ui.text(this,tr("appearance")+"  •  "+
            tr("lists")+"  •  "+tr("network"),12,Ui.MUTED,false);
        secondary.addView(hint);
        secondary.setOnClickListener(v->navigate("Postavke"));
        secondary.setOnFocusChangeListener((v,focus)->{
            android.graphics.drawable.GradientDrawable bg=
                Ui.shape(focus?Ui.SURFACE:Ui.PANEL,15,this);
            if(focus)bg.setStroke(Ui.dp(this,2),Ui.ACCENT);
            secondary.setBackground(bg);
        });
        body.addView(secondary,Ui.lp(this,-1,69));
        if(store.sources().isEmpty()){
            body.addView(Ui.space(this,18));
            TextView add=Ui.button(this,"＋  "+tr("add"),
                ()->editSource(null,"M3U"),true);
            body.addView(add,Ui.lp(this,300,52));
        }
        content.addView(scroller,new LinearLayout.LayoutParams(-1,0,1));
    }

'''
s=s[:start]+home+s[end:]
p.write_text(s)
print("v0.9.3: full hero group of four unclipped tiles, separate settings bar, compact top links, and brand icon")
