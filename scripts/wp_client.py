#!/usr/bin/env python3
"""Minimal WordPress REST client for elsaidey-lawyer.tanceq.com."""
from __future__ import annotations

import base64
import json
import ssl
import urllib.error
import urllib.request
from typing import Any

import os

SITE = os.environ.get("WP_SITE_URL", "https://elsaidey-lawyer.tanceq.com")
USER = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
if not USER or not APP_PASSWORD:
    raise SystemExit("Set WP_USERNAME and WP_APP_PASSWORD environment variables.")
UA = "Mozilla/5.0 (compatible; ElsaideySiteAgent/1.0; +https://elsaidey-lawyer.tanceq.com)"


def request(method: str, path: str, data: dict | None = None) -> Any:
    url = f"{SITE}/wp-json{path}" if path.startswith("/") else path
    body = None
    headers = {
        "User-Agent": UA,
        "Authorization": "Basic "
        + base64.b64encode(f"{USER}:{APP_PASSWORD}".encode()).decode(),
    }
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            raw = resp.read()
            if not raw:
                return None
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {err_body[:500]}") from e


def get(path: str) -> Any:
    return request("GET", path)


def post(path: str, data: dict) -> Any:
    return request("POST", path, data)


def patch(path: str, data: dict) -> Any:
    return request("PATCH", path, data)


def delete(path: str, force: bool = True) -> Any:
    suffix = "?force=true" if force else ""
    return request("DELETE", f"{path}{suffix}")
