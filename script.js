document.addEventListener('DOMContentLoaded', () => {
  const navbar   = document.getElementById('navbar');
  const menuBtn  = document.getElementById('menuBtn');
  const navDrawer = document.getElementById('navDrawer');
  const navLinks = document.querySelectorAll('.nav-links a');
  const sections = document.querySelectorAll('section[id]');

  if (!navbar) return;

  // ── Navbar scroll style ────────────────────────────
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  // ── Mobile drawer ──────────────────────────────────
  menuBtn?.addEventListener('click', () => {
    const isOpen = navDrawer.classList.toggle('open');
    menuBtn.classList.toggle('open', isOpen);
    menuBtn.setAttribute('aria-expanded', String(isOpen));
  });

  // Close drawer when clicking outside
  document.addEventListener('click', e => {
    if (
      navDrawer?.classList.contains('open') &&
      !navbar.contains(e.target)
    ) {
      navDrawer.classList.remove('open');
      menuBtn?.classList.remove('open');
      menuBtn?.setAttribute('aria-expanded', 'false');
    }
  });

  // ── Smooth scroll (all internal anchors) ──────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const offset = navbar.offsetHeight;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
      // Close mobile drawer
      navDrawer?.classList.remove('open');
      menuBtn?.classList.remove('open');
      menuBtn?.setAttribute('aria-expanded', 'false');
    });
  });

  // ── Scroll spy ─────────────────────────────────────
  const spyObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const id = entry.target.id;
      navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.section === id);
      });
    });
  }, { rootMargin: '-40% 0px -50% 0px', threshold: 0 });

  sections.forEach(s => spyObserver.observe(s));

  // ── Scroll reveal ──────────────────────────────────
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { rootMargin: '0px 0px -60px 0px', threshold: 0.05 });

  document.querySelectorAll('.reveal-section').forEach(el => {
    revealObserver.observe(el);
  });

  // Stagger child reveal items
  document.querySelectorAll('.reveal-section').forEach(section => {
    section.querySelectorAll('.reveal-item').forEach((item, i) => {
      item.style.transitionDelay = `${0.1 + i * 0.08}s`;
      revealObserver.observe(item);
    });
  });
});
