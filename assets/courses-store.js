(function () {
  const $ = (sel, root) => (root || document).querySelector(sel);

  function formatPrice(paiseOrInr) {
    const inr = Number(paiseOrInr) || 0;
    return inr === 0 ? "Free" : "₹" + inr.toLocaleString("en-IN");
  }

  async function loadCatalog() {
    const mount = $("#paid-courses-list");
    const loginBox = $("#student-login-box");
    if (!mount) return;

    const c = DocumentCentre && DocumentCentre.supabaseClient();
    if (!c) {
      mount.innerHTML =
        '<p class="doc-empty">Connect Supabase in <code>config/services.json</code> to sell paid PDF courses. See <code>PAID-COURSES.md</code>.</p>';
      return;
    }

    const session = await StudentAuth.getSession();
    if (loginBox) {
      loginBox.innerHTML = session
        ? '<p>Signed in as <strong>' +
          (session.user.email || "") +
          '</strong> · <a href="' +
          (window.SITE_BASE || "") +
          'my-courses.html">My courses</a> · <button type="button" id="student-logout" class="btn-admin" style="margin:0">Sign out</button></p>'
        : '<p><em>Sign in to access purchased PDFs.</em></p>';
      $("#student-logout")?.addEventListener("click", async () => {
        await StudentAuth.signOut();
        loadCatalog();
      });
    }

    const { data: courses, error } = await c
      .from("courses")
      .select("*")
      .eq("published", true)
      .order("sort_order", { ascending: true });

    if (error) {
      mount.innerHTML = "<p class=\"doc-missing\">" + error.message + "</p>";
      return;
    }
    if (!courses || !courses.length) {
      mount.innerHTML =
        '<p class="doc-empty">No paid courses yet. Admin can add courses in the admin panel.</p>';
      return;
    }

    const html = await Promise.all(
      courses.map(async (course) => {
        const owned =
          course.is_free ||
          (session && (await StudentAuth.hasPurchased(course.id)));
        const badge = course.is_free
          ? '<span class="price-badge free">Free</span>'
          : '<span class="price-badge paid">' + formatPrice(course.price_inr) + "</span>";
        const actions = [];
        if (course.study_path) {
          actions.push(
            '<a class="btn btn-secondary" href="' +
              (window.SITE_BASE || "") +
              course.study_path.replace(/^\//, "") +
              '">Online notes</a>'
          );
        }
        if (course.is_free && course.pdf_storage_path) {
          actions.push(
            '<button type="button" class="btn btn-primary course-dl" data-id="' +
              course.id +
              '" data-path="' +
              course.pdf_storage_path +
              '">Download PDF</button>'
          );
        } else if (owned && course.pdf_storage_path) {
          actions.push(
            '<button type="button" class="btn btn-primary course-dl" data-id="' +
              course.id +
              '" data-path="' +
              course.pdf_storage_path +
              '">Download PDF</button>'
          );
        } else if (!course.is_free && !owned) {
          const pay = window.SITE_PAYMENTS || {};
          const upiOn = pay.upiId && pay.preferUpiOverRazorpay !== false;
          if (upiOn) {
            actions.push(
              '<button type="button" class="btn btn-primary upi-pay" data-id="' +
                course.id +
                '">Pay via UPI (0% gateway)</button>'
            );
          }
          if (!upiOn && course.razorpay_payment_link) {
            actions.push(
              '<a class="btn btn-primary" href="' +
                course.razorpay_payment_link +
                '" target="_blank" rel="noopener">Pay online (Razorpay)</a>'
            );
          }
          if (!upiOn && !course.razorpay_payment_link) {
            actions.push(
              '<span class="doc-missing">Payment not configured — contact centre</span>'
            );
          }
          actions.push(
            '<span class="login-hint">After UPI: sign in and submit UTR, or wait for admin approval.</span>'
          );
        }
        return (
          '<article class="course-card paid-course-card">' +
          badge +
          "<h3>" +
          course.title +
          "</h3><p>" +
          (course.description || "") +
          "</p><div class=\"course-actions\">" +
          actions.join(" ") +
          "</div></article>"
        );
      })
    );

    mount.innerHTML = '<div class="course-grid">' + html.join("") + "</div>";

    mount.querySelectorAll(".course-dl").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const courseId = btn.getAttribute("data-id");
        const path = btn.getAttribute("data-path");
        await downloadPdf(courseId, path);
      });
    });

    mount.querySelectorAll(".upi-pay").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const session = await StudentAuth.getSession();
        if (!session) {
          alert("Please sign in first (form above), then pay via UPI.");
          return;
        }
        const id = btn.getAttribute("data-id");
        const course = (courses || []).find((c) => c.id === id);
        if (course && window.UpiPayment) UpiPayment.showUpiModal(course);
      });
    });
  }

  async function submitUpiPayment() {
    const session = await StudentAuth.getSession();
    const c = DocumentCentre && DocumentCentre.supabaseClient();
    if (!session || !c) {
      alert("Sign in required.");
      return;
    }
    const courseId = document.getElementById("upi-course-id")?.value;
    const amount = parseInt(document.getElementById("upi-amount")?.value || "0", 10);
    const utr = document.getElementById("upi-utr")?.value.trim();
    const note = document.getElementById("upi-student-note")?.value.trim();
    const { error } = await c.from("payment_requests").insert({
      user_id: session.user.id,
      course_id: courseId,
      amount_inr: amount,
      upi_reference: utr,
      student_note: note,
      status: "pending",
    });
    if (error) alert(error.message);
    else {
      alert("Submitted. Staff will verify your UPI payment and unlock the PDF.");
      loadCatalog();
    }
  }

  async function downloadPdf(courseId, storagePath) {
    const session = await StudentAuth.getSession();
    if (!session) {
      alert("Please sign in on My Courses first.");
      window.location.href = (window.SITE_BASE || "") + "my-courses.html";
      return;
    }
    const services = DocumentCentre.getServices();
    const fnUrl =
      (services.supabaseUrl || "").replace(/\/$/, "") +
      "/functions/v1/get-course-pdf";
    const res = await fetch(fnUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + session.access_token,
        apikey: services.supabaseAnonKey || "",
      },
      body: JSON.stringify({ course_id: courseId, storage_path: storagePath }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) {
      alert(body.error || "Could not unlock PDF. Complete payment or contact admin.");
      return;
    }
    if (body.url) window.open(body.url, "_blank", "noopener");
  }

  function bindLoginForm() {
    const form = $("#student-login-inline");
    if (!form) return;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        await StudentAuth.requireSignIn(
          $("#student-email").value.trim(),
          $("#student-password").value
        );
        loadCatalog();
      } catch (err) {
        alert(err.message || "Login failed");
      }
    });
    $("#student-signup-btn")?.addEventListener("click", async () => {
      try {
        await StudentAuth.signUp(
          $("#student-email").value.trim(),
          $("#student-password").value
        );
        alert("Account created. Check email if confirmation is enabled, then sign in.");
      } catch (err) {
        alert(err.message || "Sign up failed");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindLoginForm();
    loadCatalog();
  });

  window.CoursesStore = { loadCatalog, downloadPdf, submitUpiPayment };
})();