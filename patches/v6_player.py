from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/TvSidePanel.java")
s=p.read_text()
def sub(a,b,label):
    global s
    if a not in s:raise RuntimeError("v6 side panel missing "+label)
    s=s.replace(a,b,1)
sub("public static final int HIDDEN=0, CHANNELS=1, CATEGORIES=2, GUIDE=3;",
"public static final int HIDDEN=0, CHANNELS=1, CATEGORIES=2, GUIDE=3, GUIDE_DETAIL=4;","expanded guide enum")
sub("    private RecyclerView list;","    private RecyclerView list;\n    private TextView detailInfo;","details state")
sub('''        if(mode==CHANNELS){mode=CATEGORIES;refresh();}
        else if(mode==GUIDE){mode=CHANNELS;refresh();}''',
'''        if(mode==CHANNELS){mode=CATEGORIES;refresh();}
        else if(mode==GUIDE_DETAIL){mode=GUIDE;refresh();}
        else if(mode==GUIDE){mode=CHANNELS;refresh();}''',"left")
sub('''        if(mode==CATEGORIES){mode=CHANNELS;refresh();}
        else if(mode==CHANNELS){mode=GUIDE;refresh();}''',
'''        if(mode==CATEGORIES){mode=CHANNELS;refresh();}
        else if(mode==CHANNELS){mode=GUIDE;refresh();}
        else if(mode==GUIDE){mode=GUIDE_DETAIL;refresh();}''',"right")
sub("        if(list!=null)list.scrollToPosition(selection);",
'''        if(list!=null)list.scrollToPosition(selection);
        updateDetailedInfo();''',"move details")
sub("        list=null;adapter=null;rows.clear();",
"        list=null;adapter=null;detailInfo=null;rows.clear();","hide details")
sub('''        }else if(mode==GUIDE){''',
'''        }else if(mode==GUIDE||mode==GUIDE_DETAIL){''',"guide logic")
sub('''                r.subtitle=now?"● U TOKU":clock.format(new Date(program.end+store.guideOffsetHours()*3600_000L));''',
'''                r.subtitle=now?"● LIVE":clock.format(new Date(program.end+store.guideOffsetHours()*3600_000L));''',"now label")
sub('''    private void rebuild(){
        if(panel!=null)host.removeView(panel);''',
'''    private void updateDetailedInfo(){
        if(detailInfo==null || selection<0||selection>=rows.size())return;
        RowData item=rows.get(selection);
        if(item.program!=null){
            String description=item.program.description;
            detailInfo.setText((description==null||description.isEmpty())?
                item.program.title:item.program.title+"\\n"+description);
        }
    }
    private void rebuild(){
        if(panel!=null)host.removeView(panel);''',"detail updater")
sub('''        int panelWidth=Math.min((int)(screenWidth*.41f),Ui.dp(ctx,570));
        panelWidth=Math.min(panelWidth,screenWidth-Ui.dp(ctx,24));
        FrameLayout.LayoutParams frame=new FrameLayout.LayoutParams(panelWidth,-1,
            mode==GUIDE?Gravity.RIGHT:Gravity.LEFT);''',
'''        float fraction=mode==CHANNELS?.28f:mode==CATEGORIES?.40f:
            mode==GUIDE?.36f:.58f;
        int panelWidth=Math.min((int)(screenWidth*fraction),screenWidth-Ui.dp(ctx,28));
        FrameLayout.LayoutParams frame=new FrameLayout.LayoutParams(panelWidth,-1,
            (mode==GUIDE||mode==GUIDE_DETAIL)?Gravity.RIGHT:Gravity.LEFT);''',"panel widths")
sub('''        panel.setBackground(rounded(0xf20e1c2f,19));''',
'''        int alpha=(int)(255*store.panelOpacity()/100f);
        int dark=(alpha<<24)|0x081827;
        // Smooth alpha edge, with video visible underneath.
        android.graphics.drawable.GradientDrawable layer=
            new android.graphics.drawable.GradientDrawable(
            (mode==GUIDE||mode==GUIDE_DETAIL)?
                android.graphics.drawable.GradientDrawable.Orientation.LEFT_RIGHT:
                android.graphics.drawable.GradientDrawable.Orientation.RIGHT_LEFT,
            new int[]{dark,((Math.max(30,alpha-80))<<24)|0x081827});
        layer.setCornerRadius(Ui.dp(ctx,18));
        layer.setStroke(Ui.dp(ctx,1),0x5540637b);
        panel.setBackground(layer);''',"opacity")
sub('''        TextView eyebrow=Ui.text(ctx,"KELDIN IPTV   /   FULL",10,CYAN,true);''',
'''        TextView eyebrow=Ui.text(ctx,"KELDIN IPTV  /  FULL",10,Ui.ACCENT,true);''',"accent")
sub('''            mode==CHANNELS?"TV kanali":mode==CATEGORIES?"Kategorije":"TV vodič",''',
'''            mode==CHANNELS?"TV Channels":mode==CATEGORIES?"Categories":
                mode==GUIDE?"TV Guide":"TV Guide · Details",''',"titles")
sub('''        TextView detail=Ui.text(ctx,mode==GUIDE?current.name:
            mode==CHANNELS?selectedCategory:"Odaberi kategoriju",12,MUTED,false);''',
'''        TextView detail=Ui.text(ctx,(mode==GUIDE||mode==GUIDE_DETAIL)?current.name:
            mode==CHANNELS?selectedCategory:"Select category",12,MUTED,false);''',"detail")
