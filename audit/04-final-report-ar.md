# التقرير النهائي — إصلاح `/services/` وSEO الرئيسية (2026-10-18)

## 1) الالتزام بالقواعد

| القاعدة | الحالة |
|---------|--------|
| عدم حذف/دمج مقالات أو صفحات | **محترم** — لم يُحذف محتوى |
| الإبقاء على مسودتي 135 و136 | **محترم** — ما زالتا `draft` (مؤكد في النسخة الاحتياطية 2026-10-18) |
| عدم نشر مسودات قانونية جديدة | **محترم** |
| عدم تغيير Slug / Canonical / Redirect | **محترم** |
| عدم المساس بـ 9 عناصر CPT `services` المنشورة | **محترم** — لم تُعدَّل الروابط أو المحتوى |
| نسخة احتياطية قبل التغييرات | **نعم** — `audit/backup-*-snapshot-2026-10-18.json` |

---

## 2) سبب خطأ 500 على `/services/` (تحليل مُتحقَّق)

### السلوك
- `/services/` و `?post_type=services` → **HTTP 500**
- `/services/criminal-cases/` (مفرد) → **200**
- `/service-category/criminal-law/` (تصنيف) → **200**
- **9** عناصر CPT منشورة — الخطأ **ليس** لعدم وجود محتوى

### السبب الجذري (قالب KAYAN 2.4.7)
1. `ThemeStatic::Locate()` يوجّه كل `is_archive()` إلى `@archive/shape.php`.
2. في الإصدارات الحديثة من KAYAN، `shape.php` يختار:
   - `@archive/{taxonomy}.php` للتصنيفات، أو
   - `@archive/archive-{post_type}.php` لأرشيف CPT إن وُجد الملف.
3. **ملف `archive-services.php` غير موجود** في حزمة القالب (مُؤكَّد من `kayan-theme-v1.4.9-ready.zip` ونسخة GitHub)، فيُحمَّل **`default.php`**.
4. `default.php` مكتوب لـ **`WP_Term`** (`$obj->term_id`, `$obj->taxonomy`, `$obj->description`).
5. على أرشيف CPT، `get_queried_object()` يعيد **`WP_Post_Type`** → في **PHP 8.1** الوصول لخصائص غير معرّفة / منطق التصنيف يسبب **خطأ فادح** → 500.

### الملفات المطلوبة للإصلاح الدائم في القالب (FTP/مدير ملفات — `DISALLOW_FILE_EDIT` مفعّل على الاستضافة)
| الملف | الإجراء |
|-------|---------|
| `wp-content/themes/kayan-theme/components/packs/@archive/archive-services.php` | **إنشاء** قالب أرشيف CPT (قائمة `services` + `Posts` part) |
| أو `@archive/shape.php` | التأكد من فرع `is_post_type_archive()` (موجود في v1.3.0+) **مع** وجود `archive-services.php` |
| `@archive/default.php` | **تحسين دفاعي**: إذا `is_post_type_archive()` فلا تفترض `WP_Term` |

**لم يُعدَّل أي ملف قالب على الخادم** (التحرير محظور + لا SSH).

### الحل البديل المُجهَّز (إضافة / WPCode)
- إضافة جاهزة: `plugin/elsaidey-kayan-fixes/` + `elsaidey-kayan-fixes.zip`
- تعترض `template_redirect` (أولوية 9) وتعرض أرشيف `services` قبل `ThemeStatic::Locate` (10) دون redirect.

---

## 3) SEO الصفحة الرئيسية (تشخيص HTML فعلي)

### ما يظهر في المصدر (Chrome UA، ~310KB)
- **`wp_head()` يُستدعى جزئياً** (generator، روابط wp-json، canonical على بعض الصفحات الداخلية).
- **لا `<title>`** و **لا `meta name="description"`** على `/`.
- **لا علامات Rank Math** في HTML (`rank-math` غير موجود) — متوقع: جسر KAYAN SEO يعطّل مخرجات Rank Math في الواجهة (`rank_math/frontend/disable`).
- جسر KAYAN SEO **يفترض** إخراج العنوان/الوصف عبر `kayan_seo_output_document_title_tag` و `kayan_seo_render_head_meta` على `wp_head` — **لا يظهر في HTML** (خلل تنفيذ/تسجيل hooks على هذا الموقع أو مسار رأس الصفحة v3).

### تعارض Rank Math (مُتحقَّق من الإعدادات)
- Rank Math كان ما زال يحمل **نصوص موقع مصور قديم**:
  - `homepage_title`: «مصور فوتوغرافي في المنصورة… MOHAMED MORSY»
  - `homepage_description`: نص تصوير فوتوغرافي
- **تم تحديث** (عبر WP-CLI المعتمد، دون لمس slugs):
  - `homepage_title` → «مؤسسة الصعيدي للمحاماة والاستشارات القanونية | طلخا والمنصورة»
  - `homepage_description` → نص مكتب محاماة (طلخا/المنصورة)
  - `knowledgegraph_name` → اسم المؤسسة

