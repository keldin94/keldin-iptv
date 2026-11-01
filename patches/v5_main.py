from pathlib import Path

path=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=path.read_text()
def rep(old,new,title):
    global s
    if old not in s: raise RuntimeError("v0.5 missing "+title+" "+old[:75])
    s=s.replace(old,new,1)

rep('''        store = CatalogStore.shared(this);''',
'''        CrashReporter.install(this);
        store = CatalogStore.shared(this);''',"crash log install")
rep('''    @Override protected void onResume() { super.onResume(); if(store!=null && content!=null)render(); }''',
'''    @Override protected void onResume() {
        super.onResume();
        // Avoid rebuilding large 60k-row browse pages every time a video closes.
        if(store!=null && content!=null && ("Početna".equals(page)||"Favoriti".equals(page)))render();
    }''',"resume performance")
start=s.index("    @Override public void onBackPressed(){")
end=s.index("    private void createShell() {",start)
s=s[:start]+'''    @Override public void onBackPressed(){
        if(!"Početna".equals(page)){navigate("Početna");return;}
        new AlertDialog.Builder(this)
            .setTitle("Izaći iz Keldin IPTV?")
            .setMessage("Želiš li zatvoriti aplikaciju?")
            .setPositiveButton("Izađi",(dialog,which)->finish())
            .setNegativeButton("Nastavi",null).show();
    }

'''+s[end:]
# Unify theme styling, no purple shades and no colorful mixed buttons.
s=s.replace('0xff101726','0xff0c1a2b').replace('0xff292342','0xff14334b')
s=s.replace('0xff2f2b50','0xff195676').replace('0xff2a3652','0xff244a60')
s=s.replace('0xffc5c9e3','0xffb8cedb')
# Make top-level menu a full-screen dashboard instead of persistent library sidebar.
rep('''        for(int i=0;i<navItems.size();i++)applyNavStyle(navItems.get(i),PAGES[i],navItems.get(i).hasFocus());
        title.setText(page);
        subtitle.setText(store.channels().size()+" sadržaja  •  "+store.sources().size()+" lista  •  Keldin IPTV Full");''',
'''        nav.setVisibility(View.GONE);
        for(int i=0;i<navItems.size();i++)applyNavStyle(navItems.get(i),PAGES[i],navItems.get(i).hasFocus());
        title.setText("Početna".equals(page)?"KELDIN IPTV":page);
        subtitle.setText("Početna".equals(page)?
            "TV uživo, filmovi i serije na jednom mjestu":
            "Keldin IPTV   •   "+store.sources().size()+" aktivnih lista");''',"main header/landing")
rep('''        TextView add=Ui.button(this,"+  Lista",()->editSource(null,"M3U"),false);
        LinearLayout.LayoutParams addLp=Ui.lp(this,-2,42);addLp.leftMargin=Ui.dp(this,10);
        toolbar.addView(add,addLp);''',
'''        TextView home=Ui.button(this,"⌂  Početna",()->navigate("Početna"),false);
        LinearLayout.LayoutParams hp=Ui.lp(this,-2,42);hp.leftMargin=Ui.dp(this,9);
        toolbar.addView(home,hp);
        TextView search=Ui.button(this,"⌕  Pretraga",()->navigate("Pretraga"),false);
        LinearLayout.LayoutParams sp=Ui.lp(this,-2,42);sp.leftMargin=Ui.dp(this,9);
        toolbar.addView(search,sp);
        TextView add=Ui.button(this,"☷  Liste",()->navigate("Moje liste"),false);
        LinearLayout.LayoutParams addLp=Ui.lp(this,-2,42);addLp.leftMargin=Ui.dp(this,9);
        toolbar.addView(add,addLp);''',"toolbar links")
