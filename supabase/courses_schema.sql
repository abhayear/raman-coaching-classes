-- Paid courses + PDF access (run after schema.sql in Supabase SQL Editor)

create table if not exists public.courses (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  title text not null,
  description text default '',
  price_inr integer not null default 0 check (price_inr >= 0),
  is_free boolean not null default false,
  study_path text default '',
  pdf_storage_path text default '',
  razorpay_payment_link text default '',
  published boolean not null default true,
  sort_order integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.purchases (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  course_id uuid not null references public.courses(id) on delete cascade,
  amount_inr integer not null default 0,
  status text not null default 'completed' check (status in ('pending', 'completed', 'refunded')),
  razorpay_payment_id text default '',
  created_at timestamptz not null default now(),
  unique (user_id, course_id)
);

create index if not exists purchases_user_id_idx on public.purchases (user_id);
create index if not exists courses_published_idx on public.courses (published);

alter table public.courses enable row level security;
alter table public.purchases enable row level security;

-- Anyone sees published courses (catalog)
create policy "Public read published courses"
  on public.courses for select
  using (published = true);

-- Replace with your real admin email(s):
create table if not exists public.staff_emails (
  email text primary key
);
insert into public.staff_emails (email)
values ('admin@ramancoachingclasses.example')
on conflict do nothing;

create or replace function public.is_staff()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from auth.users u
    inner join public.staff_emails s on s.email = u.email
    where u.id = auth.uid()
  );
$$;

create policy "Staff write courses"
  on public.courses for insert
  to authenticated
  with check (public.is_staff());

create policy "Staff update courses"
  on public.courses for update
  to authenticated
  using (public.is_staff());

create policy "Staff delete courses"
  on public.courses for delete
  to authenticated
  using (public.is_staff());

create policy "Students read own purchases"
  on public.purchases for select
  to authenticated
  using (auth.uid() = user_id);

create or replace function public.grant_purchase_by_email(p_email text, p_course_id uuid)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  uid uuid;
begin
  if not public.is_staff() then
    raise exception 'Staff only';
  end if;
  select id into uid from auth.users where lower(email) = lower(p_email) limit 1;
  if uid is null then
    raise exception 'No student account for that email — ask them to sign up on My Courses';
  end if;
  insert into public.purchases (user_id, course_id, amount_inr, status)
  values (uid, p_course_id, 0, 'completed')
  on conflict (user_id, course_id) do update set status = 'completed';
end;
$$;

grant execute on function public.grant_purchase_by_email(text, uuid) to authenticated;

-- Storage: create PRIVATE bucket "course-pdfs" (not public).
-- Use Edge Function get-course-pdf to issue short-lived signed URLs after purchase check.