/**
 * F10: Newsletter Signup
 * Name + Email + State dropdown with inline validation and confirmation.
 */

(function () {
  'use strict';

  const STATES = [
    'Gujarat', 'Maharashtra', 'Delhi NCR', 'Karnataka', 'Tamil Nadu',
    'Telangana', 'Rajasthan', 'Haryana', 'Uttar Pradesh', 'West Bengal',
    'Punjab', 'Kerala', 'Madhya Pradesh', 'Goa', 'Andhra Pradesh',
    'Chandigarh', 'Bihar', 'Odisha', 'Assam', 'Other State / UT'
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNewsletter);
  } else {
    initNewsletter();
  }

  function initNewsletter() {
    let mount = document.getElementById('ntw-newsletter-signup');

    if (!mount) {
      const anchor = document.getElementById('ntw-testimonial-marquee') || document.querySelector('footer');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-newsletter-signup';
      anchor.parentNode.insertBefore(mount, anchor.nextSibling);
    }

    mount.innerHTML = `
      <section class="ntw-nl-section" aria-label="Architectural Newsletter Subscription">
        <div class="ntw-nl-container">
          
          <div class="ntw-nl-header">
            <span class="ntw-nl-eyebrow">Stay Inspired</span>
            <h2 class="ntw-nl-title">NewTechWood Architecture Digest</h2>
            <p class="ntw-nl-subtitle">Receive quarterly project case studies, new profile launches, and technical specifications directly to your inbox.</p>
          </div>

          <form class="ntw-nl-form" id="ntw-nl-form" novalidate>
            <!-- Honeypot -->
            <input type="text" name="company_website" style="display:none !important;" tabindex="-1" autocomplete="off" class="ntw-nl-hp" />

            <div class="ntw-nl-group" id="ntw-nl-group-name">
              <input type="text" class="ntw-nl-input" id="ntw-nl-name" placeholder="Full Name" required />
              <span class="ntw-nl-error-text">Please enter your name</span>
            </div>

            <div class="ntw-nl-group" id="ntw-nl-group-email">
              <input type="email" class="ntw-nl-input" id="ntw-nl-email" placeholder="Professional Email" required />
              <span class="ntw-nl-error-text">Please enter a valid email</span>
            </div>

            <div class="ntw-nl-group" id="ntw-nl-group-state">
              <select class="ntw-nl-select" id="ntw-nl-state" required>
                <option value="">Select State</option>
                ${STATES.map(s => `<option value="${escapeHtml(s)}">${escapeHtml(s)}</option>`).join('')}
              </select>
              <span class="ntw-nl-error-text">Please select your state</span>
            </div>

            <button type="submit" class="ntw-nl-submit-btn" id="ntw-nl-submit-btn">
              <span>Subscribe</span>
              <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
            </button>
          </form>

          <div class="ntw-nl-success" id="ntw-nl-success" role="status">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            <span>Thank you! You are now subscribed to the NewTechWood Architectural Digest.</span>
          </div>

          <div class="ntw-nl-privacy">
            🔒 Zero spam guarantee. Unsubscribe at any time with one click.
          </div>

        </div>
      </section>
    `;

    const form = document.getElementById('ntw-nl-form');
    const successBox = document.getElementById('ntw-nl-success');
    const nameInput = document.getElementById('ntw-nl-name');
    const emailInput = document.getElementById('ntw-nl-email');
    const stateSelect = document.getElementById('ntw-nl-state');

    const groupName = document.getElementById('ntw-nl-group-name');
    const groupEmail = document.getElementById('ntw-nl-group-email');
    const groupState = document.getElementById('ntw-nl-group-state');

    if (!form) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();

      // Check honeypot
      const hp = form.querySelector('.ntw-nl-hp');
      if (hp && hp.value) {
        form.style.display = 'none';
        if (successBox) successBox.classList.add('active');
        return;
      }

      let isValid = true;

      // Validate Name
      if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {
        groupName.classList.add('has-error');
        isValid = false;
      } else {
        groupName.classList.remove('has-error');
      }

      // Validate Email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailInput.value.trim())) {
        groupEmail.classList.add('has-error');
        isValid = false;
      } else {
        groupEmail.classList.remove('has-error');
      }

      // Validate State
      if (!stateSelect.value) {
        groupState.classList.add('has-error');
        isValid = false;
      } else {
        groupState.classList.remove('has-error');
      }

      if (!isValid) return;

      // Save locally
      try {
        localStorage.setItem('ntw_newsletter_subscriber', JSON.stringify({
          name: nameInput.value.trim(),
          email: emailInput.value.trim(),
          state: stateSelect.value,
          date: new Date().toISOString()
        }));
      } catch (err) {
        // storage disabled fallback
      }

      // Show animated success
      form.style.display = 'none';
      if (successBox) {
        successBox.classList.add('active');
      }
    });

    // Clear error on input
    nameInput.addEventListener('input', () => groupName.classList.remove('has-error'));
    emailInput.addEventListener('input', () => groupEmail.classList.remove('has-error'));
    stateSelect.addEventListener('change', () => groupState.classList.remove('has-error'));
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
