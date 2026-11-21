/**
 * Clarity Website — Interactive Frontend Engine
 * Avail Technologies (Pvt) Ltd.
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initSweetAlertGlobal();
  initMobileNav();
  initScrollHeader();
  initEcosystemTabs();
  initPricingToggle();
  initNewsletterAjax();
  initContactAjax();
  initHoverPrefetch();
  initLiveInstructionFilter();
});

// Global SweetAlert2 Interceptor & Theme Helper
function initSweetAlertGlobal() {
  if (typeof window !== 'undefined' && window.Swal) {
    // Intercept native window.alert
    window.alert = function (message) {
      window.Swal.fire({
        icon: 'info',
        title: 'Notice',
        text: message,
        background: '#102746',
        color: '#ffffff',
        confirmButtonColor: '#c5a253',
        customClass: {
          popup: 'apple-glass-swal'
        }
      });
    };

    // Auto-detect and render any Django server messages with SweetAlert2 Toast
    const djangoMessages = document.querySelectorAll('.server-message-item');
    djangoMessages.forEach(el => {
      const type = el.getAttribute('data-type') || 'info';
      const text = el.textContent.trim();
      const icon = type.includes('success') ? 'success' : (type.includes('error') ? 'error' : 'info');
      window.Swal.fire({
        toast: true,
        position: 'top-end',
        icon: icon,
        title: text,
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: '#102746',
        color: '#ffffff'
      });
    });
  }
}

// Mobile Navigation & Dropdowns
function initMobileNav() {
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const navMenu = document.getElementById('navMenu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      navMenu.classList.toggle('show');
      const icon = toggleBtn.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
      }
    });

    // Handle dropdown toggles on mobile/tablet screens
    const dropdownToggles = navMenu.querySelectorAll('.nav-dropdown-toggle');
    dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024) {
          e.preventDefault();
          e.stopPropagation();
          const parentItem = toggle.closest('.has-dropdown');
          if (parentItem) {
            navMenu.querySelectorAll('.has-dropdown').forEach(item => {
              if (item !== parentItem) item.classList.remove('open');
            });
            parentItem.classList.toggle('open');
          }
        }
      });
    });

    // Close when clicking simple nav links (non-dropdown)
    navMenu.querySelectorAll('.nav-item:not(.has-dropdown) .nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('show');
        const icon = toggleBtn.querySelector('i');
        if (icon) {
          icon.classList.add('fa-bars');
          icon.classList.remove('fa-times');
        }
      });
    });

    // Close when clicking sub-items or sub-buttons inside dropdowns
    navMenu.querySelectorAll('.nav-sub-item, .nav-sub-btn').forEach(subLink => {
      subLink.addEventListener('click', () => {
        navMenu.classList.remove('show');
        const icon = toggleBtn.querySelector('i');
        if (icon) {
          icon.classList.add('fa-bars');
          icon.classList.remove('fa-times');
        }
      });
    });

    // Close when clicking outside header
    document.addEventListener('click', (e) => {
      if (navMenu.classList.contains('show') && !navMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
        navMenu.classList.remove('show');
        const icon = toggleBtn.querySelector('i');
        if (icon) {
          icon.classList.add('fa-bars');
          icon.classList.remove('fa-times');
        }
      }
    });
  }
}

// Header Sticky Elevation on Scroll
function initScrollHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const onScroll = () => {
    if (window.scrollY > 8) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// Ecosystem Architecture Interactive Switcher
function initEcosystemTabs() {
  const tabBtns = document.querySelectorAll('.eco-tab-btn');
  const contentPanes = document.querySelectorAll('.eco-content-pane');

  if (!tabBtns.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');

      tabBtns.forEach(b => b.classList.remove('active'));
      contentPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(targetId);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
}

// Universal Apple Pricing Toggle Engine (Monthly vs Annual with animation)
function initPricingToggle() {
  // 1. Generic product / service / plan billing toggles
  const toggles = document.querySelectorAll('.product-billing-toggle, .service-billing-toggle, #billingToggle');
  toggles.forEach(toggle => {
    toggle.addEventListener('change', (e) => {
      const isAnnual = e.target.checked;
      const switcherWrap = toggle.closest('.billing-switcher-wrap') || toggle.parentElement;
      if (switcherWrap) {
        const monthlyLabel = switcherWrap.querySelector('.billing-label-monthly');
        const annualLabel = switcherWrap.querySelector('.billing-label-annual');
        if (monthlyLabel && annualLabel) {
          monthlyLabel.classList.toggle('active', !isAnnual);
          annualLabel.classList.toggle('active', isAnnual);
        }
      }

      // Update all pricing elements in the container or on page
      const section = toggle.closest('#pricing-section') || toggle.closest('.section-wrap') || document;
      const priceDisplays = section.querySelectorAll('.tier-price-display');
      const periodDisplays = section.querySelectorAll('.tier-period-display');

      priceDisplays.forEach(el => {
        const targetVal = isAnnual ? el.getAttribute('data-annual') : el.getAttribute('data-monthly');
        if (targetVal) {
          el.style.opacity = '0.3';
          el.style.transform = 'translateY(-4px)';
          setTimeout(() => {
            el.textContent = targetVal;
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
          }, 100);
        }
      });

      periodDisplays.forEach(el => {
        const targetPeriod = isAnnual ? el.getAttribute('data-annual') : el.getAttribute('data-monthly');
        if (targetPeriod) {
          el.textContent = targetPeriod;
        }
      });
    });
  });

  // Click on labels to toggle
  document.querySelectorAll('.billing-switcher-wrap').forEach(wrap => {
    const monthlyLabel = wrap.querySelector('.billing-label-monthly');
    const annualLabel = wrap.querySelector('.billing-label-annual');
    const checkbox = wrap.querySelector('input[type="checkbox"]');
    if (checkbox) {
      if (monthlyLabel) {
        monthlyLabel.addEventListener('click', () => {
          if (checkbox.checked) {
            checkbox.checked = false;
            checkbox.dispatchEvent(new Event('change'));
          }
        });
      }
      if (annualLabel) {
        annualLabel.addEventListener('click', () => {
          if (!checkbox.checked) {
            checkbox.checked = true;
            checkbox.dispatchEvent(new Event('change'));
          }
        });
      }
    }
  });

  // 2. Individual service cards with separate billing toggles
  const serviceToggles = document.querySelectorAll('.service-billing-toggle');
  serviceToggles.forEach(st => {
    st.addEventListener('change', (e) => {
      const isAnnual = e.target.checked;
      const card = st.closest('.bento-card') || st.closest('.service-card') || st.parentElement;
      const switcherWrap = st.closest('.billing-switcher-wrap');
      if (switcherWrap) {
        const monthlyLabel = switcherWrap.querySelector('.billing-label-monthly');
        const annualLabel = switcherWrap.querySelector('.billing-label-annual');
        if (monthlyLabel && annualLabel) {
          monthlyLabel.classList.toggle('active', !isAnnual);
          annualLabel.classList.toggle('active', isAnnual);
        }
      }

      if (card) {
        const priceEl = card.querySelector('.tier-price-display');
        const periodEl = card.querySelector('.tier-period-display');
        if (priceEl) {
          const val = isAnnual ? priceEl.getAttribute('data-annual') : priceEl.getAttribute('data-monthly');
          if (val) {
            priceEl.style.opacity = '0.3';
            setTimeout(() => {
              priceEl.textContent = val;
              priceEl.style.opacity = '1';
            }, 100);
          }
        }
        if (periodEl) {
          const p = isAnnual ? periodEl.getAttribute('data-annual') : periodEl.getAttribute('data-monthly');
          if (p) periodEl.textContent = p;
        }
      }
    });
  });
}

// Newsletter Subscription via AJAX
function initNewsletterAjax() {
  const form = document.getElementById('newsletterForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const emailInput = form.querySelector('input[type="email"]');
    const submitBtn = form.querySelector('button');
    const email = emailInput ? emailInput.value.trim() : '';

    if (!email) return;

    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    try {
      const csrfToken = getCookie('csrftoken') || '';
      const response = await fetch('/contact/newsletter/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();
      if (window.Swal) {
        Swal.fire({
          icon: data.status === 'success' ? 'success' : 'info',
          title: data.status === 'success' ? 'Subscribed!' : 'Notice',
          text: data.message,
          background: '#102746',
          color: '#ffffff',
          confirmButtonColor: '#c5a253'
        });
      } else {
        alert(data.message);
      }

      if (data.status === 'success') {
        form.reset();
      }
    } catch (err) {
      console.error(err);
      if (window.Swal) {
        Swal.fire({
          icon: 'error',
          title: 'Subscription Failed',
          text: 'Unable to connect right now. Please try again later.',
          background: '#102746',
          color: '#ffffff',
          confirmButtonColor: '#c5a253'
        });
      }
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
}

// Contact & Demo Form AJAX
function initContactAjax() {
  const forms = document.querySelectorAll('form[data-ajax="true"]');
  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
      }

      const formData = new FormData(form);
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: formData,
        });

        const data = await response.json();
        if (response.ok && data.status === 'success') {
          if (window.Swal) {
            Swal.fire({
              icon: 'success',
              title: 'Request Received!',
              text: data.message,
              background: '#102746',
              color: '#ffffff',
              confirmButtonColor: '#c5a253'
            }).then(() => {
              form.reset();
            });
          } else {
            alert(data.message);
            form.reset();
          }
        } else {
          throw new Error(data.message || 'Submission failed');
        }
      } catch (err) {
        if (window.Swal) {
          Swal.fire({
            icon: 'error',
            title: 'Submission Error',
            text: err.message || 'An error occurred. Please try again.',
            background: '#102746',
            color: '#ffffff',
            confirmButtonColor: '#c5a253'
          });
        } else {
          alert(err.message || 'Submission error');
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnText;
        }
      }
    });
  });
}

// Utility CSRF Cookie helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Theme Toggle (Light / Dark mode switcher with persistence)
function initThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  if (!toggleBtn) return;

  const updateIcon = (theme) => {
    const icon = toggleBtn.querySelector('i');
    if (icon) {
      if (theme === 'dark') {
        icon.className = 'fas fa-sun';
        toggleBtn.setAttribute('title', 'Switch to Light Mode');
      } else {
        icon.className = 'fas fa-moon';
        toggleBtn.setAttribute('title', 'Switch to Dark Mode');
      }
    }
  };

  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  updateIcon(currentTheme);

  toggleBtn.addEventListener('click', () => {
    const active = document.documentElement.getAttribute('data-theme') || 'light';
    const nextTheme = active === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    localStorage.setItem('avail_theme', nextTheme);
    updateIcon(nextTheme);
  });
}

/**
 * AJAX Link Hover Prefetcher
 * Detects internal navigation links and silently pre-fetches the HTML
 * during the 65-150ms mouse hover before the user clicks, resulting
 * in instant 0ms perceived navigation across the site.
 */
