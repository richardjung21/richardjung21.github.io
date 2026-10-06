const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { runInNewContext } = require('node:vm');

function setup({wide = false, reduced = false, scrollY = 0, observerSupport = true,
  locale = 'en', layout = [['hero', 0, 800], ['publications', 800, 1800], ['contact', 1800, 3000]]} = {}) {
  function element() {
    const classes = new Set();
    return {
      hidden: false, attrs: {}, handlers: {}, focused: false, style: {}, textContent: '',
      classList: {
        add: key => classes.add(key),
        toggle: (key, on) => on ? classes.add(key) : classes.delete(key),
        contains: key => classes.has(key),
      },
      addEventListener(name, handler) { this.handlers[name] = handler; },
      setAttribute(name, value) { this.attrs[name] = value; },
      removeAttribute(name) { delete this.attrs[name]; },
      getAttribute(name) { return this.attrs[name]; },
      focus() { this.focused = true; },
    };
  }
  const navbar = element(), menu = element(), drawer = element();
  const indicator = element(), progress = element();
  navbar.getBoundingClientRect = () => ({bottom: 68});
  const window = element();
  window.innerHeight = 800;
  window.scrollY = scrollY;
  const ids = layout.map(([id]) => id);
  const sections = ids.map((id, i) => Object.assign(element(), {
    id, getBoundingClientRect: () => ({top: layout[i][1] - window.scrollY, bottom: layout[i][2] - window.scrollY}),
  }));
  const links = ids.map((id, i) => Object.assign(element(), {
    dataset: {section:id}, attrs: {href:'#'+id}, offsetTop:i*51, offsetHeight:45,
    textContent: ['Home','Research','Contact'][i],
  }));
  drawer.querySelectorAll = () => links;
  drawer.contains = target => links.includes(target);
  navbar.contains = target => [navbar, menu, drawer, ...links].includes(target);
  const document = element();
  document.documentElement = {scrollHeight:3000, lang:locale};
  window.location = {hash:"#publications"};
  const languageLink = element();
  languageLink.attrs.href = locale === "ko" ? "index.html" : "index.ko.html";
  document.querySelector = () => links.find(link => link.attrs["aria-current"] === "location");
  const nodes = {navbar, menuBtn:menu, navDrawer:drawer, navIndicator:indicator,
    readingProgress:progress,
    ...Object.fromEntries(sections.map(s => [s.id,s]))};
  document.getElementById = id => nodes[id];
  const desktop = Object.assign(element(), {matches:wide});
  const motion = Object.assign(element(), {matches:reduced});
  window.matchMedia = query => query.includes('reduced-motion') ? motion : desktop;
  const frames = [];
  window.requestAnimationFrame = callback => frames.push(callback);
  const reveal = element();
  const animations = [];
  reveal.animate = (keyframes, timing) => {
    const animation = {keyframes, timing, cancelled:false, cancel() { this.cancelled = true; this.oncancel?.(); }};
    animations.push(animation);
    return animation;
  };
  document.querySelectorAll = selector => selector === ".language-link" ? [languageLink] : [reveal];
  const observers = [];
  class Observer {
    constructor(callback) { this.callback = callback; this.observed = new Set(); observers.push(this); }
    observe(target) { this.observed.add(target); }
    unobserve(target) { this.observed.delete(target); }
  }
  if (observerSupport) window.IntersectionObserver = Observer;
  runInNewContext(readFileSync(join(__dirname, '..', 'script.js'), 'utf8'), {
    document, window, IntersectionObserver:Observer,
  });
  document.handlers.DOMContentLoaded();
  return {navbar, menu, drawer, links, sections, document, desktop, window, indicator, progress,
    frames, motion, reveal, animations, observers, languageLink,
    active() { return links.find(link => link.attrs['aria-current'] === 'location')?.dataset.section; },
    scroll(y) { window.scrollY = y; window.handlers.scroll(); this.flush(); },
    flush() { while (frames.length) frames.shift()(); }};
}

