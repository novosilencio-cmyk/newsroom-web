(() => {
  const config = window.EXPERIMENTAL_NEWSROOM_ANALYTICS;
  if (config && config.provider === 'umami' && config.enabled) {
    if (!config.scriptUrl || !config.websiteId) {
      console.warn('Experimental Newsroom analytics is enabled but Umami configuration is incomplete.');
    } else {
      const script = document.createElement('script');
      script.defer = true;
      script.src = config.scriptUrl;
      script.dataset.websiteId = config.websiteId;
      script.dataset.domains = window.location.hostname;
      script.dataset.doNotTrack = 'true';
      // Limit Umami to explicit pageviews; do not initialize click/event/performance tracking.
      script.dataset.autoTrack = 'false';
      script.addEventListener('load', () => {
        if (window.umami && typeof window.umami.track === 'function') {
          window.umami.track();
        }
      }, { once: true });
      document.head.appendChild(script);
    }
  }

  if (window.location.pathname.endsWith('/articles/before-then-if-25-public-experiments-2026.html')) {
    const fieldLab = document.createElement('script');
    fieldLab.defer = true;
    fieldLab.src = new URL('field-lab-before.js', document.currentScript.src).href;
    document.head.appendChild(fieldLab);
  }
})();
