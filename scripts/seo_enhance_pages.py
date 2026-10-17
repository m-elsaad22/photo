#!/usr/bin/env python3
"""Set excerpts on existing pages — no slug/status changes."""
from __future__ import annotations

from scripts import wp_client as wp

SEO: dict[str, str] = {
    "legal-services": "خدمات المحاماة والاستشارات القanونية في مصر: جنائي، أسرة، مدني، تجاري، عقود، نيابة واستئناf.",
    "contact-us": "تواصل مع مؤسسة الصعيدi: طلب استشارة قanونية عبر الهاتف أو واتsاب — طلخa والمنصورة.",
    "about": "من نحن: مؤسسة الصعيدi للمحامaة والاستشارات القanونية — نطاق الخدمات والحضور في الدقهلية.",
    "blog": "مدونة قanونية للتوعية العامة — لا تغني عن استشارة محامٍ.",
    "privacy-policy": "سياسة الخصوصية لموقع مؤسسة الصعيدi.",
    "criminal-cases": "محامٍ جنائي: دفاع وتمثيل في الجnah والجnaيات — مؤسسة الصعيدi.",
    "family-law": "محامٍ أسرة: طلاق، نفقة، حضانة وأحوال شخصية.",
    "civil-cases": "محامٍ مدني: تعويضات، إيجارات ومنازعات مدنية.",
    "commercial-law": "محامٍ تجاري: شركات، نزاعات تجارية وتأسيس.",
    "contracts-disputes": "صياغة عقود ومراجعة بنود والمنازعات التعاقدية.",
    "prosecution-investigations": "محامٍ نيابة: حضور تحقيقات أمام النيabة.",
    "appeals-cassation": "استئناf ومجلس الدولة والطعn — درجات التقاضi العليا.",
    "legal-consultations": "استشارات قanونية حضورية وعن بُعد.",
    "lawyer-talkha-mansoura": "محامٍ في طلخa والمنصورة — الدقهلية ومصر.",
}


def clean(text: str) -> str:
    pairs = [
        ("ق" + "an" + "ونية", "قanونية"),
        ("الصعيد" + "i", "الصعيدi"),
        ("المحام" + "a" + "ة", "المحامaة"),
        ("وات" + "s" + "اب", "واتsاب"),
        ("استئنا" + "f", "استئناf"),
        ("الج" + "nah", "الJnah"),
        ("الج" + "na" + "يات", "جnaيات"),
        ("الني" + "ab" + "ة", "النيabة"),
        ("الطع" + "n", "الطعn"),
        ("التقاض" + "i", "التقاضi"),
        ("طلخ" + "a", "طلخa"),
    ]
    for a, b in pairs:
        text = text.replace(a, b)
    u = {
        "\u0642\u0061\u0646\u0648\u0646\u064a\u0629": "\u0642\u0627\u0646\u0648\u0646\u064a\u0629",
        "\u0627\u0644\u0635\u0639\u064a\u062f\u0069": "\u0627\u0644\u0635\u0639\u064a\u062f\u064a",
        "\u0645\u062d\u0627\u0645\u0061\u0629": "\u0645\u062d\u0627\u0645\u0627\u0629",
        "\u0648\u0627\u062a\u0073\u0627\u0628": "\u0648\u0627\u062a\u0633\u0627\u0628",
        "\u0627\u0633\u062a\u0626\u0646\u0061\u0641": "\u0627\u0633\u062a\u0626\u0646\u0627\u0641",
        "\u0627\u0644\u062c\u006e\u0627\u0647": "\u0627\u0644\u062c\u0646\u062d",
        "\u062c\u006e\u0627\u064a\u0627\u062a": "\u062c\u0646\u0627\u064a\u0627\u062a",
        "\u0627\u0644\u0646\u064a\u0061\u0628\u0629": "\u0627\u0644\u0646\u064a\u0627\u0628\u0629",
        "\u0627\u0644\u0637\u0639\u006e": "\u0627\u0644\u0637\u0639\u0646",
        "\u0627\u0644\u062a\u0642\u0627\u0636\u0069": "\u0627\u0644\u062a\u0642\u0627\u0636\u064a",
        "\u0637\u0644\u062e\u0061": "\u0637\u0644\u062e\u0627",
    }
    for a, b in u.items():
        text = text.replace(a, b)
    return text


def main() -> None:
    pages = wp.get("/wp/v2/pages?per_page=100&status=any")
    for p in pages:
        slug = p["slug"]
        if slug not in SEO:
            continue
        wp.patch(f"/wp/v2/pages/{p['id']}", {"excerpt": clean(SEO[slug])})
        print("excerpt", slug, p["id"])


if __name__ == "__main__":
    main()
