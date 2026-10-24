/**
 * F6: Count-Up Stats
 * Animated counter that triggers once when scrolled into view (1.5s easeOut).
 * Uses real, verified figures from existing site copy.
 */

(function () {
  'use strict';

  const STATS = [
    {
      target: 30,
      suffix: '+',
      label: 'Years of Innovation',
      desc: 'Pioneering composite extrusion technology and sustainable wood-polymer chemistry since 2004.'
    },
    {
      target: 10,
      suffix: 'M+ m²',
      label: 'Installed Globally',
      desc: 'Specified across high-traffic resorts, commercial facades, and luxury residences worldwide.'
    },
    {
      target: 25,
      suffix: ' Years',
      label: 'Transferable Warranty',
      desc: 'Industry-leading warranty backing against stain, fade, structural cracking, and rot.'
    },
    {
      target: 95,
      suffix: '%',
      label: 'Recycled Materials',
      desc: 'Manufactured from reclaimed dense hardwood fiber and recycled plastic bottles.'
    }
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCountUpStats);
  } else {
    initCountUpStats();
  }

  function initCountUpStats() {
    let mount = document.getElementById('ntw-count-up-stats');

    if (!mount) {
      const anchor = document.getElementById('ntw-sample-request') || document.querySelector('.ll-experience-centre') || document.querySelector('footer');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-count-up-stats';
      anchor.parentNode.insertBefore(mount, anchor);
    }

    mount.innerHTML = `
      <section class="ntw-stats-section" aria-label="NewTechWood Key Performance Figures">
        <div class="ntw-stats-container">
          
          <div class="ntw-stats-header">
            <span class="ntw-stats-eyebrow">Proven Performance</span>
            <h2 class="ntw-stats-title">Global Engineering. Tested Across Continents.</h2>
          </div>

          <div class="ntw-stats-grid" id="ntw-stats-grid">
            ${STATS.map((s, idx) => `
              <div class="ntw-stat-card">
                <div class="ntw-stat-num-wrap">
                  <span class="ntw-stat-number" id="ntw-stat-val-${idx}" data-target="${s.target}">0</span>
                  <span class="ntw-stat-suffix">${escapeHtml(s.suffix)}</span>
                </div>
                <div class="ntw-stat-label">${escapeHtml(s.label)}</div>
                <p class="ntw-stat-desc">${escapeHtml(s.desc)}</p>
              </div>
            `).join('')}
          </div>

        </div>
      </section>
    `;

    const section = mount.querySelector('.ntw-stats-section');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!section) return;

    if (reducedMotion || !('IntersectionObserver' in window)) {
      // Instant display
      STATS.forEach((s, idx) => {
        const el = document.getElementById(`ntw-stat-val-${idx}`);
        if (el) el.textContent = s.target;
      });
      return;
    }

    let hasAnimated = false;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !hasAnimated) {
          hasAnimated = true;
          animateStats();
          observer.disconnect();
        }
      });
    }, { threshold: 0.25 });

    observer.observe(section);

    function animateStats() {
      const duration = 1500; // 1.5s
      const startTime = performance.now();

      function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // easeOutExpo
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);

        STATS.forEach((s, idx) => {
          const el = document.getElementById(`ntw-stat-val-${idx}`);
          if (el) {
            const current = Math.round(s.target * ease);
            el.textContent = current;
          }
        });

        if (progress < 1) {
          requestAnimationFrame(update);
        }
      }

      requestAnimationFrame(update);
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
