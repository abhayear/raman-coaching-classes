# Complete payment method — UPI, no GST hassle (small coaching)

**Recommended for Raman Coaching Classes:** **UPI + manual approve** = **₹0 payment-gateway fee**. No Razorpay required to start.

> This is not tax advice. Many small coaching centres are **below GST registration threshold** (commonly ₹20 lakh turnover in a year for services — confirm with a CA). You can still accept UPI; you simply may not charge **GST** until registered. Use plain fee receipts without GSTIN.

---

## Part A — One-time setup (30 minutes)

### 1. Your UPI ID

Use a **business UPI** if possible (PhonePe Business / Paytm for Business / bank merchant QR).  
Or start with personal UPI: `yourname@ybl` / `@paytm` / `@oksbi`.

Edit **`config/payments.json`**:

```json
{
  "upiId": "ramancoaching@ybl",
  "payeeName": "Raman Coaching Classes",
  "preferUpiOverRazorpay": true,
  "supportPhone": "+91-98XXXXXXXX"
}
```

### 2. Supabase (already used for courses)

Run SQL files in order:

1. `supabase/schema.sql`
2. `supabase/courses_schema.sql`
3. **`supabase/payment_requests.sql`** ← UPI approvals

Update **`staff_emails`** with your admin email.

### 3. Private PDF bucket

Storage → bucket **`course-pdfs`** (private) + deploy **`get-course-pdf`** Edge Function (see `PAID-COURSES.md`).

### 4. Publish site

```powershell
python scripts/build_html.py
git add config/payments.json
git commit -m "UPI payment settings"
git push origin master
```

---

## Part B — Student pays (every sale)

1. Student opens **Courses** → **Pay via UPI (0% gateway)**.
2. Scans **QR** or copies **UPI ID** — pays **exact ₹ amount**.
3. Student copies **12-digit UTR** from GPay/PhonePe/Paytm.
4. Signs in → **I have paid — submit for approval**.
5. You verify amount + UTR in your UPI/bank app.

---

## Part C — You approve (admin)

1. Open **Admin** → sign in (staff email).
2. **Pending UPI payments** → **Approve** (unlocks PDF) or **Reject**.
3. Student opens **My courses** → **Download PDF**.

**Cash at centre:** use **Grant access** with student email (student must register on site first).

---

## Part D — Add a paid PDF course

1. Admin → **Paid PDF courses**.
2. Title, price (INR), upload PDF.
3. Leave **Razorpay link empty** if using UPI only.
4. Save.

---

## Part E — Optional: Razorpay later (still no monthly fee on standard)

When you want **auto-approve** without checking UTR:

1. Sign up at [razorpay.com](https://razorpay.com) (PAN + bank).
2. Create **Payment Link** per course.
3. Paste link in admin **Razorpay payment link**.
4. Set `"preferUpiOverRazorpay": false` in `payments.json` **or** keep both (UPI stays default while `preferUpiOverRazorpay` is true).

Razorpay charges ~**2% per transaction** (not free). GST on gateway fee may apply per their invoice.

---

## Cost comparison

| Method | Gateway fee | GST on fee | You verify UTR |
|--------|-------------|------------|----------------|
| **UPI (this guide)** | **0%** | N/A | Yes (few seconds) |
| Razorpay Payment Link | ~2% | On Razorpay invoice | Optional webhook |
| Cash | 0% | N/A | In person |

---

## Files to edit

| File | Purpose |
|------|---------|
| `config/payments.json` | UPI ID, payee name, instructions |
| `config/services.json` | Supabase keys |
| `config/branding.json` | Centre name |

---

## Live URLs

- Courses: `https://abhayear.github.io/raman-coaching-classes/courses.html`
- My courses: `…/my-courses.html`
- Admin: `…/admin/index.html`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No UPI button | Set `upiId` in `payments.json`, rebuild, push |
| Submit UTR fails | Run `payment_requests.sql` |
| Approve fails | Student email in `staff_emails`; run grant/approve SQL |
| PDF won’t open | Deploy `get-course-pdf` function |