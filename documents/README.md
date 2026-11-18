# Document Centre — how to add files

1. Put your file here (PDF, Word exported as PDF, images, etc.):
   - `documents/syllabus/`
   - `documents/notices/`
   - `documents/forms/`
   - `documents/papers/`
   - `documents/other/`

2. Register it in **`config/documents.json`** under the right category:

```json
{
  "title": "Admission form 2026",
  "file": "documents/forms/admission-2026.pdf",
  "description": "Fill and submit at the office",
  "updated": "2026-03-01"
}
```

3. Rebuild and deploy:

```powershell
python scripts/build_html.py
git add documents/ config/documents.json
git commit -m "Add documents"
git push
```

Files are copied to the live site under `/documents/...` when GitHub Actions runs.