/**
 * F18: Micro-Interactions, Scroll Reveals & Polish
 * IntersectionObserver scroll reveals, smooth offset anchor scrolling,
 * and image fade-in with prefers-reduced-motion support.
 */

(function () {
  'use strict';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMicroInteractions);
  } else {
    initMicroInteractions();
  }

  function initMicroInteractions() {
    setupScrollReveals();
    setupSmoothAnchorScroll();
    setupImageFadeIns();
  }

  function setupScrollReveals() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return;
    }

    if (!('IntersectionObserver' in window)) {
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('ntw-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -40px 0px',
      threshold: 0.1
    });

    // Select major sections & cards to apply reveals
    const targets = document.querySelectorAll(`
      .ntw-sample-band,
      .ntw-swatch-explorer,
      .ntw-hotspots-card,
      .ntw-boq-grid,
      .ntw-brochure-card,
      .ntw-pro-card,
      .ntw-nl-container,
      .ll-ec-card
    `);

    targets.forEach((el, index) => {
      el.classList.add('ntw-reveal');
      // If inside a grid, stagger
      if (el.classList.contains('ntw-brochure-card') || el.classList.contains('ntw-pro-card') || el.classList.contains('ll-ec-card')) {
        const delayClass = `ntw-reveal-delay-${(index % 3) + 1}`;
        el.classList.add(delayClass);
      }
      observer.observe(el);
    });
  }

  function setupSmoothAnchorScroll() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;

      const hash = link.getAttribute('href');
      if (hash === '#' || hash === '') return;

      const target = document.querySelector(hash);
      if (target) {
        e.preventDefault();
        const headerOffset = 80;
        const targetPos = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: targetPos,
          behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
        });

        // Update URL hash without jump
        if (history.pushState) {
          history.pushState(null, null, hash);
        }
      }
    });
  }

  function setupImageFadeIns() {
    const images = document.querySelectorAll('img[data-src], .ntw-se-img, .ntw-cat-img');
    images.forEach(img => {
      if (img.complete) {
        img.classList.add('ntw-image-loaded');
      } else {
        img.classList.add('ntw-fade-in-ready');
        img.addEventListener('load', () => {
          img.classList.add('ntw-image-loaded');
        }, { once: true });
      }
    });
  }
})();
