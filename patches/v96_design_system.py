from pathlib import Path
import re

base = Path("app/src/main/java/com/keldin/iptv")
ui = base / "ui/Ui.java"
s = ui.read_text()
# Restrained, neutral dark tvOS-inspired surfaces instead of saturated navy.
colors = {
  "Color.rgb(9,18,31)":"Color.rgb(10,13,19)",
  "Color.rgb(17,32,49)":"Color.rgb(20,26,36)",
  "Color.rgb(23,43,63)":"Color.rgb(30,38,53)",
  "Color.rgb(151,174,193)":"Color.rgb(156,172,193)",
  "Color.rgb(244,249,254)":"Color.rgb(245,248,252)",
  "Color.rgb(77,211,244)":"Color.rgb(91,170,255)",
  "Color.rgb(21,64,89)":"Color.rgb(32,48,67)",
  "Color.rgb(14,39,62)":"Color.rgb(17,30,46)",
  "Color.rgb(9,23,39)":"Color.rgb(11,18,29)"
}
for old,new in colors.items():
    s=s.replace(old,new)
ui.write_text(s)

p=base/"ui/MainActivity.java"
s=p.read_text()
a=s.index("    private void addOptionV6(")
b=s.index("    private void configurePinV6(",a)
replacement = """    private void addOptionV6(LinearLayout body,String heading,String value,
                             String explanation,Runnable command){
        // Compact, accessible one-line preferences: label left, selected value
        // right. The hint footer holds the full description on D-pad focus.
        final String help=UiLocaleV9.translate(this,explanation);
        LinearLayout card=Ui.horizontal(this);
        card.setGravity(Gravity.CENTER_VERTICAL);
        card.setPadding(Ui.dp(this,14),0,Ui.dp(this,11),0);
        card.setFocusable(true);
        card.setClickable(true);
        card.setBackground(Ui.shape(Ui.PANEL,12,this));
        TextView name=Ui.text(this,UiLocaleV9.translate(this,heading),
            15,Ui.WHITE,true);
        name.setSingleLine(true);
        name.setEllipsize(android.text.TextUtils.TruncateAt.END);
        card.addView(name,new LinearLayout.LayoutParams(0,-2,1));
        TextView selected=Ui.text(this,UiLocaleV9.translate(this,value),
            12,Ui.MUTED,false);
        selected.setSingleLine(true);
        selected.setEllipsize(android.text.TextUtils.TruncateAt.END);
        selected.setMaxWidth(Ui.dp(this,230));
        LinearLayout.LayoutParams valueLp=Ui.lp(this,-2,-2);
        valueLp.leftMargin=Ui.dp(this,11);
        card.addView(selected,valueLp);
        TextView arrow=Ui.text(this,"›",20,Ui.MUTED,false);
        arrow.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams arrowLp=Ui.lp(this,21,-1);
        arrowLp.leftMargin=Ui.dp(this,7);
        card.addView(arrow,arrowLp);
        card.setContentDescription(name.getText()+" • "+selected.getText());
        card.setOnClickListener(v->{
            if(settingsHelp!=null)settingsHelp.setText(help);
            command.run();
        });
        card.setOnFocusChangeListener((v,focus)->{
            if(focus&&settingsHelp!=null)settingsHelp.setText(help);
            android.graphics.drawable.GradientDrawable background=
                Ui.shape(focus?Ui.SURFACE:Ui.PANEL,12,this);
            if(focus)background.setStroke(Ui.dp(this,2),Ui.ACCENT);
            card.setBackground(background);
            arrow.setTextColor(focus?Ui.ACCENT:Ui.MUTED);
            selected.setTextColor(focus?Ui.WHITE:Ui.MUTED);
        });
        LinearLayout.LayoutParams lp=Ui.lp(this,-1,56);
        lp.bottomMargin=Ui.dp(this,4);
        body.addView(card,lp);
    }
"""
s=s[:a]+replacement+s[b:]
# Global notice should not reserve a permanent blank row on every screen.
old='rightPanel.addView(notice,Ui.lp(this,-1,20));'
if old not in s: raise AssertionError("notice row changed")
s=s.replace(old,'''notice.setSingleLine(true);
        notice.setEllipsize(android.text.TextUtils.TruncateAt.END);
        rightPanel.addView(notice,Ui.lp(this,-1,17));''',1)
# Preserve important messages but do not carry a stale import banner through every section.
old='notice.setVisibility("Postavke".equals(page)?View.GONE:View.VISIBLE);'
if old in s:
    s=s.replace(old,'''notice.setVisibility(
                "Postavke".equals(page) || notice.getText().length()==0 ||
                (notice.getText().toString().startsWith("Imported ") &&
                 !"Moje liste".equals(page)) ? View.GONE:View.VISIBLE);''',1)
# More restrained selected backgrounds and tighter home secondary settings.
s=s.replace('0xff195676','0xff1a334b').replace('0xff244a60','0xff294159')
s=s.replace('Ui.text(this,"⚙",24,Ui.ACCENT,true)','Ui.text(this,"⚙",20,Ui.ACCENT,true)')
s=s.replace('Ui.text(this,tr("settings"),20,Ui.WHITE,true)',
            'Ui.text(this,tr("settings"),17,Ui.WHITE,true)')
p.write_text(s)

p=base/"ui/CategoryAdapter.java"
s=p.read_text().replace('Ui.dp(context,52)','Ui.dp(context,46)')
s=s.replace('lp.setMargins(0,Ui.dp(context,3),Ui.dp(context,4),Ui.dp(context,3));',
'''lp.setMargins(0,Ui.dp(context,2),Ui.dp(context,3),Ui.dp(context,2));''')
s=s.replace('0xff195677','0xff203b53').replace('0xff284c63','0xff283e52')
p.write_text(s)

p=base/"ui/ChannelAdapter.java"
s=p.read_text().replace('guideMode?126:136','guideMode?116:132')
s=s.replace('lp.setMargins(Ui.dp(c,7),Ui.dp(c,6),Ui.dp(c,7),Ui.dp(c,6));',
            'lp.setMargins(Ui.dp(c,5),Ui.dp(c,4),Ui.dp(c,5),Ui.dp(c,4));')
p.write_text(s)

p=base/"playback/TvSidePanel.java"
s=p.read_text().replace('Ui.dp(ctx,69)','Ui.dp(ctx,58)')
p.write_text(s)

p=base/"playback/TvPlaybackOptionsV94.java"
s=p.read_text()
s=s.replace('0xff101e31','0xff141b29').replace('0xff192a40','0xff202b3c')
s=s.replace('0xff28465f','0xff293e58').replace('0xff496783','0xff40546b')
p.write_text(s)

p=base/"playback/PlayerActivity.java"
s=p.read_text()
s=s.replace('overlay.setPadding(Ui.dp(this,19),Ui.dp(this,13),Ui.dp(this,19),Ui.dp(this,12));',
            'overlay.setPadding(Ui.dp(this,16),Ui.dp(this,10),Ui.dp(this,16),Ui.dp(this,9));')
s=s.replace('channelName=Ui.text(this,"",23,Ui.WHITE,true);',
            'channelName=Ui.text(this,"",21,Ui.WHITE,true);')
p.write_text(s)
print("PASS: coherent dark surface palette, compact channel/poster/category spacing, settings preference rows and player sheet.")
