# wealth-split

Wealth Split — a percentage-based income-splitting budget tracker. Lives at GitHub Pages as an installable PWA.

## Mobile app (Android)

The web app is wrapped with [Capacitor](https://capacitorjs.com) so it can run as a native Android app you can install directly on your phone, before ever publishing anywhere. iOS is not set up yet since building it requires a Mac with Xcode — run `npx cap add ios` there when you're ready.

**One-time setup on your own computer** (this sandbox has no Android SDK, so the actual build has to happen on your machine):
1. Install [Android Studio](https://developer.android.com/studio) — it bundles the Android SDK.
2. Clone this repo and run `npm install`.

**Build and install on your phone:**
1. If you changed `index.html`/`manifest.json`/`sw.js`/`icons/`, run `npm run sync` to copy the latest web files into the native project.
2. Run `npm run open:android` — this opens the project in Android Studio.
3. Plug your phone in via USB with Developer Options + USB Debugging enabled (or use an emulator), then click the Run ▶ button in Android Studio. It builds a debug APK and installs it straight onto your device — no Play Store, no account, no cost.
4. Use the app for a while and make sure everything feels right before doing anything else.

**When you're ready to actually publish it** (Play Store):
1. Get a Google Play Developer account ($25 one-time).
2. In Android Studio, Build → Generate Signed Bundle/APK, create a signing key (keep it safe — you need the same one for every future update), and build a release AAB.
3. Create the app listing in the Play Console and upload the AAB.

The app ID is currently set to `com.wealthsplit.app` in `capacitor.config.json` and `android/app/build.gradle` — change it before publishing if you want something different (it can't be changed after your first Play Store release).