sub('''        body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        if(selection>0)list.scrollToPosition(selection);''',
'''        if(mode==CATEGORIES){
            LinearLayout split=Ui.horizontal(ctx);
            split.setGravity(Gravity.TOP);
            split.addView(list,new LinearLayout.LayoutParams(0,-1,1));
            LinearLayout logoRail=Ui.vertical(ctx);
            logoRail.setPadding(Ui.dp(ctx,6),Ui.dp(ctx,4),Ui.dp(ctx,5),0);
            int shown=0;
            for(Channel c:store.channels()){
                if(!"LIVE".equals(c.kind)||!c.sourceId.equals(current.sourceId))continue;
                if(!"Sve kategorije".equals(selectedCategory)&&!selectedCategory.equals(c.group))continue;
                if(++shown>8)break;
                android.widget.ImageView icon=new android.widget.ImageView(ctx);
                icon.setScaleType(android.widget.ImageView.ScaleType.FIT_CENTER);
                com.keldin.iptv.ui.LogoLoader.load(icon,c.logo,loaded->{});
                LinearLayout.LayoutParams cp=Ui.lp(ctx,40,47);
                cp.bottomMargin=Ui.dp(ctx,8);
                logoRail.addView(icon,cp);
            }
            split.addView(logoRail,Ui.lp(ctx,52,-1));
            body.addView(split,new LinearLayout.LayoutParams(-1,0,1));
        }else body.addView(list,new LinearLayout.LayoutParams(-1,0,1));
        if(mode==GUIDE_DETAIL){
            detailInfo=Ui.text(ctx,"",12,WHITE,false);
            detailInfo.setMaxLines(4);
            detailInfo.setPadding(Ui.dp(ctx,8),Ui.dp(ctx,8),Ui.dp(ctx,8),Ui.dp(ctx,10));
            detailInfo.setBackground(Ui.shape(0x66204058,12,ctx));
            body.addView(detailInfo,Ui.lp(ctx,-1,102));
            updateDetailedInfo();
        }
        if(selection>0)list.scrollToPosition(selection);''',"rail and details")
sub('''                mode==GUIDE?"← Kanali   •   BACK Zatvori   •   OK Detalji":''',
'''                mode==GUIDE?"← Channels   •   → Detail guide   •   OK Info":
                mode==GUIDE_DETAIL?"← Quick guide   •   BACK Close":''',"legend")
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def edit(a,b,label):
    global s
    if a not in s:raise RuntimeError("v6 Player marker missing "+label)
    s=s.replace(a,b,1)
edit('''import com.keldin.iptv.data.PlaylistSource;''',
'''import com.keldin.iptv.data.PlaylistSource;
import com.keldin.iptv.net.PlaylistSync;''',"network import")
edit('''    private TvSidePanel sidePanel;''',
'''    private TvSidePanel sidePanel;
    private PlaylistSync guideSync;
    private final java.util.HashSet<String> requestedGuides=new java.util.HashSet<>();''',"guide fields")
edit('''        createUi();
        handler.post(refreshInfo);''',
'''        createUi();
        guideSync=new PlaylistSync(this,store);
        handler.post(refreshInfo);''',"guide setup")
edit('''        handler.removeCallbacks(hideControls);
        super.onDestroy();''',
'''        handler.removeCallbacks(hideControls);
        if(guideSync!=null)guideSync.shutdown();
        super.onDestroy();''',"guide cleanup")
# live within active category only (wrap first/last)
edit('''        position=(position+delta+queue.size())%queue.size();
        releasePlayer();
        current=queue.get(position);''',
'''        if(current!=null && "LIVE".equals(current.kind)){
            ArrayList<Channel> group=new ArrayList<>();
            for(Channel ch:queue)
                if(ch.sourceId.equals(current.sourceId)&&ch.group.equals(current.group)
                    && "LIVE".equals(ch.kind))group.add(ch);
            if(group.isEmpty())return;
            int ix=0;
            for(int i=0;i<group.size();i++)
                if(group.get(i).key().equals(current.key())){ix=i;break;}
            Channel next=group.get((ix+delta+group.size())%group.size());
            position=queue.indexOf(next);
            releasePlayer();
            current=next;
        }else{
            position=(position+delta+queue.size())%queue.size();
            releasePlayer();
            current=queue.get(position);
        }''',"cycle inside group")
# Back only closes the player; confirmation on actual app exit (MainActivity).
edit('''        showExitConfirmation();
    }

    // Intercept remote navigation''',
'''        finish();
    }

    // Intercept remote navigation''',"exit semantics")
edit('''            sidePanel.openGuide(current);
            return true;''',
'''            sidePanel.openGuide(current);
            requestGuideIfNeeded();
            return true;''',"lazy guide")
# method before options
needle="    private void showOptions() {"
assert needle in s
method='''    private void requestGuideIfNeeded(){
        if(current==null||guideSync==null)return;
        PlaylistSource src=store.sourceById(current.sourceId);
        if(src==null||src.guideUrl().isEmpty()||requestedGuides.contains(src.id))return;
        requestedGuides.add(src.id);
        guideSync.refreshEpg(src,(count,status,error)->{
            if(isFinishing()||isDestroyed()||sidePanel==null)return;
            if(sidePanel.isOpen()&&current!=null)
                sidePanel.openGuide(current);
        });
    }

'''
s=s.replace(needle,method+needle,1)
# Persist selected kind during video, except radio should not use live overlay buttons.
p.write_text(s)
print("v0.6 overlay opacity, two EPG levels, group-bound channel zapping and lazy guide integrated")
