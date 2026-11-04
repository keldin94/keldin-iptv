from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
s=p.read_text()
anchor='''        return super.dispatchKeyEvent(event);
    }

    @Override public boolean onKeyDown'''
assert anchor in s
s=s.replace(anchor,'''        if(event.getAction()==KeyEvent.ACTION_UP && quickActionIndex>=0 &&
            (event.getKeyCode()==KeyEvent.KEYCODE_DPAD_CENTER||
             event.getKeyCode()==KeyEvent.KEYCODE_ENTER))
            return true; // avoid a second automatic Android click after onKeyDown
        return super.dispatchKeyEvent(event);
    }

    @Override public boolean onKeyDown''',1)
p.write_text(s)
print("v0.9.2: prevent double-activating media buttons from remote key-up")
