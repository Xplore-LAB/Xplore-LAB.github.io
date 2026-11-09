(() => {
  'use strict';
  const root = document.querySelector('[data-site-nav]');
  if (!root) return;
  const toggle = root.querySelector('.site-nav__toggle');
  const label = root.querySelector('[data-nav-toggle-label]');
  const links = root.querySelector('.site-nav__links');
  const groups = [...root.querySelectorAll('[data-nav-group]')];
  const mobile = window.matchMedia('(max-width: 900px)');
  const closeGroups = (except) => {
    groups.forEach(group => { if (group !== except) group.open = false; });
  };
  const setExpanded = (expanded) => {
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.setAttribute('aria-label', expanded ? '收起导航' : '展开导航');
    label.textContent = expanded ? '收起' : '菜单';
    links.hidden = mobile.matches && !expanded;
    if (!expanded) closeGroups();
  };
  const updateCurrent = () => {
    const current = new URL(window.location.href);
    const pathname = current.pathname.replace(/index\.html$/, '');
    groups.forEach(group => group.removeAttribute('data-current'));
    root.querySelectorAll('a[aria-current]').forEach(link => link.removeAttribute('aria-current'));
    root.querySelectorAll('a[href]').forEach(link => {
      const url = new URL(link.href, current);
      if (url.origin !== current.origin || url.pathname !== pathname) return;
      const group = link.closest('[data-nav-group]');
      if (group) group.setAttribute('data-current', 'true');
      if ((url.hash && url.hash === current.hash) || (!url.hash && !current.hash)) {
        link.setAttribute('aria-current', url.hash ? 'location' : 'page');
      }
    });
    if (root.dataset.pageLayout === 'post') {
      const writing = root.querySelector('[data-nav-group="writing"]');
      if (writing) writing.setAttribute('data-current', 'true');
    }
  };
  root.dataset.enhanced = 'true';
  setExpanded(false);
  updateCurrent();
  toggle.addEventListener('click', () => setExpanded(toggle.getAttribute('aria-expanded') !== 'true'));
  groups.forEach(group => {
    const summary = group.querySelector('summary');
    group.addEventListener('toggle', () => {
      summary.setAttribute('aria-expanded', String(group.open));
      if (group.open) closeGroups(group);
    });
  });
  root.addEventListener('click', event => {
    if (event.target.closest('a[href]')) setExpanded(false);
  });
  document.addEventListener('click', event => {
    if (!root.contains(event.target)) setExpanded(false);
  });
  document.addEventListener('focusin', event => {
    if (!root.contains(event.target)) setExpanded(false);
  });
  root.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const openGroup = groups.find(group => group.open);
    if (openGroup) {
      openGroup.open = false;
      openGroup.querySelector('summary').focus();
    } else if (mobile.matches && toggle.getAttribute('aria-expanded') === 'true') {
      setExpanded(false);
      toggle.focus();
    }
    event.preventDefault();
  });
  mobile.addEventListener('change', () => setExpanded(false));
  window.addEventListener('hashchange', updateCurrent);
})();
