from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/TvSidePanel.java")
s=p.read_text()
def sub(before,after,label):
 global s
 assert before in s, "v0.9.1 logos missing "+label
 s=s.replace(before,after,1)

# Channel drawer: show broadcaster logo beside each channel name, without a second tile.
sub('''            LinearLayout text=Ui.vertical(ctx);
            TextView title=Ui.text(ctx,"",15,WHITE,true);''',
'''            android.widget.ImageView logo=new android.widget.ImageView(ctx);
            logo.setScaleType(android.widget.ImageView.ScaleType.FIT_CENTER);
            logo.setVisibility(View.GONE);
            LinearLayout.LayoutParams logoSize=Ui.lp(ctx,42,42);
            logoSize.rightMargin=Ui.dp(ctx,10);
            row.addView(logo,logoSize);
            LinearLayout text=Ui.vertical(ctx);
            TextView title=Ui.text(ctx,"",15,WHITE,true);''',"channel row logo insertion")
sub('''            return new Holder(row,title,subtitle,arrow);''',
'''            return new Holder(row,title,subtitle,arrow,logo);''',"holder logo")
sub('''            holder.title.setText(r.title);
            holder.subtitle.setText(r.subtitle);''',
'''            holder.title.setText(r.title);
            holder.subtitle.setText(r.subtitle);
            if(mode==CHANNELS && r.channel!=null){
                holder.logo.setVisibility(View.VISIBLE);
                holder.logo.setImageDrawable(null);
                com.keldin.iptv.ui.LogoLoader.load(holder.logo,r.channel.logo,loaded->{});
            }else{
                holder.logo.setImageDrawable(null);
                holder.logo.setVisibility(View.GONE);
            }''',"logo data binding")
sub('''            final TextView title,subtitle,arrow;
            Holder(View item,TextView t,TextView s,TextView a){super(item);title=t;subtitle=s;arrow=a;}''',
'''            final TextView title,subtitle,arrow;
            final android.widget.ImageView logo;
            Holder(View item,TextView t,TextView s,TextView a,android.widget.ImageView image){
                super(item);title=t;subtitle=s;arrow=a;logo=image;
            }''',"holder logo field")

# In category drawer collapse all channel rows to an adjacent, scrollable logo-only rail.
start=s.index('''            LinearLayout logoRail=Ui.vertical(ctx);''')
end=s.index('''            body.addView(split,new LinearLayout.LayoutParams(-1,0,1));''',start)
old=s[start:end]
assert "if(++shown>8)break" in old, "expected first-eight static rail"
replacement='''            ArrayList<Channel> logoOnly=new ArrayList<>();
            for(Channel c:store.channels()){
                if(!"LIVE".equals(c.kind)||!c.sourceId.equals(current.sourceId))continue;
                if(!"Sve kategorije".equals(selectedCategory)&&!selectedCategory.equals(c.group))continue;
                logoOnly.add(c);
                if(logoOnly.size()>=12000)break; // bounded adapter, not 12k image widgets
            }
            RecyclerView logoRail=new RecyclerView(ctx);
            logoRail.setLayoutManager(new LinearLayoutManager(ctx));
            logoRail.setItemAnimator(null);
            logoRail.setHasFixedSize(true);
            logoRail.setOverScrollMode(View.OVER_SCROLL_NEVER);
            logoRail.setAdapter(new LogoOnlyAdapter(logoOnly));
            split.addView(logoRail,Ui.lp(ctx,60,-1));
'''
s=s[:start]+replacement+s[end:]
# Add recyclable and clickable logo-only rail, selected channel bordered.
anchor='''    private static final class RowData {'''
assert anchor in s
code='''    private final class LogoOnlyAdapter
        extends RecyclerView.Adapter<LogoOnlyAdapter.Holder>{
        private final List<Channel> channels;
        LogoOnlyAdapter(List<Channel> channels){this.channels=channels;}
        @Override public Holder onCreateViewHolder(ViewGroup parent,int type){
            FrameLayout outer=new FrameLayout(ctx);
            android.widget.ImageView icon=new android.widget.ImageView(ctx);
            icon.setScaleType(android.widget.ImageView.ScaleType.FIT_CENTER);
            FrameLayout.LayoutParams img=new FrameLayout.LayoutParams(
                Ui.dp(ctx,42),Ui.dp(ctx,42),Gravity.CENTER);
            outer.addView(icon,img);
            RecyclerView.LayoutParams cell=new RecyclerView.LayoutParams(
                Ui.dp(ctx,57),Ui.dp(ctx,53));
            cell.bottomMargin=Ui.dp(ctx,3);
            outer.setLayoutParams(cell);
            return new Holder(outer,icon);
        }
        @Override public void onBindViewHolder(Holder holder,int position){
            Channel ch=channels.get(position);
            holder.icon.setImageDrawable(null);
            com.keldin.iptv.ui.LogoLoader.load(holder.icon,ch.logo,loaded->{});
            boolean active=ch.key().equals(current.key());
            android.graphics.drawable.GradientDrawable bg=
                rounded(active?0x66285475:0x00000000,9);
            if(active)bg.setStroke(Ui.dp(ctx,2),Ui.ACCENT);
            holder.itemView.setBackground(bg);
            holder.itemView.setContentDescription(ch.name);
            holder.itemView.setOnClickListener(v->{
                hide();listener.play(ch);
            });
        }
        @Override public int getItemCount(){return channels.size();}
        final class Holder extends RecyclerView.ViewHolder{
            final android.widget.ImageView icon;
            Holder(View root,android.widget.ImageView icon){super(root);this.icon=icon;}
        }
    }
'''
s=s.replace(anchor,code+anchor,1)
p.write_text(s)
print("v0.9.1: broadcaster logos beside names and focus-friendly scrollable logo-only rail in expanded category panel")
