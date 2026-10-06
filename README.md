# Seungho Jung's portfolio

Edit **`content.json`** for routine updates, then run:

```sh
python build.py
```

Open `index.html` to preview, then commit `content.json` and all generated root-level
HTML pages for GitHub Pages. Python 3.9+ is the only requirement; there are no
packages to install. The published page stays fully static, so its content and
social metadata are available without JavaScript.

## Pages and navigation

`index.html` opens with a cover containing the introduction and research interests,
then scrolls naturally through every section. The sidebar links to anchors on the
same page and highlights the current section as you scroll. It remains visible
on desktop and becomes a collapsible menu on smaller screens. The highlight follows
the section occupying the most visible space, excluding the mobile header.
A section shorter than the visible viewport takes priority once more than 50% of
its height is visible, so short sections such as Skills can activate. If several
short sections qualify, the one with the most visible space wins; ties follow
page order. Contact activates only at the bottom of the page. Until then, the
last non-contact section stays active if only Contact is visible.
A thin progress line shows how far visitors have scrolled.
With JavaScript disabled, all content and navigation links remain visible.

One `python build.py` rebuilds the portfolio and six compatibility redirect files.
Previously shared URLs such as `publications.html` lead to
`index.html#publications`; a fallback link is included. `--check` reports any stale
or missing outputs. No server routing rules are required, and anchor links work
on GitHub Pages and when opening files locally.

## Where to edit

| Content | Location in `content.json` |
| --- | --- |
| Name, photo, site URL, developer experience | `profile` |
| GPA, degree, school, dates | `education` |
| Intro and buttons | `hero` |
| About paragraphs | `about.paragraphs` |
| Language proficiency and test scores | `languages`, `language_scores` |
| Skill groups and tags | `skills` |
| Jobs and research experience | `experience` |
| Papers and their status | `publications` |
| Projects and tags | `projects` |
| Email and social accounts | `contact.links` |
| Navigation labels and section headings | `sections` |
| Search/social descriptions | `metadata` |
| Copyright year and closing text | `footer` |

Change the GPA in the education entry with `id: "masters"` once; the About statistics
and education details both use it. `profile.featured_education` chooses which degree
appears in the statistics. The GPA scale also comes from that same entry.

Publication counts are computed from the list. The About statistics and social description
count **Published** papers only. The About summary separately counts **Published**,
**Accepted**, **Under Review**, and **In Progress** papers. Update a paper's `status` to one of those
exact values to update every summary automatically.

To add a paper, copy an object in `publications` and edit its fields:

```json
{
  "venue": "Conference 2027",
  "date": "2027",
  "title": "Your paper title",
  "authors": ["Seung Ho Jung", "Coauthor Name"],
  "status": "Accepted"
}
```

Publications are grouped into first-author, second-author, and (when needed)
additional coauthored papers. Your position is derived from the `authors` list by
matching `profile.publication_name`, ignoring spaces and capitalization. Keep
authors in the order printed in the paper. Missing or duplicate matches stop the
build rather than silently assigning an incorrect role. Empty groups are omitted.
For a confirmed authorship designation that differs from the byline index, set
`author_position` on that paper (for example, `2` for second author). This takes
precedence for grouping while preserving the complete printed byline. ECML PKDD
uses this field for the author's confirmed second-author designation.
Each group is automatically sorted newest-first, regardless of the order in
`content.json`. Dates also receive consistent display formatting:

| `date` in JSON | Display |
| --- | --- |
| `"2026-05-12"` | May 12, 2026 |
| `"2026-05"` | May 2026 |
| `"2026"` | 2026 |
| `""` or omitted | No date shown; placed at the bottom |

Use only the precision you know. A year-only entry follows fully dated entries
from that year; a month-only entry follows fully dated entries from that month.
Ties are resolved alphabetically by title, then venue, authors, and status.
The original English format (`"May 12, 2026"`) still works. `"To be announced"`
and `"TBA"` are also accepted as undated labels. Other unrecognized or invalid
dates stop the build with a message naming the paper. Publication status does not override date order.

Other lists retain their JSON order. Add or remove education,
languages, skills, jobs, papers, projects, and contacts in the same way; empty
lists are allowed except that education must contain the featured degree.
JSON uses double quotes and does not allow comments or trailing commas.
Write normal text, including `&` and `<`; the builder escapes HTML for you.

Contact URLs are built from `url_prefix` plus `value`, so editing an email address
or username updates both the displayed text and link. `profile.name` is shared
across the page. Author names are independent to preserve publication
bylines. The copyright year and `years_dev` are explicitly editable values.

