# Keldin IPTV v0.9.3 — Home, settings, filtering and TV navigation

## Updated Android TV interface
- New unclipped home layout: four large Live TV, Movies, Series and Radio choices, with a distinct Settings section below. Continue Watching removed from home.
- Official Keldin IPTV vector icon beside application title.
- Unnecessary Playlists button removed from the global top toolbar. Playlist management remains under Settings → Playlists.
- Settings have seven icon-only tabs: Video, Audio, Network, Playlists, Appearance, Updates and System, with the selected section's title and explanation beneath the icons. Remote Left/Right and OK can select tabs; Down enters the settings controls. Tab selection is saved locally.

## Media categories and protection
- Movie and series category rail receives focus when opening and works with Left/Right D-pad navigation, without changing grid column count during focus events.
- Select visible Movie and Series categories individually. Hiding a group does not delete the original M3U content; restore it at any time.
- Hide individual movies or entire series; restore hidden media in Settings → Playlists.
- Filter explicit categories AND program/media titles by default in Live TV, Movies, Series and global search, independent of whether a PIN has been configured.
- Film and series lists show later M3U entries first. M3U generally contains no trustworthy "date added" timestamp, so actual chronological order cannot be guaranteed.
- Supports English-first UI with Bosnian, Slovenian, German and other available languages. Some secondary text in additional locales may fall back to English.

## Update and verification
- Same `com.keldin.iptv` Android package and persistent signing key, verified against stable v0.9.2 before publication.
- No data-clearing or uninstall steps. Existing IPTV sources, favorites, selected countries, player settings, appearance preferences, language, hidden items and category selections remain in the app's private storage.
- Synthetic tests include full 183,104-item M3U import, content-filter tests, D-pad/UI source guards, Android debug and release APK signing. Final Xiaomi Box hardware verification remains required.

To update: Settings → Updates → Check for updates. Confirm Android installation when prompted. Do not uninstall the prior version.
