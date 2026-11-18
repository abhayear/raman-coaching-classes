// Deploy: supabase functions deploy get-course-pdf --no-verify-jwt
// Env: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (auto in Supabase)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
      },
    });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return json({ error: "Sign in required" }, 401);
    }

    const { course_id, storage_path } = await req.json();
    if (!course_id || !storage_path) {
      return json({ error: "Missing course_id or storage_path" }, 400);
    }

    const supabaseUser = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      { global: { headers: { Authorization: authHeader } } }
    );

    const { data: userData, error: userErr } = await supabaseUser.auth.getUser();
    if (userErr || !userData.user) {
      return json({ error: "Invalid session" }, 401);
    }

    const { data: course } = await supabaseUser
      .from("courses")
      .select("is_free, pdf_storage_path")
      .eq("id", course_id)
      .single();

    if (!course) return json({ error: "Course not found" }, 404);

    if (!course.is_free) {
      const { data: purchase } = await supabaseUser
        .from("purchases")
        .select("id")
        .eq("user_id", userData.user.id)
        .eq("course_id", course_id)
        .eq("status", "completed")
        .maybeSingle();

      if (!purchase) {
        return json({ error: "Purchase required" }, 403);
      }
    }

    const admin = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    const bucket = Deno.env.get("COURSE_PDF_BUCKET") ?? "course-pdfs";
    const { data: signed, error: signErr } = await admin.storage
      .from(bucket)
      .createSignedUrl(storage_path, 3600);

    if (signErr || !signed?.signedUrl) {
      return json({ error: signErr?.message ?? "Could not sign URL" }, 500);
    }

    return json({ url: signed.signedUrl });
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});

function json(body: Record<string, unknown>, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}