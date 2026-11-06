from pathlib import Path

BASE=Path("app/src/main/java/com/keldin/iptv")
def modify(path):
    p=BASE/path
    return p,p.read_text()

def swap(s,before,after,label):
    if before not in s:
        raise AssertionError("v0.9.7 missing "+label)
    return s.replace(before,after,1)

# ----------------- Player: one readable content area + action bar -----------------
p,s=modify("playback/PlayerActivity.java")
s=swap(s,'''    private TextView quickChannelList;''',
'''    private TextView quickChannelList;
    private TextView quickGuideV97, quickGridV97;''',"quick buttons fields")
s=swap(s,'''    private void createUi(){''',
'''    private void openGridV97(){
        if(current==null||sidePanel==null||!"LIVE".equals(current.kind))return;
        handler.removeCallbacks(hideControls);
        setControls(false);
        sidePanel.openGrid(current);
    }
    private void createUi(){''',"grid action method")
s=swap(s,'''        quickChannelList=compactAction("☷",tr("tv_channels"),this::openChannelListV95);''',
'''        quickChannelList=compactAction("☷",tr("tv_channels"),this::openChannelListV95);
        quickGuideV97=compactAction("▤  "+tr("guide"),tr("guide"),this::openGuideFromQuickV95);
        quickGridV97=compactAction("▦  "+tr("tv_grid"),tr("tv_grid"),this::openGridV97);
        quickGuideV97.setTextSize(13);
        quickGridV97.setTextSize(13);''',"visible TV guide and grid actions")
s=swap(s,'''        quickActions=new TextView[]{
            quickChannelList,quickPrevious,quickPause,quickNext,favorite,quickMore
        };
        for(TextView action:quickActions){
            LinearLayout.LayoutParams item=Ui.lp(this,44,45);
            item.leftMargin=Ui.dp(this,3);
            buttons.addView(action,item);
        }
        right.addView(Ui.space(this,6));
        right.addView(buttons,Ui.lp(this,-1,47));
        row.addView(right,Ui.lp(this,308,-2));
        overlay.addView(row);''',
'''        quickActions=new TextView[]{
            quickChannelList,quickGuideV97,quickGridV97,
            quickPrevious,quickPause,quickNext,favorite,quickMore
        };
        // Actions use a dedicated second row, so the channel title/EPG
        // never competes with the remote buttons for horizontal space.
        buttons.setGravity(Gravity.LEFT|Gravity.CENTER_VERTICAL);
        for(TextView action:quickActions){
            int width=(action==quickGuideV97||action==quickGridV97)?108:44;
            LinearLayout.LayoutParams item=Ui.lp(this,width,46);
            item.leftMargin=Ui.dp(this,4);
            buttons.addView(action,item);
        }
        row.addView(right,Ui.lp(this,166,-2));
        overlay.addView(row);
        overlay.addView(Ui.space(this,8));
        overlay.addView(buttons,Ui.lp(this,-1,48));''',"independent action row")
s=swap(s,'''        TextView hints=Ui.text(this, "← "+tr("tv_channels")+"   → "+tr("guide")+
            "   ↑↓ "+tr("tv_channels")+"   OK "+
            com.keldin.iptv.ui.UiLocaleV9.translate(this,"Options")+"   BACK",12,Ui.MUTED,false);
        help.addView(hints);''',
'''        TextView hints=Ui.text(this,"↑↓  "+tr("tv_channels")+"   •   BACK",10,Ui.MUTED,false);
        hints.setSingleLine(true);
        hints.setEllipsize(android.text.TextUtils.TruncateAt.END);
        help.addView(hints,Ui.lp(this,-2,-2));''',"clipped help shortcuts")
