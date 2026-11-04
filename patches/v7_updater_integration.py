from pathlib import Path

manifest=Path("app/src/main/AndroidManifest.xml")
m=manifest.read_text()
assert '<uses-permission android:name="android.permission.INTERNET"/>' in m
m=m.replace('<uses-permission android:name="android.permission.INTERNET"/>',
'''<uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>''',1)
anchor='''        <activity android:name=".playback.PlayerActivity"'''
assert anchor in m
m=m.replace(anchor,'''        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="\${applicationId}.updateprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/update_paths"/>
        </provider>
        <activity android:name=".playback.PlayerActivity"''',1)
manifest.write_text(m)

main=Path("app/src/main/java/com/keldin/iptv/ui/MainActivity.java")
s=main.read_text()
anchor='''                    createShell();
                    render();'''
assert anchor in s
s=s.replace(anchor,'''                    createShell();
                    render();
                    // Check no more than once daily; show an update only when a signed
                    // public release is newer. Never install silently.
                    mainHandler.postDelayed(() -> {
                        if(!isFinishing()&&!isDestroyed())
                            com.keldin.iptv.updates.AppUpdateManager.check(this,false);
                    },3000);''',1)
anchor='''        headingV6(body,"Troubleshooting");'''
assert anchor in s
s=s.replace(anchor,'''        headingV6(body,"Software updates");
        addOptionV6(body,"Check for updates",
            "Installed "+com.keldin.iptv.BuildConfig.VERSION_NAME,
            "Checks the latest signed public GitHub release. Verifies APK checksum and "+
            "asks for Android installation confirmation. Playlists remain saved.",
            () -> com.keldin.iptv.updates.AppUpdateManager.check(this,true));
        addOptionV6(body,"Automatic update checks",
            com.keldin.iptv.updates.AppUpdateManager.automaticChecks(this)?"On":"Off",
            "Checks once per day while Keldin IPTV is in use. Downloads or installation "+
            "never happen without your confirmation.",() -> {
                boolean enabled=com.keldin.iptv.updates.AppUpdateManager.automaticChecks(this);
                com.keldin.iptv.updates.AppUpdateManager.setAutomaticChecks(this,!enabled);
                render();
            });

        headingV6(body,"Troubleshooting");''',1)
main.write_text(s)

gradle=Path("app/build.gradle")
g=gradle.read_text()
assert "versionCode 7" in g and "applicationIdSuffix '.eta'" in g
g=g.replace("versionCode 7","versionCode 700",1)
g=g.replace("versionName '0.6.1-import-hotfix'","versionName '0.7.0'",1)
g=g.replace("applicationIdSuffix '.eta'","applicationIdSuffix '.updatepreview'; versionNameSuffix '-preview'",1)
anchor='''    compileOptions {'''
assert anchor in g
g=g.replace(anchor,'''    buildFeatures { buildConfig true }
    compileOptions {''',1)
g+='''
/*
 * Stable app identity: com.keldin.iptv (release).
 * Preview app identity: com.keldin.iptv.updatepreview (debug).
 *
 * NEVER publish a new release with a different key. Set these environment
 * variables only from GitHub Actions encrypted repository secrets.
 */
if (System.getenv("KELDIN_SIGNING_FILE")) {
    android {
        signingConfigs {
            keldinRelease {
                storeFile file(System.getenv("KELDIN_SIGNING_FILE"))
                storePassword System.getenv("KELDIN_SIGNING_STORE_PASSWORD")
                keyAlias System.getenv("KELDIN_SIGNING_ALIAS")
                keyPassword System.getenv("KELDIN_SIGNING_KEY_PASSWORD")
            }
        }
        buildTypes {
            release { signingConfig signingConfigs.keldinRelease }
        }
    }
}
'''
gradle.write_text(g)
print("v0.7.0 updater integrated; stable/preview IDs separated; no signing secrets in source")
