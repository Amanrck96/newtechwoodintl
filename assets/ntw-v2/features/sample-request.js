/**
 * F3: Free Sample Request Band + Modal Form
 * Handles sample request dialog, prefilling from color swatch explorer,
 * honeypot spam protection, and WhatsApp routing fallback.
 */

(function () {
  'use strict';

  const WA_NUMBER = '919824144670'; // Gujarat Experience Centre official phone

  function initSampleRequest() {
    const mount = document.getElementById('ntw-sample-request');
    if (!mount) return;

    // Render Band Markup
    mount.innerHTML = `
      <section class="ntw-sample-band" aria-label="Order Sample Kit">
        <div class="ntw-sample-band-inner">
          <div class="ntw-sample-band-text">
            <span class="ntw-sample-badge">Complimentary Architectural Kit</span>
            <h2 class="ntw-sample-title">Feel it before you build it.</h2>
            <p class="ntw-sample-desc">
              Experience the genuine wood grain, dense composite core, and weather-resistant UltraShield 360° capping in your own hands. Free sample kit delivered to your doorstep across India.
            </p>
          </div>
          <div class="ntw-sample-action">
            <button type="button" class="ntw-btn-sample-open" id="ntw-sample-open-btn" aria-haspopup="dialog">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V18z"/></svg>
              <span>Order Free Sample Box</span>
            </button>
          </div>
        </div>
      </section>

      <!-- Accessible Modal Dialog -->
      <div class="ntw-modal-backdrop" id="ntw-sample-modal" role="dialog" aria-modal="true" aria-labelledby="ntw-modal-title" aria-hidden="true">
        <div class="ntw-modal-dialog">
          
          <div class="ntw-modal-header">
            <div class="ntw-modal-header-content">
              <h3 class="ntw-modal-title" id="ntw-modal-title">Request Free Sample Kit</h3>
              <p class="ntw-modal-subtitle">Direct delivery to homeowners, architects, and builders across India.</p>
            </div>
            <button type="button" class="ntw-modal-close-btn" id="ntw-modal-close-btn" aria-label="Close dialog">&times;</button>
          </div>

          <div class="ntw-modal-body">
            
            <!-- Form State -->
            <form id="ntw-sample-form" novalidate>
              
              <!-- Honeypot anti-spam field -->
              <input type="text" name="company_website_url" class="ntw-hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" />

              <div class="ntw-form-grid">
                
                <div class="ntw-form-group" id="group-name">
                  <label class="ntw-form-label" for="ntw-input-name">Full Name <span class="req">*</span></label>
                  <input type="text" id="ntw-input-name" class="ntw-form-input" placeholder="e.g. Rahul Sharma" required />
                  <span class="ntw-form-error-msg">Please enter your name</span>
                </div>

                <div class="ntw-form-group" id="group-phone">
                  <label class="ntw-form-label" for="ntw-input-phone">Phone / WhatsApp <span class="req">*</span></label>
                  <input type="tel" id="ntw-input-phone" class="ntw-form-input" placeholder="e.g. +91 98765 43210" required />
                  <span class="ntw-form-error-msg">Please enter a valid phone number</span>
                </div>

                <div class="ntw-form-group" id="group-email">
                  <label class="ntw-form-label" for="ntw-input-email">Email Address <span class="req">*</span></label>
                  <input type="email" id="ntw-input-email" class="ntw-form-input" placeholder="e.g. rahul@example.com" required />
                  <span class="ntw-form-error-msg">Please enter a valid email address</span>
                </div>

                <div class="ntw-form-group" id="group-city">
                  <label class="ntw-form-label" for="ntw-input-city">Delivery City & State <span class="req">*</span></label>
                  <input type="text" id="ntw-input-city" class="ntw-form-input" placeholder="e.g. Ahmedabad, Gujarat" required />
                  <span class="ntw-form-error-msg">Please enter your city and state</span>
                </div>

                <div class="ntw-form-group">
                  <label class="ntw-form-label" for="ntw-select-product">Product Series</label>
                  <select id="ntw-select-product" class="ntw-form-select">
                    <option value="UltraShield Decking">UltraShield Decking</option>
                    <option value="UltraShield Wall Cladding">UltraShield Wall Cladding</option>
                    <option value="Architectural Screening / Louvers">Architectural Screening / Louvers</option>
                    <option value="Composite Fencing & Railings">Composite Fencing & Railings</option>
                    <option value="DIY Deck Tiles">QuickDeck DIY Tiles</option>
                  </select>
                </div>

                <div class="ntw-form-group">
                  <label class="ntw-form-label" for="ntw-select-color">Preferred Color</label>
                  <select id="ntw-select-color" class="ntw-form-select">
                    <option value="Peruvian Teak">Peruvian Teak (Naturale)</option>
                    <option value="Brazilian IPE">Brazilian IPE (Dark Walnut)</option>
                    <option value="Antique Oak">Antique Oak (Grey Tone)</option>
                    <option value="Canadian Maple">Canadian Maple (Golden Tan)</option>
                    <option value="Spanish Walnut">Spanish Walnut</option>
                    <option value="Hawaiian Charcoal">Hawaiian Charcoal</option>
                    <option value="Full Color Palette Kit">Full Color Palette Kit (All Swatches)</option>
                  </select>
                </div>

                <div class="ntw-form-group full-width">
                  <label class="ntw-form-label" for="ntw-input-address">Delivery Address / Project Notes</label>
                  <textarea id="ntw-input-address" class="ntw-form-textarea" placeholder="Provide postal address or project dimensions for customized sample packaging..."></textarea>
                </div>

              </div>

              <div class="ntw-form-footer">
                <button type="submit" class="ntw-form-submit-btn" id="ntw-form-submit-btn">
                  <span>Submit Sample Request</span>
                  <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                </button>
                <div class="ntw-form-trust-note">
                  🔒 Zero spam. Your details are solely used by our regional team to dispatch your physical sample kit.
                </div>
              </div>

            </form>

            <!-- Success Confirmation Screen -->
            <div class="ntw-modal-success" id="ntw-modal-success" role="status">
              <div class="ntw-success-icon">
                <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
              </div>
              <h4 class="ntw-success-title">Sample Request Received!</h4>
              <p class="ntw-success-text" id="ntw-success-text">
                Thank you! Our regional executive is packing your sample kit. You can also connect instantly on WhatsApp for faster dispatch tracking.
              </p>
              <a href="#" target="_blank" rel="noopener noreferrer" class="ntw-wa-redirect-btn" id="ntw-wa-link">
                <svg viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.12.82.83-3.04-.19-.3a8.21 8.21 0 0 1-1.26-4.48c0-4.54 3.7-8.24 8.24-8.24zm4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.54.61.19 1.16.16 1.6.1.49-.07 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.18-.06-.09-.23-.15-.48-.28z"/></svg>
                <span>Track on WhatsApp</span>
              </a>
            </div>

          </div>

        </div>
      </div>
    `;

    bindEvents();
  }

  function bindEvents() {
    const modal = document.getElementById('ntw-sample-modal');
    const openBtn = document.getElementById('ntw-sample-open-btn');
    const closeBtn = document.getElementById('ntw-modal-close-btn');
    const form = document.getElementById('ntw-sample-form');
    const successBox = document.getElementById('ntw-modal-success');
    const waLink = document.getElementById('ntw-wa-link');
    const colorSelect = document.getElementById('ntw-select-color');

    if (!modal) return;

    function openModal(prefill) {
      if (prefill && prefill.color && colorSelect) {
        // Find best match in select
        for (let i = 0; i < colorSelect.options.length; i++) {
          if (colorSelect.options[i].value.toLowerCase().includes(prefill.color.toLowerCase())) {
            colorSelect.selectedIndex = i;
            break;
          }
        }
      }

      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      // Reset form view if previously successful
      if (form) form.style.display = 'block';
      if (successBox) successBox.classList.remove('active');

      const firstInput = document.getElementById('ntw-input-name');
      if (firstInput) {
        setTimeout(() => firstInput.focus(), 100);
      }
    }

    function closeModal() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (openBtn) openBtn.focus();
    }

    if (openBtn) {
      openBtn.addEventListener('click', () => openModal());
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeModal);
    }

    // Backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Keyboard ESC & Tab trap
    window.addEventListener('keydown', (e) => {
      if (!modal.classList.contains('is-open')) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        closeModal();
        return;
      }

      if (e.key === 'Tab') {
        const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    // Listen for custom trigger from Color Swatch Explorer (F1)
    window.addEventListener('ntw:open-sample-modal', (e) => {
      openModal(e.detail);
    });

    // Form Submission
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();

        // 1. Honeypot test
        const hp = form.querySelector('.ntw-hp-field');
        if (hp && hp.value) {
          // Bot detected, silently show success without sending
          form.style.display = 'none';
          if (successBox) successBox.classList.add('active');
          return;
        }

        // 2. Field Validation
        const nameInput = document.getElementById('ntw-input-name');
        const phoneInput = document.getElementById('ntw-input-phone');
        const emailInput = document.getElementById('ntw-input-email');
        const cityInput = document.getElementById('ntw-input-city');
        const productSelect = document.getElementById('ntw-select-product');
        const colorSelectElem = document.getElementById('ntw-select-color');
        const addressInput = document.getElementById('ntw-input-address');

        let isValid = true;

        function validateField(input, group, condition) {
          if (!condition) {
            group.classList.add('has-error');
            isValid = false;
          } else {
            group.classList.remove('has-error');
          }
        }

        validateField(
          nameInput,
          document.getElementById('group-name'),
          nameInput.value.trim().length >= 2
        );

        validateField(
          phoneInput,
          document.getElementById('group-phone'),
          /^[0-9+() -]{8,15}$/.test(phoneInput.value.trim())
        );

        validateField(
          emailInput,
          document.getElementById('group-email'),
          /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim())
        );

        validateField(
          cityInput,
          document.getElementById('group-city'),
          cityInput.value.trim().length >= 2
        );

        if (!isValid) return;

        // 3. Compose WhatsApp Payload
        const name = nameInput.value.trim();
        const phone = phoneInput.value.trim();
        const email = emailInput.value.trim();
        const city = cityInput.value.trim();
        const product = productSelect.value;
        const color = colorSelectElem.value;
        const address = addressInput.value.trim() || 'Not specified';

        const text = 
`*Free Sample Box Request — NewTechWood India*
----------------------------------------
*Name:* ${name}
*Phone:* ${phone}
*Email:* ${email}
*City:* ${city}
*Product:* ${product}
*Color:* ${color}
*Address/Notes:* ${address}
----------------------------------------
(Sent via newtechwood.in sample portal)`;

        const waUrl = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`;
        if (waLink) {
          waLink.href = waUrl;
        }

        // 4. Update UI to Success State
        form.style.display = 'none';
        if (successBox) successBox.classList.add('active');

        // Optional: auto open WA in background tab
        window.open(waUrl, '_blank', 'noopener,noreferrer');
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
    document.addEventListener('DOMContentLoaded', initSampleRequest);
  } else {
    initSampleRequest();
  }
})();

