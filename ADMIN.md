# Admin document uploads (Supabase)

Students use **Document Centre** on the website. You upload files in **Admin** without pushing to Git.

## Links after deploy

| Page | URL |
|------|-----|
| Document Centre | `https://abhayear.github.io/raman-coaching-classes/documents.html` |
| Admin panel | `https://abhayear.github.io/raman-coaching-classes/admin/index.html` |

## One-time setup (~15 minutes)

### 1. Create Supabase project

1. Go to [https://supabase.com](https://supabase.com) → New project (free tier).
2. **Project Settings → API** — copy:
   - **Project URL** → `supabaseUrl`
   - **anon public** key → `supabaseAnonKey`

### 2. Database table

**SQL Editor** → paste and run: `supabase/schema.sql`

### 3. Storage bucket

1. **Storage** → New bucket  
   - Name: `centre-documents`  
   - **Public bucket**: ON  

2. **Storage → Policies** for `centre-documents`:

```sql
-- Public read
create policy "Public read centre docs"
on storage.objects for select
using ( bucket_id = 'centre-documents' );

-- Admin upload (authenticated users only)
create policy "Admin upload centre docs"
on storage.objects for insert
to authenticated
with check ( bucket_id = 'centre-documents' );

create policy "Admin delete centre docs"
on storage.objects for delete
to authenticated
using ( bucket_id = 'centre-documents' );
```

### 4. Admin login user

**Authentication → Users** → **Add user** → email + password (your staff admin).

### 5. Connect website

Edit **`config/services.json`**:

```json
{
  "supabaseUrl": "https://xxxx.supabase.co",
  "supabaseAnonKey": "eyJhbGci...",
  "storageBucket": "centre-documents"
}
```

Rebuild and push:

```powershell
python scripts/build_html.py
git add config/services.json
git commit -m "Connect Supabase document uploads"
git push origin master
```

## Daily use

1. Open **Admin** → sign in with your Supabase admin email/password.
2. Fill title, category, choose file → **Upload**.
3. Students refresh **Document Centre** — new file appears immediately (no redeploy).

## Security notes

- Only **anon** key goes in the website (safe for public sites).
- Never put the **service_role** key in the repo.
- Only your Supabase Auth users can upload or delete.
- Use a strong admin password.

## Fallback

If Supabase is not configured, static files in `documents/` + `config/documents.json` still work.