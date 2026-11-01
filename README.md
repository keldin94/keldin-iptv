# Keldin IPTV — Android TV

Privatni razvojni projekt za Xiaomi TV Box / Android TV.

**Full Preview**: M3U, Xtream Codes, EPG (XMLTV), favorites, video playback using Media3/ExoPlayer.

**Important:** This is a development preview, not a certified stable release. Playback depends on the IPTV provider and the device. No TV channels or credentials are included in the source.

## Build

The GitHub Actions workflow under `.github/workflows/build-apk.yml` assembles the debug APK. Download the `Keldin-IPTV-Full-Preview-APK` artifact from a successful workflow run.

During the first import, application source is included as compressed, base64-encoded archive chunks under `source-parts/`. The workflow reassembles it for the build. A future commit can extract the code into readable repository files.

Use only playlists that you are permitted to access.
