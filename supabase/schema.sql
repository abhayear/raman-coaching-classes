-- Run in Supabase: SQL Editor → New query → paste → Run

create table if not exists public.centre_documents (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text default '',
  category text not null default 'other',
  storage_path text not null,
  file_name text not null,
  mime_type text default 'application/octet-stream',
  updated_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists centre_documents_category_idx on public.centre_documents (category);

alter table public.centre_documents enable row level security;

-- Anyone can read (public document centre)
create policy "Public read documents"
  on public.centre_documents for select
  using (true);

-- Only signed-in admin can insert/update/delete
create policy "Admin insert documents"
  on public.centre_documents for insert
  to authenticated
  with check (true);

create policy "Admin update documents"
  on public.centre_documents for update
  to authenticated
  using (true);

create policy "Admin delete documents"
  on public.centre_documents for delete
  to authenticated
  using (true);

-- Storage bucket: create in Dashboard → Storage → New bucket
-- Name: centre-documents
-- Public bucket: ON (or use signed URLs — this schema assumes public read on files)

-- Storage policies (run after bucket exists):
-- Allow public read:
-- create policy "Public read files" on storage.objects for select using ( bucket_id = 'centre-documents' );
-- Allow authenticated upload:
-- create policy "Admin upload" on storage.objects for insert to authenticated with check ( bucket_id = 'centre-documents' );
-- create policy "Admin delete files" on storage.objects for delete to authenticated using ( bucket_id = 'centre-documents' );