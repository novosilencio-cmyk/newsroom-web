(() => {
  const beforeRewrites = {
    'TW-01': 'net-zero policy could remain remote from the places where energy, transport, consumption and trust were lived.',
    'TW-02': 'plastic, packaging, biomass, buildings and electronics often moved through separate waste and industrial systems.',
    'TW-03': 'semiconductor policy was usually narrated through capacity, performance and strategic supply.',
    'DK-01': 'nitrogen, farming, wetlands, forests and biodiversity competed on the same land but were often governed through separate measures.',
    'DK-02': 'home-care systems could turn continuity into a scheduling problem: many workers, many handovers, little room for judgement.',
    'SE-01': 'many organisations knew what they could replace or electrify but could not make the investment case close.',
    'SE-02': 'species-rich meadows and pastures were disappearing through many local losses rather than one dramatic event.',
    'SE-03': 'drained or altered landscapes could lose water retention, habitat and resilience.',
    'JP-01': 'ageing, labour shortages and climate pressure made repetitive farm work harder to sustain.',
    'JP-02': 'families outside regular nursery arrangements could still need contact, respite and early-childhood environments.',
    'JP-03': 'collection alone did not guarantee high-quality recycled material or a buyer for it.',
    'JP-04': 'a city could have plenty of recyclable material and still lack the organisations, markets or knowledge to circulate it locally.',
    'JP-05': 'carbon targets could feel abstract when separated from housing, transport, energy bills and local economic life.',
    'HK-01': 'an economy could excel at services and research while still struggling to turn technical knowledge into local production capability.',
    'CN-01': 'China’s “waste-free city” work had developed through pilot and demonstration phases across cities and regions.',
    'BR-01': 'infrastructure deficits were experienced as hours, illness, flooded streets, unsafe slopes and unreliable services.',
    'BR-02': 'small farms needed finance, risk protection, technical help and stable markets — not always in that order.',
    'BR-03': 'practices such as pasture recovery, agroforestry, integrated crop-livestock-forest systems and bioinputs were often promoted faster than their adoption could be measured.',
    'AR-01': 'the official diagnosis behind Argentina’s national literacy plan was stark: a large share of third-grade pupils did not reach minimum reading comprehension.',
    'AR-02': '“Industry 4.0” could be too broad to help an SME decide what to buy or change.',
    'KR-01': 'automating open-field farming was already hard: weather, soil, large areas and ageing workforces did not behave like controlled indoor systems.',
    'SG-01': 'Singapore already imported more than 90 per cent of its food, leaving a highly organised city exposed to disruptions beyond its borders.',
    'CL-01': 'Chile’s first green-hydrogen strategy had established large ambitions around its renewable-energy potential.',
    'RW-01': 'climate shocks, smallholder productivity and access to investment created overlapping constraints on agricultural transformation.',
    'IN-01': 'rural drinking-water access was not only a construction problem: sources, water quality, maintenance and local management determined whether infrastructure lasted.'
  };

  const findCase = id => [...document.querySelectorAll('.case')].find(card => {
    const label = card.dataset.caseId || card.querySelector('.case-label')?.textContent || '';
    return label.split('·')[0].trim() === id;
  });

  const cleanSequenceScaffolding = card => {
    const paragraphs = [...card.querySelectorAll('.sequence')];
    paragraphs.forEach((paragraph, index) => {
      if (index === 0) return;
      const text = paragraph.textContent.replace(/^(Then|When|If)\.\s*/i, '').trim();
      paragraph.textContent = text;
    });
  };

  const apply = () => {
    const story = document.querySelector('.story');
    if (!story) return;

    const deck = story.querySelector('.deck');
    if (deck && !story.querySelector('.scope-note')) {
      const scope = document.createElement('p');
      scope.className = 'scope-note';
      scope.textContent = 'Across 13 countries — including Taiwan, Japan, Denmark, Sweden, Brazil and Argentina — governments are trying practical ways to make everyday life and public systems work better, from childcare and water to farming, materials and industry.';
      deck.insertAdjacentElement('afterend', scope);
    }

    const byline = story.querySelector('.byline');
    if (byline) {
      byline.textContent = 'Experimental Newsroom Field Lab · human–AI editorial collaboration · Artistic frame: Bjørn M. Benlolo';
    }

    const method = story.querySelector('.method-note');
    if (method) {
      method.textContent = 'Official sources establish what has been launched, funded or implemented. They do not establish that the measures will work.';
    }

    const labNote = story.querySelector('.lab-note');
    if (labNote) {
      labNote.innerHTML = '<strong>The experiment:</strong> policy time, event time and discovery time do not always line up. Some sections follow what happened; others follow the point when a result can actually be checked. The interval before an outcome is part of the story.';
      const selection = labNote.nextElementSibling;
      if (selection && selection.tagName === 'P') {
        selection.textContent = 'The publishing desk selected all 25 cases because each has a current official source, a concrete public action and a next observation that could strengthen or weaken the story. Selection is not a verdict on whether the policy is good, sufficient or durable.';
      }
    }

    document.querySelectorAll('.case').forEach(card => {
      const labelNode = card.querySelector('.case-label');
      const originalLabel = labelNode?.textContent || '';
      const [rawId, ...labelParts] = originalLabel.split('·');
      const id = rawId.trim();
      card.dataset.caseId = id;

      if (labelNode && labelParts.length) {
        labelNode.textContent = labelParts.join('·').trim();
      }

      const opening = card.querySelector('.sequence');
      const sentence = beforeRewrites[id];
      if (opening && sentence) {
        opening.innerHTML = `<span class="before-marker"><span class="before-initial">B</span>efore</span>, ${sentence}`;
      }

      cleanSequenceScaffolding(card);
    });

    const tw02 = findCase('TW-02');
    if (tw02) {
      const sequences = tw02.querySelectorAll('.sequence');
      if (sequences[2]) {
        sequences[2].textContent = 'The test begins when a funded idea has to move a real material from collection through processing to a manufacturer, buyer or community that will actually use it.';
      }
    }

    if (!document.getElementById('field-lab-text-refinement-style')) {
      const style = document.createElement('style');
      style.id = 'field-lab-text-refinement-style';
      style.textContent = '.scope-note{max-width:780px;margin:-10px 0 26px;font-size:1.08rem;line-height:1.55}.before-marker{font:inherit}.before-initial{font-family:Georgia,"Times New Roman",serif;font-size:1.45em;line-height:0;letter-spacing:-.02em}.case-label{letter-spacing:.05em}';
      document.head.appendChild(style);
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply, { once: true });
  } else {
    apply();
  }
})();
