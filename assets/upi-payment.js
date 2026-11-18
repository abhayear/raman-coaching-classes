/** UPI QR + deep link (no payment gateway fee). */
(function () {
  function payments() {
    return window.SITE_PAYMENTS || {};
  }

  function upiUri(amountInr, courseTitle) {
    const p = payments();
    const pa = (p.upiId || "").trim();
    const pn = encodeURIComponent(p.payeeName || "Raman Coaching");
    const am = Number(amountInr).toFixed(2);
    const tn = encodeURIComponent(
      (courseTitle || "Course") + " — " + (p.note || "").slice(0, 80)
    );
    return "upi://pay?pa=" + encodeURIComponent(pa) + "&pn=" + pn + "&am=" + am + "&cu=INR&tn=" + tn;
  }

  function qrUrl(upi) {
    return (
      "https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=" + encodeURIComponent(upi)
    );
  }

  function ensureModal() {
    let el = document.getElementById("upi-pay-modal");
    if (el) return el;
    el = document.createElement("div");
    el.id = "upi-pay-modal";
    el.className = "upi-modal hidden";
    el.innerHTML =
      '<div class="upi-modal-backdrop"></div><div class="upi-modal-box" role="dialog">' +
      '<button type="button" class="upi-close" aria-label="Close">&times;</button>' +
      '<div id="upi-modal-body"></div></div>';
    document.body.appendChild(el);
    el.querySelector(".upi-close").onclick = () => el.classList.add("hidden");
    el.querySelector(".upi-modal-backdrop").onclick = () => el.classList.add("hidden");
    return el;
  }

  function showUpiModal(course) {
    const p = payments();
    if (!p.upiId) {
      alert("UPI not configured. Staff: edit config/payments.json and rebuild.");
      return;
    }
    const uri = upiUri(course.price_inr, course.title);
    const modal = ensureModal();
    const body = modal.querySelector("#upi-modal-body");
    const steps = (p.instructions || [])
      .map((s, i) => "<li>" + s + "</li>")
      .join("");
    body.innerHTML =
      "<h2>Pay via UPI (no gateway fee)</h2>" +
      "<p><strong>" +
      course.title +
      "</strong> · Amount: <strong>₹" +
      Number(course.price_inr).toLocaleString("en-IN") +
      "</strong></p>" +
      '<img src="' +
      qrUrl(uri) +
      '" alt="UPI QR code" width="220" height="220"/>' +
      "<p>UPI ID: <code id=\"upi-id-copy\">" +
      p.upiId +
      '</code> <button type="button" class="btn-admin" id="copy-upi">Copy</button></p>' +
      "<p><a class=\"btn btn-primary\" href=\"" +
      uri +
      '">Open in UPI app</a></p>' +
      "<ol>" +
      steps +
      "</ol>" +
      '<form id="upi-paid-form" class="admin-form">' +
      '<input type="hidden" id="upi-course-id" value="' +
      course.id +
      '"/>' +
      '<input type="hidden" id="upi-amount" value="' +
      course.price_inr +
      '"/>' +
      '<label>12-digit UTR / transaction ID</label>' +
      '<input type="text" id="upi-utr" required minlength="6" maxlength="32" placeholder="From PhonePe/GPay/Paytm receipt"/>' +
      "<label>Note (optional)</label>" +
      '<textarea id="upi-student-note" rows="2"></textarea>' +
      '<button type="submit" class="btn-admin">I have paid — submit for approval</button>' +
      "</form>" +
      "<p class=\"login-hint\">" +
      (p.gstDisclaimer || "") +
      "</p>";
    modal.classList.remove("hidden");
    document.getElementById("copy-upi")?.addEventListener("click", () => {
      navigator.clipboard.writeText(p.upiId);
      alert("UPI ID copied");
    });
    document.getElementById("upi-paid-form")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (window.CoursesStore && CoursesStore.submitUpiPayment) {
        await CoursesStore.submitUpiPayment();
        modal.classList.add("hidden");
      }
    });
  }

  window.UpiPayment = { showUpiModal, upiUri, payments };
})();