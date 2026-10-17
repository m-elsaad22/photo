# elsaidey-lawyer — SEO & site tooling

مستودع توثيق وسكربتات لموقع [مؤسسة الصعيدي](https://elsaidey-lawyer.tanceq.com).

## المجلدات

- `audit/` — تقارير التدقيق وجرد الصفحات
- `seo/` — `keyword-research.csv`، خريطة الصفحات، خطة المحتوى
- `scripts/` — نشر/صيانة عبر WordPress REST API

## تشغيل السكربتات

```bash
export WP_USERNAME="..."
export WP_APP_PASSWORD="..."
python3 -m scripts.deploy_site_content
```

راجع `audit/02-implementation-report.md` لما نُفّذ على الموقع الحي.
