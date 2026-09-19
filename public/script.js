const editionDate = document.getElementById('edition-date');
const articleGrid = document.getElementById('article-grid');

editionDate.textContent = new Intl.DateTimeFormat('en-GB', {
  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
}).format(new Date());

fetch('content/articles.json')
  .then(response => {
    if (!response.ok) throw new Error('Article data could not be loaded');
    return response.json();
  })
  .then(articles => {
    articles
      .sort((a, b) => a.priority - b.priority)
      .forEach(article => {
        // A featured story has a static card so it remains available without JS.
        if (Array.from(articleGrid.querySelectorAll('[data-article-id]'))
          .some(card => card.dataset.articleId === article.id)) return;
        const card = document.createElement('article');
        card.className = 'article-card';
        card.innerHTML = `
          <p class="article-meta">${article.region} · ${article.country} · ${article.type}</p>
          <h3>${article.title}</h3>
          <p>${article.summary}</p>
          ${article.url ? `<p><a class="text-link" href="${article.url}">Read the report →</a></p>` : ''}
        `;
        articleGrid.appendChild(card);
      });
  })
  .catch(error => {
    const notice = document.createElement('p');
    notice.textContent = 'The article index could not be loaded. Please try again later.';
    articleGrid.appendChild(notice);
    console.error(error);
  });
