# Research summary sources

Four images are figure-area extracts from the user-supplied PDFs; `quadtree.png`
is a byte-for-byte copy of the author's replacement PNG. No figure content was
redrawn or altered. The website presents editable, paraphrased
summaries, with the study figure available in a native HTML disclosure. It does
not link to the PDFs. `content.json` retains the source file and relevant pages.

## Figure extraction

PDF figures are rendered using PyMuPDF at 6 pixels per PDF point (432 DPI),
2.4 times the original export's width and height. This improves vector lines and
labels; embedded raster details remain limited by their source resolution.
The replacement ICISPC image is retained at its original 817 x 540 pixels.
Images are never stretched beyond their natural width, and each figure offers
an in-page lightbox for full-resolution inspection. Page numbers are one-based;
crop rectangles are `(left, top, right, bottom)` in PDF points. Coordinates include
panel labels, with captions supplied as editable HTML text.

| Image | Source | Page / figure | Crop |
| --- | --- | --- | --- |
| `quadtree.png` | `Qualitative_Comparison.png` | Author-supplied replacement | Uncropped original |
| `duma-clr.png` | `ICCRD_RD0320.pdf` | 3 / Fig. 2 | 42, 18, 570, 263 |
| `med-sa.png` | `ITC-CSCC_Final_Manuscript_정승호.pdf` | 3 / Fig. 2 | 122, 42, 500, 263 |
| `maskformer.png` | `Breat_Lesion_Detection.pdf` | 11 / Fig. 3 | 35, 410, 560, 610 |
| `causal-graphs.png` | `ECML_PKDD_783.pdf` | 4 / Fig. 1 | 135, 110, 485, 245 |

The Sensors article identifies itself as CC BY 4.0; its figure caption includes
author, journal, year, figure number and license attribution.

## Summary verification

- ICISPC: Table 1, p. 8: 36.21 vs. 43.88 GFLOPS (17.5% reduction), with PSNR
  29.60 vs. 34.03 dB. The summary explicitly retains the quality trade-off.
- ICCRD: Table I, p. 4: AUC 0.7638 vs. 0.7289. Section III describes 4,796 pairs,
  48-month labels and a held-out acquisition site. No claim of statistical
  significance is added to the summary.
- ITC-CSCC: Table II, p. 5: Dice 66.33% vs. 62.54% (+3.79 percentage points)
  in the noisy OAI ablation. This avoids attributing denoising gains to AdaLN/DI.
- Sensors: Tables 4-5, pp. 12 and 14: mAP 0.943 and malignant recall 0.900.
  The figure is a qualitative segmentation example, not the classification metric.
- ECML PKDD: Table 3, p. 12: MSDS AC@1 0.827 +/- 0.102, SWaT AC@3
  0.517 +/- 0.037. Results are not characterized as winning every metric.

## Metadata corrections

- ICISPC's first page lists Seung Ho Jung, Kyu Hoon Moon, Geonhyeok Lee and
  Jitae Shin. The two previously omitted middle authors were restored.
- Sensors' first page distinguishes received date (September 21, 2024) from
  publication date (October 27, 2024). The latter now drives publication sorting.
- ECML PKDD uses `author_position: 2`, reflecting the author's confirmed
  second-author designation. The manuscript's full printed byline is preserved;
  the confirmed designation takes precedence over its list index for grouping.
