(function () {
  const CATEGORIES = {
    syllabus: "Syllabus & curriculum",
    notices: "Notices & circulars",
    forms: "Forms & applications",
    papers: "Question papers & assignments",
    other: "Other documents",
  };

  function getServices() {
    return window.SITE_SERVICES || {};
  }

  function supabaseClient() {
    const s = getServices();
    if (!s.supabaseUrl || !s.supabaseAnonKey || !window.supabase) return null;
    return window.supabase.createClient(s.supabaseUrl, s.supabaseAnonKey);
  }

  function publicUrl(client, path) {
    const bucket = getServices().storageBucket || "centre-documents";
    const { data } = client.storage.from(bucket).getPublicUrl(path);
    return data.publicUrl;
  }

  function cardHtml(doc, href) {
    const title = (doc.title || "").replace(/</g, "&lt;");
    const desc = (doc.description || "").replace(/</g, "&lt;");
    const updated = doc.updated_at
      ? new Date(doc.updated_at).toLocaleDateString()
      : doc.updated || "";
    return (
      '<article class="doc-card" data-title="' +
      title.toLowerCase() +
      '">' +
      '<h3><a href="' +
      href +
      '" target="_blank" rel="noopener">' +
      title +
      "</a></h3>" +
      "<p>" +
      desc +
      "</p>" +
      '<p class="doc-meta">Updated ' +
      updated +
      ' · <a href="' +
      href +
      '" download>Download</a></p></article>'
    );
  }

  function bindSearch() {
    const input = document.getElementById("doc-search");
    if (!input) return;
    input.addEventListener("input", function () {
      const q = input.value.trim().toLowerCase();
      document.querySelectorAll(".doc-card").forEach(function (card) {
        const t = card.getAttribute("data-title") || "";
        card.style.display = !q || t.indexOf(q) !== -1 ? "" : "none";
      });
    });
  }

  async function loadDynamic() {
    const mount = document.getElementById("doc-dynamic");
    const countEl = document.getElementById("doc-count");
    if (!mount) return;
    const client = supabaseClient();
    if (!client) {
      mount.innerHTML =
        '<p class="doc-empty">Cloud document storage is not configured. Static files below still work.</p>';
      return;
    }
    const { data, error } = await client
      .from("centre_documents")
      .select("*")
      .order("updated_at", { ascending: false });
    if (error) {
      mount.innerHTML =
        '<p class="doc-missing">Could not load uploaded documents: ' +
        error.message +
        "</p>";
      return;
    }
    const byCat = {};
    (data || []).forEach(function (row) {
      const c = row.category || "other";
      if (!byCat[c]) byCat[c] = [];
      byCat[c].push(row);
    });
    let html = "";
    let total = (data || []).length;
    Object.keys(CATEGORIES).forEach(function (cid) {
      const rows = byCat[cid] || [];
      if (!rows.length) return;
      html += '<section class="doc-category" id="cloud-' + cid + '"><h2>' + CATEGORIES[cid] + " (uploads)</h2><div class=\"doc-list\">";
      rows.forEach(function (row) {
        html += cardHtml(row, publicUrl(client, row.storage_path));
      });
      html += "</div></section>";
    });
    if (!html) html = '<p class="doc-empty">No admin uploads yet.</p>';
    mount.innerHTML = html;
    if (countEl) {
      const staticN = parseInt(countEl.getAttribute("data-static") || "0", 10);
      countEl.textContent = String(staticN + total);
    }
    bindSearch();
  }

  window.DocumentCentre = {
    loadDynamic,
    supabaseClient,
    publicUrl,
    CATEGORIES,
    getServices,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadDynamic);
  } else {
    loadDynamic();
  }
})();