test('mobile menu and Escape preserve accessible state and focus', () => {
  const {menu, drawer, document} = setup();
  assert.equal(drawer.hidden, true);
  menu.handlers.click();
  assert.equal(drawer.hidden, false);
  assert.equal(menu.attrs['aria-expanded'], 'true');
  document.handlers.keydown({key:'Escape'});
  assert.equal(drawer.hidden, true);
  assert.equal(menu.focused, true);
});

test('section links close mobile navigation and focus the destination', () => {
  const {menu, drawer, links, sections} = setup();
  menu.handlers.click();
  links[1].handlers.click();
  assert.equal(drawer.hidden, true);
  assert.equal(sections[1].focused, true);
  assert.equal(sections[1].attrs.tabindex, '-1');
});

test('desktop sidebar stays visible; resizing closes mobile menu safely', () => {
  const {drawer, document, navbar, desktop, menu, links} = setup({wide:true});
  document.handlers.click({target:{}});
  navbar.handlers.focusout({relatedTarget:null});
  document.handlers.keydown({key:'Escape'});
  assert.equal(drawer.hidden, false);
  document.activeElement = links[0];
  desktop.matches = false;
  desktop.handlers.change({matches:false});
  assert.equal(drawer.hidden, true);
  assert.equal(menu.focused, true);
  desktop.matches = true;
  desktop.handlers.change({matches:true});
  assert.equal(drawer.hidden, false);
});

test('scrolling updates the active link, moving marker and progress', () => {
  const ui = setup({wide:true});
  assert.equal(ui.active(), 'hero');
  ui.window.scrollY = 1000;
  for (let i=0; i<10; i++) ui.window.handlers.scroll();
  assert.equal(ui.frames.length, 1);
  ui.flush();
  assert.equal(ui.active(), 'publications');
  assert.equal(ui.indicator.style.transform, 'translateY(51px)');
  assert.equal(ui.progress.style.transform, `scaleX(${1000/2200})`);
  assert.equal(ui.links.filter(link => link.attrs['aria-current']==='location').length, 1);
  assert.equal(ui.links[1].attrs['aria-current'], 'location');
  ui.window.scrollY = 2200;
  ui.window.handlers.scroll(); ui.flush();
  assert.equal(ui.active(), 'contact');
  assert.equal(ui.progress.style.transform, 'scaleX(1)');
  ui.window.scrollY = 0;
  ui.window.handlers.hashchange(); ui.flush();
  assert.equal(ui.active(), 'hero');
});

test('restored scroll positions and non-scrolling documents initialize correctly', () => {
  const restored = setup({scrollY:1000});
  assert.equal(restored.active(), 'publications');
  const short = setup();
  short.document.documentElement.scrollHeight = 700;
  short.window.handlers.resize(); short.flush();
  assert.equal(short.progress.style.transform, 'scaleX(0)');
  assert.equal(short.active(), 'hero');
});

test('reveals animate on entry and reduced motion cancels active animations', () => {
  const ui = setup();
  ui.observers[0].callback([{target:ui.reveal,isIntersecting:true,boundingClientRect:{top:400}}]);
  assert.equal(ui.animations.length, 1);
  assert.equal(ui.observers[0].observed.has(ui.reveal), false);
  ui.motion.matches = true;
  ui.motion.handlers.change({matches:true});
  assert.equal(ui.animations[0].cancelled, true);
  const reduced = setup({reduced:true});
  reduced.observers[0].callback([{target:reduced.reveal,isIntersecting:true,boundingClientRect:{top:400}}]);
  assert.equal(reduced.animations.length, 0);
  const fallback = setup({observerSupport:false});
  fallback.window.scrollY = 1000;
  fallback.window.handlers.scroll(); fallback.flush();
  assert.equal(fallback.active(), 'publications');
});


