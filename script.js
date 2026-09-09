document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('navbar');
  const menuBtn = document.getElementById('menuBtn');
  const navDrawer = document.getElementById('navDrawer');
  if (!navbar || !menuBtn || !navDrawer) return;

  const desktop = window.matchMedia('(min-width: 801px)');
  let scheduleUpdate = () => {};
  function setMenu(open) {
    navDrawer.hidden = !open;
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    scheduleUpdate();
  }
  function closeMobileMenu() {
    if (!desktop.matches) setMenu(false);
  }
  menuBtn.addEventListener('click', () => setMenu(navDrawer.hidden));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !desktop.matches && !navDrawer.hidden) {
      setMenu(false);
      menuBtn.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!navbar.contains(event.target)) closeMobileMenu();
  });
  navbar.addEventListener('focusout', event => {
    if (!navbar.contains(event.relatedTarget)) closeMobileMenu();
  });
  navDrawer.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.getElementById(link.getAttribute('href').slice(1));
      if (!desktop.matches) {
        setMenu(false);
      }
      if (target) {
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }
      // Native anchors handle scrolling and browser history; never intercept wheel/touch.
    });
  });
  desktop.addEventListener('change', event => {
    if (!event.matches && navDrawer.contains(document.activeElement)) menuBtn.focus();
    setMenu(event.matches);
  });
  setMenu(desktop.matches);
  navbar.classList.add('nav-ready');

  const links = Array.from(navDrawer.querySelectorAll('a[data-section]'));
  const sections = links.map(link => document.getElementById(link.dataset.section));
  const indicator = document.getElementById('navIndicator');
  const progress = document.getElementById('readingProgress');
  if (!links.length || sections.some(section => !section)) return;
  let framePending = false;
  let activeIndex = -1;

  function updatePosition() {
    framePending = false;
    const maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const fraction = maxScroll ? Math.max(0, Math.min(1, window.scrollY / maxScroll)) : 0;
    const scrollY = Math.max(0, Math.min(maxScroll, window.scrollY));
    // Measure unobscured content, independently of scroll direction.
    const viewportTop = desktop.matches ? 0 : Math.max(0, navbar.getBoundingClientRect().bottom);
    const viewportHeight = Math.max(0, window.innerHeight - viewportTop);
    const contactIndex = sections.findIndex(section => section.id === 'contact');
    const candidates = sections.map((section, index) => {
      const rect = section.getBoundingClientRect();
      const height = rect.bottom - rect.top;
      const visible = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, viewportTop));
      return { index, visible, shortMajority: height > 0 && height <= viewportHeight && visible > height / 2 };
    }).filter(section => section.index !== contactIndex);
    // Give a majority-visible short section priority so Skills is not crowded
    // out by a taller neighbor. Otherwise use the most visible section in pixels.
    const shortSections = candidates.filter(section => section.shortMajority);
    const pool = shortSections.length ? shortSections : candidates;
    const best = pool.reduce((winner, section) => !winner || section.visible > winner.visible ? section : winner, null);
    let nextIndex = best && best.visible > 0 ? best.index : (candidates[candidates.length - 1]?.index ?? 0);
    if (scrollY === 0) nextIndex = 0;
    if (maxScroll > 0 && scrollY >= maxScroll && contactIndex >= 0) nextIndex = contactIndex;
    if (nextIndex !== activeIndex) {
      activeIndex = nextIndex;
      links.forEach((link, index) => {
        link.classList.toggle('active', index === activeIndex);
        if (index === activeIndex) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
    if (indicator && !navDrawer.hidden) {
      indicator.style.transform = `translateY(${links[activeIndex].offsetTop}px)`;
      indicator.style.height = `${links[activeIndex].offsetHeight}px`;
    }
    if (progress) progress.style.transform = `scaleX(${fraction})`;
  }
  scheduleUpdate = () => {
    if (!framePending) {
      framePending = true;
      window.requestAnimationFrame(updatePosition);
    }
  };
  updatePosition();
  navbar.classList.add('scroll-ready');
  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  window.addEventListener('hashchange', scheduleUpdate);
  window.addEventListener('load', scheduleUpdate);
  if (document.fonts) document.fonts.ready.then(scheduleUpdate);
  if ('ResizeObserver' in window) {
    const resizeObserver = new ResizeObserver(scheduleUpdate);
    resizeObserver.observe(document.getElementById('main'));
    resizeObserver.observe(navbar);
  }

  // Animate only when entering the viewport. Content is never hidden by CSS,
  // so unsupported APIs, disabled JavaScript, and direct links stay readable.
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  motion.addEventListener('change', event => {
    if (event.matches) {
      animations.forEach(animation => animation.cancel());
      animations.clear();
    }
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        if (motion.matches || !entry.target.animate || entry.boundingClientRect.top < 0) return;
        const animation = entry.target.animate(
          [{ opacity: 0.45, transform: 'translateY(14px)' }, { opacity: 1, transform: 'translateY(0)' }],
          { duration: 480, easing: 'cubic-bezier(.22,1,.36,1)' }
        );
        animations.add(animation);
        animation.onfinish = () => animations.delete(animation);
        animation.oncancel = () => animations.delete(animation);
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('.section-heading, .pub-card, .project-card, .timeline-item').forEach(item => observer.observe(item));
  }
});
