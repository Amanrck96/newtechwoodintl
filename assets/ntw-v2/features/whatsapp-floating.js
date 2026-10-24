/**
 * F7: WhatsApp Floating Button + Mobile Action Bar
 * Instant WhatsApp assistance and sticky bottom mobile action bar.
 */

(function () {
  'use strict';

  const WA_NUMBER = '919824144670';
  const PREFILLED_MSG = 'Hi, I am interested in NewTechWood products.';
  const WA_URL = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(PREFILLED_MSG)}`;

  function initWhatsAppWidget() {
    createFloatingButton();
    createMobileActionBar();
  }

  function createFloatingButton() {
    if (document.getElementById('ntw-wa-float')) return;

    const btn = document.createElement('a');
    btn.href = WA_URL;
    btn.target = '_blank';
    btn.rel = 'noopener noreferrer';
    btn.id = 'ntw-wa-float';
    btn.className = 'ntw-wa-floating-btn';
    btn.setAttribute('aria-label', 'Chat on WhatsApp with NewTechWood Specialist');

    btn.innerHTML = `
      <span class="ntw-wa-online-dot"></span>
      <span class="ntw-wa-tooltip">Chat with NewTechWood India</span>
      <svg viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.12.82.83-3.04-.19-.3a8.21 8.21 0 0 1-1.26-4.48c0-4.54 3.7-8.24 8.24-8.24zm4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.54.61.19 1.16.16 1.6.1.49-.07 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.18-.06-.09-.23-.15-.48-.28z"/></svg>
    `;

    document.body.appendChild(btn);
  }

  function createMobileActionBar() {
    if (document.getElementById('ntw-mobile-bar')) return;

    const bar = document.createElement('nav');
    bar.id = 'ntw-mobile-bar';
    bar.className = 'ntw-mobile-action-bar';
    bar.setAttribute('aria-label', 'Quick mobile actions');

    bar.innerHTML = `
      <div class="ntw-mab-inner">
        
        <!-- Action 1: Centres -->
        <a href="/#experience-centre" class="ntw-mab-btn" aria-label="Find Experience Centres">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          <span>Centres</span>
        </a>

        <!-- Action 2: WhatsApp -->
        <a href="${WA_URL}" target="_blank" rel="noopener noreferrer" class="ntw-mab-btn" aria-label="Chat on WhatsApp">
          <svg viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.12.82.83-3.04-.19-.3a8.21 8.21 0 0 1-1.26-4.48c0-4.54 3.7-8.24 8.24-8.24zm4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.54.61.19 1.16.16 1.6.1.49-.07 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.18-.06-.09-.23-.15-.48-.28z"/></svg>
          <span>WhatsApp</span>
        </a>

        <!-- Action 3: Free Sample (Primary) -->
        <button type="button" class="ntw-mab-btn primary" id="ntw-mab-sample-btn" aria-label="Request Free Sample Box">
          <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V18z"/></svg>
          <span>Free Sample</span>
        </button>

        <!-- Action 4: Direct Phone Call -->
        <a href="tel:+919824144670" class="ntw-mab-btn" id="ntw-mab-call-btn" aria-label="Call NewTechWood India">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>Call</span>
        </a>

      </div>
    `;

    document.body.appendChild(bar);

    // Bind Sample Button
    const sampleBtn = bar.querySelector('#ntw-mab-sample-btn');
    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal'));
        const modal = document.getElementById('ntw-sample-modal');
        if (modal) {
          modal.classList.add('is-open');
          modal.setAttribute('aria-hidden', 'false');
          document.body.style.overflow = 'hidden';
        } else {
          // If on a subpage where modal isn't mounted, navigate to homepage sample section
          window.location.href = '/#ntw-sample-request';
        }
      });
    }
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWhatsAppWidget);
  } else {
    initWhatsAppWidget();
  }
})();

