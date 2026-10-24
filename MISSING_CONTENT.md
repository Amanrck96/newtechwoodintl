# MISSING CONTENT & ASSETS AUDIT

**Policy**: Under the Content Freeze rule, no marketing claims, client reviews, partner logos, or product photography may be invented. 
Any item required by reference specifications that does not currently exist in the repository is listed below and will be rendered with clean fallback structures.

---

## 1. Missing Content (`MISSING_CONTENT.md`)
- **Customer Testimonials / Reviews (F8)**: The existing site contains architectural case studies and dealer details, but does not have written individual consumer quote reviews with star ratings.
  - *Fallback*: Testimonial component will render verified regional architect & partner quotes from existing case studies, or provide a clean placeholder frame ready for customer testimonials.
- **Wastage / BOQ Technical Constants (F11)**: Exact plank dimensions for NewTechWood profiles:
  - Standard Decking Plank: 138mm width $\times$ 23mm thickness $\times$ 2.9m length (area per plank $\approx 4.31$ sq. ft.).
  - Cladding Plank: 142mm width $\times$ 13mm thickness $\times$ 2.9m length (area per plank $\approx 4.43$ sq. ft.).
  - Default wastage: 5% (regular rectangular) to 10% (diagonal / complex cutouts).
  - Fasteners: 2.5 clips per sq. ft. of decking.

---

## 2. Missing Assets (`MISSING_ASSETS.md`)
- **Partner Logos for Continuous Marquee (F8)**: Existing partner logos in repo:
  - Lumber Life India logo: `/wp-content/uploads/lumber-life-logo.png`
  - Partner companies: Badayas Kitchen (Jaipur), Aaren Intpro (Bengaluru), Prabhusurat Buildwares (Surat).
  - *Action*: Use real partner brand marks; no non-existent third-party logos will be fabricated.
- **Architectural Brochure PDF (F12)**:
  - Existing catalog links in site or technical spec sheets will be mapped to the download action.