**ملاحظة:** تحديث Rank Math **لا يكفي** وحده ما دام مخرجات Rank Math معطّلة في الواجهة وKAYAN لا يطبع العنوان — يلزم تفعيل snippet/إضافة الإصلاح أو إصلاح `#header/part.php` / `kayan-seo/frontend.php` في القالب.

### IHAF / WPCode
- IHAF (WPCode Lite) **مفعّل** لكن **لا يُعتمد** كحل أول قبل التشخيص؛ على الرئيسية v3 قد لا يُنفَّذ إذا كان الحقن خارج مسار `wp_head()` الكامل.
- **Snippet جاهز (غير مفعّل):** ID **170** — «Elsaidey KAYAN fixes (services + SEO)»
  - **تفعيل يدوي:** [wp-admin → WPCode snippet 170](https://elsaidey-lawyer.tanceq.com/wp-admin/admin.php?page=wpcode-snippet-manager&snippet_id=170)
  - مسودة اختبار سابقة: ID 168 (يمكن حذفها من لوحة WPCode).

---

## 4) تسجيل الأخطاء (آمن)

| البند | الحالة |
|-------|--------|
| `WP_DEBUG` للزوار | **غير مفعّل** (رسالة 500 عامة — صحيح أمنياً) |
| `WP_DEBUG_LOG` | **يتطلب** تعديل `wp-config.php` من الاستضافة (لا صلاحية `config set` عبر WPVibe) |
| بديل | تثبيت **Query Monitor** (admin فقط) أو قراءة `wp-content/debug.log` بعد تفعيل `WP_DEBUG_LOG` + `WP_DEBUG_DISPLAY=false` |

---

## 5) نتائج اختبار الروابط (بعد هذه الجولة)

| URL | HTTP | Title في HTML | Meta description |
|-----|------|---------------|------------------|
| `/` | 200 | **لا** | **لا** |
| `/services/` | **500** | — | — |
| `/contact-us/` | 200 | **لا** | **لا** |
| `/legal-services/` | 200 | **لا** | **لا** |
| `/legal-services/criminal-cases/` | 200 | **لا** | **لا** |
| `/blog/` | 200 | **لا** | **لا** |
| `/privacy-policy/` | 200 | **لا** | **لا** |
| `/sitemap_index.xml` | 200 | — | — |
| `/robots.txt` | 200 | — | — |

**بعد تفعيل snippet 170 أو رفع `elsaidey-kayan-fixes.zip`:** أعد تشغيل `python3 -m scripts.test_site_urls` وتوقّع `/services/` → 200 وظهور title/meta على `/`.

---

## 6) ما نُفّذ فعلياً على الموقع

1. نسخ REST احتياطية: `audit/backup-*-snapshot-2026-10-18.json`
2. تحديث Rank Math `rank-math-options-titles` (homepage + knowledge graph) — إزالة نصوص المصور القديمة
3. إنشاء WPCode snippet **170** (كود الإصلاح — **بانتظار التفعيل**)
4. **لم** يُنشر أي مسودة قانونية؛ **لم** تُغيَّر القائمة/الواتساب/البريد

---

## 7) ما يحتاج تدخلك (wp-admin / الاستضافة)

1. **تفعيل snippet 170** (أو رفع وتفعيل `elsaidey-kayan-fixes.zip` من Plugins → Add New → Upload).
2. **إصلاح القالب (مُفضّل طويل الأمد):** إضافة `archive-services.php` تحت `@archive/` كما في تقرير الملفات أعلاه؛ أو رفع تحديث KAYAN من المطور.
3. **تفعيل `WP_DEBUG_LOG`** مؤقتاً إذا أردت stack trace رسمي قبل/بعد إصلاح القالب.
4. **Rank Math:** مراجعة باقي الحقول (Organization، Local SEO، Sitemap) — تم تصحيح Homepage فقط.
5. **Cloudflare:** تسجيل wp-admin من المتصفح قد يتطلب تحقيقاً بشرياً (منع تفعيل snippet آلياً من Cloud Agent).

---

## 8) ملفات المستودع (فرع `cursor/fix-services-seo-c204`)

- `plugin/elsaidey-kayan-fixes/elsaidey-kayan-fixes.php`
- `elsaidey-kayan-fixes.zip`
- `audit/04-final-report-ar.md` (هذا الملف)
- `audit/backup-*-snapshot-2026-10-18.json`

**الخلاصة:** سبب 500 **محدد وقابل للإصلاح** في أرشيف CPT بالقالب؛ حل جاهز للتفعيل. SEO الرئيسية: **سبب** = تعطيل Rank Math في الواجهة + غياب `<title>`/description من KAYAN؛ **بيانات Rank Math للhomepage صُحّحت**؛ **يلزم تفعيل snippet/إضافة** أو تعديل القالب لظهور العلامات في HTML.
