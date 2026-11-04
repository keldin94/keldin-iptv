# Keldin IPTV — in-app updates (Android TV)

## What is implemented in v0.7.0

- Settings → Software updates → Check for updates
- Automatic check every 24 hours when app is in use (toggleable)
- Checks the repository's **latest stable** GitHub release, not beta releases
- Shows version and release notes, and requests approval before downloading
- Checks the APK's GitHub SHA-256 digest, size, package name and version before installation
- Uses a private FileProvider and Android's normal package installer
- Android may require **Install unknown apps** permission for Keldin IPTV
- Local playlists, favorites, language and settings stay untouched on a **valid in-place update**

The preview APK intentionally has a separate ID:
\`com.keldin.iptv.updatepreview\`. It **cannot** update the stable package.
The stable package always uses \`com.keldin.iptv\`.

## Critical: configure the long-term signing key ONCE

A public repository must NEVER contain \`.jks\` files, unencrypted private keys, passwords or
base64 copies of signing keys. Create and keep your own release key somewhere private.

From a trusted computer with Java installed:

\`\`\`bash
keytool -genkeypair -v -keystore keldin-release.jks \
  -alias keldin -keyalg RSA -keysize 4096 -validity 12000 -storetype PKCS12
\`\`\`

Keep the private \`keldin-release.jks\` backed up safely. Use unique strong passwords.

To convert the keystore to the text needed for GitHub Actions:

\`\`\`bash
base64 < keldin-release.jks | tr -d '\n' > keldin-keystore-base64.txt
\`\`\`

In GitHub repository **Settings → Secrets and variables → Actions → New repository secret** add:

| Secret | Value |
| --- | --- |
| \`KELDIN_KEYSTORE_BASE64\` | Contents of private \`keldin-keystore-base64.txt\` |
| \`KELDIN_KEYSTORE_PASSWORD\` | The keystore password |
| \`KELDIN_KEY_ALIAS\` | \`keldin\` |
| \`KELDIN_KEY_PASSWORD\` | Key password (sometimes same as store password) |

Do NOT attach this keystore to a GitHub issue, commit, release or public workflow artifact.

## First stable release

1. Go to GitHub **Actions → Build Keldin IPTV v0.7 Update Preview → Run workflow**.
2. Set **publish_stable = true**.
3. The workflow builds a **release** APK using the stored private key and publishes
   non-prerelease \`v0.7.0\`, with asset \`keldin-iptv.apk\`.
4. Install that signed stable APK once. On existing beta builds (different package IDs)
   the M3U list must be reentered **one final time**. Older apps cannot directly read
   another Android app's private storage.
5. All later releases built with the exact same package name + signing key upgrade in-place.

The workflow refuses to overwrite an already published stable release of the same version.

## For all subsequent releases

- Increase Android \`versionCode\` (e.g. 701), \`versionName\` (e.g. 0.7.1)
  and the workflow stable tag (e.g. \`v0.7.1\`) together.
- Never change stable applicationId \`com.keldin.iptv\` or the release signing key.
- Run tests, then workflow with \`publish_stable=true\`.
- The app notices the new signed GitHub release and offers **Download & install**.
- Android asks the user to confirm the install; silent installation is not available
  for an ordinary sideloaded Android TV app.

## Security and operational limits

- Existing old beta builds with unique suffixes and different ephemeral debug signatures
  cannot be upgraded seamlessly into the signed stable APK.
- The update checker does not send M3U URLs, usernames, passwords or viewing history
  to GitHub. It only fetches public release metadata and the selected APK.
- App Store / Google Play distribution will require an alternative update strategy
  subject to their own store policies.
- If the latest stable release API returns 404, no stable signed release exists yet.
- Real Xiaomi Box installation permission and update behavior still need device testing.
