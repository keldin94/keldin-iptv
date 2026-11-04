# Keldin IPTV v0.8.0 — first signed Android TV release

This is the first stable release using the owner's permanent signing certificate.

Changes:
- In-app update checker from public signed GitHub releases
- Manual "Check for updates" in Settings and daily background checks while app is open
- In-app APK download with SHA-256 verification and Android installation approval
- Import selection of countries/categories for large IPTV playlists
- Full 183,104-item test playlist import without the former 150,000-entry rejection
- English-first navigation with optional Bosnian and other languages

Important: The first stable installation has a new Android package identity relative to old beta APKs. Imported M3U playlists have to be entered once; future stable updates with the same signing certificate retain local app data.

Caution: Validation covers Android CI and synthetic large M3U import, not device-level playback or memory on the user's Xiaomi Box. Keep previous beta installed during initial validation.
