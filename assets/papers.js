/* Local-only progressive enhancement: the complete catalogue remains in HTML. */
(() => {
  'use strict';
  const form = document.querySelector('#paper-tools');
  if (!form) return;
  const search = document.querySelector('#paper-search');
  const topic = document.querySelector('#paper-topic');
  const clear = document.querySelector('#paper-clear');
  const sort = document.querySelector('#paper-sort');
  const list = document.querySelector('#paper-list');
  const status = document.querySelector('#paper-results');
  const empty = document.querySelector('#no-papers');
  const normalize = text => text.normalize('NFKD').replace(/\p{M}/gu, '').toLocaleLowerCase('en').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  const papers = [...document.querySelectorAll('[data-paper]')].map((element, index) => ({
    index,
    title: element.dataset.title,
    date: element.dataset.date,
    element,
    text: normalize(element.dataset.search),
    topics: element.dataset.topics.split('|')
  }));
  function update() {
    const ordered = [...papers].sort((a, b) => {
      if (sort.value === 'title') return a.title.localeCompare(b.title, 'en') || a.index - b.index;
      const dates = a.date.localeCompare(b.date);
      return (sort.value === 'oldest' ? dates : -dates) || a.index - b.index;
    });
    for (const paper of ordered) list.append(paper.element);
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
    const orderLabel = sort.selectedOptions[0].textContent;
    status.textContent = `${active ? `${count} of ${papers.length}` : papers.length} papers · ${orderLabel}`;
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', update);
  topic.addEventListener('change', update);
  sort.addEventListener('change', update);
  clear.addEventListener('click', () => {
    search.value = '';
    topic.value = '';
    update();
    search.focus();
  });
  function openLinkedConnection() {
    const id = location.hash.slice(1);
    if (!id.startsWith('connection-')) return;
    const group = document.getElementById(id);
    if (group?.matches('details.connection-group')) group.open = true;
  }
  window.addEventListener('hashchange', openLinkedConnection);
  openLinkedConnection();
  window.addEventListener('pageshow', update);
  update();
  form.hidden = false;
})();
