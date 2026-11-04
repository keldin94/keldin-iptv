from pathlib import Path
main=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java").read_text().splitlines()
def region(a,b):
    ia=next((i for i,l in enumerate(main) if a in l),-1)
    ib=next((i for i,l in enumerate(main) if b in l and i>ia),-1)
    if ia<0:print("MISSING",a);return
    if ib<0:ib=min(ia+145,len(main))
    print(f"\n### {a} from {ia+1} to {ib+1}")
    for j in range(ia,min(ib+1,ia+150,len(main))):print(f"{j+1:04d}: {main[j]}")
for a,b in [
("private void createShell()","private void navigate("),
("private void showHome()","private void landingTile("),
("private void showChannelGrid(boolean guideMode)","private ArrayList<Channel> filterSection("),
("private void showSettingsV6()","private void headingV6("),
("private void showSearch()","private void showLists()"),
("private void openMediaDetails(","private void showGuide()")
]:region(a,b)