s=swap(s,'''            moveQuickFocus(dir<0?1:3);''',
'''            moveQuickFocus(dir<0?3:5);''',"left/right initial action focus")
s=swap(s,'''                moveQuickFocus(2); // Focus Pause after adding Channels button.''',
'''                moveQuickFocus(4); // Pause after Channels, Guide and Grid.''',"initial play pause focus")
# Player remains the same instance while opening navigation; no playback reset.
p.write_text(s)

# ------------------- Side panel: accessible rows, no dummy logo rail -----------------
p,s=modify("playback/TvSidePanel.java")
s=swap(s,'''public static final int HIDDEN=0, CHANNELS=1, CATEGORIES=2, GUIDE=3;''',
'''public static final int HIDDEN=0, CHANNELS=1, CATEGORIES=2, GUIDE=3;
    public static final int GRID=5;''',"grid mode")
s=swap(s,'''    public void openGuide(Channel channel){''',
'''    public void openGrid(Channel channel){
        if(channel==null)return;
        current=channel;
        mode=GRID;
        refresh();
        resetAutoHide();
    }
    public void openGuide(Channel channel){''',"open grid while stream continues")
s=swap(s,'''        else if(mode==GUIDE){hide();}
    }
    public void right(){''',
'''        else if(mode==GUIDE){hide();}
        else if(mode==GRID){mode=CHANNELS;refresh();resetAutoHide();}
    }
    public void right(){''',"grid left to channel list")
s=swap(s,'''        else if(mode==GUIDE){mode=GUIDE_DETAIL;refresh();resetAutoHide();}
    }''',
'''        else if(mode==GUIDE){mode=GUIDE_DETAIL;refresh();resetAutoHide();}
        else if(mode==GRID){mode=GUIDE;refresh();resetAutoHide();}
    }''',"grid right to guide")
s=swap(s,'''        if(mode==CHANNELS && r.channel!=null){''',
'''        if((mode==CHANNELS||mode==GRID) && r.channel!=null){''',"grid selects channel")
s=swap(s,'''        if(mode==CHANNELS){
            List<Channel> channels=store.channels();''',
'''        if(mode==CHANNELS||mode==GRID){
            List<Channel> channels=store.channels();''',"grid scans live TV")
s=swap(s,'''                if(!"Sve kategorije".equals(selectedCategory)&&!selectedCategory.equals(c.group))continue;
                RowData r=new RowData();''',
'''                if(mode==CHANNELS && !"Sve kategorije".equals(selectedCategory)
                    && !selectedCategory.equals(c.group))continue;
                RowData r=new RowData();''',"grid includes every live category")
s=swap(s,'''                r.subtitle=c.group+(store.favorite(c)?"  •  ♥":"");''',
'''                r.subtitle=""; // lazy EPG binding; no repeated category name.''',"no duplicate category label")
s=swap(s,'''        float fraction=mode==CHANNELS?.28f:mode==CATEGORIES?.40f:
            mode==GUIDE?.36f:.58f;''',
'''        float fraction=mode==GRID?.88f:mode==CHANNELS?.37f:
            mode==CATEGORIES?.36f:mode==GUIDE?.40f:.44f;''',"legible overlay width")
s=swap(s,'''            (mode==GUIDE||mode==GUIDE_DETAIL)?Gravity.RIGHT:Gravity.LEFT);''',
'''            mode==GRID?Gravity.CENTER:
                ((mode==GUIDE||mode==GUIDE_DETAIL)?Gravity.RIGHT:Gravity.LEFT));''',
"grid centered above video")
s=swap(s,'''        int margin=Ui.dp(ctx,16);''',
'''        int margin=Ui.dp(ctx,12);''',"comfortable safe margins")
s=swap(s,'''        int alpha=(int)(255*store.panelOpacity()/100f);''',
'''        int alpha=Math.max(215,(int)(255*store.panelOpacity()/100f));''',"readable text contrast")
s=swap(s,'''        body.setPadding(Ui.dp(ctx,18),Ui.dp(ctx,19),Ui.dp(ctx,15),Ui.dp(ctx,13));''',
'''        body.setPadding(Ui.dp(ctx,17),Ui.dp(ctx,13),Ui.dp(ctx,17),Ui.dp(ctx,13));''',"panel safe padding")
s=swap(s,'''            mode==CHANNELS?tr("tv_channels"):mode==CATEGORIES?tr("categories"):
                mode==GUIDE?tr("guide"):tr("guide")+" · "+tr("details"),
            26,WHITE,true);''',
'''            mode==CHANNELS?tr("tv_channels"):mode==CATEGORIES?tr("categories"):
                mode==GRID?tr("tv_grid"):mode==GUIDE?tr("guide"):
                    tr("guide")+" · "+tr("details"),
            23,WHITE,true);
        title.setMaxLines(2);
        title.setEllipsize(android.text.TextUtils.TruncateAt.END);''',"smaller readable panel titles")
