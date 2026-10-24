/**
 * F16: Pro Architectural Resources & Technical Specs
 * Searchable, categorized repository of official installation manuals,
 * environmental certifications, and warranty documents.
 */

(function () {
  'use strict';

  const RESOURCES = [
    // Installation
    {
      id: 'res-deck-guide',
      category: 'installation',
      title: 'UltraShield Decking Installation Guide',
      desc: 'Complete substructure joist spans, thermal expansion gaps, and clip installation techniques.',
      url: '/pdf/Decking_Installation_Guide.pdf',
      format: 'PDF Manual'
    },
    {
      id: 'res-cladding-cast',
      category: 'installation',
      title: 'Castellated Cladding UH61 Installation Manual',
      desc: 'Step-by-step horizontal and vertical installation for fluted architectural siding.',
      url: '/pdf/Castellation_Cladding_UH61_Installation_Guide_Encryption.pdf',
      format: 'PDF Manual'
    },
    {
      id: 'res-cladding-us09',
      category: 'installation',
      title: 'UltraShield Wall Cladding US09 Guide',
      desc: 'Architectural rainscreen details, corner trims, and flashing specifications.',
      url: '/pdf/Wall-Cladding-US09-installation-guide.pdf',
      format: 'PDF Manual'
    },
    {
      id: 'res-deck-tile',
      category: 'installation',
      title: 'QuickDeck DIY Tile Assembly Guide',
      desc: 'Modular interlocking tile layout over existing concrete and waterproofing membranes.',
      url: '/pdf/UltraShield_Deck_Tile_Installation.pdf',
      format: 'PDF Guide'
    },

    // Certifications
    {
      id: 'res-green-label',
      category: 'certifications',
      title: 'Singapore Green Label Environmental Certificate',
      desc: 'SEC Certified eco-friendly building material containing 95% recycled core components.',
      url: '/pdf/NewTechWood-Green-Label-Certificate-Singapore.pdf',
      format: 'Certification'
    },
    {
      id: 'res-iso-9001',
      category: 'certifications',
      title: 'SGS ISO 9001:2015 Quality Management',
      desc: 'Certified manufacturing quality standards, precision tolerances, and testing protocols.',
      url: '/pdf/SGS_ISO_9001.pdf',
      format: 'SGS Certificate'
    },
    {
      id: 'res-iso-14001',
      category: 'certifications',
      title: 'SGS ISO 14001 Environmental Management',
      desc: 'Certified ecological manufacturing, zero hazardous waste, and water recycling compliance.',
      url: '/pdf/SGS_ISO_14001.pdf',
      format: 'SGS Certificate'
    },
    {
      id: 'res-ccmc',
      category: 'certifications',
      title: 'CCMC Architectural Compliance Report',
      desc: 'Structural load capacity, slip resistance, and weatherability compliance documentation.',
      url: '/pdf/CCMC-Report.pdf',
      format: 'Evaluation'
    },

    // Warranty & Maintenance
    {
      id: 'res-warranty-res',
      category: 'warranty',
      title: '25-Year Residential Limited Warranty',
      desc: 'Official homeowner warranty policy covering cracking, splitting, rot, and termites.',
      url: '/pdf/NEWTECHWOOD-RESIDENTIAL-LIMITED-WARRANTY.pdf',
      format: 'Warranty Policy'
    },
    {
      id: 'res-warranty-comm',
      category: 'warranty',
      title: '10-Year Commercial Limited Warranty',
      desc: 'Performance warranty terms for high-footfall public and commercial developments.',
      url: '/pdf/NEWTECHWOOD-COMMERCIAL-LIMITED-WARRANTY.pdf',
      format: 'Warranty Policy'
    },
    {
      id: 'res-care-cleaning',
      category: 'warranty',
      title: 'UltraShield Care & Maintenance Guidelines',
      desc: 'Standard cleaning practices, removing oil/grease, and seasonal maintenance.',
      url: '/pdf/Care-and-Cleaning.pdf',
      format: 'Maintenance'
    },
    {
      id: 'res-msds',
      category: 'warranty',
      title: 'Material Safety Data Sheet (MSDS)',
      desc: 'UltraShield composition, non-toxicity, and occupational safety documentation.',
      url: '/pdf/MSDS_UltraShield.pdf',
      format: 'MSDS'
    }
  ];

  let activeCategory = 'all';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProResources);
  } else {
    initProResources();
  }

  function initProResources() {
    let mount = document.getElementById('ntw-pro-resources');
    if (!mount) {
      const anchor = document.getElementById('ntw-brochures-block') || document.getElementById('ntw-sample-request');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-pro-resources';
      anchor.parentNode.insertBefore(mount, anchor.nextSibling);
    }

    mount.innerHTML = `
      <section class="ntw-pro-section" aria-label="Professional Technical Resources">
        <div class="ntw-pro-container">
          
          <div class="ntw-pro-header">
            <span class="ntw-pro-eyebrow">For Architects &amp; Specifiers</span>
            <h2 class="ntw-pro-title">Architectural &amp; Technical Library</h2>
            <p class="ntw-pro-subtitle">
              Access comprehensive CAD details, installation manuals, international certifications, and warranty documents for your project files.
            </p>
          </div>

          <!-- Category Filter Tabs -->
          <div class="ntw-pro-tabs" role="tablist" aria-label="Filter resources by category">
            <button type="button" class="ntw-pro-tab-btn active" data-category="all" role="tab" aria-selected="true">All Resources</button>
            <button type="button" class="ntw-pro-tab-btn" data-category="installation" role="tab" aria-selected="false">Installation Manuals</button>
            <button type="button" class="ntw-pro-tab-btn" data-category="certifications" role="tab" aria-selected="false">Certifications &amp; Tests</button>
            <button type="button" class="ntw-pro-tab-btn" data-category="warranty" role="tab" aria-selected="false">Warranty &amp; Care</button>
          </div>

          <!-- Cards Grid -->
          <div class="ntw-pro-grid" id="ntw-pro-grid">
            <!-- Rendered by renderCards() -->
          </div>

        </div>
      </section>
    `;

    bindEvents();
    renderCards();
  }

  function bindEvents() {
    const tabs = document.querySelectorAll('.ntw-pro-tab-btn');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        activeCategory = tab.getAttribute('data-category') || 'all';
        renderCards();
      });
    });
  }

  function renderCards() {
    const grid = document.getElementById('ntw-pro-grid');
    if (!grid) return;

    const filtered = (activeCategory === 'all')
      ? RESOURCES
      : RESOURCES.filter(r => r.category === activeCategory);

    grid.innerHTML = filtered.map(r => `
      <div class="ntw-pro-card" id="${escapeHtml(r.id)}">
        <div>
          <div class="ntw-pro-card-top">
            <div class="ntw-pro-icon">
              <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
            </div>
            <h3 class="ntw-pro-card-title">${escapeHtml(r.title)}</h3>
          </div>
          <p class="ntw-pro-card-desc">${escapeHtml(r.desc)}</p>
        </div>

        <div class="ntw-pro-card-footer">
          <span class="ntw-pro-tag">${escapeHtml(r.format)}</span>
          <a href="${escapeHtml(r.url)}" class="ntw-pro-dl-link" download title="Download ${escapeHtml(r.title)}">
            <span>Download</span>
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
        </div>
      </div>
    `).join('');
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
