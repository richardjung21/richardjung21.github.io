# Portfolio Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page dark terminal-themed portfolio site for Seungho Jung hosted on GitHub Pages.

**Architecture:** Pure HTML/CSS/JS — no framework, no build step. A fixed sidebar handles navigation; the right panel scrolls through sections. JavaScript handles scroll spy and smooth scroll. Mobile view collapses the sidebar into a hamburger menu.

**Tech Stack:** HTML5, CSS3 (custom properties, flexbox, CSS Grid), Vanilla JS (IntersectionObserver API)

---

## File Map

| File | Responsibility |
|---|---|
| `index.html` | All page markup — sidebar + all content sections |
| `style.css` | All styles — theme variables, layout, sections, responsive |
| `script.js` | Scroll spy (IntersectionObserver), smooth scroll, mobile menu toggle |
| `assets/profile.jpg` | Profile photo (user supplies) |

---

## Task 1: Project Scaffold

**Files:**
- Create: `index.html`
- Create: `style.css`
- Create: `script.js`
- Create: `assets/` directory

- [ ] **Step 1: Create `assets/` directory**

```bash
mkdir -p assets
```

- [ ] **Step 2: Create `index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Seungho Jung</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <button class="hamburger" id="hamburger" aria-label="Toggle navigation">
    <span></span><span></span><span></span>
  </button>

  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <!-- populated in Task 2 -->
    </aside>
    <main class="content" id="content">
      <!-- populated in Tasks 3–9 -->
    </main>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

- [ ] **Step 3: Create `style.css` with CSS custom properties and reset**

```css
/* ── Variables ─────────────────────────────────────── */
:root {
  --bg:         #0d0d0d;
  --bg-sidebar: #111111;
  --border:     #1e1e1e;
  --accent:     #00ff88;
  --accent-dim: rgba(0, 255, 136, 0.08);
  --accent-mid: rgba(0, 255, 136, 0.25);
  --text:       #ffffff;
  --text-sec:   #aaaaaa;
  --text-muted: #555555;
  --font:       'Courier New', Courier, monospace;
  --sidebar-w:  220px;
}

/* ── Reset ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 14px;
  line-height: 1.6;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ── Layout ─────────────────────────────────────────── */
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: var(--sidebar-w);
  flex-shrink: 0;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 28px 18px;
  gap: 4px;
  z-index: 100;
}

.content {
  margin-left: var(--sidebar-w);
  flex: 1;
  padding: 48px 52px;
  max-width: 860px;
}

/* ── Hamburger (hidden on desktop) ─────────────────── */
.hamburger {
  display: none;
  position: fixed;
  top: 14px;
  left: 14px;
  z-index: 200;
  background: var(--bg-sidebar);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
  flex-direction: column;
  gap: 4px;
}
.hamburger span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--accent);
  border-radius: 2px;
  transition: transform 0.2s, opacity 0.2s;
}
.hamburger.open span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; }
.hamburger.open span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }

/* ── Mobile ─────────────────────────────────────────── */
@media (max-width: 768px) {
  .hamburger { display: flex; }
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.25s ease;
  }
  .sidebar.open { transform: translateX(0); }
  .content {
    margin-left: 0;
    padding: 64px 20px 32px;
  }
}
```

- [ ] **Step 4: Create `script.js` (empty shell for now)**

```js
// script.js — filled in Task 10
document.addEventListener('DOMContentLoaded', () => {});
```

- [ ] **Step 5: Open `index.html` in a browser and verify a black page loads with no console errors**

Open: `index.html` in your browser (or `python3 -m http.server 8080` and visit `http://localhost:8080`)

- [ ] **Step 6: Commit**

```bash
git add index.html style.css script.js assets/
git commit -m "feat: project scaffold with layout and CSS variables"
```

---

## Task 2: Sidebar

**Files:**
- Modify: `index.html` — fill in `<aside class="sidebar">`
- Modify: `style.css` — add sidebar styles

