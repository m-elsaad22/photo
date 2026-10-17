# تقرير تدقيق موقع مؤسسة الصعيدي (2026-10-17)

**النطاق:** فحص فعلي عبر WordPress REST API، وزحف HTTP للصفحات العامة، وLighthouse (أداء/SEO).  
**ما لم يُفحص:** ملفات PHP/CSS/JS على الخادم (لا وصول FTP/SSH)، إعدادات Rank Math الداخلية بالكامل، Google Search Console/Analytics (غير متاح).

---

## 1. ملخص تنفيذي

الموقع **قابل للاستخدام بصرياً كLanding Page قانونية** على قالب KAYAN، لكنه يحمل **آثار مشروع سابق (تصوير/photo.tanceq.com)** ومشاكل **SEO تقنية حرجة** (غياب `<title>` وMeta على القالب)، و**روابط مكسورة/معاد توجيهها**، و**خطأ 500** على `/services/`.  
تم تنفيذ جزء من الإصلاحات عبر API (صفحات خدمات، تواصل، about، خصوصية، إلغاء Sample Page).

---

## 2. WordPress — الإعدادات والمحتوى

| البند | الحالة المؤكدة |
|--------|----------------|
| عنوان الموقع | مؤسسة الصعيدi |
| الوصف | للمحاماة والاستشارات القanونية |
| اللغة | ar |
| الصفحة الرئيسية | `show_on_front: posts` (ليست صفحة ثابتة) |
| مقالات منشورة | 0 (قبل المسودات) |
| صفحات قبل التدخل | Sample Page (منشورة)، Privacy Policy (مسودة إنجليزية) |
| GUIDs قديمة | `photo.tanceq.com` في صفحات |
| البريد الإداري | `admin@photo.tanceq.com` |
| أنواع محتوى مخصصة (CPT) | services, reviews, faqs, portfolio, pricing + taxonomy `cities` |
| عناصر CPT منشورة | 0 (services/reviews/…) |

**القالب النشط:** KAYAN Theme (YourColor/Rukn). **Twenty Twenty-Four** غير مفعّل.

**إضافات نشطة (API):** Classic Editor، Classic Widgets، Rank Math SEO، WPVibe.

---

## 3. الصفحة الرئيسية (/)

**محتوى مؤكد (من HTML):**
- H1: مؤسسة الصعيدي للمحامaة والاستشارات القanونية
- المستشار عيد الصعيدي — استئناf عالي، مجلس الدولة، جنايات، عسkrية
- عنوان: طلخa، المنصورة، الدقهلية + متابعة عن بُعد
- هاتف: `+201002120325` | واتساب: `+201055833331` (ورقم آخر `201151481000` في أجزاء من الصفحة)
- placeholder: `[[عدد القضايا والاستشارات]]`
- قائمة `<nav class="menu"></nav>` **فارغة**
- مبدّل دولة افتراضي **الإمارات (ae)** وليس مصر

**SEO (مؤكد):**
- لا `<title>`، لا meta description، لا canonical، لا JSON-LD على الرئيسية
- Rank Math **لا يظهر** في HTML الرئيسية (القالب لا يمر عبر `wp_head` بالشكل المعتاد أو يعطل المeta)

**Lighthouse (2026-10-17):** Performance **0.81** | SEO **0.82** | FCP **3.3s** | LCP **3.5s**

---

## 4. URLs حرجة

| URL | HTTP | ملاحظة |
|-----|------|--------|
| `/` | 200 | Landing KAYAN |
| `/contact-us/` | 200 | **أُنشئت** — كانت 302 → الرئيسية |
| `/about/` | 200 | **أُنشئت** |
| `/legal-services/` + 9 فروع | 200 | **أُنشئت** |
| `/blog/` | 200 | **أُنشئت** (placeholder) |
| `/privacy-policy/` | 200 | **نُشرت** بالعربية |
| `/sample-page/` | 302 → `/` | **أُلغي النشر** (draft) |
| `/services/` | **500** | أرشيف CPT — خطأ فادح في القالب/الإضafa |
| `robots.txt` | فارغ/غير متاح من الفحص الأول | |
| `sitemap_index.xml` | 200 | Rank Math — **page-sitemap فقط** (قبل توسيع المحتوى) |

---

## 5. SEO تقني

| العنصر | الحالة |
|--------|--------|
| Permalinks | pretty URLs تعمل للصفحات الجديدة |
| Canonical | يظهر على **صفحات WordPress** الجديدة فقط |
| Schema | غير مؤكد على الرئيسية؛ لم يُضبط عبر Rank Math API (صلاحيات/nonce) |
| Sitemap | لا يشمل بعد كل الصفحات الجديدة حتى إعادة توليد Rank Math |
| روابط داخلية من الرئيسية | كثيرها يشير `/contact-us/` (كانت مكسورة — أُصلحت جزئياً) |
| بقايا مشروع التصوير | GUIDs، بريد photo، CPT portfolio/before_after، tags تصوير (لم يُكمل حذفها — API tags بطيء/timeout) |
| Geo switcher خليجي | غير مناسب لمكتب في مصر |

---

## 6. التحويل والتواصل

- أزرار اتصال/واتساب **موجودة** على الرئيسية
- **لا نموذج WordPress** مؤكد على الرئيسية (لا `<form>` في HTML المحفوظ)
- **رقمان واتساب** — يحتاج قراراً من المؤسسة
- `/contact-us/` يعرض أرقاماً واضحة + CTA

---

## 7. أولويات الإصلاح (مرتبة)

### P0 — حرج
1. إصلاح **`<title>` + meta + Schema** للرئيسية عبر لوحة KAYAN/Rank Math أو mu-plugin (يتطلب wp-admin/ملفات)
2. إصلاح **500 على `/services/`** أو إيقاف أرشيف CPT واستخدام `/legal-services/` في القالب
3. **توحيد واتساب** وإزالة placeholder `[[عدد القضايا]]`
4. ضبط **الدولة الافتراضية مصر** وإزالة/تعطيل geo غير relevant

### P1 — مهم
5. Rank Math: عناوين/descriptions لكل صفحة خدمة + إعادة توليد Sitemap
6. ربط **Google Search Console + Analytics**
7. Google Business Profile (طلخa/المنصورة) — اتساق NAP
8. تحديث **admin email** وبريد المؤسسة الرسمي

### P2 — نمو
9. نشر مقالات المدونة بعد **مراجعة قanونية**
10. تنظيف tags/CPT التصوير
11. تحسين LCP (صور WebP، تقليل JS particles/owl)

---

## 8. بيانات تحتاج تأكيداً منكم

- البريد الرسمي للمؤسسة
- رقم واتساب الوحيد المعتمد
- ساعات العمل
- قائمة خدمات **غير** مذكورة على الموقع (إن وُجدت)
- صلاحية ادعاء «محامٍ بالاستئناf…» للصياغة التسويقية
- وصول wp-admin لقالب KAYAN (Theme Options) أو FTP
- Google Business Profile / Search Console

---

## 9. ما تم تنفيذه في هذه الجولة (API)

- إلغاء نشر Sample Page
- نشر: contact-us, about, legal-services (+9 خدمات), blog, privacy-policy
- مسودتا مقال `[مراجعة قanونية]`
- إنشاء taxonomy service_categories (criminal-law) — تجريبي

راجع `audit/02-implementation-report.md` للتفاصيل.
