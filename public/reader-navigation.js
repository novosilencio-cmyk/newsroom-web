/* Progressive local filtering: the complete guide works without JavaScript. */
(() => {
  const form = document.querySelector('.map-search');
  if (!form) return;
  const query = document.getElementById('map-query');
  const language = document.getElementById('map-language');
  const result = document.getElementById('map-results');
  const empty = document.getElementById('map-empty');
  const sections = [...document.querySelectorAll('.map-section')];
  const entries = [...document.querySelectorAll('.map-entry')];
  const no = document.documentElement.lang === 'nb';
  const parameters = new URLSearchParams(window.location.search);
  query.value = parameters.get('q') || '';
  const requestedLanguage = parameters.get('lang') || '';
  if ([...language.options].some(option => option.value === requestedLanguage)) language.value = requestedLanguage;
  const normalise = value => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ø/g, 'o').replace(/æ/g, 'ae');
  const texts = new Map(entries.map(entry => [entry, normalise(entry.dataset.search)]));
  function filter() {
    const words = normalise(query.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const entry of entries) {
      const matches = words.every(word => texts.get(entry).includes(word)) &&
        (!language.value || entry.dataset.languages.split(' ').includes(language.value));
      entry.hidden = !matches;
      if (matches) count += 1;
    }
    for (const section of sections) {
      section.hidden = ![...section.querySelectorAll('.map-entry')].some(entry => !entry.hidden);
      const jump = document.querySelector(`.map-jumps a[href="#${section.id}"]`);
      if (jump) jump.hidden = section.hidden;
    }
    empty.hidden = count !== 0;
    result.textContent = no ? `${count} av ${entries.length} oppføringer vises.` : `Showing ${count} of ${entries.length} entries.`;
  }
  function rememberQuery() {
    const url = new URL(window.location.href);
    if (query.value.trim()) url.searchParams.set('q', query.value.trim()); else url.searchParams.delete('q');
    if (language.value) url.searchParams.set('lang', language.value); else url.searchParams.delete('lang');
    window.history.replaceState(null, '', url);
    filter();
  }
  let timer;
  query.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(rememberQuery, 150); });
  language.addEventListener('change', rememberQuery);
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); rememberQuery(); });
  form.addEventListener('reset', event => {
    event.preventDefault();
    clearTimeout(timer);
    query.value = ''; language.value = ''; rememberQuery(); query.focus();
  });
  form.hidden = false;
  filter();
})();
