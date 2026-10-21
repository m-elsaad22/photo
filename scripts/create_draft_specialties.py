#!/usr/bin/env python3
"""Create DRAFT specialty pages pending client confirmation — no deletes."""
from __future__ import annotations

from scripts.deploy_site_content import blocks, cta, heading, list_block, para
from scripts import wp_client as wp

DRAFTS = [
    (
        "labor-law",
        "القضايا العمالية (مسودة — بانتظار اعتماد)",
        "مسودة: صفحة للتوعية بخدمات عمالية إذا اعتمدتها المؤسسة. لا تُعد خدمة مؤكدة حتى موافقتكم.",
    ),
    (
        "real-estate-law",
        "المنازعات العقارية (مسودة — بانتظار اعتماد)",
        "مسودة: نزاعات عقارية وإيجارات — تحتاج تأكيد نطاق المكتب.",
    ),
    (
        "inheritance-law",
        "قضايا الميراث (مسودة — بانتظار اعتماد)",
        "مسودة: إجراءات تركة وتقسيم — قد تتداخل مع صفحة الأسرة؛ للمراجعة قبل النشر.",
    ),
    (
        "administrative-law",
        "المنازعات الإدارية (مسودة — بانتظار اعتماد)",
        "مسودة: دعاوى إدارية ومجلس الدولة — تأكيد التخصص مطلوب.",
    ),
    (
        "terms-and-conditions",
        "الشروط والأحكام (مسودة)",
        "مسودة عامة لاستخدام الموقع والتواصل — تحتاج مراجعة قanونية قبل النشر.",
    ),
]


def main() -> None:
    hub = wp.get("/wp/v2/pages?slug=legal-services&status=any")
    parent = hub[0]["id"] if hub else 0
    for slug, title, intro in DRAFTS:
        existing = wp.get(f"/wp/v2/pages?slug={slug}&status=any")
        content = blocks(
            para(f"<strong>تنبيه:</strong> {intro}"),
            heading("نطاق مقترح", 2),
            list_block(["يُحدد بعد اعتماد المؤسسة."]),
            cta(),
        )
        payload = {
            "title": title,
            "slug": slug,
            "status": "draft",
            "content": content,
            "parent": parent if slug != "terms-and-conditions" else 0,
        }
        if existing:
            wp.patch(f"/wp/v2/pages/{existing[0]['id']}", payload)
            print("updated draft", slug)
        else:
            wp.post("/wp/v2/pages", payload)
            print("created draft", slug)


if __name__ == "__main__":
    main()