- [ ] **Step 1: Replace the `<aside class="sidebar">` comment in `index.html`**

```html
<aside class="sidebar" id="sidebar">
  <!-- Profile -->
  <div class="sidebar-profile">
    <img src="assets/profile.jpg" alt="Seungho Jung" class="profile-photo" onerror="this.style.display='none'">
    <div class="profile-name">Seungho Jung</div>
    <div class="profile-title">ML Researcher &amp; Engineer</div>
  </div>

  <!-- Nav -->
  <div class="sidebar-label">NAVIGATE</div>
  <nav class="sidebar-nav">
    <a href="#about"        class="nav-link active" data-section="about"       >&gt; about</a>
    <a href="#skills"       class="nav-link"        data-section="skills"      >$ skills</a>
    <a href="#experience"   class="nav-link"        data-section="experience"  >$ experience</a>
    <a href="#publications" class="nav-link"        data-section="publications">$ publications</a>
    <a href="#projects"     class="nav-link"        data-section="projects"    >$ projects</a>
    <a href="#contact"      class="nav-link"        data-section="contact"     >$ contact</a>
  </nav>

  <!-- Social links -->
  <div class="sidebar-links">
    <div class="sidebar-label">LINKS</div>
    <a href="https://github.com/richardjung21" target="_blank" rel="noopener" class="social-link">⟶ GitHub</a>
    <a href="https://linkedin.com/in/YOUR-LINKEDIN" target="_blank" rel="noopener" class="social-link">⟶ LinkedIn</a>
    <a href="mailto:richardjung@g.skku.edu" class="social-link">⟶ Email</a>
  </div>
</aside>
```

- [ ] **Step 2: Add sidebar styles to `style.css`**

```css
/* ── Sidebar internals ──────────────────────────────── */
.sidebar-profile {
  text-align: center;
  margin-bottom: 24px;
}
.profile-photo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  object-fit: cover;
  display: block;
  margin: 0 auto 10px;
}
.profile-name {
  color: var(--text);
  font-size: 13px;
  font-weight: 700;
}
.profile-title {
  color: var(--accent);
  font-size: 10px;
  margin-top: 3px;
  letter-spacing: 0.5px;
}

.sidebar-label {
  color: var(--text-muted);
  font-size: 9px;
  letter-spacing: 2px;
  margin: 12px 0 6px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-link {
  color: var(--text-muted);
  font-size: 11px;
  padding: 6px 10px;
  border-radius: 3px;
  border-left: 2px solid transparent;
  transition: color 0.15s, background 0.15s;
}
.nav-link:hover { color: var(--text-sec); text-decoration: none; }
.nav-link.active {
  color: var(--accent);
  background: var(--accent-dim);
  border-left-color: var(--accent);
}

.sidebar-links {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.social-link {
  color: var(--accent);
  font-size: 11px;
}
.social-link:hover { text-decoration: underline; }
```

- [ ] **Step 3: Verify in browser — sidebar should appear on the left with profile area and nav links**

Expected: dark sidebar visible, "SJ" initials area if no photo yet, green nav links, social links at bottom.

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: sidebar with nav links and social links"
```

---

## Task 3: About Section

**Files:**
- Modify: `index.html` — add `#about` section inside `<main>`
- Modify: `style.css` — add section base styles + about styles

- [ ] **Step 1: Add section base styles to `style.css`**

```css
/* ── Section base ───────────────────────────────────── */
.section {
  margin-bottom: 60px;
  scroll-margin-top: 32px;
}
.section-header {
  color: var(--text-muted);
  font-size: 10px;
  letter-spacing: 3px;
  margin-bottom: 20px;
}
```

- [ ] **Step 2: Add the `#about` section inside `<main class="content">` in `index.html`**

