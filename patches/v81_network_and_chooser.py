from pathlib import Path

p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java")
s=p.read_text()
old='PlaylistSync.open(source.playlistUrl(),source.userAgent,MAX_BYTES)'
assert old in s, "playlist download call not found"
s=s.replace(old,'PlaylistImportHttpV81.open(source.playlistUrl(),source.userAgent,MAX_BYTES)',1)

# Android AlertDialog cannot reliably display a message and a multichoice list
# together on TV. Use a real, remotely navigable checkbox ScrollView.
start=s.index('        new AlertDialog.Builder(activity)\n            .setTitle("3/3 · Choose countries and content")')
end=s.index('    }\n    private void save(',start)
fragment=s[start:end]
assert '.setMultiChoiceItems(labels,enabled,' in fragment
# Keep the original button logic; only replace setMessage/setMultiChoiceItems
fragment=fragment.replace('''        new AlertDialog.Builder(activity)
            .setTitle("3/3 · Choose countries and content")
            .setMessage(explanation)
            .setMultiChoiceItems(labels,enabled,(dialog,index,checked)->enabled[index]=checked)
''','''        LinearLayout selector=Ui.vertical(activity);
        int pad=Ui.dp(activity,14);
        selector.setPadding(pad,pad,pad,Ui.dp(activity,8));
        TextView guidance=Ui.text(activity,explanation,14,Ui.MUTED,false);
        selector.addView(guidance);
        selector.addView(Ui.space(activity,8));

        android.widget.ScrollView scroller=new android.widget.ScrollView(activity);
        scroller.setFillViewport(false);
        scroller.setVerticalScrollBarEnabled(true);
        LinearLayout checks=Ui.vertical(activity);
        for(int i=0;i<labels.length;i++){
            final int index=i;
            android.widget.CheckBox checkbox=new android.widget.CheckBox(activity);
            checkbox.setText(labels[i]);
            checkbox.setTextColor(Ui.WHITE);
            checkbox.setTextSize(16f);
            checkbox.setMinHeight(Ui.dp(activity,48));
            checkbox.setPadding(Ui.dp(activity,6),Ui.dp(activity,6),
                Ui.dp(activity,6),Ui.dp(activity,6));
            checkbox.setFocusable(true);
            checkbox.setChecked(enabled[i]);
            checkbox.setOnCheckedChangeListener((button,checked)->enabled[index]=checked);
            checks.addView(checkbox,new LinearLayout.LayoutParams(-1,-2));
        }
        scroller.addView(checks);
        selector.addView(scroller,new LinearLayout.LayoutParams(-1,Ui.dp(activity,360)));
        AlertDialog choiceDialog=new AlertDialog.Builder(activity)
            .setTitle("3/3 · Choose countries and content")
            .setView(selector)
''',1)
fragment=fragment.replace('''            .setCancelable(false).show();''','''            .setCancelable(false).create();
        choiceDialog.show();
        if(checks.getChildCount()>0)checks.getChildAt(0).requestFocus();''',1)
assert '.setMultiChoiceItems' not in fragment
s=s[:start]+fragment+s[end:]
p.write_text(s)

p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 800" in s and "versionName '0.8.0'" in s
s=s.replace("versionCode 800","versionCode 801")
s=s.replace("versionName '0.8.0'","versionName '0.8.1'")
p.write_text(s)
print("v0.8.1: Playlist downloader retry and remote-friendly category picker patched")