test('the mainly visible section wins independently of scroll direction', () => {
  const ui = setup({wide:true});
  ui.scroll(1);
  assert.equal(ui.active(), 'hero');
  ui.scroll(399);
  assert.equal(ui.active(), 'hero');
  ui.scroll(401);
  assert.equal(ui.active(), 'publications');
  ui.scroll(402);
  ui.scroll(401);
  assert.equal(ui.active(), 'publications');
  ui.scroll(399);
  assert.equal(ui.active(), 'hero');
  ui.window.handlers.resize(); ui.flush();
  assert.equal(ui.active(), 'hero');
});

const shortLayout = [
  ['hero', 0, 800], ['publications', 800, 2200],
  ['skills', 2200, 2350], ['contact', 2350, 3000],
];

test('Skills takes priority only after more than half of its height is visible', () => {
  const ui = setup({wide:true, layout:shortLayout});
  ui.scroll(1474);
  assert.equal(ui.active(), 'publications');
  ui.scroll(1475); // Exactly 75 of 150 pixels: not more than half.
  assert.equal(ui.active(), 'publications');
  ui.scroll(1476);
  assert.equal(ui.active(), 'skills');
  ui.scroll(1477);
  ui.scroll(1476);
  assert.equal(ui.active(), 'skills');
  ui.scroll(1475);
  assert.equal(ui.active(), 'publications');
});

test('Contact activates only at the absolute bottom and deactivates on scrolling up', () => {
  const ui = setup({wide:true, layout:shortLayout});
  ui.scroll(2100); // Contact occupies most of the viewport.
  assert.equal(ui.active(), 'skills');
  ui.scroll(2199.9);
  assert.equal(ui.active(), 'skills');
  ui.scroll(2200);
  assert.equal(ui.active(), 'contact');
  ui.scroll(2199.9);
  assert.equal(ui.active(), 'skills');

  // Even if only Contact is visible, keep the preceding tab until the bottom.
  const tallContact = setup({wide:true});
  tallContact.scroll(2100);
  assert.equal(tallContact.active(), 'publications');
  tallContact.scroll(2200);
  assert.equal(tallContact.active(), 'contact');
  tallContact.scroll(2199);
  assert.equal(tallContact.active(), 'publications');
  assert.equal(setup({wide:true, scrollY:2200}).active(), 'contact');
});

test('mobile majority measurements exclude content covered by the sticky header', () => {
  // Include another visible section to distinguish threshold from fallback.
  const overlap = setup({layout:[
    ['hero', 0, 800], ['publications', 800, 1600],
    ['skills', 1600, 1800], ['projects', 1800, 2800], ['contact', 2800, 3000],
  ]});
  overlap.scroll(1631); // 101 of 200 pixels below header.
  assert.equal(overlap.active(), 'skills');
  overlap.scroll(1632); // Exactly half; Projects occupies more visible space.
  assert.equal(overlap.active(), 'projects');
});


test('language switch preserves the visible section in both directions', () => {
  for (const locale of ['en', 'ko']) {
    const state = setup({locale, wide:true});
    state.scroll(1000);
    state.languageLink.handlers.click();
    assert.equal(state.languageLink.attrs.href, (locale === 'ko' ? 'index.html' : 'index.ko.html') + '#publications');
    state.scroll(0);
    state.languageLink.handlers.click();
    assert.equal(state.languageLink.attrs.href, (locale === 'ko' ? 'index.html' : 'index.ko.html') + '#hero');
  }
});

test('Korean mobile menu retains translated accessible labels', () => {
  const {menu} = setup({locale:'ko'});
  assert.equal(menu.attrs['aria-label'], '메뉴 열기');
  menu.handlers.click();
  assert.equal(menu.attrs['aria-label'], '메뉴 닫기');
  menu.handlers.click();
  assert.equal(menu.attrs['aria-label'], '메뉴 열기');
});
