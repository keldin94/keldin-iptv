# Keldin IPTV v0.9.1 — Compact player overlay and smoother live playback

## Improvements
- Live player information is now a compact, rounded, lightly bordered bottom overlay rather than a large full-width shade. Retains channel title, guide/current and next program, player status, format and the remotely focusable favorite heart.
- Reduced font sizes and vertical spacing, with adequate room for long channel names.
- Investigated a real app-side source of recurring live skips: a hard-coded 22-second buffering watchdog could forcibly reconnect a live stream and jump to the newer live position.
- Increased the default stall-recovery interval to 60 seconds. Users can select 30 / 45 / 60 / 90 / 120 seconds or Never in **Settings → Video → Buffer stall recovery**.
- Enlarged the live stream jitter buffer while leaving VOD buffer rules unchanged.
- Added local-only playback diagnostics: buffering events, buffered durations, stream reconnect attempts, timestamped playback discontinuities, and dropped video frames from the decoder. See **Settings → System → Playback diagnostics** or the player's Error details option. The diagnostic recorder excludes playlist URLs and credentials.
- **All existing IPTV playlists, favorites and settings remain stored on a normal update**, because the Android package remains `com.keldin.iptv` and the APK is signed using the same permanent signing key. Do not uninstall or clear Android app data.
- Preserves v0.9.0's neutral central navigation step, EPG improvements, country filtering, and horizontal settings tabs.

## Test scope
Automated source regression, large M3U import, debug APK and signed-release verification succeeded. These tests cannot prove whether a particular IPTV provider or Wi-Fi network causes stream stuttering; after updating, watch a channel and review the in-app playback diagnostics to distinguish decoder frame drops from buffering/reconnection.
