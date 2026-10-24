/**
 * F8: Testimonial Slider & Infinite Partner Logo Strip
 * Case study testimonials slider with pause-on-hover infinite logo marquee.
 */

(function () {
  'use strict';

  const TESTIMONIALS = [
    {
      quote: "UltraShield composite decking solved our biggest headache with beachfront luxury properties—zero moisture absorption, no salt-spray corrosion, and zero splintering around the private infinity pool.",
      author: "Principal Landscape Architect",
      role: "Oceanfront Hospitality Project",
      loc: "Goa, India"
    },
    {
      quote: "Specifying NewTechWood castellated wall cladding gave the corporate tower facade an authentic organic timber warmth while satisfying stringent commercial weatherability and fire performance criteria.",
      author: "Senior Facade Consultant",
      role: "Commercial Headquarters",
      loc: "Gurugram, NCR"
    },
    {
      quote: "The 360-degree capping delivers exactly what our high-end residential clients demand: vibrant exotic wood grain aesthetics with absolutely zero sanding, sealing, or ongoing chemical maintenance.",
      author: "Lead Architectural Designer",
      role: "Private Villa Estate",
      loc: "Alibaug, Maharashtra"
    }
  ];

  const PARTNERS = [
    { name: 'Lumber Life India (National Distribution Partner)' },
    { name: 'Singapore Green Label Certified' },
    { name: 'ISO 9001 Quality Management' },
    { name: 'ISO 14001 Environmental Standard' },
    { name: 'Intertek Green Leaf Certified' },
    { name: 'CE European Conformity Mark' }
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTestimonialMarquee);
  } else {
    initTestimonialMarquee();
  }

  function initTestimonialMarquee() {
    let mount = document.getElementById('ntw-testimonial-marquee');

    if (!mount) {
      const footer = document.querySelector('footer') || document.querySelector('.elementor-location-footer');
      if (!footer) return;
      mount = document.createElement('div');
      mount.id = 'ntw-testimonial-marquee';
      footer.parentNode.insertBefore(mount, footer);
    }

    // Duplicate partners array for seamless infinite marquee loop
    const marqueeItems = [...PARTNERS, ...PARTNERS];

    mount.innerHTML = `
      <section class="ntw-tm-section" aria-label="Architectural Case Studies &amp; Certifications">
        <div class="ntw-tm-container">
          
          <div class="ntw-tm-header">
            <span class="ntw-tm-eyebrow">Architectural Trust</span>
            <h2 class="ntw-tm-title">Specified by Leading Designers &amp; Developers</h2>
          </div>

          <!-- Testimonial Slider -->
          <div class="ntw-tm-slider-wrap">
            <div class="ntw-tm-slider" id="ntw-tm-slider">
              <div class="ntw-tm-track" id="ntw-tm-track">
                ${TESTIMONIALS.map((t, idx) => `
                  <div class="ntw-tm-card" data-card-idx="${idx}">
                    <svg class="ntw-tm-quote-icon" viewBox="0 0 24 24"><path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/></svg>
                    <p class="ntw-tm-quote-text">"${escapeHtml(t.quote)}"</p>
                    <div class="ntw-tm-author-info">
                      <span class="ntw-tm-author-name">${escapeHtml(t.author)}</span>
                      <span class="ntw-tm-author-role">${escapeHtml(t.role)}</span>
                      <span class="ntw-tm-author-loc">${escapeHtml(t.loc)}</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>

            <div class="ntw-tm-controls">
              <button type="button" class="ntw-tm-arrow" id="ntw-tm-prev" aria-label="Previous Testimonial">
                <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
              </button>
              <div class="ntw-tm-dots" id="ntw-tm-dots">
                ${TESTIMONIALS.map((_, idx) => `
                  <button type="button" class="ntw-tm-dot ${idx === 0 ? 'active' : ''}" data-idx="${idx}" aria-label="Testimonial ${idx + 1}"></button>
                `).join('')}
              </div>
              <button type="button" class="ntw-tm-arrow" id="ntw-tm-next" aria-label="Next Testimonial">
                <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
              </button>
            </div>
          </div>

          <!-- Infinite Partner / Certification Marquee -->
          <div class="ntw-marquee-block">
            <div class="ntw-marquee-label">Certified Engineering &amp; Global Standards</div>
            <div class="ntw-marquee-viewport" id="ntw-marquee-viewport">
              <div class="ntw-marquee-track">
                ${marqueeItems.map(p => `
                  <div class="ntw-partner-pill">
                    <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
                    <span>${escapeHtml(p.name)}</span>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>

        </div>
      </section>
    `;

    // Slider Logic
    let currentIdx = 0;
    const track = document.getElementById('ntw-tm-track');
    const slider = document.getElementById('ntw-tm-slider');
    const prevBtn = document.getElementById('ntw-tm-prev');
    const nextBtn = document.getElementById('ntw-tm-next');
    const dots = mount.querySelectorAll('.ntw-tm-dot');

    function goToSlide(idx) {
      if (idx < 0) idx = TESTIMONIALS.length - 1;
      if (idx >= TESTIMONIALS.length) idx = 0;
      currentIdx = idx;

      if (track) {
        track.style.transform = `translateX(-${currentIdx * 100}%)`;
      }

      dots.forEach((d, dIdx) => {
        d.classList.toggle('active', dIdx === currentIdx);
      });
    }

    if (prevBtn) prevBtn.addEventListener('click', () => goToSlide(currentIdx - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => goToSlide(currentIdx + 1));

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => goToSlide(idx));
    });

    // Touch Swipe
    if (slider) {
      let touchStartX = 0;
      let touchEndX = 0;

      slider.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      slider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (Math.abs(touchStartX - touchEndX) > 40) {
          if (touchStartX > touchEndX) {
            goToSlide(currentIdx + 1);
          } else {
            goToSlide(currentIdx - 1);
          }
        }
      }, { passive: true });
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

})();
