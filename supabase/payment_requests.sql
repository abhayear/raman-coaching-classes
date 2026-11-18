-- UPI manual payments (zero payment-gateway fee). Run after courses_schema.sql.

create table if not exists public.payment_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  course_id uuid not null references public.courses(id) on delete cascade,
  amount_inr integer not null default 0,
  upi_reference text not null default '',
  student_note text default '',
  status text not null default 'pending'
    check (status in ('pending', 'approved', 'rejected')),
  reviewed_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists payment_requests_status_idx on public.payment_requests (status, created_at desc);

alter table public.payment_requests enable row level security;

create policy "Students insert own payment requests"
  on public.payment_requests for insert
  to authenticated
  with check (auth.uid() = user_id and status = 'pending');

create policy "Students read own payment requests"
  on public.payment_requests for select
  to authenticated
  using (auth.uid() = user_id);

create policy "Staff read all payment requests"
  on public.payment_requests for select
  to authenticated
  using (public.is_staff());

create policy "Staff update payment requests"
  on public.payment_requests for update
  to authenticated
  using (public.is_staff());

create or replace function public.approve_payment_request(p_request_id uuid)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  r public.payment_requests%rowtype;
begin
  if not public.is_staff() then
    raise exception 'Staff only';
  end if;
  select * into r from public.payment_requests where id = p_request_id for update;
  if not found then
    raise exception 'Request not found';
  end if;
  if r.status <> 'pending' then
    raise exception 'Already processed';
  end if;
  insert into public.purchases (user_id, course_id, amount_inr, status)
  values (r.user_id, r.course_id, r.amount_inr, 'completed')
  on conflict (user_id, course_id) do update set status = 'completed', amount_inr = r.amount_inr;
  update public.payment_requests
  set status = 'approved', reviewed_at = now()
  where id = p_request_id;
end;
$$;

create or replace function public.reject_payment_request(p_request_id uuid)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  if not public.is_staff() then
    raise exception 'Staff only';
  end if;
  update public.payment_requests
  set status = 'rejected', reviewed_at = now()
  where id = p_request_id and status = 'pending';
end;
$$;

grant execute on function public.approve_payment_request(uuid) to authenticated;
grant execute on function public.reject_payment_request(uuid) to authenticated;