# Replace the entire old dashboard and statistic widgets with restrained section chooser.
start=s.index("    private void showHome() {")
end=s.index("    private void addStat(",start)
s=s[:start]+'''    private void showHome() {
        ScrollView scroll=new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setVerticalScrollBarEnabled(false);
        LinearLayout body=Ui.vertical(this);
        body.setPadding(Ui.dp(this,6),Ui.dp(this,8),Ui.dp(this,6),Ui.dp(this,12));
        scroll.addView(body);

        TextView eyebrow=Ui.text(this,"ODABERI SEKCIJU",12,Ui.ACCENT,true);
        eyebrow.setLetterSpacing(.14f);
        body.addView(eyebrow);
        body.addView(Ui.space(this,13));

        LinearLayout first=Ui.horizontal(this);
        landingTile(first,"◉","TV uživo","Kanali, kategorije i EPG","Uživo");
        landingTile(first,"▷","Filmovi","Žanrovi, pretraga i nastavak","Filmovi");
        body.addView(first,Ui.lp(this,-1,165));
        body.addView(Ui.space(this,13));

        LinearLayout second=Ui.horizontal(this);
        landingTile(second,"▤","Serije","Sezone, epizode i historija","Serije");
        landingTile(second,"⚙","Postavke","Liste, player i podešavanja","Postavke");
        body.addView(second,Ui.lp(this,-1,165));
        body.addView(Ui.space(this,25));

        List<Channel> recent=store.recentChannels();
        if(!recent.isEmpty()){
            body.addView(Ui.text(this,"Nastavi gledati",18,Ui.WHITE,true));
            body.addView(Ui.space(this,12));
            addHorizontalCards(body,recent,7);
        }
        content.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));
    }

    private void landingTile(LinearLayout row,String symbol,String label,String description,String target){
        LinearLayout card=Ui.vertical(this);
        card.setPadding(Ui.dp(this,23),Ui.dp(this,18),Ui.dp(this,16),Ui.dp(this,14));
        card.setBackground(Ui.shape(Ui.PANEL,17,this));
        card.setFocusable(true);
        card.setClickable(true);

        TextView icon=Ui.text(this,symbol,27,Ui.ACCENT,true);
        TextView name=Ui.text(this,label,23,Ui.WHITE,true);
        TextView detail=Ui.text(this,description,12,Ui.MUTED,false);
        card.addView(icon);
        card.addView(Ui.space(this,8));
        card.addView(name);
        card.addView(Ui.space(this,3));
        card.addView(detail);
        card.setOnClickListener(v->navigate(target));
        Ui.focus(card,Ui.PANEL);
        LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,-1,1);
        lp.rightMargin=Ui.dp(this,12);
        row.addView(card,lp);
    }
'''+s[end:]
# Clean landing "recent" thumbnails: no BH initials.
start=s.index("    private void addHorizontalCards(")
end=s.index("    private String shortName(",start)
s=s[:start]+'''    private void addHorizontalCards(LinearLayout parent,List<Channel> list,int limit) {
        if(list.isEmpty())return;
        HorizontalScrollView scroll=new HorizontalScrollView(this);
        scroll.setHorizontalScrollBarEnabled(false);
        LinearLayout row=Ui.horizontal(this);
        for(int i=0;i<Math.min(limit,list.size());i++){
            Channel ch=list.get(i);
            LinearLayout card=Ui.vertical(this);
            card.setFocusable(true);card.setClickable(true);
            card.setPadding(Ui.dp(this,14),Ui.dp(this,12),Ui.dp(this,12),Ui.dp(this,10));
            card.setBackground(Ui.shape(Ui.PANEL,14,this));
            TextView symbol=Ui.text(this,"▶",19,Ui.ACCENT,true);
            TextView name=Ui.text(this,ch.name,16,Ui.WHITE,true);
            name.setSingleLine(true);
            name.setEllipsize(android.text.TextUtils.TruncateAt.END);
            TextView group=Ui.text(this,ch.group,11,Ui.MUTED,false);
            group.setSingleLine(true);
            group.setEllipsize(android.text.TextUtils.TruncateAt.END);
            card.addView(symbol);
            card.addView(Ui.space(this,8));
            card.addView(name);
            card.addView(Ui.space(this,4));
            card.addView(group);
            card.setOnClickListener(v->play(ch));
            Ui.focus(card,Ui.PANEL);
            LinearLayout.LayoutParams lp=Ui.lp(this,198,116);
            lp.rightMargin=Ui.dp(this,11);
            row.addView(card,lp);
        }
        scroll.addView(row);
        parent.addView(scroll);
    }
'''+s[end:]
start=s.index("    private void showChannelGrid(boolean guideMode) {")
end=s.index("    private void showGuide() {",start)
s=s[:start]+'''    private void showChannelGrid(boolean guideMode) {
        // Filter only once per section. RecyclerViews virtualize thousands of rows.
        List<Channel> source="Favoriti".equals(page)?store.favorites():store.channels();
        String kind=page.equals("Filmovi")?"MOVIES":page.equals("Serije")?"SERIES":
            page.equals("Uživo")?"LIVE":"";
        ArrayList<Channel> section=new ArrayList<>();
        LinkedHashSet<String> groupSet=new LinkedHashSet<>();
        groupSet.add("Sve kategorije");
        for(Channel ch:source){
            if(!kind.isEmpty()&&!kind.equals(ch.kind))continue;
            section.add(ch);
            groupSet.add(ch.group==null||ch.group.isEmpty()?"Ostalo":ch.group);
        }
        if(!groupSet.contains(selectedGroup))selectedGroup="Sve kategorije";
        LinearLayout main=Ui.horizontal(this);
        main.setGravity(Gravity.TOP);
        LinearLayout categoryBox=Ui.vertical(this);
        categoryBox.setPadding(Ui.dp(this,11),Ui.dp(this,12),Ui.dp(this,9),Ui.dp(this,8));
        categoryBox.setBackground(Ui.shape(Ui.PANEL,14,this));

        TextView categoryLabel=Ui.text(this,"KATEGORIJE",11,Ui.ACCENT,true);
        categoryLabel.setLetterSpacing(.14f);
        categoryBox.addView(categoryLabel);
        categoryBox.addView(Ui.space(this,11));
        RecyclerView categories=new RecyclerView(this);
        categories.setLayoutManager(new androidx.recyclerview.widget.LinearLayoutManager(this));
        categories.setItemAnimator(null);
        categories.setHasFixedSize(true);
        categoryBox.addView(categories,new LinearLayout.LayoutParams(-1,0,1));
        LinearLayout.LayoutParams clp=Ui.lp(this,225,-1);
        clp.rightMargin=Ui.dp(this,16);
        main.addView(categoryBox,clp);

        LinearLayout browsing=Ui.vertical(this);
        TextView count=Ui.text(this,"",13,Ui.MUTED,false);
        browsing.addView(count);
        browsing.addView(Ui.space(this,9));
        RecyclerView grid=new RecyclerView(this);
        grid.setLayoutManager(new GridLayoutManager(this,4));
        grid.setHasFixedSize(true);
        grid.setItemAnimator(null);
        grid.setClipToPadding(false);

        ArrayList<Channel> visible=new ArrayList<>();
        for(Channel ch:section){
            String group=ch.group==null||ch.group.isEmpty()?"Ostalo":ch.group;
            if("Sve kategorije".equals(selectedGroup)||selectedGroup.equals(group))visible.add(ch);
        }
        ChannelAdapter adapter=new ChannelAdapter(store,visible,this::play,guideMode);
        grid.setAdapter(adapter);
        count.setText(visible.size()+" sadržaja  •  OK za otvaranje");
        browsing.addView(grid,new LinearLayout.LayoutParams(-1,0,1));
        main.addView(browsing,new LinearLayout.LayoutParams(0,-1,1));
        CategoryAdapter groupAdapter=new CategoryAdapter(this,new ArrayList<>(groupSet),selectedGroup,group->{
            selectedGroup=group;
            ArrayList<Channel> filtered=new ArrayList<>();
            for(Channel ch:section){
                String g=ch.group==null||ch.group.isEmpty()?"Ostalo":ch.group;
                if("Sve kategorije".equals(group)||group.equals(g))filtered.add(ch);
            }
            adapter.setItems(filtered);
            count.setText(filtered.size()+" sadržaja  •  "+group);
            grid.scrollToPosition(0);
        });
        categories.setAdapter(groupAdapter);
        content.addView(main,new LinearLayout.LayoutParams(-1,0,1));
    }
'''+s[end:]
# Optional crash summary in settings for users; no credentials or URLs in reports.
needle='''        body.addView(Ui.space(this,26));
        body.addView(Ui.text(this,"PRISTUP I NAPLATA",12,Ui.ACCENT,true));'''
rep(needle,'''        body.addView(Ui.space(this,20));
        addSetting(body,"Dijagnostika zatvaranja",CrashReporter.summary(this),()->{
            new AlertDialog.Builder(this).setTitle("Dijagnostika")
                .setMessage(CrashReporter.details(this))
                .setPositiveButton("U redu",null).show();
        });
        body.addView(Ui.space(this,26));
        body.addView(Ui.text(this,"PRISTUP I NAPLATA",12,Ui.ACCENT,true));''',"crash diagnostics settings")
# UI labels consistent case
s=s.replace('"KELDIN IPTV   •   FULL"','"KELDIN IPTV   •   FULL"')
path.write_text(s)
p=Path("app/build.gradle")
g=p.read_text()
assert "versionCode 4" in g and "applicationIdSuffix '.delta'" in g
g=g.replace("versionCode 4","versionCode 5")
g=g.replace("versionName '0.4.0-tv-remote-panels'","versionName '0.5.0-navigation'")
g=g.replace("applicationIdSuffix '.delta'","applicationIdSuffix '.epsilon'")
p.write_text(g)
print("Keldin IPTV v0.5 home/section/category layout ready")
