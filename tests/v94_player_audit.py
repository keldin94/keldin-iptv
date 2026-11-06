from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/playback/PlayerActivity.java")
lines=p.read_text().splitlines()
keywords=["private void showOptions(", "private void showTrackChoices(", "private void showExitConfirmation(",
          "@Override public boolean dispatchKeyEvent(", "@Override public boolean onKeyDown(", "private void changeChannel(",
          "private void showControls(", "private void setControls(", "private void scheduleHide(", "private void releaseQuickFocus(", "private void moveQuickFocus("]
for target in keywords:
    found=[i for i,line in enumerate(lines) if target in line]
    for start in found:
        print(f"\n=== METHOD {target} at {start+1} ===")
        lo=max(0,start-3)
        hi=min(len(lines),start+(135 if "showOptions" in target or "dispatchKeyEvent" in target else 55))
        for j in range(lo,hi):
            print(f"{j+1:04d}: {lines[j]}")

# v0.9.5 investigation: public source only, no private playlists or credentials.
for target in [
 "app/src/main/java/com/keldin/iptv/data/Channel.java",
 "app/src/main/java/com/keldin/iptv/ui/ChannelAdapter.java",
 "app/src/main/java/com/keldin/iptv/ui/UiLocaleV9.java",
 "app/src/main/java/com/keldin/iptv/ui/I18n.java"
]:
    source=Path(target)
    if source.exists():
        print("\n=== V95 SOURCE AUDIT: "+source.name+" ===")
        for line_number,code in enumerate(source.read_text().splitlines(),1):
            print(f"{line_number:04d}: {code}")
