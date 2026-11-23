/* Bright Chapter Realty — small enhancements. Every page still works without JavaScript. */
(function () {
  "use strict";
  var root = document.documentElement;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toast.t); toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }
  function money(n) { return isFinite(n) ? "$" + Math.round(n).toLocaleString("en-US") : "—"; }

  // ---- Menu ----
  var menuBtn = document.querySelector(".menu-btn"), nav = document.getElementById("site-nav");
  if (menuBtn && nav) menuBtn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.textContent = open ? "Close" : "Menu";
  });

  // ---- Text size ----
  var sizes = ["", "text-lg", "text-xl"], labels = ["Normal", "Large", "Extra large"];
  var sizeBtn = document.querySelector(".text-size-btn");
  if (sizeBtn) sizeBtn.addEventListener("click", function () {
    var i = 0; for (var j = 1; j < sizes.length; j++) if (root.classList.contains(sizes[j])) i = j;
    i = (i + 1) % sizes.length;
    sizes.forEach(function (c) { if (c) root.classList.remove(c); });
    if (sizes[i]) root.classList.add(sizes[i]);
    store("bcr-text-size", String(i));
    toast("Text size: " + labels[i]);
  });

  // ---- Share ----
  document.querySelectorAll("[data-share]").forEach(function (b) {
    b.addEventListener("click", function () {
      var data = { title: b.getAttribute("data-share"), url: location.href };
      if (navigator.share) { navigator.share(data).catch(function () {}); }
      else if (navigator.clipboard) { navigator.clipboard.writeText(data.url).then(function () { toast("Link copied"); }); }
      else { window.prompt("Copy this link:", data.url); }
    });
  });

  // ---- Listing filters ----
  var filters = document.querySelector("[data-filters]");
  if (filters) {
    var cards = Array.prototype.slice.call(document.querySelectorAll("[data-listings] .lcard"));
    var countEl = document.querySelector("[data-count]"), none = document.querySelector(".no-results");
    function fromHash() {
      var h = location.hash.replace("#", "");
      if (h === "single") filters.single.checked = true;
      if (h === "c55") filters.c55.checked = true;
      if (h === "condo") filters.type.value = "Condo";
    }
    fromHash();
    window.addEventListener("hashchange", function () { fromHash(); apply(); });
    function apply() {
      var max = +filters.price.value || Infinity, beds = +filters.beds.value || 0, type = filters.type.value;
      var shown = 0;
      cards.forEach(function (c) {
        var ok = +c.dataset.price <= max && +c.dataset.beds >= beds && (!type || c.dataset.type === type) &&
          (!filters.single.checked || c.dataset.single === "1") && (!filters.c55.checked || c.dataset["55"] === "1") &&
          (!filters.active.checked || c.dataset.status !== "Sold");
        c.hidden = !ok; if (ok) shown++;
      });
      if (countEl) countEl.textContent = shown + (shown === 1 ? " home" : " homes");
      if (none) none.hidden = shown !== 0;
    }
    filters.addEventListener("change", apply);
    apply();
  }

  // ---- Mortgage maths ----
  function payment(loan, ratePct, years) {
    var r = ratePct / 100 / 12, n = years * 12;
    if (loan <= 0) return 0;
    if (r === 0) return loan / n;
    return loan * r / (1 - Math.pow(1 + r, -n));
  }
  document.querySelectorAll("[data-calc]").forEach(function (box) {
    var price = +box.dataset.price, out = box.querySelector("[data-out]");
    function run() {
      var down = +box.querySelector("[name=down]").value || 0, rate = +box.querySelector("[name=rate]").value || 0;
      var term = +box.querySelector("[name=term]").value || 30;
      out.textContent = money(payment(price * (1 - down / 100), rate, term)) + " per month";
    }
    box.addEventListener("input", run); box.addEventListener("change", run); run();
  });
  var full = document.querySelector("[data-full-calc]");
  if (full) {
    var f = function (n) { return +full.querySelector("[name=" + n + "]").value || 0; };
    var o = function (k) { return full.querySelector('[data-o="' + k + '"]'); };
    var runFull = function () {
      var loan = f("price") * (1 - f("down") / 100);
      var pi = payment(loan, f("rate"), f("term") || 30);
      var extra = f("tax") / 12 + f("ins") / 12 + f("hoa");
      o("loan").textContent = money(loan); o("pi").textContent = money(pi);
      o("extra").textContent = money(extra); o("total").textContent = money(pi + extra);
    };
    full.addEventListener("input", runFull); full.addEventListener("change", runFull); runFull();
  }

  // ---- Forms: post to the form service if set, otherwise open the visitor's email app ----
  document.querySelectorAll("[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var note = form.querySelector(".form-note");
      if (form.getAttribute("action") && form.getAttribute("action") !== "#") {
        e.preventDefault();
        fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
          .then(function (r) { if (!r.ok) throw 0; form.reset(); note.textContent = "Thank you! Your message was sent. We will be in touch soon."; note.hidden = false; })
          .catch(function () { note.textContent = "Sorry, something went wrong. Please call or email us instead."; note.hidden = false; });
        return;
      }
      e.preventDefault();
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.name.charAt(0) === "_" || el.type === "checkbox" || !el.value) return;
        var label = form.querySelector('label[for="' + el.id + '"]');
        lines.push((label ? label.textContent.replace(/\(optional\)/, "").trim() : el.name) + ": " + el.value);
      });
      location.href = "mailto:" + form.dataset.email + "?subject=" + encodeURIComponent(form.dataset.subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      note.textContent = "Your email app should open with your message ready to send. If it does not, please email " + form.dataset.email + ".";
      note.hidden = false;
    });
  });
})();
