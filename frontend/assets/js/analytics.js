/* Onda cookieless analytics. No cookies, no persistent id, no PII.
   Session id lives in sessionStorage (cleared on tab close). Safe to fail. */
(function () {
  "use strict";
  try {
    var ENDPOINT = "/api/track";

    function sid() {
      try {
        var k = "onda_sid", v = sessionStorage.getItem(k);
        if (!v) {
          v = (crypto && crypto.randomUUID)
            ? crypto.randomUUID()
            : "s-" + Date.now() + "-" + Math.random().toString(16).slice(2);
          sessionStorage.setItem(k, v);
        }
        return v;
      } catch (e) { return "nostore"; }
    }

    var SESSION = sid();
    var LANG = (document.documentElement.getAttribute("lang") || "").slice(0, 8);

    function send(type, extra) {
      try {
        var body = JSON.stringify(Object.assign({
          event_type: type,
          session_id: SESSION,
          page: location.pathname,
          lang: LANG,
          referrer: document.referrer || ""
        }, extra || {}));
        if (navigator.sendBeacon) {
          navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
        } else {
          fetch(ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body, keepalive: true
          });
        }
      } catch (e) { /* analytics must never break the page */ }
    }

    /* pageview */
    send("pageview");

    /* scroll depth: 25/50/75/100 once each */
    var marks = [25, 50, 75, 100], hit = {};
    function onScroll() {
      var de = document.documentElement;
      var max = (de.scrollHeight - de.clientHeight);
      var pct = max > 0 ? Math.round((window.scrollY || de.scrollTop) / max * 100) : 100;
      for (var i = 0; i < marks.length; i++) {
        var m = marks[i];
        if (pct >= m && !hit[m]) { hit[m] = 1; send("scroll", { scroll_depth: m }); }
      }
      if (hit[100]) window.removeEventListener("scroll", throttled);
    }
    var tmr = null;
    function throttled() {
      if (tmr) return;
      tmr = setTimeout(function () { tmr = null; onScroll(); }, 400);
    }
    window.addEventListener("scroll", throttled, { passive: true });

    /* delegated clicks: CTA to contact + navigation to work pages */
    document.addEventListener("click", function (e) {
      var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("#contact") !== -1) {
        send("cta_click", { meta: { href: href } });
      } else if (/(?:^|\/)(portfolio|process)(_es|_ka)?\.html/.test(href)
                 || /(?:^|\/)examples\//.test(href)) {
        send("nav_click", { meta: { href: href } });
      }
    }, true);

    /* contact form became visible */
    var contact = document.getElementById("contact");
    if (contact && "IntersectionObserver" in window) {
      var seen = false;
      var io = new IntersectionObserver(function (ents) {
        if (!seen && ents[0] && ents[0].isIntersecting) {
          seen = true; send("form_view"); io.disconnect();
        }
      }, { threshold: 0.3 });
      io.observe(contact);
    }

    /* successful lead (dispatched by the page's existing submit handler) */
    document.addEventListener("onda:lead", function () { send("form_submit"); });
  } catch (e) { /* never throw */ }
})();
