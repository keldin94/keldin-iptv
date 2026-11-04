# Keldin IPTV v0.9.2 — Live TV remote controls and logos

Android TV release signed with the existing long-term Keldin signing certificate.

- Compact framed live overlay inherited from v0.9.1, preserving channel name, current and next program, playback state and quality.
- Focusable on-screen icons: previous channel, play/pause, next channel, favorite heart and additional options.
- Press OK while watching to focus the controls; Left/Right selects an icon; OK activates it.
- Up/Down reliably changes channels within the current live TV category even when controls are focused. Fixes the v0.9 bug where Down instead forced focus onto the favorite heart.
- Left channel drawer displays broadcaster logos next to channel names.
- A second Left expands categories while the channel rail collapses into an independently scrollable, logo-only list.
- Retains v0.9.1's larger live buffer, delayed auto-reconnect and local-only playback diagnostics. Actual cause of periodic jumps needs device diagnostics, not GitHub Actions logs.
- Explicit signed-release certificate check against v0.9.1 to prevent publishing an update under a different signing certificate.
- Same Android application ID, no change to local playlists, favorites, account entries, audio/video settings, language, filters, or other preferences.

Validation: Android CI smoke/unit tests, full 183104-item M3U import test and Android debug/release build passed. Hardware D-pad focus, stream interruptions and specific provider behavior require Xiaomi Box testing.