s=swap(s,'''        list.setLayoutManager(new LinearLayoutManager(ctx));''',
'''        list.setLayoutManager(mode==GRID?
            new androidx.recyclerview.widget.GridLayoutManager(ctx,3):
            new LinearLayoutManager(ctx));''',"three-column TV Grid")
start=s.index('''        if(mode==CATEGORIES){
            LinearLayout split=Ui.horizontal(ctx);''',s.index("    private void rebuild(){"))
end=s.index("        if(mode==GUIDE_DETAIL){",start)
s=s[:start]+'''        // A single RecyclerView owns rows and selection.
        // The old independent logo rail scrolled out of sync and covered text.
        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
'''+s[end:]
s=swap(s,'''            body.addView(detailInfo,Ui.lp(ctx,-1,102));''',
'''            detailInfo.setEllipsize(android.text.TextUtils.TruncateAt.END);
            body.addView(detailInfo,Ui.lp(ctx,-1,-2));''',"guide detail wrap content")
s=swap(s,'''            mode==CATEGORIES?"→ "+tr("tv_channels")+"   •   ↑↓   •   OK":''',
'''            mode==GRID?"← "+tr("tv_channels")+"   •   → "+tr("guide")+"   •   OK":
            mode==CATEGORIES?"→ "+tr("tv_channels")+"   •   ↑↓   •   OK":''',"TV Grid remote hint")
s=swap(s,'''        body.addView(legend);
    }

    private final class LogoOnlyAdapter''',
'''        legend.setSingleLine(true);
        legend.setEllipsize(android.text.TextUtils.TruncateAt.END);
        body.addView(legend);
    }

    private final class LogoOnlyAdapter''',"footer fits safe area")
s=swap(s,'''            row.setPadding(Ui.dp(ctx,13),Ui.dp(ctx,11),Ui.dp(ctx,10),Ui.dp(ctx,11));''',
'''            row.setPadding(Ui.dp(ctx,12),Ui.dp(ctx,9),Ui.dp(ctx,10),Ui.dp(ctx,9));
            row.setMinimumHeight(Ui.dp(ctx,72));''',"rows can grow with text")
