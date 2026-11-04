from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
def rep(a,b,label):
    global s
    assert a in s, "v0.9.1 compact overlay marker missing: "+label
    s=s.replace(a,b,1)

rep('''        overlay=Ui.vertical(this);overlay.setPadding(Ui.dp(this,45),Ui.dp(this,30),Ui.dp(this,45),Ui.dp(this,27));
        overlay.setBackgroundColor(0xa6091020);
        FrameLayout.LayoutParams overLp=new FrameLayout.LayoutParams(-1,-2,Gravity.BOTTOM);
        screen.addView(overlay,overLp);''',
'''        // Compact, bordered video information panel rather than a full-width bottom shade.
        overlay=Ui.vertical(this);
        overlay.setPadding(Ui.dp(this,19),Ui.dp(this,13),Ui.dp(this,19),Ui.dp(this,12));
        android.graphics.drawable.GradientDrawable infoFrame=
            Ui.shape(0xe60b192a,17,this);
        infoFrame.setStroke(Ui.dp(this,1),0x8896b3cc);
        overlay.setBackground(infoFrame);
        overlay.setElevation(Ui.dp(this,12));
        int videoWidth=getResources().getDisplayMetrics().widthPixels;
        int boxWidth=Math.min((int)(videoWidth*.84f),Ui.dp(this,1020));
        FrameLayout.LayoutParams overLp=new FrameLayout.LayoutParams(
            boxWidth,-2,Gravity.BOTTOM|Gravity.CENTER_HORIZONTAL);
        overLp.setMargins(Ui.dp(this,12),0,Ui.dp(this,12),Ui.dp(this,17));
        screen.addView(overlay,overLp);''',"compact framed video overlay")
rep('''TextView top=Ui.text(this,"KELDIN IPTV   •   FULL",12,Ui.ACCENT,true);''',
    '''TextView top=Ui.text(this,"KELDIN IPTV   •   FULL",10,Ui.ACCENT,true);''',"smaller eyebrow")
rep('''channelName=Ui.text(this,"",29,Ui.WHITE,true);''',
    '''channelName=Ui.text(this,"",23,Ui.WHITE,true);
        channelName.setMaxLines(2);''',"channel title")
rep('''programName=Ui.text(this,"",17,Ui.WHITE,false);''',
    '''programName=Ui.text(this,"",14,Ui.WHITE,false);''',"program name")
rep('''upNext=Ui.text(this,"",12,Ui.MUTED,false);''',
    '''upNext=Ui.text(this,"",11,Ui.MUTED,false);''',"next event line")
rep('''nameBlock.addView(top);nameBlock.addView(Ui.space(this,6));''',
    '''nameBlock.addView(top);nameBlock.addView(Ui.space(this,3));''',"top gap")
rep('''nameBlock.addView(channelName);nameBlock.addView(Ui.space(this,7));''',
    '''nameBlock.addView(channelName);nameBlock.addView(Ui.space(this,3));''',"title gap")
rep('''nameBlock.addView(programName);nameBlock.addView(Ui.space(this,3));''',
    '''nameBlock.addView(programName);nameBlock.addView(Ui.space(this,2));''',"program gap")
rep('''right.addView(live);right.addView(Ui.space(this,7));right.addView(qualityHint);''',
    '''right.addView(live);right.addView(Ui.space(this,3));right.addView(qualityHint);''',"right gap")
rep('''right.addView(Ui.space(this,9));right.addView(favorite);''',
    '''right.addView(Ui.space(this,3));right.addView(favorite);''',"heart gap")
rep('''row.addView(right,Ui.lp(this,190,-2));''',
    '''row.addView(right,Ui.lp(this,172,-2));''',"smaller right column")
rep('''overlay.addView(Ui.space(this,19));''',
    '''overlay.addView(Ui.space(this,7));''',"footer gap")
rep('''favorite.setMinHeight(Ui.dp(this,46));''',
    '''favorite.setMinHeight(Ui.dp(this,36));''',"short heart row")
rep('''favorite.setPadding(Ui.dp(this,9),Ui.dp(this,9),Ui.dp(this,9),Ui.dp(this,9));''',
    '''favorite.setPadding(Ui.dp(this,5),Ui.dp(this,4),Ui.dp(this,5),Ui.dp(this,4));''',"heart padding")
p.write_text(s)
print("v0.9.1: framed mini-player overlay (84% width, lower line spacing), keeps all fields")