```html
<main class="content" id="content">

  <!-- ABOUT -->
  <section id="about" class="section">
    <div class="section-header">// ABOUT</div>
    <div class="about-grid">
      <div class="about-text">
        <h1 class="about-name">Seungho Jung</h1>
        <p class="about-subtitle">MS Candidate · ECE · Sungkyunkwan University</p>
        <p class="about-bio">
          Graduate researcher specializing in Generative Models (Diffusion Models),
          Computer Vision, and Medical Image Analysis. Currently a Graduate Researcher
          at Crescom and a freelance web developer. 2 published papers with a 3rd on
          the way. Native English and Korean speaker.
        </p>
        <div class="about-meta">
          <div class="about-meta-group">
            <span class="meta-label">Education</span>
            <span class="meta-value">SKKU MS ECE &nbsp;·&nbsp; 2025–present &nbsp;·&nbsp; GPA 4.33/4.5</span>
            <span class="meta-value">SKKU BS EE &nbsp;·&nbsp; 2019–2025 &nbsp;·&nbsp; GPA 3.46/4.5</span>
          </div>
          <div class="about-meta-group">
            <span class="meta-label">Languages</span>
            <span class="meta-value">English (Fluent) &nbsp;·&nbsp; Korean (Fluent)</span>
            <span class="meta-value">Mandarin Chinese (Conversational) &nbsp;·&nbsp; Tagalog (Conversational)</span>
          </div>
        </div>
      </div>
      <img src="assets/profile.jpg" alt="Seungho Jung" class="about-photo" onerror="this.style.display='none'">
    </div>
  </section>

</main>
```

- [ ] **Step 3: Add about styles to `style.css`**

```css
/* ── About ──────────────────────────────────────────── */
.about-grid {
  display: flex;
  gap: 28px;
  align-items: flex-start;
}
.about-text { flex: 1; }
.about-photo {
  width: 100px;
  height: 100px;
  border-radius: 8px;
  border: 1px solid var(--border);
  object-fit: cover;
  flex-shrink: 0;
}
.about-name {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}
.about-subtitle {
  color: var(--accent);
  font-size: 12px;
  margin-bottom: 14px;
}
.about-bio {
  color: var(--text-sec);
  font-size: 13px;
  line-height: 1.8;
  margin-bottom: 20px;
}
.about-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.about-meta-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.meta-label {
  color: var(--text-muted);
  font-size: 9px;
  letter-spacing: 2px;
  margin-bottom: 4px;
}
.meta-value {
  color: var(--text-sec);
  font-size: 11px;
}
```

- [ ] **Step 4: Verify in browser — about section should show name, subtitle, bio, education, and languages**

- [ ] **Step 5: Commit**

```bash
git add index.html style.css
git commit -m "feat: about section with bio, education, and languages"
```

---

## Task 4: Skills Section

**Files:**
- Modify: `index.html` — add `#skills` section
- Modify: `style.css` — add skills styles

- [ ] **Step 1: Add `#skills` section after `#about` in `index.html`**

