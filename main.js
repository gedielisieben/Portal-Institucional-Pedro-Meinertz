// ═══════════════════════════════════════════════════════════════════════════
//  Portal Escola Pedro Meinerz — main.js
// ═══════════════════════════════════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", () => {

  // ── Navbar scroll ──────────────────────────────────────────────────────
  const navbar = document.getElementById("navbar");
  const onScroll = () => {
    navbar.classList.toggle("scrolled", window.scrollY > 40);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ── Mobile nav toggle ──────────────────────────────────────────────────
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks  = document.querySelector(".nav-links");
  navToggle?.addEventListener("click", () => {
    navLinks.classList.toggle("open");
    const isOpen = navLinks.classList.contains("open");
    navToggle.setAttribute("aria-expanded", isOpen);
  });

  // Close nav when link is clicked
  navLinks?.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", () => navLinks.classList.remove("open"));
  });

  // ── Active nav on scroll ───────────────────────────────────────────────
  const sections = document.querySelectorAll("section[id]");
  const navAnchors = document.querySelectorAll(".nav-links a[href^='#']");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navAnchors.forEach(a => {
          a.classList.toggle("active", a.getAttribute("href") === `#${entry.target.id}`);
        });
      }
    });
  }, { rootMargin: "-40% 0px -55% 0px" });

  sections.forEach(s => observer.observe(s));

  // ── Scroll reveal ──────────────────────────────────────────────────────
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add("visible"), i * 80);
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll(".reveal").forEach(el => revealObs.observe(el));

  // ── Counter animation ──────────────────────────────────────────────────
  const counters = document.querySelectorAll("[data-count]");
  const countObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || "";
      const dur    = 1800;
      const step   = 16;
      const inc    = target / (dur / step);
      let cur = 0;
      const timer = setInterval(() => {
        cur += inc;
        if (cur >= target) { cur = target; clearInterval(timer); }
        el.textContent = Math.floor(cur) + suffix;
      }, step);
      countObs.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(c => countObs.observe(c));

  // ── Formulário de contato ──────────────────────────────────────────────
  const form     = document.getElementById("form-contato");
  const sucesso  = document.getElementById("form-sucesso");
  const toast    = document.getElementById("toast");

  const showToast = (msg, cor = "#2D7A4F") => {
    toast.textContent = msg;
    toast.style.background = cor;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3500);
  };

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = form.querySelector(".btn-enviar");
    btn.textContent = "Enviando…";
    btn.disabled = true;

    const payload = {
      nome:    form.nome.value,
      email:   form.email.value,
      assunto: form.assunto.value,
      mensagem: form.mensagem.value,
    };

    try {
      const res  = await fetch("/api/contato", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      form.reset();
      if (sucesso) { sucesso.style.display = "block"; }
      showToast("✅ " + data.mensagem);
    } catch {
      showToast("❌ Erro ao enviar. Tente novamente.", "#c0392b");
    } finally {
      btn.textContent = "Enviar Mensagem";
      btn.disabled = false;
    }
  });

  // ── Galeria: feedback visual de clique ────────────────────────────────
  document.querySelectorAll(".galeria-item").forEach(item => {
    item.addEventListener("click", () => {
      showToast("📷 Galeria completa em breve!");
    });
  });

  // ── Docs: feedback ────────────────────────────────────────────────────
  document.querySelectorAll(".doc-card").forEach(card => {
    card.addEventListener("click", () => {
      showToast("📄 Documento disponível em breve!");
    });
  });

});