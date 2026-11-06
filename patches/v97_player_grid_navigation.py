from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def change(old,new,label):
    global s
    if old not in s: raise AssertionError("v0.9.7 player: "+label)
    s=s.replace(old,new,1)

change('''    private TextView quickChannelList;''',
'''    private TextView quickChannelList,quickGuideV97,quickGridV97;
    private TvGridPanelV97 gridPanelV97;
    private boolean gridBackUpV97=false;''',"grid controls and state")

change('''    private void createUi(){''',
'''    private void openTvGridV97(){
        if(current==null||gridPanelV97==null||!"LIVE".equals(current.kind))return;
        handler.removeCallbacks(hideControls);
        if(sidePanel!=null&&sidePanel.isOpen())sidePanel.hide();
        setControls(false);
        gridPanelV97.open(current); // Keep existing ExoPlayer running behind TV grid.
    }

    private void createUi(){''',"grid opening method")

change('''        buttons.setGravity(Gravity.RIGHT|Gravity.CENTER_VERTICAL);''',
'''        buttons.setGravity(Gravity.CENTER_VERTICAL);''',
"actions full width")

change('''        quickChannelList=compactAction("☷",tr("tv_channels"),this::openChannelListV95);''',
'''        quickGridV97=compactAction("▦  "+
            com.keldin.iptv.ui.UiLocaleV9.translate(this,"TV Grid"),
            com.keldin.iptv.ui.UiLocaleV9.translate(this,"TV Grid"),
            this::openTvGridV97);
        quickGridV97.setTextSize(13f);
        quickGridV97.setSingleLine(true);
        quickGridV97.setEllipsize(android.text.TextUtils.TruncateAt.END);
        quickGuideV97=compactAction("▤  "+tr("guide"),tr("guide"),
            this::openGuideFromQuickV95);
        quickGuideV97.setTextSize(13f);
        quickGuideV97.setSingleLine(true);
        quickGuideV97.setEllipsize(android.text.TextUtils.TruncateAt.END);
        quickChannelList=compactAction("☷",tr("tv_channels"),this::openChannelListV95);''',
"TV Grid and Guide primary actions")

change('''        quickActions=new TextView[]{
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
        overlay.addView(row);
        overlay.addView(Ui.space(this,5));''',
'''        quickActions=new TextView[]{
            quickGridV97,quickGuideV97,quickChannelList,quickPrevious,
            quickPause,quickNext,favorite,quickMore
        };
        for(TextView action:quickActions){
            float weight=(action==quickGridV97||action==quickGuideV97)?1.7f:1f;
            LinearLayout.LayoutParams item=new LinearLayout.LayoutParams(
                0,Ui.dp(this,49),weight);
            item.leftMargin=Ui.dp(this,3);
            buttons.addView(action,item);
        }
        // A two-level mini-panel: programme information first, clearly
        // labelled TV Grid / Guide and transport controls second.
        row.addView(right,Ui.lp(this,155,-2));
        overlay.addView(row);
        overlay.addView(Ui.space(this,8));
        overlay.addView(buttons,Ui.lp(this,-1,51));
        overlay.addView(Ui.space(this,5));''',
"balanced information and full-width accessible buttons")

change('''        help.addView(hints);
        overlay.addView(help);''',
'''        hints.setMaxLines(2);
        // Control names are visible in the row above; keep the status strip
        // small instead of printing an overflowing remote-instruction line.
        overlay.addView(help);''',"hide redundant instruction strip")

change('''        sidePanel=new TvSidePanel(this,screen,store,channel->selectOverlayChannel(channel));''',
'''        sidePanel=new TvSidePanel(this,screen,store,channel->selectOverlayChannel(channel));
        gridPanelV97=new TvGridPanelV97(
            this,screen,store,channel->selectOverlayChannel(channel));''',"initialize grid overlay")

change('''            moveQuickFocus(dir<0?1:3);''',
'''            moveQuickFocus(dir<0?3:5);''',"navigation focus indexes")

change('''                moveQuickFocus(2); // Focus Pause after adding Channels button.''',
'''                moveQuickFocus(4); // Pause stays the default focus with TV Grid + Guide.''',
"initial OK focus")

change('''    @Override public boolean dispatchKeyEvent(KeyEvent event){
        if(handleOverlayBackV94(event))return true;''',
'''    @Override public boolean dispatchKeyEvent(KeyEvent event){
        int gridKey=event.getKeyCode();
        if(gridBackUpV97&&event.getAction()==KeyEvent.ACTION_UP&&
           (gridKey==KeyEvent.KEYCODE_BACK||gridKey==KeyEvent.KEYCODE_ESCAPE)){
            gridBackUpV97=false;
            return true;
        }
        if(gridPanelV97!=null&&gridPanelV97.isOpen()){
            if(event.getAction()==KeyEvent.ACTION_DOWN &&
               (gridKey==KeyEvent.KEYCODE_BACK||gridKey==KeyEvent.KEYCODE_ESCAPE))
                gridBackUpV97=true;
            if(event.getAction()==KeyEvent.ACTION_DOWN&&
               (gridKey==KeyEvent.KEYCODE_DPAD_CENTER||gridKey==KeyEvent.KEYCODE_ENTER))
                remoteCentreConsumedV95=true;
            if(gridPanelV97.handleKey(event))return true;
        }
        if(handleOverlayBackV94(event))return true;''',
"intercept TV Grid remote keys before mini-panel")

# Direct onBackPressed can be called by device implementations that bypass dispatch.
change('''    @Override public void onBackPressed(){''',
'''    @Override public void onBackPressed(){
        if(gridPanelV97!=null&&gridPanelV97.isOpen()){
            gridPanelV97.hide();
            return;
        }''',"back closes grid before exiting player")

change('''    @Override protected void onStop(){
        handler.removeCallbacks(retry);''',
'''    @Override protected void onStop(){
        if(gridPanelV97!=null)gridPanelV97.hide();
        handler.removeCallbacks(retry);''',"cleanup grid on player lifecycle")

p.write_text(s)
print("PASS: TV Grid and Guide primary OK actions, two-level mini-panel, remote and back behavior")
