(() => {
  const rewrites = {
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

  const apply = () => {
    document.querySelectorAll('.case').forEach(card => {
      const label = card.querySelector('.case-label')?.textContent || '';
      const id = label.split('·')[0].trim();
      const opening = card.querySelector('.sequence');
      const sentence = rewrites[id];
      if (!opening || !sentence) return;
      opening.innerHTML = `<strong class="before-marker"><span class="before-initial">B</span>efore</strong>, ${sentence}`;
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply, { once: true });
  } else {
    apply();
  }
})();
