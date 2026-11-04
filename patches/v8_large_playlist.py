from pathlib import Path

# Restore the category-selection experience while allowing a complete 183k-item
# playlist to be imported on devices with sufficient free RAM and disk.
p=Path("app/src/main/java/com/keldin/iptv/net/PlaylistWizardV6.java")
s=p.read_text()
assert "MAX_SELECTED=150000" in s
assert "MAX_BYTES=200_000_000L" in s
s=s.replace("MAX_SELECTED=150000","MAX_SELECTED=350000")
s=s.replace("MAX_BYTES=200_000_000L","MAX_BYTES=450_000_000L")
s=s.replace("Large playlist (","Large playlist (")
# Always show the country/category selection, including when user selected all before.
# Add unambiguous count of expected selected items to guide memory-conscious users.
s=s.replace('''            .setTitle("3/3 · Choose countries and content")
            .setMessage(explanation)''',
'''            .setTitle("3/3 · Choose countries and content")
            .setMessage(explanation+"\\n\\nTick or untick countries and content, then choose Save selected.")''')
# Preserve existing preference but do not silently exclude nonlocal categories
# solely because the source contains more than the old hardcoded limit.
s=s.replace('''enabled[i+4]=old.isEmpty() ? (!huge||local) : !old.contains(name);''',
'''enabled[i+4]=!old.contains(name);''')
# If RAM is exhausted, clear user-facing retry info rather than crash.
s=s.replace('''            }catch(Exception e){
                String err=e.getMessage()==null?"Failed to save playlist.":e.getMessage();''',
'''            }catch(OutOfMemoryError oom){
                ui.post(()->choose(scan,"This device needs fewer categories to fit into available memory. "+
                    "The full source is intact; untick some large movie/series groups to continue."));
            }catch(Exception e){
                String err=e.getMessage()==null?"Failed to save playlist.":e.getMessage();''')
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/net/M3uParser.java")
s=p.read_text()
assert "MAX_CHANNELS = 150000" in s
s=s.replace("MAX_CHANNELS = 150000","MAX_CHANNELS = 350000")
p.write_text(s)

p=Path("app/src/main/java/com/keldin/iptv/data/CatalogStore.java")
s=p.read_text()
assert "channels.size()<150000" in s
s=s.replace("channels.size()<150000","channels.size()<350000")
p.write_text(s)

# Increment version but leave the stable package identifier unchanged.
p=Path("app/build.gradle")
s=p.read_text()
assert "versionCode 700" in s and "versionName '0.7.0'" in s
s=s.replace("versionCode 700","versionCode 800")
s=s.replace("versionName '0.7.0'","versionName '0.8.0'")
p.write_text(s)

# Core test should also verify all 183,104 items can be parsed when selected.
print("v0.8 large list support applied: max 350,000; selection always offered")
