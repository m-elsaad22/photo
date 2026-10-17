#!/usr/bin/env python3
"""Upload and activate a plugin ZIP via WordPress admin update endpoint."""
from __future__ import annotations

import base64
import os
import ssl
import urllib.request
from pathlib import Path

SITE = os.environ.get("WP_SITE_URL", "https://elsaidey-lawyer.tanceq.com")
USER = os.environ["WP_USERNAME"]
PASS = os.environ["WP_APP_PASSWORD"]
UA = "Mozilla/5.0 (compatible; ElsaideySiteAgent/1.0)"


def main() -> None:
    zip_path = Path(__file__).resolve().parents[1] / "elsaidey-seo-head.zip"
    if not zip_path.is_file():
        raise SystemExit(f"Missing {zip_path}")

    # Try REST plugin install from org first pattern; custom zip uses update.php?action=upload-plugin
    url = f"{SITE}/wp-admin/update.php?action=upload-plugin"
    boundary = "----ElsaideyBoundary7MA4YWxk"
    data = []
    data.append(f"--{boundary}\r\n".encode())
    data.append(
        b'Content-Disposition: form-data; name="pluginzip"; filename="elsaidey-seo-head.zip"\r\n'
    )
    data.append(b"Content-Type: application/zip\r\n\r\n")
    data.append(zip_path.read_bytes())
    data.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(data)

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "User-Agent": UA,
            "Authorization": "Basic "
            + base64.b64encode(f"{USER}:{PASS}".encode()).decode(),
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
            html = resp.read(8000).decode("utf-8", errors="replace")
            print("HTTP", resp.status, "len", len(html))
            print(html[:1500])
    except Exception as e:
        print("upload failed:", e)
        # Fallback: REST activate if folder already exists
        auth = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
        activate_url = f"{SITE}/wp-json/wp/v2/plugins/elsaidey-seo-head/elsaidey-seo-head"
        req2 = urllib.request.Request(
            activate_url,
            data=b'{"status":"active"}',
            headers={
                "User-Agent": UA,
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req2, context=ctx, timeout=60) as resp2:
                print("activate", resp2.read()[:500])
        except Exception as e2:
            print("activate failed", e2)


if __name__ == "__main__":
    main()
