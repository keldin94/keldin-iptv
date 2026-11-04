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
