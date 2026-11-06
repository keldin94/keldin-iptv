from pathlib import Path

BASE=Path("app/src/main/java/com/keldin/iptv")
main=BASE/"ui/MainActivity.java"
s=main.read_text()

def change(before,after,label):
    global s
    if before not in s:
        raise AssertionError("v0.9.6 UI anchor missing: "+label)
    s=s.replace(before,after,1)

# Global Android TV shell: trim blank header bands, keep buttons large enough for D-pad.
change('rightPanel.setPadding(Ui.dp(this,28),Ui.dp(this,20),Ui.dp(this,22),Ui.dp(this,16));',
       'rightPanel.setPadding(Ui.dp(this,18),Ui.dp(this,10),Ui.dp(this,16),Ui.dp(this,9));',"global outer padding")
change('title=Ui.text(this,"",28,Ui.WHITE,true);',
       'title=Ui.text(this,"",24,Ui.WHITE,true);',"header title")
change('toolbar.addView(header,new LinearLayout.LayoutParams(0,Ui.dp(this,62),1));',
       'toolbar.addView(header,new LinearLayout.LayoutParams(0,Ui.dp(this,49),1));',"header band")
change('toolbar.addView(now,Ui.lp(this,115,42));',
       'toolbar.addView(now,Ui.lp(this,96,36));',"toolbar date")
change('LinearLayout.LayoutParams hp=Ui.lp(this,-2,42);hp.leftMargin=Ui.dp(this,9);',
       'LinearLayout.LayoutParams hp=Ui.lp(this,-2,36);hp.leftMargin=Ui.dp(this,6);',"home toolbar")
change('LinearLayout.LayoutParams sp=Ui.lp(this,-2,42);sp.leftMargin=Ui.dp(this,9);',
       'LinearLayout.LayoutParams sp=Ui.lp(this,-2,36);sp.leftMargin=Ui.dp(this,6);',"search toolbar")
change('cp.topMargin=Ui.dp(this,7);','cp.topMargin=Ui.dp(this,3);',"content start gap")
change('''        page=destination;searchQuery="";
        if("Postavke".equals(page)){''',
'''        page=destination;searchQuery="";
        if(notice!=null)
            notice.setVisibility("Postavke".equals(page)?View.GONE:View.VISIBLE);
        if("Postavke".equals(page)){''',"hide unnecessary status banner in Settings")
# Opening Settings from player should not trigger startup-channel playback.
change('tile.setPadding(Ui.dp(this,20),Ui.dp(this,19),Ui.dp(this,14),Ui.dp(this,17));',
       'tile.setPadding(Ui.dp(this,15),Ui.dp(this,12),Ui.dp(this,12),Ui.dp(this,11));',"dashboard tile padding")
change('TextView mark=Ui.text(this,glyph,43,Ui.ACCENT,true);',
       'TextView mark=Ui.text(this,glyph,34,Ui.ACCENT,true);',"dashboard icon")
change('TextView name=Ui.text(this,label,25,Ui.WHITE,true);',
       'TextView name=Ui.text(this,label,21,Ui.WHITE,true);',"dashboard labels")
change('tile.addView(Ui.space(this,20));',
       'tile.addView(Ui.space(this,10));',"dashboard title gap")
change('tile.addView(Ui.space(this,8));',
       'tile.addView(Ui.space(this,5));',"dashboard subtitle gap")
change('body.addView(label);body.addView(Ui.space(this,14));',
       'body.addView(label);body.addView(Ui.space(this,9));',"dashboard hero heading")
change('''        int heroHeight=Math.max(Ui.dp(this,220),
            Math.min(Ui.dp(this,345),(int)(screenHeight*.47f)));''',
'''        int heroHeight=Math.max(Ui.dp(this,162),
            Math.min(Ui.dp(this,234),(int)(screenHeight*.34f)));''',"dashboard tile height")
