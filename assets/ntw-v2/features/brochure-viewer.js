/**
 * F12: Brochure Block & Interactive Catalog Viewer
 * Renders 3D brochure showcases with instant PDF downloads and interactive modal previews.
 */

(function () {
  'use strict';

  const BROCHURES = [
    {
      id: 'decking-catalog',
      title: 'UltraShield Decking & Railing Catalogue',
      edition: 'Architectural Edition 2026',
      class: 'decking',
      tag: 'Decking & Railing',
      desc: 'Complete technical profile specifications, span tables, color series, and hidden clip installation details.',
      pdfUrl: '/pdf/UltraShield-product-catalog-Decking-Railing.pdf',
      pages: [
        {
          heading: 'UltraShield Decking Portfolio',
          subtitle: 'Solid & Hollow Profiles with 360° Shield Technology',
          content: 'Engineered for residential balconies, luxury terraces, and high-traffic commercial promenades across India. Highly resistant to stains, fading, moisture, and termite attack.'
        },
        {
          heading: 'Core Architecture & 360° Shield',
          subtitle: 'Engineered Polymer Co-Extrusion',
          content: 'The outer shield completely encapsulates all four sides around its dense composite core. It protects the board from the harshest UV radiation, high humidity, and monsoon rains.'
        },
        {
          heading: 'Naturale & Vintage Color Finishes',
          subtitle: 'Authentic Multi-Chromatic Hardwood Grain',
          content: 'Available in Peruvian Teak, Brazilian Ipe, Antique Oak, Canadian Maple, Spanish Walnut, and Charcoal finishes with natural wood embossed textures.'
        },
        {
          heading: 'Installation & Engineering Spans',
          subtitle: 'Hidden Clip System & Joist Guidelines',
          content: 'Maximum recommended joist spacing: 350mm to 400mm centre-to-centre. Hidden T-clips and locking clips allow controlled thermal movement.'
        }
      ]
    },
    {
      id: 'cladding-catalog',
      title: 'UltraShield Architectural Facade & Cladding',
      edition: 'Architectural Edition 2026',
      class: 'cladding',
      tag: 'Wall Cladding & Louvers',
      desc: 'Castellated fluted siding, contemporary shiplap profiles, European rainscreen systems, and ventilation details.',
      pdfUrl: '/pdf/UltraShield-product-catalog-Cladding.pdf',
      pages: [
        {
          heading: 'Architectural Cladding Systems',
          subtitle: 'Castellated Fluted & Modern Shiplap Profiles',
          content: 'Transform building exteriors, feature walls, and soffits with modern fluted timber aesthetics that never require staining, varnishing, or painting.'
        },
        {
          heading: 'Rainscreen & Ventilation System',
          subtitle: 'Thermal Air Gap & Moisture Barrier',
          content: 'Designed with continuous rear air cavity to facilitate moisture drainage and natural airflow, enhancing acoustic dampening and thermal insulation.'
        },
        {
          heading: 'Commercial Certification & Fire Tests',
          subtitle: 'Rigorous International Standards',
          content: 'Singapore Green Label, CE Certification, ISO 9001 and ISO 14001 certified manufacturing with 25-Year Residential and 10-Year Commercial Warranty.'
        },
        {
          heading: 'Profile Dimensions & Clip Accessories',
          subtitle: 'UH61 & UH108 Profiles',
          content: 'Profile widths 142mm, length 2900mm. Hidden starter clips and aluminum corner trims ensure flawless architectural joints.'
        }
      ]
    },
    {
      id: 'tiles-catalog',
      title: 'QuickDeck Tiles & Outdoor Solutions',
      edition: 'Edition 2026',
      class: 'tiles',
      tag: 'Tiles & Planters',
      desc: 'DIY interlocking composite tiles, modular planter boxes, screening louvers, and balcony transformation systems.',
      pdfUrl: '/pdf/UltraShield-product-catalog-Deck-tile-Planter-box.pdf',
      pages: [
        {
          heading: 'QuickDeck DIY Interlocking Tiles',
          subtitle: '300 × 300 mm Modular Balcony Solution',
          content: 'Instant balcony and terrace upgrades without joists or adhesives. Snaps together over existing tiled or concrete floors in hours.'
        },
        {
          heading: 'Engineered Grid Base',
          subtitle: 'Rapid Monsoon Drainage Technology',
          content: 'Interlocking polymer grid allows water to drain freely underneath, preventing stagnant pooling on residential high-rise balconies.'
        },
        {
          heading: 'Planter Boxes & Garden Accents',
          subtitle: 'Weather-Resistant Landscaping Elements',
          content: 'Matching UltraShield composite planter boxes and modular garden kits that harmonize seamlessly with your deck.'
        },
        {
          heading: 'Specifications & Care',
          subtitle: 'Zero Sanding, Zero Oil',
          content: 'Cleans effortlessly with water and gentle soap. Resistant to mold, mildew, and pet stains.'
        }
      ]
    }
  ];

  let currentBrochure = null;
  let currentPageIndex = 0;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBrochureViewer);
  } else {
    initBrochureViewer();
  }

  function initBrochureViewer() {
    let mount = document.getElementById('ntw-brochures-block');
    if (!mount) {
      const anchor = document.getElementById('ntw-material-calculator') || document.getElementById('ntw-sample-request');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-brochures-block';
      anchor.parentNode.insertBefore(mount, anchor.nextSibling);
    }

    mount.innerHTML = `
      <section class="ntw-brochure-section" aria-label="Architectural Catalogues">
        <div class="ntw-brochure-container">
          
          <div class="ntw-brochure-header">
            <span class="ntw-brochure-eyebrow">Technical Downloads</span>
            <h2 class="ntw-brochure-title">Architectural Catalogues &amp; Spec Sheets</h2>
            <p class="ntw-brochure-subtitle">
              Download comprehensive product brochures, profile cross-sections, span tables, and installation manuals directly.
            </p>
          </div>

          <div class="ntw-brochure-grid">
            ${BROCHURES.map(b => `
              <div class="ntw-brochure-card" id="card-${b.id}">
                <div>
                  <div class="ntw-book-wrap">
                    <div class="ntw-book">
                      <div class="ntw-book-cover ${b.class}">
                        <span class="ntw-book-tag">${escapeHtml(b.tag)}</span>
                        <div>
                          <div class="ntw-book-name">${escapeHtml(b.title)}</div>
                          <div class="ntw-book-edition">${escapeHtml(b.edition)}</div>
                        </div>
                        <div style="font-size: 8px; opacity: 0.6; text-transform: uppercase;">NewTechWood India</div>
                      </div>
                    </div>
                  </div>

                  <div class="ntw-brochure-info">
                    <h3>${escapeHtml(b.title)}</h3>
                    <p>${escapeHtml(b.desc)}</p>
                  </div>
                </div>

                <div class="ntw-brochure-actions">
                  <a href="${b.pdfUrl}" class="ntw-btn-download-pdf" download title="Download ${escapeHtml(b.title)} PDF">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                    <span>Download PDF</span>
                  </a>
                  <button type="button" class="ntw-btn-preview-flipbook" data-brochure="${b.id}">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    <span>Preview</span>
                  </button>
                </div>
              </div>
            `).join('')}
          </div>

        </div>
      </section>

      <!-- Flipbook Modal Preview -->
      <div class="ntw-flipbook-modal" id="ntw-flipbook-modal" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Brochure Preview">
        <div class="ntw-flipbook-dialog">
          
          <div class="ntw-flipbook-header">
            <h3 class="ntw-flipbook-title" id="ntw-fb-modal-title">Brochure Preview</h3>
            <button type="button" class="ntw-flipbook-close" id="ntw-fb-close-btn" aria-label="Close Preview">&times;</button>
          </div>

          <div class="ntw-flipbook-viewer">
            <div class="ntw-flipbook-page-canvas" id="ntw-fb-canvas">
              <span class="ntw-book-tag" id="ntw-fb-page-tag" style="margin-bottom: 8px;">Section</span>
              <h4 id="ntw-fb-page-title" style="font-size: 20px; font-weight: 700; color: #111827; margin: 0 0 8px;">Title</h4>
              <h5 id="ntw-fb-page-sub" style="font-size: 14px; color: #6b7280; font-weight: 500; margin: 0 0 16px;">Subtitle</h5>
              <p id="ntw-fb-page-content" style="font-size: 14px; color: #374151; line-height: 1.6; max-width: 480px; margin: 0 auto 24px;">Content text</p>
              <a href="#" id="ntw-fb-full-pdf-link" class="ntw-btn-download-pdf" download style="display: inline-flex; width: auto; padding: 8px 18px;">
                Download Complete PDF
              </a>
            </div>
          </div>

          <div class="ntw-flipbook-controls">
            <button type="button" class="ntw-fb-btn" id="ntw-fb-prev-btn">&larr; Previous Page</button>
            <div class="ntw-fb-counter" id="ntw-fb-counter">Page 1 of 4</div>
            <button type="button" class="ntw-fb-btn" id="ntw-fb-next-btn">Next Page &rarr;</button>
          </div>

        </div>
      </div>
    `;

    bindEvents();
  }

  function bindEvents() {
    const previewBtns = document.querySelectorAll('.ntw-btn-preview-flipbook');
    const modal = document.getElementById('ntw-flipbook-modal');
    const closeBtn = document.getElementById('ntw-fb-close-btn');
    const prevBtn = document.getElementById('ntw-fb-prev-btn');
    const nextBtn = document.getElementById('ntw-fb-next-btn');

    previewBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-brochure');
        openPreview(id);
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', closePreview);
    }

    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closePreview();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentPageIndex > 0) {
          currentPageIndex--;
          renderCurrentPage();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (currentBrochure && currentPageIndex < currentBrochure.pages.length - 1) {
          currentPageIndex++;
          renderCurrentPage();
        }
      });
    }

    window.addEventListener('keydown', (e) => {
      if (!modal || !modal.classList.contains('active')) return;
      if (e.key === 'Escape') closePreview();
      else if (e.key === 'ArrowRight' && nextBtn) nextBtn.click();
      else if (e.key === 'ArrowLeft' && prevBtn) prevBtn.click();
    });
  }

  function openPreview(brochureId) {
    const found = BROCHURES.find(b => b.id === brochureId);
    if (!found) return;

    currentBrochure = found;
    currentPageIndex = 0;

    const modal = document.getElementById('ntw-flipbook-modal');
    const titleElem = document.getElementById('ntw-fb-modal-title');
    const pdfLink = document.getElementById('ntw-fb-full-pdf-link');

    if (titleElem) titleElem.textContent = found.title;
    if (pdfLink) pdfLink.href = found.pdfUrl;

    renderCurrentPage();

    if (modal) {
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
  }

  function closePreview() {
    const modal = document.getElementById('ntw-flipbook-modal');
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  function renderCurrentPage() {
    if (!currentBrochure) return;
    const page = currentBrochure.pages[currentPageIndex];
    if (!page) return;

    const pageTag = document.getElementById('ntw-fb-page-tag');
    const pageTitle = document.getElementById('ntw-fb-page-title');
    const pageSub = document.getElementById('ntw-fb-page-sub');
    const pageContent = document.getElementById('ntw-fb-page-content');
    const counter = document.getElementById('ntw-fb-counter');
    const prevBtn = document.getElementById('ntw-fb-prev-btn');
    const nextBtn = document.getElementById('ntw-fb-next-btn');

    if (pageTag) pageTag.textContent = currentBrochure.tag;
    if (pageTitle) pageTitle.textContent = page.heading;
    if (pageSub) pageSub.textContent = page.subtitle;
    if (pageContent) pageContent.textContent = page.content;

    if (counter) {
      counter.textContent = `Page ${currentPageIndex + 1} of ${currentBrochure.pages.length}`;
    }

    if (prevBtn) prevBtn.disabled = (currentPageIndex === 0);
    if (nextBtn) nextBtn.disabled = (currentPageIndex === currentBrochure.pages.length - 1);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
})();
