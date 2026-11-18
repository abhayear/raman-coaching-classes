(function () {
  const base = window.SITE_BASE || "";

  async function refresh() {
    const mount = document.getElementById("my-courses-mount");
    const auth = document.getElementById("my-courses-auth");
    if (!mount) return;

    const session = await StudentAuth.getSession();
    if (!session) {
      mount.classList.add("hidden");
      auth?.classList.remove("hidden");
      return;
    }
    auth?.classList.add("hidden");
    mount.classList.remove("hidden");
    document.getElementById("my-email").textContent = session.user.email || "";

    try {
      const rows = await StudentAuth.myPurchases();
      if (!rows.length) {
        mount.innerHTML =
          '<p>No purchases yet. <a href="' +
          base +
          'courses.html">Browse courses</a> and pay with Razorpay using this same email.</p>';
        return;
      }
      mount.innerHTML =
        '<ul class="admin-list">' +
        rows
          .map(function (row) {
            const c = row.courses || {};
            return (
              "<li><span><strong>" +
              (c.title || "Course") +
              "</strong></span><button type=\"button\" class=\"btn-admin my-dl\" data-id=\"" +
              row.course_id +
              '" data-path="' +
              (c.pdf_storage_path || "") +
              '">Open PDF</button></li>'
            );
          })
          .join("") +
        "</ul>";
      mount.querySelectorAll(".my-dl").forEach(function (btn) {
        btn.addEventListener("click", function () {
          CoursesStore.downloadPdf(btn.getAttribute("data-id"), btn.getAttribute("data-path"));
        });
      });
    } catch (e) {
      mount.innerHTML = "<p class=\"doc-missing\">" + e.message + "</p>";
    }
  }

  document.getElementById("my-login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await StudentAuth.requireSignIn(
        document.getElementById("my-email-in").value.trim(),
        document.getElementById("my-pass-in").value
      );
      refresh();
    } catch (err) {
      alert(err.message);
    }
  });

  document.getElementById("my-signup")?.addEventListener("click", async () => {
    try {
      await StudentAuth.signUp(
        document.getElementById("my-email-in").value.trim(),
        document.getElementById("my-pass-in").value
      );
      alert("Account created. Sign in after email confirmation if required.");
    } catch (err) {
      alert(err.message);
    }
  });

  document.getElementById("my-logout")?.addEventListener("click", async () => {
    await StudentAuth.signOut();
    refresh();
  });

  document.addEventListener("DOMContentLoaded", refresh);
})();