change('body.addView(Ui.space(this,20));\n\n        LinearLayout secondary=Ui.horizontal(this);',
       'body.addView(Ui.space(this,11));\n\n        LinearLayout secondary=Ui.horizontal(this);',"dashboard secondary gap")
change('body.addView(secondary,Ui.lp(this,-1,69));',
       'body.addView(secondary,Ui.lp(this,-1,56));',"dashboard settings shortcut height")

# All browse screens (live, movies, series, radio, favorites): compact category rail and toolbar.
change('categoryBox.setPadding(Ui.dp(this,10),Ui.dp(this,12),Ui.dp(this,9),Ui.dp(this,8));',
       'categoryBox.setPadding(Ui.dp(this,8),Ui.dp(this,9),Ui.dp(this,7),Ui.dp(this,7));',"browse rail padding")
change('categoryBox.addView(Ui.space(this,12));',
       'categoryBox.addView(Ui.space(this,6));',"browse rail title gap")
change('LinearLayout.LayoutParams catParams=Ui.lp(this,220,-1);',
       'LinearLayout.LayoutParams catParams=Ui.lp(this,190,-1);',"browse rail width")
change('catParams.rightMargin=Ui.dp(this,15);',
       'catParams.rightMargin=Ui.dp(this,9);',"browse rail gap")
change('browsing.addView(count);browsing.addView(Ui.space(this,8));',
       'browsing.addView(count);browsing.addView(Ui.space(this,5));',"browse count gap")
change('browsing.addView(categoryManager,Ui.lp(this,-1,48));',
       'browsing.addView(categoryManager,Ui.lp(this,-1,42));',"movie category tools")
change('browsing.addView(Ui.space(this,8));',
       'browsing.addView(Ui.space(this,5));',"movie category tools gap")

# Settings: free up vertical viewport and retain focusable 7-tab rail.
change('''    private void showSettingsV6(){
        LinearLayout layout=Ui.vertical(this);''',
'''    private void showSettingsV6(){
        if(notice!=null)notice.setVisibility(View.GONE);
        LinearLayout layout=Ui.vertical(this);''',"settings hide redundant imported-count banner")
change('''        tabRow.setPadding(Ui.dp(this,6),Ui.dp(this,1),
            Ui.dp(this,6),Ui.dp(this,5));''',
'''        tabRow.setPadding(Ui.dp(this,3),0,
            Ui.dp(this,3),Ui.dp(this,2));''',"settings icon rail padding")
change('''            TextView tab=Ui.text(this,symbols[i],28,''',
'''            TextView tab=Ui.text(this,symbols[i],23,''',"settings icon size")
change('''            LinearLayout.LayoutParams slot=new LinearLayout.LayoutParams(
                0,Ui.dp(this,65),1f);''',
'''            LinearLayout.LayoutParams slot=new LinearLayout.LayoutParams(
                0,Ui.dp(this,49),1f);''',"settings icon height")
change('''            slot.leftMargin=Ui.dp(this,4);
            slot.rightMargin=Ui.dp(this,4);''',
'''            slot.leftMargin=Ui.dp(this,3);
            slot.rightMargin=Ui.dp(this,3);''',"settings icon spacing")
change('layout.addView(tabRow,Ui.lp(this,-1,73));',
       'layout.addView(tabRow,Ui.lp(this,-1,53));',"settings tab band")
