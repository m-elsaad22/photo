#!/usr/bin/env python3
"""Publish core legal pages and services for elsaidey-lawyer.tanceq.com."""
from __future__ import annotations

import json
from scripts import wp_client as wp

PHONE = "+201002120325"
WA = "+201055833331"
BASE = "https://elsaidey-lawyer.tanceq.com"
ADDRESS = "شقة 2، الدور الرابع، عمارة السمنودي، شارع فرنش بيكر، طلخا، الدقهلية"
HUB_SLUG = "legal-services"


def blocks(*parts: str) -> str:
    return "\n\n".join(p.strip() for p in parts if p.strip())


def para(text: str) -> str:
    return f"<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->"


def heading(text: str, level: int = 2) -> str:
    return f'<!-- wp:heading {{"level":{level}}} -->\n<h{level}>{text}</h{level}>\n<!-- /wp:heading -->'


def list_block(items: list[str]) -> str:
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return f"<!-- wp:list -->\n<ul>{lis}</ul>\n<!-- /wp:list -->"


def cta() -> str:
    return blocks(
        heading("تواصل مع المكتب", 2),
        para(
            f'لطلب استشارة، تواصل عبر <a href="https://wa.me/{WA.lstrip("+")}">واتساب</a> '
            f'أو <a href="tel:{PHONE}">اتصل على {PHONE}</a>. '
            "اذكر نوع المشكلة والمستندات المتوفرة دون إرسال بيانات حساسة غير ضرورية."
        ),
    )


def service_url(slug: str) -> str:
    return f"{BASE}/{HUB_SLUG}/{slug}/"


def service_page(
    title: str,
    slug: str,
    intro: str,
    scope: list[str],
    steps: list[str],
    docs: list[str],
    faqs: list[tuple[str, str]],
    related_slugs: list[str],
) -> dict:
    faq_html: list[str] = []
    for q, a in faqs:
        faq_html.extend([heading(q, 3), para(a)])
    related_links = " · ".join(
        f'<a href="{service_url(s)}">{s.replace("-", " ")}</a>' for s in related_slugs
    )
    content = blocks(
        para(intro),
        heading("نطاق الخدمة", 2),
        list_block(scope),
        heading("كيف نعمل", 2),
        list_block(steps),
        heading("مستندات مفيدة (حسب نوع القضية)", 2),
        list_block(docs),
        heading("أسئلة شائعة", 2),
        *faq_html,
        heading("خدمات ذات صلة", 2),
        para(related_links),
        cta(),
        para(
            "<em>تنبيه:</em> المعلومات للتوعية العامة ولا تُعد استشارة قانونية ملزمة "
            "حتى يتم فحص مستندات القضية. النتائج تختلف بحسب الوقائع والإجراءات."
        ),
    )
    return {"title": title, "slug": slug, "status": "publish", "content": content, "excerpt": intro[:280]}


