# التقرير النهائي — استكمال موقع مؤسسة الصعيدي (2026-10-17)

## 1) قواعد الالتزام

| القاعدة | الحالة |
|---------|--------|
| عدم حذف/دمج صفحات أو مقالات | **محترم** — لم يُحذف أي محتوى منشور أو مسودة (بما فيها 135 و136) |
| عدم تغيير Slugs أو Redirects | **محترم** — لم تُغيَّر روابط الصفحات المنشورة |
| عدم حذف صور/تصنيفات/CPT | **محترم** |
| عدم نشر مسودات 135 و136 | **محترم** — ما زالتا `draft` |
| نسخة احتياطية | **جزئي عبر API** — `audit/backup-pages.json` و`audit/backup-posts.json` (محتوى REST). Rank Math `runBackup` رفض الإجراء. يُفضّل نسخ Updraft/host قبل تعديل القالب. |

---

## 2) فحص الحالة (قبل → بعد هذه الجولة)

### الصفحة الرئيسية — Title / Meta
- **قبل:** لا `<title>` ولا meta description في HTML (مؤكد سابقاً).
- **بعد:** **ما زال غير ظاهر** في HTML عند الاختبار الآلي (القالب KAYAN لا يمرّر Rank Math على الواجهة، أو الإعدادات غير مكتملة).
- **إجراءات نُفّذت:**
  - تفعيل إضافة **Insert Headers and Footers** (`insert-headers-and-footers/ihaf`).
  - تجهيز snippet جاهز: `audit/ihaf-homepage-head.html` (للصق في لوحة التحكم).
  - تجهيز plugin بديل: `elsaidey-seo-head.zip` + `plugin/elsaidey-seo-head/` (حقن title/meta عبر output buffering) — **لم يُرفع** (رفع ZIP عبر REST أعاد 406).
- **Rank Math `updateSettings`:** HTTP 403 (صلاحيات/nonce) — لم يُضبط Homepage عبر API.

### `/services/` — خطأ 500
- **قبل:** HTTP 500.
- **بعد:** **HTTP 500** (رسالة WordPress العامة «خطأ فادح» — `WP_DEBUG` مغلق).
- **تحقيق:** أُنشئت **9** عناصر CPT `services` منشورة + مسودة اختبار (139) — **لم يُحل** الخطأ → السبب **في ملفات قالب KAYAN/PHP** (غير متاحة عبر REST).
- **لم يُنفَّذ Redirect** إلى `/legal-services/` (حسب طلبك).

### صفحات منشورة (بدون تغيير روابط)
`/contact-us/` · `/about/` · `/legal-services/` + 9 تخصصات · `/blog/` · `/privacy-policy/` — **محفوظة**.

---

## 3) ما نُفّذ فعلياً على الموقع

1. **Excerpt/meta فرعي** لـ 14 صفحة (بدون تغيير slug/status) — `scripts/seo_enhance_pages.py`.
2. **5 مسودات جديدة** (لا نشر): `labor-law`, `real-estate-law`, `inheritance-law`, `administrative-law`, `terms-and-conditions` — تحت `/legal-services/` أو جذر للشروط.
3. **9 CPT services** منشورة (مرآة للتخصصات) — لمحاولة إصلاح الأرشيف.
4. **إضافات مثبتة:** IHAF (مفعّلة)، HFCM وWP Headers (غير مفعّلة) — **لم تُحذف**.
5. **مسودة CPT 139** (اختبار داخلي) — `draft` وليست محذوفة.

---

## 4) صفحات/مسودات جديدة

| Slug | الحالة | ملاحظة |
|------|--------|--------|
| labor-law | draft | بانتظار اعتماد تخصص عمالي |
| real-estate-law | draft | بانتظار اعتماد |
| inheritance-law | draft | بانتظار اعتماد |
| administrative-law | draft | بانتظار اعتماد |
| terms-and-conditions | draft | مراجعة قanونية قبل النشر |

---

## 5) نتائج اختبار (شغّل `python3 -m scripts.test_site_urls`)

يُحدَّث عند كل تشغيل. آخر تشغيل في هذه الجلسة تعرض **بطء/انقطاع** شبكة من بيئة الوكيل؛ راجع المخرجات محلياً بعد الرفع.

---

## 6) مشكلات ما زالت قائمة

| # | المشكلة | السبب | المطلوب |
|---|---------|--------|---------|
| 1 | لا title/meta على `/` | KAYAN + Rank Math | صق `audit/ihaf-homepage-head.html` في IHAF **أو** رفع `elsaidey-seo-head.zip` من wp-admin |
| 2 | `/services/` 500 | خطأ PHP في القالب | wp-admin/FTP: تفعيل `WP_DEBUG_LOG`، إصلاح `archive-services.php` أو ما ي equivalent |
| 3 | KAYAN: قائمة فارغة، geo AE، placeholder، واتساب مزدوج | إعدادات Theme Options | دخول لوحة KAYAN |
| 4 | Rank Math sitemap/meta كامل | 403 API + إعداد يدوي | Rank Math → Titles + regenerate sitemap |
| 5 | GSC / GA / GBP | لا صلاحيات | دعوة + NAP |
| 6 | بريد `admin@photo.tanceq.com` | إعداد WordPress | بريدكم الرسمي |

---

## 7) استعادة النسخة الاحتياطية

- **REST JSON:** استرجاع من `audit/backup-*.json` يدوياً عبر wp-admin أو سكربت PATCH.
- **استضافة:** استخدم نسخ Updraft/cPanel **قبل** أي تعديل على ملفات القالب.
- **IHAF:** إلغاء تفعيل الإضافة أو تفريغ حقل Header.

---

## 8) بيانات/صلاحيات مطلوبة منكم

1. تأكيد التخصصات: عمالي، عقاري، ميراث، إداري — للموافقة على نشر المسودات.
2. **رقم واتساب واحد** + ساعات العمل + البريد الرسمي.
3. رفع **`elsaidey-seo-head.zip`** أو لصق IHAF snippet + تأكيد ظهور title في View Source.
4. وصول **Theme Options KAYAN** أو FTP لإصلاح `/services/`.
5. Rank Math: حساب بصلاحية `manage_options` كاملة أو تنفيذ Homepage meta يدوياً.
6. Google Search Console / Business Profile (اختياري للمرحلة المحلية).

---

## 9) ملفات المستودع الم added

- `scripts/seo_enhance_pages.py`, `create_draft_specialties.py`, `sync_cpt_services.py`, `test_site_urls.py`, `install_plugin_zip.py`
- `plugin/elsaidey-seo-head/`, `elsaidey-seo-head.zip`
- `audit/backup-pages.json`, `backup-posts.json`, `ihaf-homepage-head.html`, هذا التقرير

**المهمة غير مكتملة** حتى: (أ) title/meta على الرئيسية مُتحقق، (ب) `/services/` يعمل أو خطة معتمدة بدون redirect غير موافق عليه، (ج) إعدادات KAYAN الحرجة.
