/**
 * F3: Hero Promo Banners
 * Auto-rotating promotional cards featuring real site solutions:
 * Decking, Cladding, Louvers, and Experience Centres.
 * Swipeable on mobile, pause on hover, dots + arrow controls, prefers-reduced-motion.
 */

(function () {
  'use strict';

  const BANNERS = [
    {
      tag: 'Architectural Outdoor Flooring',
      title: 'UltraShield® Naturale Composite Decking',
      desc: 'Engineered with 360-degree capping for total defense against stains, fading, and intense monsoon dampness. Covered by a 25-year structural warranty.',
      btnText: 'Explore Decking Systems',
      url: '/product/decking/',
      img: '/wp-content/uploads/2025/09/NewTechWood-decking.jpg',
      alt: 'NewTechWood UltraShield composite decking poolside installation'
    },
    {
      tag: 'Facade Innovation',
      title: 'All-Weather & Castellated Wall Cladding',
      desc: 'Distinctive fluted profiles and architectural shadowlines designed to elevate residential facades, modern villas, and commercial exteriors across India.',
      btnText: 'Explore Cladding Profiles',
      url: '/product/cladding/',
      img: '/wp-content/uploads/2025/09/NewTechWood-cladding.jpg',
      alt: 'Architectural composite wall cladding facade with castellated wood texture'
    },
    {
      tag: 'Solar Shading & Privacy',
      title: 'Architectural Louvers, Screening & Beams',
      desc: 'Lightweight composite beams and continuous louvers delivering natural sunlight diffusion, aesthetic depth, and privacy without warp or rot.',
      btnText: 'Explore Louvers & Beams',
      url: '/product/screening/',
      img: '/wp-content/uploads/2025/09/beams.jpg',
      alt: 'NewTechWood architectural composite screening and exterior louvers'
    },
    {
      tag: 'National Presence',
      title: 'Experience Centres in Ahmedabad, Delhi, Mumbai & Bengaluru',
      desc: 'Touch full-scale architectural installations, test sample swatches in natural daylight, and consult our technical specialists at our dedicated regional studios.',
      btnText: 'Find an Experience Centre',
      url: '/#experience-centre',
      img: '/wp-content/uploads/2025/08/NewTechWood-History.jpg',
      alt: 'NewTechWood state-of-the-art architectural experience centre in India'
    }
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroPromoBanners);
  } else {
    initHeroPromoBanners();
  }

  function initHeroPromoBanners() {
    let mount = document.getElementById('ntw-hero-promo-banners');

    if (!mount) {
      // Find the hero video container and insert after it
      const hero = document.querySelector('.elementor-element-b91bda7') || document.querySelector('.elementor-location-header');
      if (!hero) return;
      mount = document.createElement('div');
      mount.id = 'ntw-hero-promo-banners';
      hero.parentNode.insertBefore(mount, hero.nextSibling);
    }

    let currentIndex = 0;
    let timer = null;
    let isPaused = false;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    mount.innerHTML = `
      <section class="ntw-hero-promo-section" aria-label="Featured Architectural Highlights">
        <div class="ntw-hero-promo-container">
          
          <div class="ntw-hero-promo-header">
            <div>
              <div class="ntw-hero-promo-eyebrow">Architectural Highlights</div>
              <h2 class="ntw-hero-promo-title">Featured UltraShield® Applications</h2>
            </div>
            <div class="ntw-hero-promo-controls">
              <button type="button" class="ntw-hero-promo-arrow" id="ntw-hp-prev" aria-label="Previous Highlight">
                <svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
              </button>
              <button type="button" class="ntw-hero-promo-arrow" id="ntw-hp-next" aria-label="Next Highlight">
                <svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
              </button>
            </div>
          </div>

          <div class="ntw-hero-promo-slider" id="ntw-hp-slider">
            <div class="ntw-hero-promo-track" id="ntw-hp-track">
              ${BANNERS.map((b, idx) => `
                <div class="ntw-hero-promo-card" data-card-index="${idx}">
                  <div class="ntw-hero-promo-card-content">
                    <span class="ntw-hero-promo-card-tag">${escapeHtml(b.tag)}</span>
                    <h3 class="ntw-hero-promo-card-h3">${escapeHtml(b.title)}</h3>
                    <p class="ntw-hero-promo-card-desc">${escapeHtml(b.desc)}</p>
                    <a href="${b.url}" class="ntw-hero-promo-card-btn">
                      <span>${escapeHtml(b.btnText)}</span>
                      <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </a>
                  </div>
                  <div class="ntw-hero-promo-card-media">
                    <img src="${b.img}" alt="${escapeHtml(b.alt)}" class="ntw-hero-promo-card-img" loading="lazy" />
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="ntw-hero-promo-dots" id="ntw-hp-dots" role="tablist" aria-label="Slide Selection">
            ${BANNERS.map((_, idx) => `
              <button type="button" class="ntw-hero-promo-dot ${idx === 0 ? 'active' : ''}" data-dot-index="${idx}" role="tab" aria-selected="${idx === 0 ? 'true' : 'false'}" aria-label="Slide ${idx + 1}"></button>
            `).join('')}
          </div>

        </div>
      </section>
    `;

    const track = document.getElementById('ntw-hp-track');
    const slider = document.getElementById('ntw-hp-slider');
    const prevBtn = document.getElementById('ntw-hp-prev');
    const nextBtn = document.getElementById('ntw-hp-next');
    const dots = mount.querySelectorAll('.ntw-hero-promo-dot');

    function goToSlide(index) {
      if (index < 0) {
        index = BANNERS.length - 1;
      } else if (index >= BANNERS.length) {
        index = 0;
      }
      currentIndex = index;

      if (track) {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
      }

      dots.forEach((dot, idx) => {
        const isActive = idx === currentIndex;
        dot.classList.toggle('active', isActive);
        dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
    }

    function nextSlide() {
      goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      goToSlide(currentIndex - 1);
    }

    // Button controls
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => goToSlide(idx));
    });

    // Auto-rotation timer
    function startAutoPlay() {
      if (reducedMotion) return;
      stopAutoPlay();
      timer = setInterval(() => {
        if (!isPaused) {
          nextSlide();
        }
      }, 5000);
    }

    function stopAutoPlay() {
      if (timer) clearInterval(timer);
    }

    if (slider) {
      slider.addEventListener('mouseenter', () => { isPaused = true; });
      slider.addEventListener('mouseleave', () => { isPaused = false; });
      slider.addEventListener('focusin', () => { isPaused = true; });
      slider.addEventListener('focusout', () => { isPaused = false; });

      // Touch / Swipe support
      let touchStartX = 0;
      let touchEndX = 0;

      slider.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        isPaused = true;
      }, { passive: true });

      slider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        isPaused = false;
        handleSwipe();
      }, { passive: true });

      function handleSwipe() {
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 45) {
          if (diff > 0) {
            nextSlide(); // swipe left
          } else {
            prevSlide(); // swipe right
          }
        }
      }
    }

    startAutoPlay();
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
