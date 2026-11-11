from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/ui/ThemeV914.java")
s=p.read_text()
def change(a,b,label):
    global s
    if a not in s:raise AssertionError("v917 studio missing "+label)
    s=s.replace(a,b,1)
change("public static final int CLASSIC=0, CINEMA=1, GUIDE=2, GLASS=3, COMPACT=4;",
       "public static final int CLASSIC=0, CINEMA=1, GUIDE=2, GLASS=3, COMPACT=4, STUDIO=5;",
       "stable theme IDs")
change('"KELDIN Glass","KELDIN Compact"\n    };',
       '"KELDIN Glass","KELDIN Compact","KELDIN Studio"\n    };',
       "six-gallery labels")
change('"Dense dashboard with more channels visible at once."\n    };',
       '"Dense dashboard with more channels visible at once.",\n        "Editorial TV hub with featured channels, movies and services."\n    };',
       "theme gallery description")
change('return Math.max(CLASSIC,Math.min(COMPACT,saved));',
       'return Math.max(CLASSIC,Math.min(STUDIO,saved));',
       "new theme persistence")
change('''            case COMPACT:return 184;
            default:return 232;''',
       '''            case COMPACT:return 184;
            case STUDIO:return 235;
            default:return 232;''',"studio navigation rail")
change('''            case COMPACT:return posters?6:5;
            default:return 4;''',
       '''            case COMPACT:return posters?6:5;
            case STUDIO:return posters?5:3;
            default:return 4;''',"studio browse density")
change('''        int bg=theme==GLASS?0x9b25354a:''',
       '''        int bg=theme==STUDIO?0xff111c1b:
            theme==GLASS?0x9b25354a:''',"studio browsing background")
change('''        int round=theme==COMPACT?8:theme==GLASS?24:16;''',
       '''        int round=theme==STUDIO?13:
            theme==COMPACT?8:theme==GLASS?24:16;''',"studio rail corners")
change('''        if(theme==GLASS)shape.setStroke(Ui.dp(ctx,1),0x886abadd);''',
       '''        if(theme==GLASS)shape.setStroke(Ui.dp(ctx,1),0x886abadd);
        if(theme==STUDIO)shape.setStroke(Ui.dp(ctx,1),0xff325947);''',"studio rail outline")
change('''        int base=theme==GLASS?0xa62b405b:''',
       '''        int base=theme==STUDIO?0xff1a2925:
            theme==GLASS?0xa62b405b:''',"studio selection card")
change('''        if(emphasis==1)base=theme==CINEMA?0xff343448:''',
       '''        if(emphasis==1)base=theme==STUDIO?0xff31563d:
            theme==CINEMA?0xff343448:''',"studio featured card")
change('''        GradientDrawable bg=Ui.shape(focused?0xff355877:base,
            theme==GLASS?25:theme==COMPACT?10:18,a);''',
       '''        GradientDrawable bg=Ui.shape(
            focused&&theme==STUDIO?0xff385b4e:focused?0xff355877:base,
            theme==STUDIO?14:theme==GLASS?25:theme==COMPACT?10:18,a);''',"studio focused card")
change('''            focused?Ui.ACCENT:theme==GLASS?0x8877c6e7:0x77576b87);''',
       '''            focused&&theme==STUDIO?0xffb7f5cd:
            focused?Ui.ACCENT:theme==STUDIO?0x8879a68a:
            theme==GLASS?0x8877c6e7:0x77576b87);''',"studio highlighted border")
change('''        }else{
            caption(a,body,"KELDIN COMPACT   •   "+tr(a,"choose"),17);''',
       '''        }else if(theme==STUDIO){
            StudioHomeV917.populate(a,body,nav);
        }else{
            caption(a,body,"KELDIN COMPACT   •   "+tr(a,"choose"),17);''',"Studio original editorial home layout")
change('''            theme==COMPACT?(int)(sw*.70f):(int)(sw*.85f);''',
       '''            theme==COMPACT?(int)(sw*.70f):
            theme==STUDIO?(int)(sw*.83f):(int)(sw*.85f);''',"studio playback overlay width")
change('''            theme==COMPACT?0xf2101824:0xf20d1b2b,''',
       '''            theme==COMPACT?0xf2101824:
            theme==STUDIO?0xf1142724:0xf20d1b2b,''',"studio playback surface")
change('''            theme==COMPACT?12:theme==GLASS?25:18,a);''',
       '''            theme==COMPACT?12:theme==STUDIO?16:theme==GLASS?25:18,a);''',"studio playback corners")
change('''            theme==GLASS?0x99a5daf3:0x886385a1);''',
       '''            theme==GLASS?0x99a5daf3:
            theme==STUDIO?0xff588d70:0x886385a1);''',"studio playback border")
change('''            theme==GLASS?new int[][]{{2,1},{1,1,1}}:
            new int[][]{{1,1,1},{1,1,1}};''',
       '''            theme==GLASS?new int[][]{{2,1},{1,1,1}}:
            theme==STUDIO?new int[][]{{3,1},{1,1,1,1}}:
            new int[][]{{1,1,1},{1,1,1}};''',"studio theme gallery miniature")
change('''theme==GUIDE?0xff315b69:0xff365069,5,a));''',
       '''theme==GUIDE?0xff315b69:
                    theme==STUDIO?0xff478764:0xff365069,5,a));''',"studio theme gallery palette")
change('''    /** D-pad-friendly theme gallery with five miniature layout previews. */''',
       '''    /** D-pad-friendly theme gallery with six miniature layout previews. */''',"gallery docs")
p.write_text(s)
p=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=p.read_text()
old='''                "Five distinct layouts: KELDIN Classic, Cinema, TV Guide, Glass and Compact. "+'''
new='''                "Six layouts: KELDIN Classic, Cinema, TV Guide, Glass, Compact and Studio. "+'''
if old not in s:raise AssertionError("Theme Gallery setting description changed")
p.write_text(s.replace(old,new,1))
print("PASS KELDIN Studio: six selectable layouts and original OTT style without changing channel engine")
