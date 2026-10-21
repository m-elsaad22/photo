#!/usr/bin/env python3
"""HTTP checks for published URLs (browser UA)."""
from __future__ import annotations

import re
import ssl
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
URLS = [
    "https://elsaidey-lawyer.tanceq.com/",
    "https://elsaidey-lawyer.tanceq.com/contact-us/",
    "https://elsaidey-lawyer.tanceq.com/about/",
    "https://elsaidey-lawyer.tanceq.com/legal-services/",
    "https://elsaidey-lawyer.tanceq.com/legal-services/criminal-cases/",
    "https://elsaidey-lawyer.tanceq.com/blog/",
    "https://elsaidey-lawyer.tanceq.com/privacy-policy/",
    "https://elsaidey-lawyer.tanceq.com/services/",
    "https://elsaidey-lawyer.tanceq.com/sitemap_index.xml",
    "https://elsaidey-lawyer.tanceq.com/robots.txt",
]


def check(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=90) as r:
        body = r.read(150000).decode("utf-8", errors="ignore")
        title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        t = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else ""
        desc = re.search(r'name=["\']description["\'][^>]*content=["\']([^"\']*)', body, re.I)
        return {
            "url": url,
            "status": r.status,
            "title": t[:100],
            "meta_desc": (desc.group(1)[:80] if desc else ""),
            "has_canonical": "rel=\"canonical\"" in body or "rel='canonical'" in body,
        }


def main() -> None:
    for u in URLS:
        try:
            print(check(u))
        except Exception as e:
            print({"url": u, "error": str(e)[:120]})


if __name__ == "__main__":
    main()