The About paragraphs, hero eyebrow/bio, contact description, and metadata support
`{name}`, `{published_count}`, `{accepted_count}`, `{under_review_count}`, `{in_progress_count}`, and
`{publication_summary}` placeholders. Use `{{` and `}}` for literal braces there.

## Layout and validation

- `templates/page.html`: shared sidebar, metadata, footer, and page shell.
- `templates/home.html`: introductory cover.
- `templates/redirect.html`: compatibility links for former separate pages.
- Other `templates/*.html`: the content layout for each section.
- `build.py`: markup for repeated cards and automatic values.
- `style.css`: appearance; the `:root` tokens control colors, fonts, spacing, and page width.
- `script.js`: responsive menu, active-section tracking, progress, and reveal animations.

Keep the existing IDs when editing `sections`; its order controls both the reading
order and sidebar after Home. Adding another section requires an entry in `PAGE_FILES` in
`build.py` and a matching template. Routine content changes do not require editing
these files. Do not edit generated root-level HTML directly because the next
build replaces it.

Check that generated HTML matches the source before publishing:

```sh
python build.py --check
python -m unittest discover -s tests
node --test tests/navigation.test.cjs tests/lightbox.test.cjs
```

The builder adds a content hash to every local CSS and JavaScript URL. Whenever
one of those files changes, run `python build.py` and commit the rebuilt HTML
alongside it. Browsers then request the new asset URL instead of reusing an old
cached version. Hashes are stable across Windows and Unix line endings.
`--check` also detects HTML that has not been rebuilt after a CSS or JS edit.

The researcher profile uses DM Sans and JetBrains Mono from Google Fonts, with
system sans-serif/monospace fallbacks. Lightbox2 includes its bundled jQuery; all JavaScript is served locally.
`hero.research_interests` controls the research-area summaries. Each entry can be
a plain title or an object with `title` and `description`. `profile.photo_caption`
controls the portrait caption. Projects use equally weighted cards with optional
`details` entries, each containing a `label` and `text`, for application and
implementation descriptions.
Publication status colors are automatic. Navigation uses native smooth anchor
scrolling; wheel and touch scrolling retain their normal behavior. Section headings
and cards gently fade and rise once as they enter view. The sidebar marker moves
to the current section, while the progress line follows the page's scroll position.
Reduced-motion preferences disable smooth scrolling, reveals, and transitions.
Content remains readable without JavaScript or animation API support.

Projects and publications can include an optional `links` list:

```json
"links": [
  { "label": "Code", "url": "https://github.com/your-account/your-repository" },
  { "label": "Paper", "url": "https://example.com/your-paper" }
]
```

Only supplied links appear; there are no placeholder buttons. Replace example
URLs with the real destinations. Hero buttons may use `"contact": "GitHub"`
instead of `href` to reuse a contact entry, keeping the username in one place.

`profile.publication_name` controls the author name emphasized in publication
bylines. The degree and school in the introduction come from the featured
education entry. Graduation dates remain manually editable in `education.period`.

## Paper summaries and figures

Each paper can include an optional `overview` object in `content.json`:

- `takeaway`: one sentence describing the research idea.
- `method`: short strings shown as a numbered method diagram.
- `results`: objects with `label` and `value`, shown as prominent result tiles.
- `context`: dataset, comparison, and table/page reference for those results.
- `note`: the relevant trade-off or scope of the result.
- `figure`: `src`, `width`, `height`, `alt`, and `caption` for an extracted image.
- `source`: local PDF filename and page numbers for editorial verification; this
  metadata is not rendered or linked on the website.

Summaries, method diagrams, results, and figures are collapsed together by default.
Visitors can expand "At a glance & figure" to view them in one disclosure.
Click a figure or "Enlarge figure" to open an individual Lightbox2 viewer. It uses the
upstream white image border, dark overlay, captions,
600 ms fades and 700 ms container resizing. Escape, the close control, or the
overlay dismisses it. Reduced-motion preferences disable the animations.
`lightbox.js` configures the library and connects caption links to their images. Each figure opens independently, with no previous/next navigation. The
image frame and caption are centered vertically in the viewport. Without
JavaScript, links open the image normally.
Lightbox2 2.12.0 and its bundled jQuery are vendored under
`assets/vendor/lightbox2/`, with upstream license notices retained.
The disclosure works without JavaScript. Figure images are loaded lazily and
reserve their dimensions to avoid layout shifts. Papers without an overview,
including unfinished work, keep the usual citation card.

The initial summaries were checked against the supplied manuscripts. Figures live
in `assets/research/`; extraction locations and metadata corrections are recorded
in `assets/research/README.md`. Updating ordinary summary text does not require
PDF tools or any new build dependency.
