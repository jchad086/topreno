/* ==========================================================================
   TOP Reno — site behaviour
   Vanilla JS, no dependencies. Loaded with `defer`.
   ========================================================================== */
(function () {
  'use strict';

  /* --- Mobile navigation ------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    // Close the drawer on Escape.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });

    // Close when a link is tapped (same-page anchors would otherwise stay open).
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Reset state if the viewport grows past the desktop breakpoint.
    var mq = window.matchMedia('(min-width: 900px)');
    var reset = function (e) {
      if (e.matches) {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    };
    mq.addEventListener ? mq.addEventListener('change', reset) : mq.addListener(reset);
  }

  /* --- Scroll reveal ----------------------------------------------------- */
  var revealables = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // No observer support, or the visitor asked for less motion: show everything.
    Array.prototype.forEach.call(revealables, function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
  }

  /* --- Contact form ------------------------------------------------------ */
  var form = document.getElementById('contactForm');
  if (!form) return;

  var btn = form.querySelector('.btn-submit');
  var okMsg = document.getElementById('formOk');
  var errMsg = document.getElementById('formErr');
  var btnLabel = btn ? btn.innerHTML : '';

  function showOnly(el) {
    if (okMsg) okMsg.classList.remove('show');
    if (errMsg) errMsg.classList.remove('show');
    if (el) el.classList.add('show');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot: real people never fill this in.
    var trap = form.querySelector('input[name="_gotcha"]');
    if (trap && trap.value) return;

    // The endpoint still holds the placeholder — fail loudly rather than silently.
    if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
      showOnly(errMsg);
      return;
    }

    if (btn) {
      btn.disabled = true;
      btn.innerHTML = 'Sending&hellip;';
    }
    showOnly(null);

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (res) {
        if (res.ok) {
          form.reset();
          showOnly(okMsg);
          if (btn) btn.innerHTML = 'Message sent';
          if (okMsg) okMsg.focus();
        } else {
          throw new Error('Bad response');
        }
      })
      .catch(function () {
        showOnly(errMsg);
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = btnLabel;
        }
      });
  });
})();
