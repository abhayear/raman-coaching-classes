# Deploy — Raman Coaching Classes website

## Rebrand (rename later)

Edit **`config/branding.json`** (`siteName`, `phone`, `email`, etc.), then:

```powershell
python scripts/build_html.py
```

For GitHub Pages, set `deployWebBasePath` to `/<your-repo-name>/` and use the same value in `.github/workflows/deploy-pages.yml` as `SITE_BASE_PATH`.

## Local preview

```powershell
.\start-book.bat
```

Open **http://localhost:8765/index.html** (coaching home).

## Deploy to GitHub Pages (free, public)

1. Create a GitHub repo named **`raman-coaching-classes`** (must match `deployWebBasePath` in config).
2. Push this project to `main` or `master`.
3. In GitHub: **Settings → Pages → Build: GitHub Actions**.
4. Push triggers `.github/workflows/deploy-pages.yml`.
5. Live URL: `https://<your-username>.github.io/raman-coaching-classes/`

The `book/` folder is built in CI (not committed).

## One-time push

```powershell
git add -A
git commit -m "Raman Coaching Classes website and study library"
gh repo create raman-coaching-classes --public --source=. --remote=origin --push
```

Then enable **Pages → GitHub Actions** in the repo settings.