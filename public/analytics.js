(() => {
  const config = window.EXPERIMENTAL_NEWSROOM_ANALYTICS;
  if (!config || config.provider !== 'umami' || !config.enabled) return;
  if (!config.scriptUrl || !config.websiteId) {
    console.warn('Experimental Newsroom analytics is enabled but Umami configuration is incomplete.');
    return;
  }

  const script = document.createElement('script');
  script.defer = true;
  script.src = config.scriptUrl;
  script.dataset.websiteId = config.websiteId;
  script.dataset.domains = window.location.hostname;
  script.dataset.doNotTrack = 'true';
  document.head.appendChild(script);
})();
