# Keldin IPTV v0.9.0 — Android TV navigation and settings

## Changes
- D-pad center step between left channel drawer and right TV guide: Left panel → video → EPG (and vice versa).
- The player favorite heart is remotely focusable: when the bottom controls are visible press Down and then OK to toggle favorite.
- Channel/EPG drawers auto-hide after inactivity, adjustable under Settings → Video → Overlay auto-hide (Never, 3, 5, 6, 8, 12, 20 seconds).
- Settings redesigned into horizontal sections: Video, Audio, Network, Playlists, Appearance, Updates, System.
- New preferred audio language choice and adjustable playlist reconnect timeout.
- EPG: attempt same-host XMLTV auto-discovery for recognized Xtream-style M3U paths; user-supplied XMLTV URL takes priority. If the IPTV provider does not support that endpoint, EPG URL still has to be provided by the user.
- Clearer guide-empty states and safer error messages that do not reveal provider URLs or passwords.
- English default, Bosnian and German packs retained and Slovenian added. The original additional languages remain selectable; some secondary texts in them may still fall back to English.
- Signed with the same permanent release key and com.keldin.iptv package as v0.8.x. Use Settings → Updates → Check for updates; existing IPTV playlists/favorites remain stored.

## Validation
Synthetic large M3U imports and EPG URL tests passed. Android debug and release-verification builds passed in GitHub Actions. On-device playback, D-pad focus behavior and provider-specific XMLTV must be verified on the actual Xiaomi TV Box.
