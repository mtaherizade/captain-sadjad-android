# Captain Sadjad — Android APK

بستهٔ اندروید بازی **PlayCanvas** «Captain Sadjad».

بازی‌های PlayCanvas در واقع یک «صفحهٔ وب» هستند؛ این پروژه همان خروجی وب بازی را داخل یک
**WebView تمام‌صفحه** بسته‌بندی می‌کند و آن را به یک فایل `.apk` قابل‌نصب تبدیل می‌کند.

---

## ۱. نصب APK روی گوشی

1. فایل `app-release.apk` (یا اگر نبود، `app-debug.apk`) را روی گوشی کپی کن.
2. اگر اندروید اجازه نداد: **تنظیمات → امنیت → نصب برنامه‌های ناشناس** را برای فایل‌منیجر یا مرورگرت فعال کن.
3. روی فایل APK بزن و **Install** را تأیید کن.
4. آیکن «Captain Sadjad» در لیست برنامه‌ها ظاهر می‌شود.

> `app-release.apk` نسخهٔ نهایی و امضاشده است (برای Google Play هم مناسب است).
> `app-debug.apk` نسخهٔ آزمایشی است؛ کنار نسخهٔ release نصب می‌شود و برای تست خوب است.

---

## ۲. ساختار پروژه

```
.
├── .github/workflows/build-apk.yml   ← ساخت خودکار APK در فضای ابری GitHub
├── app/
│   ├── build.gradle                  ← تنظیمات ماژول اندروید
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/captainsadjad/game/MainActivity.java   ← WebView تمام‌صفحه
│       ├── res/                      ← آیکن، نام برنامه، تم
│       └── assets/www/               ← ★ فایل‌های بازی اینجا می‌روند (index.html + assets)
├── build.gradle / settings.gradle / gradle.properties
├── gradlew / gradlew.bat / gradle/wrapper/
└── tools/make_icon.py                ← ساخت مجدد آیکن برنامه
```

---

## ۳. چرا WebView و نه فایل مستقیم؟

خروجی PlayCanvas را **نمی‌توان** با `file://` اجرا کرد، چون موتور بازی فایل‌های
`config.json`، صحنه‌ها و همهٔ asset ها را با `fetch()`/`XHR` می‌خواند و Chromium
دسترسی `fetch` روی `file://` را مسدود می‌کند.

این پروژه از **`WebViewAssetLoader`** استفاده می‌کند: یک دامنهٔ مجازی
(`https://appassets.androidplatform.net/assets/…`) می‌سازد و همان فایل‌های داخل APK را
روی HTTPS سرو می‌کند. نتیجه: موتور بازی یک «سرور وب معمولی» می‌بیند و همه‌چیز
(JSON، تکسچر، صدا، wasm) درست لود می‌شود.

نکات پیاده‌سازی در `MainActivity.java`:

- حالت **تمام‌صفحه / Immersive** (نوار وضعیت و ناوبری مخفی، در حالت sticky)
- روشن ماندن صفحه در حین بازی (`FLAG_KEEP_SCREEN_ON`)
- فعال بودن WebGL، JavaScript، DOM Storage و پخش صدا بدون نیاز به لمس اول
- پشتیبانی از نمایشگرهای نوچ‌دار (`LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`)
- دکمهٔ Back اندروید → عقب‌گرد در تاریخچهٔ WebView

---

## ۴. جایگزینی / به‌روزرسانی فایل‌های بازی

1. در PlayCanvas → **Publish** → **DOWNLOAD .ZIP** (Download Format = **Static Website**).
2. محتوای ZIP را در `app/src/main/assets/www/` بریز — طوری که
   `app/src/main/assets/www/index.html` وجود داشته باشد.
3. فایل‌های قبلی داخل `assets/www/` را پاک کن (به‌جز خود پوشه).
4. Commit و Push کن؛ ساخت خودکار شروع می‌شود.

> صفحهٔ فعلی `assets/www/index.html` فقط یک **placeholder** است تا مطمئن شویم Build
> درست کار می‌کند. با فایل‌های واقعی بازی جایگزینش کن.

---

## ۵. ساخت APK (GitHub Actions — رایگان)

```bash
git init
git add .
git commit -m "Captain Sadjad Android wrapper"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

سپس در GitHub:

1. تب **Actions** → ورک‌فلو **Build Android APK** خودش اجرا می‌شود.
2. بعد از چند دقیقه، پایین صفحهٔ همان اجرا → بخش **Artifacts**:
   - `CaptainSadjad-APK` → شامل `app-release.apk` و `app-debug.apk`
   - `CaptainSadjad-keystore` → کلید امضا (برای انتشارهای بعدی نگهش دار!)
3. دانلود و نصب کن.

با هر `push` روی شاخهٔ `main` و همچنین با دکمهٔ **Run workflow** دستی اجرا می‌شود.

### نکتهٔ امنیتی دربارهٔ کلید امضا

ورک‌فلو در هر اجرا یک `release.keystore` با رمز پیش‌فرض `captainsadjad2024` می‌سازد
تا APK امضاشده بسازد. **اگر می‌خواهی بازی را در Google Play منتشر کنی:**

1. یک keystore واقعی با رمز قوی بساز.
2. آن را به‌صورت Base64 در **GitHub Secrets** ذخیره کن.
3. مقادیر رمز را از Secrets بخوان (نه به‌صورت متن ساده در فایل).

رمز پیش‌فرض فقط برای نصب شخصی/تست مناسب است.

---

## ۶. ساخت روی کامپیوتر خودت (اختیاری)

نیازها: **JDK 17**، **Android SDK** (build-tools 34.0.0 + platform android-34)، اینترنت.

```bash
./gradlew assembleDebug      # → app/build/outputs/apk/debug/app-debug.apk
./gradlew assembleRelease    # امضاشده، اگر keystore.properties موجود باشد
```

اگر می‌خواهی روی سیستم خودت build امضاشده بگیری، فایل `keystore.properties` بساز:

```properties
storeFile=/مسیر/به/release.keystore
storePassword=...
keyAlias=...
keyPassword=...
```

---

## ۷. مجوزها و مشخصات

- **Package:** `com.captainsadjad.game` (نسخهٔ debug: `com.captainsadjad.game.debug`)
- **minSdk:** 21 (اندروید ۵) · **targetSdk / compileSdk:** 34
- **مجوزها:** فقط `INTERNET` (برای بازی‌هایی که محتوای آنلاین می‌خوانند؛ فایل‌های داخل APK به شبکه نیازی ندارند)
- **نیاز سخت‌افزاری:** OpenGL ES 2.0 (WebGL)
- **آیکن:** با `python tools/make_icon.py` دوباره ساخته می‌شود

---

## English summary

Android wrapper for the PlayCanvas game *Captain Sadjad*. The PlayCanvas **Static
Website** export is bundled in `app/src/main/assets/www/` and served to a fullscreen
`WebView` through **AndroidX `WebViewAssetLoader`**, which is required because Chromium
blocks `fetch()`/XHR on `file://` URLs. Build with `./gradlew assembleDebug assembleRelease`,
or automatically via the included GitHub Actions workflow
(`.github/workflows/build-apk.yml`), which produces signed `app-release.apk`,
`app-debug.apk` and the signing keystore as artifacts.