function initHoverPrefetch() {
  const prefetchedUrls = new Set();

  const prefetchUrl = (url) => {
    if (!url || prefetchedUrls.has(url)) return;

    try {
      const parsed = new URL(url, window.location.href);
      if (parsed.origin !== window.location.origin) return;
      if (parsed.pathname === window.location.pathname && parsed.search === window.location.search) return;
      // Skip static assets, media, admin, logout, and file extensions
      if (parsed.pathname.match(/\.(png|jpg|jpeg|webp|svg|pdf|zip|css|js)$/i)) return;
      if (parsed.pathname.startsWith('/admin') || parsed.pathname.startsWith('/static') || parsed.pathname.startsWith('/media')) return;

      prefetchedUrls.add(url);

      // Use native prefetch link
      const link = document.createElement('link');
      link.rel = 'prefetch';
      link.href = url;
      link.as = 'document';
      document.head.appendChild(link);
    } catch (e) {
      // Ignore invalid URLs
    }
  };

  const attachPrefetchListeners = () => {
    const links = document.querySelectorAll('a[href^="/"], a[href^="' + window.location.origin + '"]');
    links.forEach(a => {
      const href = a.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

      let timer = null;
      a.addEventListener('mouseenter', () => {
        timer = setTimeout(() => prefetchUrl(href), 65);
      }, { passive: true });

      a.addEventListener('mouseleave', () => {
        if (timer) clearTimeout(timer);
      }, { passive: true });

      a.addEventListener('touchstart', () => {
        prefetchUrl(href);
      }, { passive: true });
    });
  };

  attachPrefetchListeners();
}

/**
 * Live Client-Side Filter for Product Manuals / Instructions
 */
function initLiveInstructionFilter() {
  const searchInput = document.getElementById('instructionSearchInput');
  const cards = document.querySelectorAll('.instruction-card');
  if (!searchInput || !cards.length) return;

  searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase().trim();
    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      if (!term || text.includes(term)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