SERVICES = [
    service_page(
        "القضايا الجنائية والدفاع الجنائي",
        "criminal-cases",
        "دفاع جنائي وتمثيل أمام محاكم الجنح والجنايات والمحاكم العسكرية وفق إجراءات منضبطة.",
        [
            "الحضور أمام النيابة والتحقيقات في الملفات الجنائية.",
            "المرافعة في الجنح والجنايات.",
            "الطعن والاستئناف في الأحكام الجنائية — وفق المهل والأسس القانونية.",
            "متابعة ملفات التحقيق حتى الإحالة أو غيرها من الإجراءات.",
        ],
        [
            "تقييم أولي للواقعة والمستندات.",
            "تحديد الإجراء العاجل (حضور تحقيق، طلبات procedural مناسبة).",
            "إعداد المذكرات والمرافعة في الجلسات.",
            "متابعة الطعون والتنفيذ حسب الحكم.",
        ],
        ["محضر أو قرار تحقيق", "بطاقة شخصية", "مستندات إثبات أو دفاع", "أحكام سابقة إن وُجدت"],
        [
            ("هل تتعاملون مع قضايا المخدرات والنصب؟", "نعم ضمن الدفاع الجنائي العام بعد مراجعة الوقائع."),
            ("هل يمكن الحضور عن بُعد؟", "بعض الإجراءات تتطلب حضوراً شخصياً؛ يُحدد ذلك بعد معرفة نوع الجلسة."),
        ],
        ["prosecution-investigations", "appeals-cassation"],
    ),
    service_page(
        "قضايا الأسرة والأحوال الشخصية",
        "family-law",
        "طلاق، نفقة، حضانة، رؤية، إثبات نسب، وإجراءات أحوال شخصية وفق القانون المصري.",
        ["دعاوى الطلاق والخلع", "النفقة والحضانة والرؤية", "إثبات أو نفي نسب", "إجراءات تركة — بالتنسيق حسب الملف"],
        ["استشارة أولية", "تحديد الدعوى والاختصاص", "إعداد صحيفة الدعوى", "متابعة الجلسات والتنفيذ"],
        ["عقد الزواج", "شهادات الميلاد", "محاضر أو أحكام سابقة", "إثبات دخل عند طلب النفقة"],
        [("هل الاستشارة الأولى عن بُعد؟", "نعم، مع إمكانية حضور في المنصورة/طلخا عند الحاجة.")],
        ["legal-consultations", "lawyer-talkha-mansoura"],
    ),
    service_page(
        "القضايا المدنية والتعويضات",
        "civil-cases",
        "منازعات مدنية، تعويضات، إيجارات، وملكية — مع بناء استراتيجية للملف.",
        ["دعاوى التعويض", "منازعات الإيجار", "دعاوى الملكية والحيازة", "تنفيذ أحكام مدنية — حسب الإجراء"],
        ["تحليل العقد أو الضرر", "تقدير المسار والمدة", "رفع الدعوى أو الدفاع", "متابعة التنفيذ"],
        ["عقود", "إنذارات", "محاضر", "فواتير أو تقارير للتعويض"],
        [("ما المدة المتوقعة؟", "تختلف حسب المحكمة والاختصاص ومدى التعقيد.")],
        ["contracts-disputes", "commercial-law"],
    ),
    service_page(
        "القضايا التجارية وتأسيس الشركات",
        "commercial-law",
        "تأسيس شركات، حوكمة، ونزاعات تجارية بين الشركاء أو مع الغير.",
        ["تأسيس الشركات وصياغة عقود الشركاء", "نزاعات تجارية", "مطالبات مستحقات", "مراجعة عقود B2B"],
        ["تحديد الشكل القانوني", "إعداد المستندات", "التسجيل والمتابعة", "حل النزاع بالتراضي أو التقاضي"],
        ["هويات الشركاء", "عقد تأسيس", "سجل تجاري", "مراسلات النزاع"],
        [("هل تصيغون عقود شركاء؟", "نعم، مع مراجعة بنود الحوكمة والخروج.")],
        ["contracts-disputes", "legal-consultations"],
    ),
    service_page(
        "العقود والمنازعات التعاقدية",
        "contracts-disputes",
        "صياغة ومراجعة عقود ببنود واضحة تقلل النزاع قبل وقوعه.",
        ["صياغة عقود", "مراجعة بنود", "مطالبات تنفيذ عقد", "فسخ وإبطال — حسب السبب"],
        ["فهم الالتزامات", "صياغة أو تعديل البنود", "تفاوض", "تقاضي عند اللزوم"],
        ["مسودات العقد", "فواتير", "مراسلات", "إثبات التسليم"],
        [("هل مراجعة العقد تكفي؟", "غالباً للكشف عن المخاطر؛ التعديل يعتمد على طرفي العقد.")],
        ["commercial-law", "civil-cases"],
    ),
    service_page(
        "النيابة والتحقيقات",
        "prosecution-investigations",
        "حضور تحقيقات النيابة وإعداد دفاع أولي وطلبات مناسبة.",
        ["حضور التحقيقات", "تقديم مستندات الدفاع", "متابعة قرارات النيابة", "الطعن على التصرفات — وفق المهل"],
        ["معرفة موعد التحقيق", "مراجعة المحضر", "حضور مع الموكل", "متابعة الإجراء التالي"],
        ["محضر", "بطاقة", "مستندات", "توكيل"],
        [("ماذا أفعل بعد تحرير محضر؟", "تواصل فوراً مع محامٍ؛ راجع أيضاً مقالات المدونة للتوعية العامة.")],
        ["criminal-cases", "legal-consultations"],
    ),
    service_page(
        "الاستئناف والنقض ومجلس الدولة",
        "appeals-cassation",
        "تمثيل أمام الاستئناف العالي ومجلس الدولة في ملفات مدروسة.",
        ["استئناف أحكام", "مرافعات النقض — حسب الأهلية", "دعاوى مجلس الدولة", "مراجعة أسباب الطعن"],
        ["مراجعة الحكم والملف", "تحديد المهل", "إعداد مذكرات", "متابعة الجلسات"],
        ["الحكم", "ملف الدعوى", "مذكرات سابقة"],
        [("ما الفرق بين الاستئناف والنقض؟", "موضوع للمراجعة — راجع مقال المدونة المخصص (مسودة).")],
        ["criminal-cases", "civil-cases"],
    ),
    service_page(
        "الاستشارات القانونية",
        "legal-consultations",
        "رأي قانوني واضح قبل أي خطوة مصيرية — حضوري أو عن بُعد.",
        ["استشارة أولية", "مراجعة مستندات", "خطة إجراءات", "تحويل لتمثيل كامل عند الحاجة"],
        ["تحديد السؤال", "تقييم المستندات", "توصية مكتوبة", "متابعة اختيارية"],
        ["عقود", "مراسلات", "أحكام"],
        [("هل الاستشارة تُنشئ علاقة محامٍ/موكل؟", "لا إلا باتفاق صريح على التوكيل.")],
        ["family-law", "commercial-law"],
    ),
    service_page(
        "محامي في طلخا والمنصورة",
        "lawyer-talkha-mansoura",
        "مكتب محاماة في طلخا والمنصورة (الدقهلية) مع متابعة عن بُعد في أنحاء مصر.",
        ["استشارات حضورية في المقر", "تمثيل أمام محاكم الدقهلية", "متابعة عن بُعد لمحافظات أخرى"],
        ["تحديد موعد", "تقييم الملف", "تمثيل أو استشارة", "متابعة"],
        ["حسب نوع القضية"],
        [("هل لديكم فروع أخرى؟", "لا نُعلن فروعاً غير المقر المذكور.")],
        ["legal-consultations", "family-law"],
    ),
]


