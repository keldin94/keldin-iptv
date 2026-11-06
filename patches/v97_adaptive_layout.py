from pathlib import Path

base=Path("app/src/main/java/com/keldin/iptv")
def edit(file, before, after, label):
    p=base/file
    source=p.read_text()
    if before not in source: raise AssertionError("v97 layout anchor: "+label)
    p.write_text(source.replace(before,after,1))

# Correct the actual clipping regression: do not force a two-line header
# into 49dp, or a multi-line Settings hint into 40dp.
edit("ui/MainActivity.java",
'''        toolbar.addView(header,new LinearLayout.LayoutParams(0,Ui.dp(this,49),1));''',
'''        title.setMaxLines(2);
        subtitle.setMaxLines(2);
        title.setEllipsize(android.text.TextUtils.TruncateAt.END);
        subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);
        header.setMinimumHeight(Ui.dp(this,63));
        header.setPadding(0,Ui.dp(this,2),0,Ui.dp(this,6));
        toolbar.addView(header,new LinearLayout.LayoutParams(0,-2,1));''',
"main heading auto height")
edit("ui/MainActivity.java",
'''        layout.addView(settingsMetaV96,Ui.lp(this,-1,35));''',
'''        settingsMetaV96.setMinimumHeight(Ui.dp(this,47));
        layout.addView(settingsMetaV96,Ui.lp(this,-1,-2));''',
"active Settings subtitle height")
edit("ui/MainActivity.java",
'''        scope.setSingleLine(true);''',
'''        scope.setMaxLines(2);''',"settings scope adaptive")
edit("ui/MainActivity.java",
'''        layout.addView(settingsHelp,Ui.lp(this,-1,40));''',
'''        settingsHelp.setMaxLines(4);
        settingsHelp.setMinHeight(Ui.dp(this,44));
        layout.addView(settingsHelp,Ui.lp(this,-1,-2));''',
"settings help expands to 4 lines")
edit("ui/MainActivity.java",
'''        card.setGravity(Gravity.CENTER_VERTICAL);
        card.setPadding(Ui.dp(this,14),0,Ui.dp(this,11),0);''',
'''        card.setGravity(Gravity.CENTER_VERTICAL);
        card.setPadding(Ui.dp(this,14),Ui.dp(this,9),Ui.dp(this,11),Ui.dp(this,9));
        card.setMinimumHeight(Ui.dp(this,62));''',"settings preferences not clipped")
edit("ui/MainActivity.java",
'''        name.setSingleLine(true);
        name.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
'''        name.setMaxLines(2);
        name.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
"settings two-line names")
edit("ui/MainActivity.java",
'''        LinearLayout.LayoutParams lp=Ui.lp(this,-1,56);
        lp.bottomMargin=Ui.dp(this,4);''',
'''        LinearLayout.LayoutParams lp=Ui.lp(this,-1,-2);
        lp.bottomMargin=Ui.dp(this,4);''',
"settings options wrap content")
edit("ui/MainActivity.java",
'''        TextView hint=Ui.text(this,tr("appearance")+"  •  "+''',
'''        TextView hint=Ui.text(this,tr("appearance")+"  •  "+''',
"home hint marker sanity")

# Clear crowded Home subtitle when the heading repeats the same call-to-action.
edit("ui/MainActivity.java",
'''        subtitle=Ui.text(this,"",12,Ui.MUTED,false);''',
'''        subtitle=Ui.text(this,"",12,Ui.MUTED,false);
        subtitle.setMaxLines(2);''',"home subtitle measurement")
edit("ui/MainActivity.java",
'''        TextView hint=Ui.text(this,tr("appearance")+"  •  "+
            tr("lists")+"  •  "+tr("network"),12,Ui.MUTED,false);''',
'''        TextView hint=Ui.text(this,tr("appearance")+"  •  "+
            tr("lists")+"  •  "+tr("network"),11,Ui.MUTED,false);
        hint.setMaxLines(2);''',"long settings hints")
