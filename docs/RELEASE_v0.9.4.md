# Keldin IPTV v0.9.4 — Remote control stability and playback options

Stable Android TV maintenance update.

- **Back button:** A single Back press closes the bottom mini-player overlay, even when a playback icon is focused. Side panels also close correctly; pressing Back with all overlays hidden returns to the main app.
- **Channel zapping:** Up and Down change live TV channels within the current category while the compact player is open, regardless of which playback icon is focused. Channel Up/Down keys are also supported.
- One action per physical remote press, preventing unintended repeats and focus changes on key release.
- Group channel lists are cached during playback so large IPTV catalogs do not require a full list scan for every channel switch.
- Safe local diagnostics record remote key actions and active category sizes, not channel names, stream URLs or passwords.
- **Options icon (⋯):** replaces the system default text-list dialog with a modern dark rounded TV panel: icons, grouped Stream / Playback / Channel actions, short explanations, visible D-pad focus, scrolling and standard Back dismissal.
- Retains all twelve pre-existing playback commands and restarts the mini-overlay auto-hide countdown after dismissing the options menu.
- Preserves v0.9.3 home design, settings categories, playlist country filters, blocked content, favorites and all existing app preferences.

**Install:** Settings → Updates → Check for updates → Download & install. This is a signed in-place update using the unchanged `com.keldin.iptv` Android package and the same permanent Keldin key as v0.9.3. Do not uninstall the existing application.

**Verification:** Automatic source regression tests and full Android debug and release-verification build passed. The production publishing workflow additionally checks the actual APK signature fingerprint against v0.9.3. D-pad hardware behavior on the user's Xiaomi TV Box is not verified by CI and should be checked after installation.
