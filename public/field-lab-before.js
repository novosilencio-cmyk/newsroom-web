(() => {
  const apply = () => {
    document.querySelectorAll('.case').forEach(card => {
      const label = card.querySelector('.case-label');
      const [id, ...parts] = (label?.textContent || '').split('·');
      card.dataset.caseId = id.trim();
      if (label && parts.length) label.textContent = parts.join('·').trim();
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();
