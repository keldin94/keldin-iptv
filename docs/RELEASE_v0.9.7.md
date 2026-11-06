# Keldin IPTV v0.9.7 — TV layout and remote navigation

## Fixed
- Removed the cause of clipped channel, category, EPG, Settings and options text: fixed-height rows now expand to their contents (including larger user-selected fonts).
- Responsive main toolbar and text labels; category list no longer has a separate, unsynchronized channel-logo rail.
- Wider, higher-contrast side panels. Long titles and schedule hints can use two lines; provider channel titles remain unchanged.
- Live cards and movie/series posters expand for long titles and EPG text instead of slicing them.

## Live TV / remote
- OK opens a compact information panel with clearly labeled TV Grid and TV Guide buttons, plus channel list, previous, pause/play, next, favorites and options.
- TV Grid uses a lazy, remote-navigated grid over the playing video: browsing channels does not restart the current stream. The selected channel starts only when confirmed.
- LEFT from the mini-panel boundary opens the channel list. From channels, LEFT opens categories. RIGHT from video opens the existing EPG drawer. BACK dismisses the active overlay first.
- Up/down continues changing live channels when no channel list / grid is open. Inside TV Grid it moves selection, and BACK dismisses the grid without stopping the video.

## Languages
- Default English and existing Bosnian, Slovenian and German authored UI translations are retained.
- All 16 supported locales now have additional translations for 43 Settings and playback control labels, and the TV Grid caption. Core navigation uses the existing 16-language dictionary.
- Some longer supplemental explanations and provider-supplied titles remain in their original language; therefore complete translation coverage of all strings in all 16 locales is not claimed.

## Safety and verification
- Retains the stable Android ID `com.keldin.iptv`, signing certificate, stored playlists, favorites and settings.
- Android TV regression checks, APK compilation and signed release verification passed in CI. Device-specific visual layout and stream jitter still require validation on the target TV Box.
- If playback freezes, record the private playback diagnostics so network, IPTV server and decoder faults can be distinguished. There is not yet a confirmed device-specific stutter cause.
