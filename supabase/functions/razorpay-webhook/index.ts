// Optional: auto-unlock course after Razorpay payment.
// Deploy: supabase functions deploy razorpay-webhook --no-verify-jwt
// Set Razorpay webhook URL to this function URL.
// Env: RAZORPAY_WEBHOOK_SECRET, SUPABASE_SERVICE_ROLE_KEY
// In Payment Link notes, pass: course_id, student_email

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req) => {
  const raw = await req.text();
  const secret = Deno.env.get("RAZORPAY_WEBHOOK_SECRET") ?? "";
  const signature = req.headers.get("x-razorpay-signature") ?? "";

  // TODO: verify HMAC SHA256 signature with secret (see Razorpay webhook docs)
  if (!secret) {
    return new Response("Webhook secret not configured", { status: 500 });
  }

  let payload: { event?: string; payload?: { payment?: { entity?: Record<string, unknown> } } };
  try {
    payload = JSON.parse(raw);
  } catch {
    return new Response("Bad JSON", { status: 400 });
  }

  if (payload.event !== "payment.captured") {
    return new Response("ignored", { status: 200 });
  }

  const payment = payload.payload?.payment?.entity;
  if (!payment) return new Response("no payment", { status: 400 });

  const email = (payment.email as string) || (payment.notes as Record<string, string>)?.student_email;
  const courseId = (payment.notes as Record<string, string>)?.course_id;
  if (!email || !courseId) {
    return new Response("missing notes", { status: 400 });
  }

  const admin = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
  );

  const { data: users } = await admin.auth.admin.listUsers();
  const user = users.users.find((u) => u.email?.toLowerCase() === email.toLowerCase());
  if (!user) {
    return new Response("user not registered", { status: 200 });
  }

  const amount = Math.round(Number(payment.amount ?? 0) / 100);
  await admin.from("purchases").upsert({
    user_id: user.id,
    course_id: courseId,
    amount_inr: amount,
    status: "completed",
    razorpay_payment_id: String(payment.id ?? ""),
  });

  return new Response("ok", { status: 200 });
});