change('''        TextView chosenSectionLabel=Ui.text(this,tabNames[selectedSettingsTab],17,Ui.WHITE,true);
        chosenSectionLabel.setPadding(Ui.dp(this,17),Ui.dp(this,5),
            Ui.dp(this,14),Ui.dp(this,1));
        layout.addView(chosenSectionLabel);
        TextView scope=Ui.text(this,settingsScopeV93(selectedSettingsTab),13,Ui.MUTED,false);
        scope.setPadding(Ui.dp(this,17),0,Ui.dp(this,14),Ui.dp(this,11));
        layout.addView(scope);''',
'''        LinearLayout settingsMetaV96=Ui.horizontal(this);
        settingsMetaV96.setGravity(Gravity.CENTER_VERTICAL);
        settingsMetaV96.setPadding(Ui.dp(this,11),0,Ui.dp(this,9),Ui.dp(this,4));
        TextView chosenSectionLabel=Ui.text(this,tabNames[selectedSettingsTab],16,Ui.WHITE,true);
        chosenSectionLabel.setSingleLine(true);
        settingsMetaV96.addView(chosenSectionLabel,Ui.lp(this,-2,-2));
        TextView scope=Ui.text(this,settingsScopeV93(selectedSettingsTab),12,Ui.MUTED,false);
        scope.setSingleLine(true);
        scope.setEllipsize(android.text.TextUtils.TruncateAt.END);
        LinearLayout.LayoutParams scopeV96=new LinearLayout.LayoutParams(0,-2,1);
        scopeV96.leftMargin=Ui.dp(this,18);
        settingsMetaV96.addView(scope,scopeV96);
        layout.addView(settingsMetaV96,Ui.lp(this,-1,35));''',"one-line Settings active tab")
change('body.setPadding(Ui.dp(this,5),Ui.dp(this,4),Ui.dp(this,5),Ui.dp(this,12));',
       'body.setPadding(Ui.dp(this,4),0,Ui.dp(this,4),Ui.dp(this,6));',"settings list padding")
change('''        settingsHelp.setPadding(Ui.dp(this,15),Ui.dp(this,10),Ui.dp(this,15),Ui.dp(this,10));''',
       '        settingsHelp.setPadding(Ui.dp(this,12),Ui.dp(this,5),Ui.dp(this,12),Ui.dp(this,5));',"settings help padding")
change('layout.addView(settingsHelp,Ui.lp(this,-1,50));',
       'layout.addView(settingsHelp,Ui.lp(this,-1,40));',"settings help height")
# Condensed settings rows and headings (still >= 52dp D-pad touch/focus targets).
change('''        body.addView(Ui.space(this,14));
        TextView label=Ui.text(this,heading.toUpperCase(Locale.ROOT),12,Ui.ACCENT,true);''',
'''        body.addView(Ui.space(this,7));
        TextView label=Ui.text(this,heading.toUpperCase(Locale.ROOT),11,Ui.ACCENT,true);''',"settings section heading")
change('label.setLetterSpacing(.13f);',
       'label.setLetterSpacing(.08f);',"settings small heading tracking")
change('''        body.addView(Ui.space(this,11));
    }
    private void addOptionV6''',
'''        body.addView(Ui.space(this,5));
    }
    private void addOptionV6''',"settings small section spacing")
change('card.setPadding(Ui.dp(this,18),0,Ui.dp(this,17),0);',
       'card.setPadding(Ui.dp(this,14),0,Ui.dp(this,12),0);',"settings card padding")
change('LinearLayout.LayoutParams lp=Ui.lp(this,-1,69);lp.bottomMargin=Ui.dp(this,8);',
       'LinearLayout.LayoutParams lp=Ui.lp(this,-1,56);lp.bottomMargin=Ui.dp(this,4);',"settings compact cards")
main.write_text(s)

# Poster listing has large built-in gaps; preserve 4-column TV-grid poster focus.
poster=BASE/"ui/PosterAdapterV6.java"
t=poster.read_text()
for a,b in [
 ('Ui.dp(c,295)','Ui.dp(c,255)'),
 ('lp.setMargins(Ui.dp(c,5),Ui.dp(c,5),Ui.dp(c,5),Ui.dp(c,5));','lp.setMargins(Ui.dp(c,4),Ui.dp(c,4),Ui.dp(c,4),Ui.dp(c,4));'),
 ('root.addView(Ui.space(c,10));','root.addView(Ui.space(c,6));')
]:
    if a not in t:raise AssertionError("Poster layout missing "+a)
    t=t.replace(a,b,1)
poster.write_text(t)


print('PASS: Compact Android TV layout on home, catalog, settings and poster cards')
