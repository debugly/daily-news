(async () => {
  const tabs = document.getElementById('tabs');
  const list = document.getElementById('list');
  const reader = document.getElementById('reader');

  let data;
  try {
    data = await (await fetch('data.json')).json();
  } catch (e) {
    list.innerHTML = '<p class="empty">加载失败：' + e.message + '</p>';
    return;
  }

  let current = (data.categories && data.categories[0]) ? data.categories[0].slug : null;

  function renderTabs() {
    tabs.innerHTML = '';
    for (const c of data.categories) {
      const b = document.createElement('button');
      b.textContent = c.label;
      b.className = 'tab' + (c.slug === current ? ' active' : '');
      b.onclick = () => { current = c.slug; renderTabs(); renderList(); };
      tabs.appendChild(b);
    }
  }

  function renderList() {
    const items = data.articles.filter(a => a.slug === current);
    list.innerHTML = '';
    if (!items.length) {
      list.innerHTML = '<p class="empty">暂无内容</p>';
      reader.innerHTML = '<p class="empty">暂无内容</p>';
      return;
    }
    for (const a of items) {
      const card = document.createElement('div');
      card.className = 'card';
      card.dataset.path = a.path;
      const t = document.createElement('h3');
      t.textContent = a.title;
      const d = document.createElement('span');
      d.className = 'date';
      d.textContent = a.date;
      card.appendChild(t);
      card.appendChild(d);
      card.onclick = () => select(a);
      list.appendChild(card);
    }
    select(items[0]);
  }

  function select(a) {
    for (const card of list.querySelectorAll('.card')) {
      card.classList.toggle('active', card.dataset.path === a.path);
    }
    renderReader(a);
    scrollToReader();
  }

  function scrollToReader() {
    const header = document.querySelector('.site-header');
    const offset = header ? header.offsetHeight + 8 : 0;
    const y = reader.getBoundingClientRect().top + window.pageYOffset - offset;
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }

  function renderReader(a) {
    reader.innerHTML = '';
    const h = document.createElement('h2');
    h.textContent = a.title;
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = a.category + ' · ' + a.date;
    const body = document.createElement('div');
    body.className = 'article-body';
    body.innerHTML = a.html;
    reader.appendChild(h);
    reader.appendChild(meta);
    reader.appendChild(body);
  }

  renderTabs();
  renderList();
})();
