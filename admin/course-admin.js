(function () {
  const $ = (sel) => document.querySelector(sel);

  function client() {
    return DocumentCentre && DocumentCentre.supabaseClient();
  }

  async function ensureStaff() {
    const session = await StudentAuth.getSession();
    if (!session) return false;
    return true;
  }

  async function loadCoursesAdmin() {
    const c = client();
    const list = $("#course-admin-list");
    if (!c || !list) return;
    const { data, error } = await c.from("courses").select("*").order("sort_order");
    if (error) {
      list.innerHTML = "<li>" + error.message + "</li>";
      return;
    }
    list.innerHTML = (data || [])
      .map(
        (row) =>
          "<li><span><strong>" +
          row.title +
          "</strong> · " +
          (row.is_free ? "Free" : "₹" + row.price_inr) +
          "</span><button type=\"button\" data-id=\"" +
          row.id +
          '" class="btn-admin btn-danger btn-del-course">Delete</button></li>'
      )
      .join("");
    list.querySelectorAll(".btn-del-course").forEach((btn) => {
      btn.addEventListener("click", async () => {
        if (!confirm("Delete this course?")) return;
        await c.from("courses").delete().eq("id", btn.getAttribute("data-id"));
        loadCoursesAdmin();
      });
    });
  }

  $("#course-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!(await ensureStaff())) {
      alert("Sign in as staff first.");
      return;
    }
    const c = client();
    const bucket = DocumentCentre.getServices().coursePdfBucket || "course-pdfs";
    const file = $("#course-pdf").files[0];
    let pdfPath = $("#course-pdf-path").value.trim();
    const slug = $("#course-slug").value.trim().toLowerCase().replace(/\s+/g, "-");

    if (file) {
      pdfPath = slug + "/" + Date.now() + "_" + file.name.replace(/[^a-zA-Z0-9._-]/g, "_");
      const { error: up } = await c.storage.from(bucket).upload(pdfPath, file, {
        upsert: true,
        contentType: file.type || "application/pdf",
      });
      if (up) {
        alert("PDF upload failed: " + up.message);
        return;
      }
    }

    const row = {
      slug,
      title: $("#course-title").value.trim(),
      description: $("#course-desc").value.trim(),
      price_inr: parseInt($("#course-price").value, 10) || 0,
      is_free: $("#course-free").checked,
      study_path: $("#course-study").value.trim(),
      pdf_storage_path: pdfPath,
      razorpay_payment_link: $("#course-razorpay").value.trim(),
      published: true,
      sort_order: parseInt($("#course-sort").value, 10) || 0,
    };

    const { error } = await c.from("courses").insert(row);
    if (error) alert(error.message);
    else {
      alert("Course saved.");
      e.target.reset();
      loadCoursesAdmin();
    }
  });

  $("#grant-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const c = client();
    const email = $("#grant-email").value.trim();
    const courseId = $("#grant-course").value;
    const { error } = await c.rpc("grant_purchase_by_email", {
      p_email: email,
      p_course_id: courseId,
    });
    if (error) alert(error.message);
    else alert("Access granted.");
  });

  async function loadCourseSelect() {
    const c = client();
    const sel = $("#grant-course");
    if (!c || !sel) return;
    const { data } = await c.from("courses").select("id, title").order("title");
    sel.innerHTML = (data || [])
      .map((r) => '<option value="' + r.id + '">' + r.title + "</option>")
      .join("");
  }

  document.addEventListener("DOMContentLoaded", function () {
    if ($("#course-admin-list")) {
      loadCoursesAdmin();
      loadCourseSelect();
    }
  });
})();