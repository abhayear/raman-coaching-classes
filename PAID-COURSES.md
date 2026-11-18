# Paid courses & PDF sales — Raman Coaching Classes

## Best stack for this feature

| Piece | Technology | Why |
|-------|------------|-----|
| Website & notes | Static HTML (GitHub Pages) | Cheap, fast for 1,600+ chapters |
| Student accounts | Supabase Auth | Login, secure purchases |
| Course catalog & purchases | Supabase Postgres | Who bought what |
| Paid PDF files | Supabase Storage (private `course-pdfs`) | PDFs not public until paid |
| Payments (India) | **Razorpay Payment Links** | No custom backend to start |
| Unlock PDF | Supabase Edge Function `get-course-pdf` | Signed URL after purchase check |
| Optional auto-unlock | Edge Function `razorpay-webhook` | After online payment |

## Setup checklist

1. Run `supabase/schema.sql` + `supabase/courses_schema.sql`
2. Replace admin email in `staff_emails` table with your real staff email
3. Storage: private bucket **`course-pdfs`**
4. Deploy Edge Function **`get-course-pdf`** (required for PDF download)
5. Enable student sign-up: Supabase → Authentication → Providers → Email
6. Razorpay: create a **Payment Link** per paid course; paste URL in admin when creating course

## Student flow

1. **Courses** → see paid course → **Buy & pay** (Razorpay)
2. **Create account / Sign in** (same email as Razorpay)
3. **My courses** → **Open PDF** (or download on Courses page)

## Staff flow

1. **Admin** → sign in (staff email in `staff_emails`)
2. **Paid PDF courses** → upload PDF, set price, paste Razorpay link → Save
3. **Grant access** — for cash payments: enter student email (they must have registered)

## Razorpay Payment Link tips

- In link **Notes**, add `course_id` (UUID from Supabase `courses` table) for webhook automation
- Amount = course price in INR
- For manual unlock: skip webhook; use **Grant access** in admin after verifying payment

## Deploy Edge Function `get-course-pdf`

```bash
supabase login
supabase link --project-ref YOUR_REF
supabase functions deploy get-course-pdf
```

Set secret `COURSE_PDF_BUCKET=course-pdfs` in function settings.

## Pages on your site

| Page | Path |
|------|------|
| Course catalog | `/courses.html` |
| My courses | `/my-courses.html` |
| Admin | `/admin/index.html` |

## Rename coaching centre

Still only `config/branding.json` — payments and courses are separate.