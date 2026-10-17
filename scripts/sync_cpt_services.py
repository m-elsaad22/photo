#!/usr/bin/env python3
"""Publish KAYAN CPT `services` entries — mirrors legal-services pages."""
from __future__ import annotations

from scripts import wp_client as wp

BASE = "https://elsaidey-lawyer.tanceq.com/legal-services"

SERVICES: dict[str, str] = {
    "criminal-cases": "\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u062c\u0646\u0627\u0626\u064a\u0629 \u0648\u0627\u0644\u062f\u0641\u0627\u0639 \u0627\u0644\u062c\u0646\u0627\u0626\u064a",
    "family-law": "\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u0623\u0633\u0631\u0629 \u0648\u0627\u0644\u0623\u062d\u0648\u0627\u0644 \u0627\u0644\u0634\u062e\u0635\u064a\u0629",
    "civil-cases": "\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u0645\u062f\u0646\u064a\u0629 \u0648\u0627\u0644\u062a\u0639\u0648\u064a\u0636\u0627\u062a",
    "commercial-law": "\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u062a\u062c\u0627\u0631\u064a\u0629 \u0648\u062a\u0623\u0633\u064a\u0633 \u0627\u0644\u0634\u0631\u0643\u0627\u062a",
    "contracts-disputes": "\u0627\u0644\u0639\u0642\u0648\u062f \u0648\u0627\u0644\u0645\u0646\u0627\u0632\u0639\u0627\u062a \u0627\u0644\u062a\u0639\u0627\u0642\u062f\u064a\u0629",
    "prosecution-investigations": "\u0627\u0644\u0646\u064a\u0627\u0628\u0629 \u0648\u0627\u0644\u062a\u062d\u0642\u064a\u0642\u0627\u062a",
    "appeals-cassation": "\u0627\u0644\u0627\u0633\u062a\u0626\u0646\u0627\u0641 \u0648\u0627\u0644\u0646\u0642\u0636 \u0648\u0645\u062c\u0644\u0633 \u0627\u0644\u062f\u0648\u0644\u0629",
    "legal-consultations": "\u0627\u0644\u0627\u0633\u062a\u0634\u0627\u0631\u0627\u062a \u0627\u0644\u0642\u0627\u0646\u0648\u0646\u064a\u0629",
    "lawyer-talkha-mansoura": "\u0645\u062d\u0627\u0645\u064d \u0641\u064a \u0637\u0644\u062e\u0627 \u0648\u0627\u0644\u0645\u0646\u0635\u0648\u0631\u0629",
}


def main() -> None:
    for slug, title in SERVICES.items():
        link = f"{BASE}/{slug}/"
        existing = wp.get(f"/wp/v2/services?slug={slug}&status=any")
        body = {
            "title": title,
            "slug": slug,
            "status": "publish",
            "content": f'<!-- wp:paragraph --><p>صفحة التفاصيل: <a href="{link}">{link}</a></p><!-- /wp:paragraph -->',
        }
        if existing:
            wp.patch(f"/wp/v2/services/{existing[0]['id']}", body)
            print("updated", slug)
        else:
            wp.post("/wp/v2/services", body)
            print("created", slug)


if __name__ == "__main__":
    main()
