(() => {
  const config = window.EXPERIMENTAL_NEWSROOM_ANALYTICS;
  const consentKey = 'en-analytics-consent-v1';
  const bannerId = 'en-analytics-consent-banner';

  function savedChoice() {
    try {
      const choice = window.localStorage.getItem(consentKey);
      return choice === 'granted' || choice === 'denied' ? choice : null;
    } catch {
      return null;
    }
  }

  function remember(choice) {
    try {
      window.localStorage.setItem(consentKey, choice);
    } catch {
      // The visitor's explicit choice still applies to this page load.
    }
  }

  function doNotTrack() {
    return navigator.doNotTrack === '1' || window.doNotTrack === '1';
  }

  function startTracking() {
    if (!config || config.provider !== 'umami' || !config.enabled ||
        savedChoice() !== 'granted' || doNotTrack() ||
        !config.scriptUrl || !config.websiteId ||
        document.getElementById('en-umami-script')) return;

    const script = document.createElement('script');
    script.id = 'en-umami-script';
    script.defer = true;
    script.src = config.scriptUrl;
    script.dataset.websiteId = config.websiteId;
    script.dataset.domains = window.location.hostname;
    script.dataset.doNotTrack = 'true';
    // Disable automatic views, clicks and other events. Send a minimal pageview below.
    script.dataset.autoTrack = 'false';
    script.addEventListener('load', () => {
      if (window.umami && typeof window.umami.track === 'function') {
        // Do not send query strings, referrers, screen size or arbitrary event data.
        window.umami.track({
          website: config.websiteId,
          url: window.location.pathname,
          title: document.title
        });
      }
    }, { once: true });
    document.head.appendChild(script);
  }

  function showConsent() {
    if (document.getElementById(bannerId) || !document.body) return;
    const isNorwegian = /^(nb|no)(-|$)/i.test(document.documentElement.lang || '');
    const banner = document.createElement('section');
    banner.id = bannerId;
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-labelledby', 'en-analytics-consent-title');

    const style = document.createElement('style');
    style.textContent = `
      #${bannerId}{position:fixed;z-index:10000;left:1rem;right:1rem;bottom:1rem;max-width:48rem;margin:auto;padding:1rem 1.1rem;background:#fff;color:#171717;border:2px solid #171717;box-shadow:0 8px 30px #0003;font:16px/1.5 system-ui,sans-serif}
      #${bannerId} h2{font:700 1.15rem/1.25 system-ui,sans-serif;margin:0 0 .4rem}
      #${bannerId} p{margin:.3rem 0 .8rem}
      #${bannerId} a{color:inherit}
      #${bannerId} .en-consent-actions{display:flex;flex-wrap:wrap;gap:.6rem}
      #${bannerId} button{font:600 1rem system-ui,sans-serif;padding:.55rem .85rem;border:2px solid #171717;background:#fff;color:#171717;cursor:pointer}
      #${bannerId} button:first-child{background:#171717;color:#fff}
      @media(prefers-reduced-motion:reduce){#${bannerId}{scroll-behavior:auto}}
    `;
    const title = document.createElement('h2');
    title.id = 'en-analytics-consent-title';
    title.textContent = isNorwegian ? 'Vil du bidra til besøksstatistikk?' : 'Would you like to contribute to audience statistics?';
    const description = document.createElement('p');
    description.textContent = isNorwegian
      ? 'Hvis du tillater det, sender vi én sidevisning til Umami Cloud. Vi sender sidesti uten søkestreng og sidetittel. Umami mottar tekniske opplysninger som IP-adresse og nettleserdata for å beregne statistikk. Avslag stopper sporeren. Du kan endre valget på personvernsiden.'
      : 'If you allow it, we send one page view to Umami Cloud. We send the page path without its query string and the page title. Umami receives technical data such as IP address and browser data to calculate statistics. Declining prevents the tracker from loading. You can change your choice on the privacy page.';
    const details = document.createElement('p');
    const link = document.createElement('a');
    link.href = new URL('/privacy.html', window.location.origin).href;
    link.textContent = isNorwegian ? 'Les personvernerklæringen' : 'Read the privacy notice';
    details.appendChild(link);
    const actions = document.createElement('div');
    actions.className = 'en-consent-actions';

    function choose(value) {
      remember(value);
      banner.remove();
      style.remove();
      if (value === 'granted') startTracking();
    }

    const accept = document.createElement('button');
    accept.type = 'button';
    accept.textContent = isNorwegian ? 'Tillat besøksstatistikk' : 'Allow audience statistics';
    accept.addEventListener('click', () => choose('granted'));
    const reject = document.createElement('button');
    reject.type = 'button';
    reject.textContent = isNorwegian ? 'Avslå' : 'Decline';
    reject.addEventListener('click', () => choose('denied'));
    actions.append(accept, reject);
    banner.append(title, description, details, actions);
    document.head.appendChild(style);
    document.body.appendChild(banner);
  }

  function initialize() {
    if (config && config.provider === 'umami' && config.enabled) {
      const choice = savedChoice();
      if (choice === 'granted') startTracking();
      else if (choice === null && !doNotTrack()) showConsent();
    }

    document.querySelectorAll('[data-analytics-consent-reopen]').forEach(button => {
      button.addEventListener('click', () => {
        try { window.localStorage.removeItem(consentKey); } catch {}
        showConsent();
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }

  if (window.location.pathname.endsWith('/articles/before-then-if-25-public-experiments-2026.html')) {
    const fieldLab = document.createElement('script');
    fieldLab.defer = true;
    fieldLab.src = new URL('field-lab-before.js', document.currentScript.src).href;
    document.head.appendChild(fieldLab);
  }
})();
