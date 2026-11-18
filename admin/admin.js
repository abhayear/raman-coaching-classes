(function () {
  const $ = (sel) => document.querySelector(sel);
  const msg = (text, kind) => {
    const el = $("#admin-message");
    if (!el) return;
    el.className = "admin-msg " + (kind || "ok");
    el.textContent = text;
    el.classList.remove("hidden");
  };

  function client() {
    return window.DocumentCentre && DocumentCentre.supabaseClient();
  }

  function showSetup() {
    $("#login-panel").classList.add("hidden");
    $("#upload-panel").classList.add("hidden");
    $("#manage-panel")?.classList.add("hidden");
    $("#courses-admin-panel")?.classList.add("hidden");
    $("#setup-panel").classList.remove("hidden");
  }

  function showLogin() {
    $("#setup-panel").classList.add("hidden");
    $("#upload-panel").classList.add("hidden");
    $("#manage-panel")?.classList.add("hidden");
    $("#courses-admin-panel")?.classList.add("hidden");
    $("#login-panel").classList.remove("hidden");
  }

  function showUpload(email) {
    $("#setup-panel").classList.add("hidden");
    $("#login-panel").classList.add("hidden");
    $("#upload-panel").classList.remove("hidden");
    $("#manage-panel")?.classList.remove("hidden");
    $("#courses-admin-panel")?.classList.remove("hidden");
    $("#admin-user").textContent = email || "Admin";
    loadAdminList();
  }

  async function init() {
    const s = DocumentCentre.getServices();
    if (!s.supabaseUrl || !s.supabaseAnonKey) {
      showSetup();
      return;
    }
    const c = client();
    if (!c) {
      msg("Supabase library failed to load.", "err");
      showSetup();
      return;
    }
    const { data } = await c.auth.getSession();
    if (data.session) showUpload(data.session.user.email);
    else showLogin();
  }

  $("#login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const c = client();
    const email = $("#login-email").value.trim();
    const password = $("#login-password").value;
    const { error } = await c.auth.signInWithPassword({ email, password });
    if (error) msg(error.message, "err");
    else showUpload(email);
  });

  $("#logout-btn")?.addEventListener("click", async () => {
    await client().auth.signOut();
    showLogin();
    msg("Signed out.", "ok");
  });

  $("#upload-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const c = client();
    const bucket = DocumentCentre.getServices().storageBucket || "centre-documents";
    const title = $("#doc-title").value.trim();
    const description = $("#doc-description").value.trim();
    const category = $("#doc-category").value;
    const fileInput = $("#doc-file");
    const file = fileInput.files && fileInput.files[0];
    if (!file) {
      msg("Choose a file.", "err");
      return;
    }
    const btn = $("#upload-btn");
    btn.disabled = true;
    const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, "_");
    const path = category + "/" + Date.now() + "_" + safeName;

    const { error: upErr } = await c.storage.from(bucket).upload(path, file, {
      upsert: false,
      contentType: file.type || "application/octet-stream",
    });
    if (upErr) {
      msg("Upload failed: " + upErr.message, "err");
      btn.disabled = false;
      return;
    }

    const { error: dbErr } = await c.from("centre_documents").insert({
      title,
      description,
      category,
      storage_path: path,
      file_name: file.name,
      mime_type: file.type || "application/octet-stream",
    });
    if (dbErr) {
      msg("File uploaded but database error: " + dbErr.message, "err");
      btn.disabled = false;
      return;
    }

    msg("Document uploaded. Students see it on the Document Centre immediately.", "ok");
    e.target.reset();
    btn.disabled = false;
    loadAdminList();
  });

  async function loadAdminList() {
    const c = client();
    const list = $("#admin-doc-list");
    if (!c || !list) return;
    const { data, error } = await c
      .from("centre_documents")
      .select("*")
      .order("updated_at", { ascending: false });
    if (error) {
      list.innerHTML = "<li>Error: " + error.message + "</li>";
      return;
    }
    if (!data.length) {
      list.innerHTML = "<li>No uploads yet.</li>";
      return;
    }
    const bucket = DocumentCentre.getServices().storageBucket || "centre-documents";
    list.innerHTML = data
      .map(function (row) {
        const url = DocumentCentre.publicUrl(c, row.storage_path);
        return (
          "<li><span><strong>" +
          row.title +
          "</strong> (" +
          row.category +
          ')</span><span><a href="' +
          url +
          '" target="_blank">View</a> · <button type="button" class="btn-admin btn-danger btn-sm" data-id="' +
          row.id +
          '" data-path="' +
          row.storage_path +
          '">Delete</button></span></li>"
        );
      })
      .join("");

    list.querySelectorAll("button[data-id]").forEach(function (btn) {
      btn.addEventListener("click", async function () {
        if (!confirm("Delete this document?")) return;
        const id = btn.getAttribute("data-id");
        const path = btn.getAttribute("data-path");
        await c.from("centre_documents").delete().eq("id", id);
        await c.storage.from(bucket).remove([path]);
        msg("Deleted.", "ok");
        loadAdminList();
      });
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();