def upsert_page(spec: dict, parent: int | None = None) -> dict:
    slug = spec["slug"]
    existing = wp.get(f"/wp/v2/pages?slug={slug}&status=any")
    payload = {
        "title": spec["title"],
        "slug": slug,
        "status": spec["status"],
        "content": spec["content"],
    }
    if parent:
        payload["parent"] = parent
    if spec.get("excerpt"):
        payload["excerpt"] = spec["excerpt"]
    if existing:
        return wp.patch(f"/wp/v2/pages/{existing[0]['id']}", payload)
    return wp.post("/wp/v2/pages", payload)


def main() -> None:
    service_links = "".join(
        f'<li><a href="{service_url(s["slug"])}">{s["title"]}</a></li>' for s in SERVICES
    )
    hub = upsert_page(
        {
            "title": "الخدمات القانونية",
            "slug": HUB_SLUG,
            "status": "publish",
            "content": blocks(
                heading("خدمات المحاماة والاستشارات", 1),
                para(
                    "اختر التخصص الأقرب لاحتياجك. كل صفحة توضّح نطاق الخدمة وخطوات العمل "
                    "دون وعود بنتائج محددة."
                ),
                f"<!-- wp:list -->\n<ul>{service_links}</ul>\n<!-- /wp:list -->",
                cta(),
            ),
        }
    )
    hub_id = hub["id"]

    upsert_page(
        {
            "title": "تواصل معنا",
            "slug": "contact-us",
            "status": "publish",
            "content": blocks(
                heading("طلب استشارة قانونية", 1),
                para(
                    "مؤسسة الصعيدي للمحاماة والاستشارات القانونية — حضور محلي في طلخا والمنصورة، "
                    "ومتابعة عن بُعد في مختلف محافظات مصر."
                ),
                heading("بيانات التواصل", 2),
                list_block(
                    [
                        f'هاتف: <a href="tel:{PHONE}">{PHONE}</a>',
                        f'واتساب: <a href="https://wa.me/{WA.lstrip("+")}">اضغط للمراسلة</a>',
                        f"العنوان: {ADDRESS}",
                    ]
                ),
                heading("ماذا نحتاج في أول تواصل؟", 2),
                list_block(
                    [
                        "نوع المشكلة (جنائي، أسرة، مدني، تجاري، إلخ).",
                        "موعد تقريبي للواقعة أو الإجراء إن وُجد.",
                        "هل توجد مستندات (محضر، عقد، حكم، إنذار)؟",
                    ]
                ),
                para(
                    "نحافظ على سرية البيانات. تجنّب إرسال مستندات حساسة عبر قنوات غير آمنة "
                    "حتى يتم الاتفاق على آلية التسليم المناسبة."
                ),
            ),
        }
    )

    upsert_page(
        {
            "title": "من نحن",
            "slug": "about",
            "status": "publish",
            "content": blocks(
                heading("مؤسسة الصعيدي للمحاماة والاستشارات القانونية", 1),
                para(
                    "يقود المكتب المستشار عيد الصعيدي، محامٍ بالاستئناف العالي ومجلس الدولة "
                    "ومحاكم الجنايات والمحاكم العسكرية."
                ),
                heading("نطاق العمل", 2),
                list_block(
                    [
                        "المرافعة أمام درجات التقاضي المختلفة.",
                        "الاستئناف العالي ومجلس الدولة.",
                        "الجنايات والمحاكم العسكرية.",
                        "صياغة العقود وتأسيس الشركات.",
                        "الاستشارات القانونية للأفراد والشركات.",
                    ]
                ),
                heading("الموقع الجغرافي", 2),
                para(
                    f"مقر المكتب: {ADDRESS}. نخدم طلخا والمنصورة والدقهلية "
                    "مع متابعة ملفات عن بُعد في أنحاء مصر حسب طبيعة القضية."
                ),
                cta(),
            ),
        }
    )

    results = {"hub": hub["link"], "services": []}
    for spec in SERVICES:
        p = upsert_page(spec, parent=hub_id)
        results["services"].append({"title": spec["title"], "link": p["link"]})

    privacy = blocks(
        heading("سياسة الخصوصية", 1),
        para("موقع elsaidey-lawyer.tanceq.com تديره مؤسسة الصعيدي للمحاماة والاستشارات القانونية."),
        heading("البيانات التي نجمعها", 2),
        para("نستخدم بيانات الاتصال التي تقدمها طوعاً للرد على طلب الاستشارة."),
        heading("الاتصال", 2),
        para(f"هاتف: {PHONE} — العنوان: {ADDRESS}"),
    )
    existing = wp.get("/wp/v2/pages?slug=privacy-policy&status=any")
    if existing:
        wp.patch(
            f"/wp/v2/pages/{existing[0]['id']}",
            {"title": "سياسة الخصوصية", "status": "publish", "content": privacy, "slug": "privacy-policy"},
        )
    else:
        wp.post(
            "/wp/v2/pages",
            {"title": "سياسة الخصوصية", "slug": "privacy-policy", "status": "publish", "content": privacy},
        )

    blog = upsert_page(
        {
            "title": "المدونة القانونية",
            "slug": "blog",
            "status": "publish",
            "content": blocks(
                heading("مدونة مؤسسة الصعيدي", 1),
                para("مقالات للتوعية العامة — لا تغني عن استشارة قانونية مباشرة."),
            ),
        }
    )
    results["blog"] = blog["link"]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
