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
    const staticCards = new Map(Array.from(articleGrid.querySelectorAll("[data-article-id]")).map(card => [card.dataset.articleId, card]));
    articleGrid.replaceChildren();
    articles
      .sort((a, b) => b.published.localeCompare(a.published) || (a.priority ?? 999) - (b.priority ?? 999))
      .forEach(article => {
        if (staticCards.has(article.id)) {
          articleGrid.appendChild(staticCards.get(article.id));
          return;
        }
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