s=swap(s,'''            title.setSingleLine(true);
            title.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
'''            title.setMaxLines(2);
            title.setEllipsize(android.text.TextUtils.TruncateAt.END);''',"row heading two lines")
s=swap(s,'''            subtitle.setSingleLine(true);
            subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);''',
'''            subtitle.setMaxLines(2);
            subtitle.setEllipsize(android.text.TextUtils.TruncateAt.END);''',"EPG now two lines")
s=swap(s,'''            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(ctx,58));''',
'''            RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,-2);''',"wrap rows instead of clipping")
s=swap(s,'''            holder.subtitle.setText(r.subtitle);''',
'''            String subtitle=r.subtitle;
            if((mode==CHANNELS||mode==GRID)&&r.channel!=null){
                subtitle=tr("guide_unavailable");
                long now=System.currentTimeMillis();
                List<GuideProgram> guide=store.schedule(r.channel,now);
                for(GuideProgram program:guide){
                    long a=program.start+store.guideOffsetHours()*3600_000L;
                    long b=program.end+store.guideOffsetHours()*3600_000L;
                    if(a<=now && b>now){subtitle=program.title;break;}
                }
            }
            holder.subtitle.setText(subtitle);''',"show actual EPG on live channel rows")
# Shorter timeout only for regular overlay, grid remains accessible for browsing.
s=swap(s,'''        if(mode!=HIDDEN&&seconds>0)
            autoHideHandler.postDelayed(autoHideTask,Math.min(30,seconds)*1000L);''',
'''        if(mode!=HIDDEN&&seconds>0)
            autoHideHandler.postDelayed(autoHideTask,
                (mode==GRID?Math.max(30,seconds):Math.min(30,seconds))*1000L);''',
"TV Grid not auto dismissed after six seconds")
p.write_text(s)

# -------- Global home page, lists, settings: no fixed-height text clipping --------
p,s=modify("ui/MainActivity.java")
s=swap(s,'''        toolbar.addView(header,new LinearLayout.LayoutParams(0,Ui.dp(this,49),1));''',
'''        header.setMinimumHeight(Ui.dp(this,60));
        toolbar.addView(header,new LinearLayout.LayoutParams(0,-2,1));''',
"flexible page heading and subtitle")
s=swap(s,'''        layout.addView(settingsHelp,Ui.lp(this,-1,40));''',
'''        settingsHelp.setMaxLines(3);
        settingsHelp.setEllipsize(android.text.TextUtils.TruncateAt.END);
        layout.addView(settingsHelp,Ui.lp(this,-1,-2));''',
"settings hint wrap not cropped")
s=swap(s,'''        layout.addView(settingsMetaV96,Ui.lp(this,-1,35));''',
'''        settingsMetaV96.setMinimumHeight(Ui.dp(this,38));
        layout.addView(settingsMetaV96,Ui.lp(this,-1,-2));''',
"setting tab descriptor wrap")
p.write_text(s)

p,s=modify("ui/CategoryAdapter.java")
s=swap(s,'''        shell.setPadding(Ui.dp(context,15),0,Ui.dp(context,9),0);''',
'''        shell.setPadding(Ui.dp(context,13),Ui.dp(context,8),
            Ui.dp(context,9),Ui.dp(context,8));
        shell.setMinimumHeight(Ui.dp(context,54));''',
"category safe vertical area")
s=swap(s,'''        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,Ui.dp(context,46));''',
'''        RecyclerView.LayoutParams lp=new RecyclerView.LayoutParams(-1,-2);''',
"category grows with text")
s=swap(s,'''        label.setMaxLines(1);''',
'''        label.setMaxLines(2);''',"category titles show two lines")
p.write_text(s)

# New UI strings on every supported locale are in the same I18n table.
p,s=modify("ui/I18n.java")
anchor='''        put("tv_channels",'''
assert anchor in s,"missing translated tv_channels anchor"
new='''        put("tv_grid","TV Grid","TV mreža","TV-mreža","Cuadrícula TV","Grade TV",
            "टीवी ग्रिड","شبكة القنوات","Grille TV","Kisi TV","TV-Raster",
            "TV ızgarası","TVグリッド","TV 그리드","电视网格","Сетка каналов","টিভি গ্রিড");
'''
s=s.replace(anchor,new+anchor,1)
p.write_text(s)
g=Path("app/build.gradle")
s=g.read_text()
assert "versionCode 906" in s and "versionName '0.9.6'" in s,"incorrect source version before 0.9.7"
g.write_text(s.replace("versionCode 906","versionCode 907",1)
               .replace("versionName '0.9.6'","versionName '0.9.7'",1))
print("PASS: v0.9.7 flexible text, visible TV Guide/TV Grid buttons, live channel EPG, independent D-pad overlay without reloading video")
