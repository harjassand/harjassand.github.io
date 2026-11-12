/* Local-only progressive enhancement: the complete catalogue remains in HTML. */
(() => {
  'use strict';
  const form = document.querySelector('#paper-tools');
  if (!form) return;
  const search = document.querySelector('#paper-search');
  const topic = document.querySelector('#paper-topic');
  const clear = document.querySelector('#paper-clear');
  const status = document.querySelector('#paper-results');
  const empty = document.querySelector('#no-papers');
  const normalize = text => text.normalize('NFKD').replace(/\p{M}/gu, '').toLocaleLowerCase('en').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  const papers = [...document.querySelectorAll('[data-paper]')].map(element => ({
    element,
    text: normalize(element.dataset.search),
    topics: element.dataset.topics.split('|')
  }));
  function update() {
    const words = normalize(search.value).split(/\s+/).filter(Boolean);
    let count = 0;
    for (const paper of papers) {
      const matches = (!topic.value || paper.topics.includes(topic.value)) && words.every(word => paper.text.includes(word));
      paper.element.hidden = !matches;
      if (matches) count++;
    }
    const active = search.value.length > 0 || topic.value !== '';
    clear.hidden = !active;
    empty.hidden = count !== 0;
    status.textContent = active ? `${count} of ${papers.length} papers` : `${papers.length} papers · Newest first`;
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', update);
  topic.addEventListener('change', update);
  clear.addEventListener('click', () => {
    form.reset();
    update();
    search.focus();
  });
  window.addEventListener('pageshow', update);
  update();
  form.hidden = false;
})();