```html
  <!-- SKILLS -->
  <section id="skills" class="section">
    <div class="section-header">// SKILLS</div>
    <div class="skills-groups">
      <div class="skills-group">
        <div class="skills-group-label">Languages</div>
        <div class="skills-tags">
          <span class="tag">Python</span>
          <span class="tag">C++</span>
          <span class="tag">Java</span>
          <span class="tag">JavaScript</span>
        </div>
      </div>
      <div class="skills-group">
        <div class="skills-group-label">ML / AI</div>
        <div class="skills-tags">
          <span class="tag">PyTorch</span>
          <span class="tag">OpenCV</span>
          <span class="tag">Diffusion Models</span>
          <span class="tag">SAM</span>
        </div>
      </div>
      <div class="skills-group">
        <div class="skills-group-label">Web</div>
        <div class="skills-tags">
          <span class="tag">Node.js</span>
          <span class="tag">Express</span>
          <span class="tag">React</span>
        </div>
      </div>
      <div class="skills-group">
        <div class="skills-group-label">Tools</div>
        <div class="skills-tags">
          <span class="tag">Git</span>
          <span class="tag">Linux</span>
          <span class="tag">Arduino</span>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 2: Add skills styles to `style.css`**

```css
/* ── Skills ─────────────────────────────────────────── */
.skills-groups {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.skills-group-label {
  color: var(--text-muted);
  font-size: 9px;
  letter-spacing: 2px;
  margin-bottom: 8px;
}
.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.tag {
  background: var(--accent-dim);
  color: var(--accent);
  border: 1px solid var(--accent-mid);
  padding: 4px 12px;
  border-radius: 3px;
  font-size: 11px;
}
```

- [ ] **Step 3: Verify in browser — skill pills should appear grouped by category in green**

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: skills section with categorized tags"
```

---

## Task 5: Experience Section

**Files:**
- Modify: `index.html` — add `#experience` section
- Modify: `style.css` — add experience styles

- [ ] **Step 1: Add `#experience` section after `#skills` in `index.html`**

```html
  <!-- EXPERIENCE -->
  <section id="experience" class="section">
    <div class="section-header">// EXPERIENCE</div>
    <div class="timeline">

      <div class="timeline-item">
        <div class="timeline-meta">
          <span class="timeline-date">2025 – present</span>
          <span class="timeline-badge current">current</span>
        </div>
        <div class="timeline-body">
          <div class="timeline-title">Graduate Researcher</div>
          <div class="timeline-org">Crescom</div>
          <p class="timeline-desc">Research on Generative Models and Computer Vision at a startup. Focus on practical applications of diffusion models and image analysis.</p>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-meta">
          <span class="timeline-date">Freelance</span>
        </div>
        <div class="timeline-body">
          <div class="timeline-title">Freelance Developer</div>
          <div class="timeline-org">Waterbe</div>
          <p class="timeline-desc">Frontend and backend web development. Contributed across the full stack.</p>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-meta">
          <span class="timeline-date">2024.02 – 2025.02</span>
        </div>
        <div class="timeline-body">
          <div class="timeline-title">Undergraduate Researcher</div>
          <div class="timeline-org">SKKU Media System Laboratory</div>
          <p class="timeline-desc">12 months of research experience within the university lab.</p>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-meta">
          <span class="timeline-date">2021 – 2024</span>
        </div>
        <div class="timeline-body">
          <div class="timeline-title">Developer</div>
          <div class="timeline-org">NNS Company</div>
          <p class="timeline-desc">Multiple development projects: NLP natural language classifier (2021), Arduino-based water control system (2023), KNN pest &amp; disease classifier (2023), Node.js/Express website (2023–2024).</p>
        </div>
      </div>

      <div class="timeline-item">
        <div class="timeline-meta">
          <span class="timeline-date">2022.12 – 2023.02</span>
        </div>
        <div class="timeline-body">
          <div class="timeline-title">Programming Tutor</div>
          <div class="timeline-org">평정 학원</div>
          <p class="timeline-desc">Taught C++, Java, and Python fundamentals to students.</p>
        </div>
      </div>

    </div>
  </section>
```

- [ ] **Step 2: Add experience styles to `style.css`**

```css
/* ── Experience ─────────────────────────────────────── */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.timeline-item {
  display: flex;
  gap: 20px;
  padding-bottom: 28px;
  position: relative;
}
.timeline-item::before {
  content: '';
  position: absolute;
  left: 100px;
  top: 6px;
  bottom: 0;
  width: 1px;
  background: var(--border);
}
.timeline-item:last-child::before { display: none; }
.timeline-item::after {
  content: '';
  position: absolute;
  left: 96px;
  top: 6px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg);
}
.timeline-meta {
  width: 96px;
  flex-shrink: 0;
  text-align: right;
  padding-right: 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-top: 2px;
}
.timeline-date {
  color: var(--text-muted);
  font-size: 10px;
}
.timeline-badge {
  font-size: 8px;
  padding: 2px 6px;
  border-radius: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  align-self: flex-end;
}
.timeline-badge.current {
  background: var(--accent-dim);
  color: var(--accent);
  border: 1px solid var(--accent-mid);
}
.timeline-body { padding-left: 20px; }
.timeline-title {
  color: var(--text);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 2px;
}
.timeline-org {
  color: var(--accent);
  font-size: 11px;
  margin-bottom: 6px;
}
.timeline-desc {
  color: var(--text-sec);
  font-size: 12px;
  line-height: 1.7;
}
```

- [ ] **Step 3: Verify in browser — timeline entries should appear with green dots and connecting lines**

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: experience section with timeline layout"
```

---

## Task 6: Publications Section

**Files:**
- Modify: `index.html` — add `#publications` section
- Modify: `style.css` — add publication styles

- [ ] **Step 1: Add `#publications` section after `#experience` in `index.html`**

```html
  <!-- PUBLICATIONS -->
  <section id="publications" class="section">
    <div class="section-header">// PUBLICATIONS</div>
    <div class="pub-list">

      <div class="pub-item pub-published">
        <div class="pub-venue">ICCRD 2026 &nbsp;·&nbsp; January 24, 2026</div>
        <div class="pub-title">Dual-Manifold Alignment Contrastive Learning for Knee Osteoarthritis Prediction</div>
        <div class="pub-authors">Seungho Jung, Jitae Shin</div>
      </div>

      <div class="pub-item pub-published">
        <div class="pub-venue">ITC-CSCC 2025 &nbsp;·&nbsp; July 7, 2025</div>
        <div class="pub-title">Medical SAM Adapter++: Adaptive Normalization with Domain Interpretation for Better Adaptation</div>
        <div class="pub-authors">Seungho Jung, Jitae Shin</div>
      </div>

      <div class="pub-item pub-upcoming">
        <div class="pub-venue">// coming soon</div>
        <div class="pub-title">Upcoming publication</div>
        <div class="pub-authors">Seungho Jung et al.</div>
      </div>

    </div>
  </section>
```

- [ ] **Step 2: Add publication styles to `style.css`**

```css
/* ── Publications ───────────────────────────────────── */
.pub-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.pub-item {
  padding: 14px 16px;
  border-left: 3px solid var(--border);
  border-radius: 0 4px 4px 0;
}
.pub-published {
  border-left-color: var(--accent);
  background: var(--accent-dim);
}
.pub-upcoming {
  border-left-color: var(--border);
  opacity: 0.5;
}
.pub-venue {
  color: var(--accent);
  font-size: 10px;
  letter-spacing: 1px;
  margin-bottom: 6px;
}
.pub-upcoming .pub-venue {
  color: var(--text-muted);
}
.pub-title {
  color: var(--text);
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 4px;
  line-height: 1.5;
}
.pub-authors {
  color: var(--text-muted);
  font-size: 11px;
}
```

- [ ] **Step 3: Verify in browser — two published papers in green-bordered cards, one grayed upcoming entry**

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: publications section with upcoming placeholder"
```

---

## Task 7: Projects Section

**Files:**
- Modify: `index.html` — add `#projects` section
- Modify: `style.css` — add project card styles

- [ ] **Step 1: Add `#projects` section after `#publications` in `index.html`**

```html
  <!-- PROJECTS -->
  <section id="projects" class="section">
    <div class="section-header">// PROJECTS</div>
    <div class="project-grid">

      <div class="project-card">
        <div class="project-header">
          <div class="project-title">Next-Generation Functional Desk</div>
          <div class="project-date">2024</div>
        </div>
        <p class="project-desc">Wireless power transmission and reception system integrated into a desk design. Includes a CNN-based OCR model that reads handwritten letters and translates them to machine text.</p>
        <div class="project-tags">
          <span class="tag">Arduino</span>
          <span class="tag">CNN</span>
          <span class="tag">OCR</span>
          <span class="tag">Python</span>
          <span class="tag">Wireless Charging</span>
        </div>
      </div>

      <div class="project-card">
        <div class="project-header">
          <div class="project-title">KNN Pest Disease Classifier</div>
          <div class="project-date">2023</div>
        </div>
        <p class="project-desc">Agricultural pest and disease image classification system. Built for NNS to identify plant diseases from images using K-Nearest Neighbors.</p>
        <div class="project-tags">
          <span class="tag">Python</span>
          <span class="tag">KNN</span>
          <span class="tag">OpenCV</span>
        </div>
      </div>

      <div class="project-card">
        <div class="project-header">
          <div class="project-title">NLP Natural Language Classifier</div>
          <div class="project-date">2021</div>
        </div>
        <p class="project-desc">Natural language classification system developed for NNS Company. Categorizes text input using NLP techniques.</p>
        <div class="project-tags">
          <span class="tag">Python</span>
          <span class="tag">NLP</span>
        </div>
      </div>

      <div class="project-card">
        <div class="project-header">
          <div class="project-title">Arduino Water Control System</div>
          <div class="project-date">2023</div>
        </div>
        <p class="project-desc">Automated water control system using Arduino sensors and actuators. Developed for NNS Company.</p>
        <div class="project-tags">
          <span class="tag">Arduino</span>
          <span class="tag">C++</span>
        </div>
      </div>

    </div>
  </section>
```

- [ ] **Step 2: Add project card styles to `style.css`**

```css
/* ── Projects ───────────────────────────────────────── */
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.project-card {
  background: #111;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: border-color 0.2s;
}
.project-card:hover { border-color: var(--accent-mid); }
.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}
.project-title {
  color: var(--text);
  font-size: 13px;
  font-weight: 700;
  line-height: 1.4;
}
.project-date {
  color: var(--text-muted);
  font-size: 10px;
  flex-shrink: 0;
}
.project-desc {
  color: var(--text-sec);
  font-size: 11px;
  line-height: 1.7;
  flex: 1;
}
.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
```

- [ ] **Step 3: Verify in browser — project cards appear in a 2-column grid with tags**

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: projects section with card grid layout"
```

---

## Task 8: Contact Section

**Files:**
- Modify: `index.html` — add `#contact` section
- Modify: `style.css` — add contact styles

- [ ] **Step 1: Add `#contact` section after `#projects` in `index.html`**

```html
  <!-- CONTACT -->
  <section id="contact" class="section">
    <div class="section-header">// CONTACT</div>
    <p class="contact-tagline">Open to SWE and ML/AI roles. Feel free to reach out.</p>
    <div class="contact-links">
      <a href="mailto:richardjung@g.skku.edu" class="contact-item">
        <span class="contact-icon">✉</span>
        <span>richardjung@g.skku.edu</span>
      </a>
      <a href="https://github.com/richardjung21" target="_blank" rel="noopener" class="contact-item">
        <span class="contact-icon">⌥</span>
        <span>github.com/richardjung21</span>
      </a>
      <a href="https://linkedin.com/in/YOUR-LINKEDIN" target="_blank" rel="noopener" class="contact-item">
        <span class="contact-icon">in</span>
        <span>LinkedIn</span>
      </a>
    </div>
  </section>

</main>
```

- [ ] **Step 2: Add contact styles to `style.css`**

```css
/* ── Contact ────────────────────────────────────────── */
.contact-tagline {
  color: var(--text-sec);
  font-size: 13px;
  margin-bottom: 20px;
}
.contact-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-sec);
  font-size: 13px;
  transition: color 0.15s;
}
.contact-item:hover { color: var(--accent); text-decoration: none; }
.contact-icon {
  color: var(--accent);
  font-size: 14px;
  width: 20px;
  text-align: center;
}
```

- [ ] **Step 3: Verify in browser — contact section shows tagline and three linked items**

- [ ] **Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: contact section with email, GitHub, LinkedIn"
```

---

## Task 9: Page Title and Meta

**Files:**
- Modify: `index.html` — add meta description and Open Graph tags

- [ ] **Step 1: Replace the `<head>` block in `index.html`**

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Seungho Jung — ML Researcher and Software Engineer. MS candidate at SKKU specializing in Generative Models and Computer Vision.">
  <meta property="og:title" content="Seungho Jung — Portfolio">
  <meta property="og:description" content="ML Researcher & Software Engineer · SKKU · 2 Publications">
  <meta property="og:type" content="website">
  <title>Seungho Jung — Portfolio</title>
  <link rel="stylesheet" href="style.css">
</head>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: add meta description and Open Graph tags"
```

---

## Task 10: JavaScript — Scroll Spy, Smooth Scroll, Mobile Menu

**Files:**
- Modify: `script.js` — implement all interactions

- [ ] **Step 1: Replace `script.js` with full implementation**

```js
document.addEventListener('DOMContentLoaded', () => {
  // ── Smooth scroll ──────────────────────────────────
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
      // Close mobile menu on link click
      sidebar.classList.remove('open');
      hamburger.classList.remove('open');
    });
  });

  // ── Scroll spy ────────────────────────────────────
  const sections = document.querySelectorAll('.section');
  const navLinks = document.querySelectorAll('.nav-link');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(link => {
          link.classList.toggle(
            'active',
            link.dataset.section === entry.target.id
          );
        });
      }
    });
  }, {
    rootMargin: '-30% 0px -60% 0px',
    threshold: 0
  });

  sections.forEach(section => observer.observe(section));

  // ── Mobile hamburger menu ─────────────────────────
  const hamburger = document.getElementById('hamburger');
  const sidebar   = document.getElementById('sidebar');

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', e => {
    if (
      window.innerWidth <= 768 &&
      !sidebar.contains(e.target) &&
      !hamburger.contains(e.target)
    ) {
      sidebar.classList.remove('open');
      hamburger.classList.remove('open');
    }
  });
});
```

- [ ] **Step 2: Verify scroll spy — scroll down the page and confirm the active nav item updates**

- [ ] **Step 3: Verify smooth scroll — click a nav link and confirm it scrolls smoothly to that section**

- [ ] **Step 4: Verify mobile menu — resize browser to < 768px, confirm hamburger appears, clicking it shows/hides sidebar**

- [ ] **Step 5: Commit**

```bash
git add script.js
git commit -m "feat: scroll spy, smooth scroll, and mobile hamburger menu"
```

---

## Task 11: Add Profile Photo

**Files:**
- Add: `assets/profile.jpg`

- [ ] **Step 1: Copy your photo into the assets folder**

```bash
# Replace /path/to/your/photo.jpg with the actual path to your photo
cp /path/to/your/photo.jpg assets/profile.jpg
```

The photo should be at least 200×200px. Square crop works best for the circular sidebar display.

- [ ] **Step 2: Verify in browser — photo appears in the sidebar (circular) and in the about section**

- [ ] **Step 3: Commit**

```bash
git add assets/profile.jpg
git commit -m "feat: add profile photo"
```

---

## Task 12: Deploy to GitHub Pages

**Files:** None — just git push

- [ ] **Step 1: Verify everything looks correct locally one final time**

Open `index.html` via `python3 -m http.server 8080` and visit `http://localhost:8080`. Check all sections, scroll spy, mobile view.

- [ ] **Step 2: Push to GitHub**

```bash
git push origin main
```

- [ ] **Step 3: Verify the site is live**

Visit `https://richardjung21.github.io` — GitHub Pages typically deploys within 1–2 minutes of pushing.

If the site doesn't appear, go to the repo's **Settings → Pages** and confirm Source is set to `Deploy from a branch → main → / (root)`.

---

## Open Items (fill in before or after launch)

- Replace `YOUR-LINKEDIN` in `index.html` (2 places: sidebar + contact) with your actual LinkedIn profile URL
- Add Waterbe employment dates to the experience section
- Update the upcoming publication entry once the 3rd paper is accepted
- Add `assets/profile.jpg`
