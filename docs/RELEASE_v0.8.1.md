# Keldin IPTV 0.8.1 — IPTV playlist connection improvements

Stable maintenance release, signed with the same permanent Keldin certificate as 0.8.0.

- Retains the existing playlist fetcher for servers where it already works.
- On transport/connection timeouts, retries with longer timeouts, an independent HTTP client, redirects and an alternate user agent.
- Shows a clear, safe error if all connection attempts still time out.
- Fixes the Android TV country/category selection dialog: scrollable, focusable checkboxes controlled by the remote, including on large playlists.
- Keeps 350,000 selected-item safeguard from v0.8.0 (not an unlimited catalog database).
- Includes regression tests for network timeouts, HTTP redirection, HTTP errors, country selection and the 183,104-item playlist import.

All tests are synthetic. IPTV server connectivity and device memory use must be verified on the actual Xiaomi TV Box.

To update from signed 0.8.0: Settings > Software updates > Check for updates. Android will request installation approval. Local playlists/settings are preserved by matching package ID and signing certificate.