# Hide decorative FULL PREVIEW slogan instead of leaving untranslated branding.
edit("ui/MainActivity.java",
'''        TextView premium=Ui.text(this,"✦  FULL PREVIEW",12,Ui.ACCENT,true);''',
'''        TextView premium=Ui.text(this,"KELDIN IPTV",12,Ui.ACCENT,true);''',
"brand badge without stale English")

# Browse category rails need up to two lines at enlarged text sizes.
edit("ui/CategoryAdapter.java",
'''        label.setMaxLines(1);''',
'''        label.setMaxLines(2);''',
"two-line category labels")
edit("ui/CategoryAdapter.java",
'''        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(context,46));''',
'''        shell.setMinimumHeight(Ui.dp(context,53));
        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,ViewGroup.LayoutParams.WRAP_CONTENT);''',
"category heights follow font and title")
edit("ui/CategoryAdapter.java",
'''        shell.setPadding(Ui.dp(context,15),0,Ui.dp(context,9),0);''',
'''        shell.setPadding(Ui.dp(context,12),Ui.dp(context,10),Ui.dp(context,9),Ui.dp(context,10));''',
"category row vertical padding")

# The card previously forced 2-line content into 132dp, and a 32dp
# 2-line EPG label. Both must be measured rather than cropped.
edit("ui/ChannelAdapter.java",
'''        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,Ui.dp(c,guideMode?116:132));''',
'''        box.setMinimumHeight(Ui.dp(c,guideMode?142:150));
        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT);''',
"live cards measured height")
edit("ui/ChannelAdapter.java",
'''        box.addView(program,Ui.lp(c,-1,32));''',
'''        program.setMinHeight(Ui.dp(c,32));
        box.addView(program,Ui.lp(c,-1,-2));''',
"EPG text measured height")
edit("ui/ChannelAdapter.java",
'''        LinearLayout.LayoutParams bar=Ui.lp(c,0,3);bar.topMargin=Ui.dp(c,9);''',
'''        LinearLayout.LayoutParams bar=Ui.lp(c,0,3);bar.topMargin=Ui.dp(c,6);''',
"less unnecessary EPG spacing")

# Player side drawers were 28% wide with a disconnected vertical logo-only
# rail in Categories. Their item rows were always 69dp, causing clipped
# descriptions at TV text scale > 1.0.
p=base/"playback/TvSidePanel.java"; s=p.read_text()
old='''        float fraction=mode==CHANNELS?.28f:mode==CATEGORIES?.40f:
            mode==GUIDE?.36f:.58f;'''
new='''        float fraction=mode==CHANNELS?.38f:mode==CATEGORIES?.39f:
            mode==GUIDE?.38f:.56f;'''
assert old in s,"panel fractions changed"
s=s.replace(old,new,1)
old='''        int alpha=(int)(255*store.panelOpacity()/100f);
        int dark=(alpha<<24)|0x081827;'''
new='''        // Preserve translucency without allowing live video to compete with
        // legibility. 87% opacity is the minimum for text-heavy drawers.
        int alpha=Math.max(222,(int)(255*store.panelOpacity()/100f));
        int dark=(alpha<<24)|0x101927;'''
assert old in s,"panel alpha"
s=s.replace(old,new,1)
s=s.replace('new int[]{dark,((Math.max(30,alpha-80))<<24)|0x081827});',
            'new int[]{dark,((Math.max(206,alpha-12))<<24)|0x101927});',1)
s=s.replace('body.setPadding(Ui.dp(ctx,18),Ui.dp(ctx,19),Ui.dp(ctx,15),Ui.dp(ctx,13));',
            'body.setPadding(Ui.dp(ctx,16),Ui.dp(ctx,14),Ui.dp(ctx,14),Ui.dp(ctx,12));',1)
s=s.replace('''            26,WHITE,true);
        body.addView(title);''',
'''            22,WHITE,true);
        title.setMaxLines(2);
        body.addView(title);''',1)
s=s.replace('detail.setSingleLine(true);detail.setEllipsize(android.text.TextUtils.TruncateAt.END);',
'''detail.setMaxLines(2);
        detail.setEllipsize(android.text.TextUtils.TruncateAt.END);''',1)
