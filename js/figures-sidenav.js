/* figures-sidenav.js - quiet left TOC for the /figures/ page.
   Loaded conditionally from _includes/nav-assets.html.
   Self-contained: injects its own styles, markup, scroll spy and mobile drawer. */
(function () {
  'use strict';

  /* Guard: only run on the figures page, even if another page includes this file. */
  var path = window.location.pathname.replace(/index\.html$/, '');
  if (!/(^|\/)figures(\/|\.html)?$/.test(path)) return;
  if (document.getElementById('fig-sidenav')) return;

  var SECTIONS = [
    { id: 'gallery',                  label: '图例速览',            level: 1, group: '图例示例' },
    { id: 'fig-method',               label: 'A · 方法与流程',       level: 2, group: '图例示例' },
    { id: 'fig-original-comparison',  label: '顶会案例 · 原图对照',   level: 3, group: '图例示例' },
    { id: 'fig-results',              label: 'B · 实验结果',         level: 2, group: '图例示例' },
    { id: 'fig-analysis',             label: 'C · 消融与分析',       level: 2, group: '图例示例' },
    { id: 'fig-advanced',             label: 'D · 机制展开版',       level: 1, group: '完整图组' },
    { id: 'fig-paper-grade',          label: 'E · 完整方法图',       level: 1, group: '完整图组' },
    { id: 'howto',                    label: '实图绘制方法论',       level: 1, group: '方法与资源' },
    { id: 'methods',                  label: '常用方法',             level: 1, group: '方法与资源' },
    { id: 'materials',                label: '素材与资源',           level: 1, group: '方法与资源' }
  ];
  var MOBILE_BREAKPOINT = 1320;
  var STORE_KEY = 'fig-sidenav-collapsed';

  var CSS = [
    'html { scroll-behavior: smooth; }',
    ':root { --fig-nav-w: 220px; --fig-nav-h: var(--site-nav-height, 68px); }',
    '@media (min-width: 1320px) {',
    '  body.has-fig-sidenav:not(.fig-nav-collapsed) div.page { max-width: 1360px; padding-left: 272px; }',
    '}',
    '.fig-sidenav {',
    '  position: fixed; top: calc(var(--fig-nav-h) + 20px); left: 16px; z-index: 30;',
    '  display: flex; flex-direction: column; width: var(--fig-nav-w);',
    '  max-height: calc(100vh - var(--fig-nav-h) - 44px);',
    '  max-height: calc(100dvh - var(--fig-nav-h) - 44px);',
    '  overflow: hidden; background: transparent; border: 0; border-radius: 0;',
    '  font: 13px/1.5 var(--sans, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);',
    '  color: var(--ink, #24292f);',
    '}',
    '@media (min-width: 1360px) {',
    '  .fig-sidenav { left: max(16px, calc((100vw - 1360px) / 2 + 16px)); }',
    '}',
    '.fig-sidenav__head {',
    '  flex: none; display: flex; align-items: center; gap: 6px;',
    '  height: 30px; padding: 0 12px;',
    '}',
    '.fig-sidenav__title { flex: 1; min-width: 0; font-size: 11px; font-weight: 400; color: #b0b6bd; }',
    '.fig-sidenav__close, .fig-sidenav__collapse, .fig-nav-restore {',
    '  display: none; width: 26px; height: 26px; padding: 0;',
    '  border: 0; border-radius: 6px; background: transparent;',
    '  color: #9aa1a9; font: 16px/1 var(--sans, sans-serif); cursor: pointer;',
    '}',
    '.fig-sidenav__collapse { opacity: 0; transition: opacity .15s ease, background .15s ease; }',
    '.fig-sidenav:hover .fig-sidenav__collapse { opacity: .75; }',
    '.fig-sidenav__collapse:hover, .fig-sidenav__close:hover, .fig-nav-restore:hover {',
    '  background: #f2f3f5; color: #4b5563;',
    '}',
    '.fig-sidenav__body {',
    '  overflow-y: auto; overscroll-behavior: contain; padding: 2px 4px 6px;',
    '}',
    '.fig-sidenav__body::-webkit-scrollbar { width: 4px; }',
    '.fig-sidenav__body::-webkit-scrollbar-track { background: transparent; }',
    '.fig-sidenav__body::-webkit-scrollbar-thumb { background: #e8eaed; border-radius: 2px; }',
    '.fig-sidenav ul { list-style: none; margin: 0; padding: 0; }',
    '.fig-sidenav__group {',
    '  padding: 13px 12px 4px; font-size: 11px; font-weight: 400; color: #a9afb7;',
    '}',
    '.fig-sidenav__group:not(:first-child) { margin-top: 2px; padding-top: 15px; }',
    '.fig-sidenav a {',
    '  display: block; margin: 1px 4px; padding: 6px 10px; border-radius: 6px;',
    '  color: #6f7781; text-decoration: none;',
    '  transition: background .15s ease, color .15s ease;',
    '}',
    '.fig-sidenav a:hover { color: #2b3138; background: #f5f6f7; }',
    '.fig-sidenav a:focus-visible { outline: 2px solid #c9d2da; outline-offset: 1px; }',
    '.fig-sidenav__list a[data-level="2"] { padding-left: 22px; }',
    '.fig-sidenav__list a[data-level="3"] {',
    '  padding-left: 32px; font-size: 12.5px; color: #8d949d;',
    '}',
    '.fig-sidenav__list a.active, .fig-sidenav__list a.active:hover {',
    '  color: #20262d; font-weight: 500; background: #eff1f3;',
    '}',
    '.fig-sidenav__cases { margin: 9px 4px 2px; padding-top: 7px; border-top: 1px solid #f0f1f3; }',
    '.fig-sidenav__cases > summary {',
    '  list-style: none; cursor: pointer; display: flex; align-items: center; gap: 7px;',
    '  padding: 6px 10px; border-radius: 6px;',
    '  font-size: 12.5px; font-weight: 400; color: #8d949d;',
    '}',
    '.fig-sidenav__cases > summary:hover { background: #f5f6f7; color: #2b3138; }',
    '.fig-sidenav__cases > summary::-webkit-details-marker { display: none; }',
    '.fig-sidenav__cases > summary::before {',
    '  content: ""; width: 0; height: 0;',
    '  border-left: 4px solid #b6bcc4;',
    '  border-top: 3.5px solid transparent; border-bottom: 3.5px solid transparent;',
    '  transition: transform .15s ease;',
    '}',
    '.fig-sidenav__cases[open] > summary::before { transform: rotate(90deg); }',
    '.fig-sidenav__count { margin-left: auto; font-size: 11px; color: #b0b6bd; }',
    '.fig-sidenav__case-group { padding: 2px 0 5px; }',
    '.fig-sidenav__case-group b {',
    '  display: block; padding: 6px 10px 3px; font-size: 11px;',
    '  font-weight: 400; color: #a9afb7;',
    '}',
    '.fig-sidenav__case-group a { margin: 0 4px; padding: 4px 8px 4px 18px; font-size: 12.5px; }',
    '.fig-sidenav__case-group .fnum {',
    '  display: inline-block; min-width: 27px; color: #a9afb7;',
    '  font: 400 11px/1.4 var(--mono, Menlo, Consolas, monospace);',
    '}',
    '.fig-sidenav__top {',
    '  flex: none; display: block; width: 100%; padding: 9px 14px;',
    '  border: 0; background: transparent; color: #b0b6bd;',
    '  font: 11px/1.4 var(--sans, sans-serif); text-align: left; cursor: pointer;',
    '  transition: color .15s ease;',
    '}',
    '.fig-sidenav__top:hover { color: #6f7781; background: transparent; }',
    '.fig-nav-toggle, .fig-nav-backdrop { display: none; }',
    '@media (min-width: 1320px) {',
    '  .fig-sidenav__collapse { display: inline-flex; align-items: center; justify-content: center; }',
    '  body.fig-nav-collapsed .fig-sidenav { display: none; }',
    '  .fig-nav-restore {',
    '    position: fixed; left: 12px; top: calc(var(--fig-nav-h) + 14px); z-index: 30;',
    '  }',
    '  body.fig-nav-collapsed .fig-nav-restore { display: inline-flex; align-items: center; justify-content: center; }',
    '}',
    '@media (max-width: 1319px) {',
    '  .fig-sidenav {',
    '    top: 0; bottom: 0; left: 0; z-index: 1002;',
    '    width: min(84vw, 300px); max-height: none;',
    '    background: #fff; border-right: 1px solid #eceef0; border-radius: 0;',
    '    transform: translateX(-105%); transition: transform .26s cubic-bezier(.22,1,.36,1);',
    '  }',
    '  .fig-sidenav__head { height: 56px; padding: 0 14px; }',
    '  .fig-sidenav__title { font-size: 12px; }',
    '  body.fig-nav-open .fig-sidenav { transform: none; }',
    '  body.fig-nav-open { overflow: hidden; }',
    '  .fig-sidenav__close { display: inline-flex; align-items: center; justify-content: center; }',
    '  .fig-nav-toggle {',
    '    position: fixed; left: 14px; bottom: 16px; z-index: 970;',
    '    display: inline-flex; align-items: center; justify-content: center;',
    '    width: 36px; height: 36px; padding: 0;',
    '    border: 1px solid #eceef0; border-radius: 10px;',
    '    background: rgba(255,255,255,.92); color: #8d949d;',
    '    box-shadow: 0 2px 8px rgba(36,41,47,.06);',
    '    font: 15px/1 var(--sans, sans-serif); cursor: pointer;',
    '  }',
    '  .fig-nav-toggle:hover { color: #4b5563; }',
    '  body.fig-nav-open .fig-nav-toggle { opacity: 0; pointer-events: none; }',
    '  .fig-nav-backdrop {',
    '    position: fixed; inset: 0; z-index: 1001; display: block;',
    '    background: rgba(28,34,40,.32);',
    '    opacity: 0; pointer-events: none; transition: opacity .22s ease;',
    '  }',
    '  body.fig-nav-open .fig-nav-backdrop { opacity: 1; pointer-events: auto; }',
    '}',
    '@media (prefers-reduced-motion: reduce) {',
    '  html { scroll-behavior: auto; }',
    '  .fig-sidenav, .fig-nav-backdrop, .fig-sidenav a { transition: none; }',
    '}',
    '@media print {',
    '  .fig-sidenav, .fig-nav-toggle, .fig-nav-backdrop, .fig-nav-restore { display: none !important; }',
    '  body.has-fig-sidenav div.page { max-width: 1120px; padding-left: 32px; }',
    '}'
  ].join('\n');

  var style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  var aside = document.createElement('aside');
  aside.id = 'fig-sidenav';
  aside.className = 'fig-sidenav';
  aside.setAttribute('aria-label', '科研绘图页目录');
  aside.innerHTML =
    '<div class="fig-sidenav__head">' +
    '<span class="fig-sidenav__title">目录</span>' +
    '<button class="fig-sidenav__collapse" type="button" aria-label="收起目录" title="收起目录">&#171;</button>' +
    '<button class="fig-sidenav__close" type="button" aria-label="关闭目录">&times;</button></div>' +
    '<div class="fig-sidenav__body"><ul class="fig-sidenav__list"></ul>' +
    '<details class="fig-sidenav__cases"><summary>案例索引<span class="fig-sidenav__count"></span></summary>' +
    '<div class="fig-sidenav__case-groups"></div></details></div>' +
    '<button class="fig-sidenav__top" type="button">回到顶部</button>';
  document.body.appendChild(aside);
  document.body.classList.add('has-fig-sidenav');

  /* Chapter links, split into quiet group labels */
  var list = aside.querySelector('.fig-sidenav__list');
  var items = [];
  var lastGroup = null;
  SECTIONS.forEach(function (s) {
    var el = document.getElementById(s.id);
    if (!el) return;
    if (s.group !== lastGroup) {
      var gli = document.createElement('li');
      gli.className = 'fig-sidenav__group';
      gli.textContent = s.group;
      list.appendChild(gli);
      lastGroup = s.group;
    }
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + s.id;
    a.textContent = s.label;
    a.setAttribute('data-level', s.level);
    li.appendChild(a);
    list.appendChild(li);
    items.push({ el: el, a: a });
  });

  /* Case index, generated from the existing .case-index wall */
  var caseIndex = document.querySelector('.case-index');
  var groupsBox = aside.querySelector('.fig-sidenav__case-groups');
  var caseCount = 0;
  if (caseIndex) {
    var group = null;
    Array.prototype.forEach.call(caseIndex.children, function (node) {
      if (node.classList.contains('ci-label')) {
        group = document.createElement('div');
        group.className = 'fig-sidenav__case-group';
        var b = document.createElement('b');
        b.textContent = node.textContent.replace(/\s*\d+\s*张\s*$/, '').trim();
        group.appendChild(b);
        groupsBox.appendChild(group);
      } else if (node.classList.contains('case-card') && group) {
        var a = document.createElement('a');
        a.href = node.getAttribute('href');
        var num = node.querySelector('.fnum');
        var title = node.querySelector('.title');
        if (num) {
          var span = document.createElement('span');
          span.className = 'fnum';
          span.textContent = num.textContent;
          a.appendChild(span);
        }
        var text = document.createElement('span');
        text.textContent = title ? title.textContent : node.textContent;
        a.appendChild(text);
        group.appendChild(a);
        caseCount++;
      }
    });
    aside.querySelector('.fig-sidenav__count').textContent = caseCount + ' 张';
  }

  /* Desktop collapse, like a chat sidebar. State survives reloads. */
  var restore = document.createElement('button');
  restore.className = 'fig-nav-restore';
  restore.type = 'button';
  restore.setAttribute('aria-label', '展开目录');
  restore.title = '展开目录';
  restore.innerHTML = '<span aria-hidden="true">&#9776;</span>';
  document.body.appendChild(restore);

  function readCollapsed() {
    try { return window.localStorage.getItem(STORE_KEY) === '1'; } catch (e) { return false; }
  }
  function writeCollapsed(v) {
    try { window.localStorage.setItem(STORE_KEY, v ? '1' : '0'); } catch (e) { /* ignore */ }
  }
  if (readCollapsed()) document.body.classList.add('fig-nav-collapsed');
  aside.querySelector('.fig-sidenav__collapse').addEventListener('click', function () {
    document.body.classList.add('fig-nav-collapsed');
    writeCollapsed(true);
  });
  restore.addEventListener('click', function () {
    document.body.classList.remove('fig-nav-collapsed');
    writeCollapsed(false);
  });

  /* Mobile drawer controls */
  var toggle = document.createElement('button');
  toggle.className = 'fig-nav-toggle';
  toggle.type = 'button';
  toggle.setAttribute('aria-label', '打开本页目录');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.innerHTML = '<span aria-hidden="true">&#9776;</span>';
  var backdrop = document.createElement('div');
  backdrop.className = 'fig-nav-backdrop';
  document.body.appendChild(backdrop);
  document.body.appendChild(toggle);

  function setOpen(open) {
    document.body.classList.toggle('fig-nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  toggle.addEventListener('click', function () {
    setOpen(!document.body.classList.contains('fig-nav-open'));
  });
  backdrop.addEventListener('click', function () { setOpen(false); });
  aside.querySelector('.fig-sidenav__close').addEventListener('click', function () { setOpen(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setOpen(false);
  });

  /* Scroll spy */
  var bodyBox = aside.querySelector('.fig-sidenav__body');
  var activeLink = null;
  function setActive(a) {
    if (activeLink === a) return;
    if (activeLink) activeLink.classList.remove('active');
    activeLink = a;
    if (!a) return;
    a.classList.add('active');
    var br = bodyBox.getBoundingClientRect();
    var ar = a.getBoundingClientRect();
    if (ar.top < br.top + 6) bodyBox.scrollTop -= (br.top + 6 - ar.top);
    else if (ar.bottom > br.bottom - 6) bodyBox.scrollTop += (ar.bottom - (br.bottom - 6));
  }

  function currentItem() {
    if (!items.length) return null;
    var navH = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--site-nav-height')) || 68;
    var line = navH + 48;
    var ordered = items.slice().sort(function (x, y) {
      return x.el.getBoundingClientRect().top - y.el.getBoundingClientRect().top;
    });
    var pick = ordered[0];
    for (var i = 0; i < ordered.length; i++) {
      if (ordered[i].el.getBoundingClientRect().top <= line) pick = ordered[i];
      else break;
    }
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 6) {
      pick = ordered[ordered.length - 1];
    }
    return pick;
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      var it = currentItem();
      if (it) setActive(it.a);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  document.addEventListener('toggle', onScroll, true);
  window.addEventListener('hashchange', function () {
    var id = window.location.hash.slice(1);
    var hit = null;
    for (var i = 0; i < items.length; i++) {
      if (items[i].el.id === id) { hit = items[i]; break; }
    }
    if (hit) setActive(hit.a);
    else window.setTimeout(onScroll, 80);
  });
  onScroll();

  /* Links: pre-open collapsed cards, then close the drawer on small screens */
  aside.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var target = document.getElementById(a.getAttribute('href').slice(1));
    if (target && target.tagName === 'DETAILS') target.open = true;
    setActive(a);
    if (window.innerWidth < MOBILE_BREAKPOINT) setOpen(false);
  });
  aside.querySelector('.fig-sidenav__top').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    setOpen(false);
  });
})();
