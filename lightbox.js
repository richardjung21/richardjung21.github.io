// Lightbox2 retains its upstream appearance and animation timings.
document.addEventListener('DOMContentLoaded', () => {
  if (!window.lightbox) return;
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  function configure() {
    window.lightbox.option({
      fadeDuration: motion.matches ? 0 : 600,
      imageFadeDuration: motion.matches ? 0 : 600,
      resizeDuration: motion.matches ? 0 : 700,
      disableScrolling: true,
      sanitizeTitle: true
    });
    // Includes the library's caption animation, which uses jQuery's fast preset.
    window.jQuery.fx.off = motion.matches;
  }
  configure();
  motion.addEventListener('change', configure);
  document.querySelectorAll('.paper-full-image').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      // Open this figure's individual lightbox from either trigger.
      link.closest('figure').querySelector('[data-lightbox]').click();
    });
  });
});