s=s.replace('body.addView(Ui.space(ctx,12));','body.addView(Ui.space(ctx,8));',1)
start=s.index('''        if(mode==CATEGORIES){
            LinearLayout split=Ui.horizontal(ctx);''')
end=s.index('''        if(mode==GUIDE_DETAIL){''',start)
assert 'LogoOnlyAdapter' in s[start:end],"expected obsolete logo rail"
s=s[:start]+'''        // One scrollable list. A parallel logo rail was not synchronized
        // with categories, reduced label width and caused overlapping rows.
        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
'''+s[end:]
s=s.replace('body.addView(detailInfo,Ui.lp(ctx,-1,102));',
'''detailInfo.setMinimumHeight(Ui.dp(ctx,88));
            body.addView(detailInfo,Ui.lp(ctx,-1,-2));''',1)
s=s.replace('''        body.addView(legend);''',
'''        legend.setMaxLines(2);
        body.addView(legend);''',1)
s=s.replace('''            row.setPadding(Ui.dp(ctx,13),Ui.dp(ctx,11),Ui.dp(ctx,10),Ui.dp(ctx,11));''',
'''            row.setPadding(Ui.dp(ctx,12),Ui.dp(ctx,9),Ui.dp(ctx,10),Ui.dp(ctx,9));
            row.setMinimumHeight(Ui.dp(ctx,70));''',1)
s=s.replace('''            title.setSingleLine(true);
            title.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
'''            title.setMaxLines(2);
            title.setEllipsize(android.text.TextUtils.TruncateAt.END);''',1)
s=s.replace('''            subtitle.setSingleLine(true);
            subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
'''            subtitle.setMaxLines(2);
            subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);''',1)
s=s.replace('''            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(ctx,69));''',
'''            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(
                -1,ViewGroup.LayoutParams.WRAP_CONTENT);''',1)
s=s.replace('''            lp.bottomMargin=Ui.dp(ctx,5);''',
'''            lp.bottomMargin=Ui.dp(ctx,4);''',1)
s=s.replace('''        TextView eyebrow=Ui.text(ctx,"KELDIN IPTV  /  FULL",10,Ui.ACCENT,true);''',
'''        TextView eyebrow=Ui.text(ctx,"KELDIN IPTV",10,Ui.ACCENT,true);''',1)
p.write_text(s)
# Player options are also translated and must expand when a label wraps.
edit("playback/TvPlaybackOptionsV94.java",
'''            LinearLayout.LayoutParams cell=Ui.lp(activity,-1,64);''',
'''            item.setMinimumHeight(Ui.dp(activity,65));
            LinearLayout.LayoutParams cell=Ui.lp(activity,-1,-2);''',
"options dialog auto height")
edit("playback/TvPlaybackOptionsV94.java",
'''            TextView name=Ui.text(activity,actions[i],17,Ui.WHITE,true);
            TextView detail=Ui.text(activity,details[i],12,Ui.MUTED,false);''',
'''            TextView name=Ui.text(activity,actions[i],16,Ui.WHITE,true);
            name.setMaxLines(2);
            TextView detail=Ui.text(activity,details[i],12,Ui.MUTED,false);
            detail.setMaxLines(3);''',
"options translated descriptions measured")

# Long film/series titles need two lines without losing poster height.
edit("ui/PosterAdapterV6.java",
'''        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(c,255));''',
'''        root.setMinimumHeight(Ui.dp(c,255));
        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(
            -1,ViewGroup.LayoutParams.WRAP_CONTENT);''',
"poster cards adapt to titles")
edit("ui/PosterAdapterV6.java",
'''        root.addView(poster,new LinearLayout.LayoutParams(-1,0,1));''',
'''        root.addView(poster,new LinearLayout.LayoutParams(-1,Ui.dp(c,186)));''',
"poster image retains explicit height")
edit("ui/PosterAdapterV6.java",
'''        title.setSingleLine(true);title.setEllipsize(TextUtils.TruncateAt.END);''',
'''        title.setMaxLines(2);title.setEllipsize(TextUtils.TruncateAt.END);''',
"fuller film/series titles")

print("PASS: flexible row heights, readable channel/category/EPG panels, no disconnected category logo rail")
