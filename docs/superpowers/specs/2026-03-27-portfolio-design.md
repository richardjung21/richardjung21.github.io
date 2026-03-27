# Portfolio Website Design Spec
**Date:** 2026-03-27
**Owner:** Seungho Jung
**Site:** richardjung21.github.io

---

## Overview

A single-page personal portfolio targeting SWE and DS/ML recruiters. Built with pure HTML/CSS/JS — no framework, no build step. Hosted directly on GitHub Pages.

---

## Visual Style

- **Theme:** Dark terminal aesthetic
- **Background:** `#0d0d0d` (near-black)
- **Accent:** `#00ff88` (neon green)
- **Text:** `#ffffff` (primary), `#aaaaaa` (secondary), `#555555` (muted/comments)
- **Font:** `'Courier New', monospace` for terminal feel
- **Section headers styled as code comments:** `// ABOUT`, `// SKILLS`, etc.

---

## Layout

Two-column layout with a fixed sidebar and a scrollable content panel.

### Sidebar (fixed, left, ~220px wide)
- Circular profile photo with neon green border
- Name: **Seungho Jung**
- Subtitle: *ML Researcher & Engineer*
- Navigation links (active link highlighted green with `>` prefix, inactive styled as `$` shell commands):
  - `> about`
  - `$ skills`
  - `$ experience`
  - `$ publications`
  - `$ projects`
  - `$ contact`
- Social links pinned to bottom: GitHub, LinkedIn, Email

### Main Content Panel (scrollable, right)
Sections stack vertically. Smooth scroll on nav click. Scroll spy updates active nav item as user scrolls.

---

## Sections

### `// ABOUT`
- Profile photo (inline, right-aligned) + name + subtitle
- Short bio paragraph: MS candidate at SKKU, specializing in Generative Models (Diffusion Models), Computer Vision (Image Segmentation, Representation Learning), and Medical Image Analysis. Currently a Graduate Researcher at Crescom and freelance web developer. Native English speaker. 2 publications, 3rd upcoming.
- Education badges: SKKU MS ECE (2025–present, GPA 4.33/4.5), SKKU BS EE (2019–2025, GPA 3.46/4.5)

### `// SKILLS`
Green pill-style tags grouped into categories:

| Category | Skills |
|---|---|
| Languages | Python, C++, Java, JavaScript |
| ML / AI | PyTorch, OpenCV, Diffusion Models, SAM |
| Web | Node.js, Express, React |
| Tools | Git, Linux, Arduino |

### `// EXPERIENCE`
Timeline-style entries, newest first:

1. **Crescom** — Graduate Researcher *(2025–present)*
   Research on Generative Models and Computer Vision for startup.

2. **Waterbe** — Freelance Developer *(dates TBD by user)*
   Frontend and backend web development.

3. **SKKU Media System Laboratory** — Undergraduate Researcher *(2024.02–2025.02)*
   12 months research experience.

4. **NNS Company** — Developer *(2021–2024)*
   Multiple projects: NLP classification (2021), water control system with Arduino (2023), KNN pest disease classification (2023), Node.js/Express website (2023–2024).

5. **평정 학원** — Programming Tutor *(2022.12–2023.02)*
   Taught C++, Java, Python basics.

### `// PUBLICATIONS`
Each entry: title, venue (green), authors, year. Left border accent (green = published, gray = upcoming).

1. **Dual-Manifold Alignment Contrastive Learning for Knee Osteoarthritis Prediction**
   ICCRD 2026 · Seungho Jung, Jitae Shin · January 24, 2026

2. **Medical SAM Adapter++: Adaptive Normalization with Domain Interpretation for Better Adaptation**
   ITC-CSCC 2025 · Seungho Jung, Jitae Shin · July 7, 2025

3. *(Upcoming — title and venue TBD)* — grayed out with `// coming soon` label

### `// PROJECTS`
Card-style entries with title, description, and tech tags:

1. **Next-Generation Functional Desk** *(2024)*
   Wireless power transmission/reception system integrated with a desk. Includes OCR CNN model for handwritten letter recognition and machine translation.
   Tags: `Arduino`, `CNN`, `OCR`, `Python`, `Wireless Charging`

2. **KNN Pest Disease Classifier** *(2023)*
   Agricultural pest and disease image classification system built for NNS.
   Tags: `Python`, `KNN`, `OpenCV`

3. **NLP Natural Language Classifier** *(2021)*
   Natural language classification system built for NNS using NLP techniques.
   Tags: `Python`, `NLP`

4. **Water Control System** *(2023)*
   Arduino-based automated water control system.
   Tags: `Arduino`, `C++`

### `// CONTACT`
- Email: richardjung@g.skku.edu (mailto link)
- GitHub: github.com/richardjung21 (link)
- LinkedIn: (user to provide URL)
- Short prompt: "Open to SWE and ML/AI roles. Feel free to reach out."

---

## Interactions

- **Scroll spy:** Active nav item updates automatically as user scrolls through sections
- **Smooth scroll:** Clicking a nav item scrolls smoothly to the section
- **Mobile responsive:** Below 768px, sidebar collapses into a hamburger menu at the top

---

## File Structure

```
richardjung21.github.io/
├── index.html          # All section markup
├── style.css           # All styles (dark theme, layout, responsive)
├── script.js           # Scroll spy + smooth scroll + mobile menu
├── assets/
│   └── profile.jpg     # Profile photo (user to add)
└── README.md
```

---

## Open Items (need user input before/during build)

- Waterbe employment dates
- LinkedIn profile URL
- 3rd publication title, venue, and expected date
- Profile photo file (to place in `assets/`)
