/* figures-sidenav.js - left side TOC for the /figures/ page.
   Loaded conditionally from _includes/nav-assets.html.
   Self-contained: injects its own styles, markup, scroll spy and mobile drawer. */
(function () {
  'use strict';

  /* Guard: only run on the figures page, even if another page includes this file. */
  var path = window.location.pathname.replace(/index\.html$/, '');
  if (!/(^|\/)figures(\/|\.html)?$/.test(path)) return;
  if (document.getElementById('fig-sidenav')) return;

  var SECTIONS = [
    { id: 'gallery',                  label: '图例速览',            level: 1 },
    { id: 'fig-method',               label: 'A · 方法与流程',       level: 2 },
    { id: 'fig-original-comparison',  label: '顶会案例 · 原图对照',   level: 3 },
    { id: 'fig-results',              label: 'B · 实验结果',         level: 2 },
    { id: 'fig-analysis',             label: 'C · 消融与分析',       level: 2 },
    { id: 'fig-advanced',             label: 'D · 机制展开版',       level: 1 },
    { id: 'fig-paper-grade',          label: 'E · 完整方法图',       level: 1 },
    { id: 'howto',                    label: '实图绘制方法论',       level: 1 },
    { id: 'methods',                  label: '常用方法',             level: 1 },
    { id: 'materials',                label: '素材与资源',           level: 1 }
  ];
  var MOBILE_BREAKPOINT = 1320;

  var CSS = [
    'html { scroll-behavior: smooth; }',
    ':root { --fig-nav-w: 216px; --fig-nav-h: var(--site-nav-height, 68px); }',
    '@media (min-width: 1320px) {',
    '  body.has-fig-sidenav div.page { max-width: 1356px; padding-left: 268px; }',
    '}',
    '.fig-sidenav {',
    '  position: fixed; top: calc(var(--fig-nav-h) + 20px); left: 16px; z-index: 30;',
    '  display: flex; flex-direction: column; width: var(--fig-nav-w);',
    '  max-height: calc(100vh - var(--fig-nav-h) - 44px);',
    '  max-height: calc(100dvh - var(--fig-nav-h) - 44px);',
    '  overflow: hidden; background: #fff;',
    '  border: 1px solid var(--line, #e5e9ee); border-radius: 12px;',
    '  box-shadow: 0 8px 28px rgba(36,41,47,.07);',
    '  font: 13px/1.55 var(--sans, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);',
    '  color: var(--ink, #24292f);',
    '}',
    '@media (min-width: 1356px) {',
    '  .fig-sidenav { left: max(16px, calc((100vw - 1356px) / 2 + 16px)); }',
    '}',
    '.fig-sidenav__head {',
    '  flex: none; display: flex; align-items: center; justify-content: space-between; gap: 8px;',
    '  padding: 12px 14px 10px; border-bottom: 1px solid var(--line, #e5e9ee);',
    '  font-size: 13px; font-weight: 700;',
    '}',
    '.fig-sidenav__head small { margin-left: 5px; font-size: 11px; font-weight: 400; color: var(--ink-faint, #8b949e); }',
    '.fig-sidenav__close {',
    '  display: none; width: 28px; height: 28px; padding: 0; border: 0; border-radius: 6px;',
    '  background: var(--wash, #f6f8fa); color: var(--ink-soft, #57606a);',
    '  font-size: 20px; line-height: 1; cursor: pointer;',
    '}',
    '.fig-sidenav__body { overflow-y: auto; overscroll-behavior: contain; padding: 8px 8px 10px; }',
    '.fig-sidenav ul { list-style: none; margin: 0; padding: 0; }',
    '.fig-sidenav a {',
    '  display: block; padding: 5px 10px; border-left: 2px solid transparent; border-radius: 0 6px 6px 0;',
    '  color: var(--ink-soft, #57606a); text-decoration: none;',
    '  transition: background .18s ease, color .18s ease;',
    '}',
    '.fig-sidenav a:hover { color: var(--ink, #24292f); background: var(--wash, #f6f8fa); }',
    '.fig-sidenav a[data-level="2"] { padding-left: 20px; font-size: 12.5px; }',
    '.fig-sidenav a[data-level="3"] { padding-left: 30px; font-size: 12px; color: var(--ink-faint, #8b949e); }',
    '.fig-sidenav__list a.active, .fig-sidenav__list a.active:hover {',
    '  color: #0b7fa8; background: #eaf6fb; border-left-color: var(--accent, #0ea5e9); font-weight: 600;',
    '}',
    '.fig-sidenav__cases { margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--line, #e5e9ee); }',
    '.fig-sidenav__cases > summary {',
    '  list-style: none; cursor: pointer; padding: 5px 10px;',
    '  font-size: 12.5px; font-weight: 600; color: var(--ink-soft, #57606a);',
    '}',
    '.fig-sidenav__cases > summary::-webkit-details-marker { display: none; }',
    '.fig-sidenav__cases > summary::before {',
    '  content: "\\25B8"; display: inline-block; margin-right: 6px; color: var(--ink-faint, #8b949e);',
    '  transition: transform .2s ease;',
    '}',
    '.fig-sidenav__cases[open] > summary::before { transform: rotate(90deg); }',
    '.fig-sidenav__count { float: right; font-size: 11px; font-weight: 400; color: var(--ink-faint, #8b949e); }',
    '.fig-sidenav__case-group { padding: 3px 0 6px; }',
    '.fig-sidenav__case-group b {',
    '  display: block; padding: 5px 10px 3px; font-size: 11px; font-weight: 600;',
    '  color: var(--ink-faint, #8b949e);',
    '}',
    '.fig-sidenav__case-group a { padding: 3px 8px 3px 20px; font-size: 12px; }',
    '.fig-sidenav__case-group .fnum {',
    '  display: inline-block; min-width: 26px; color: var(--accent, #0ea5e9);',
    '  font: 11px/1.4 var(--mono, Menlo, Consolas, monospace);',
    '}',
    '.fig-sidenav__top {',
    '  flex: none; display: block; width: 100%; padding: 9px 14px;',
    '  border: 0; border-top: 1px solid var(--line, #e5e9ee); background: #fff;',
    '  color: var(--ink-faint, #8b949e); font: 12px/1.4 inherit; text-align: center; cursor: pointer;',
    '}',
    '.fig-sidenav__top:hover { color: var(--accent, #0ea5e9); background: var(--wash, #f6f8fa); }',
    '.fig-nav-toggle, .fig-nav-backdrop { display: none; }',
    '@media (max-width: 1319px) {',
    '  .fig-sidenav {',
    '    top: 0; bottom: 0; left: 0; z-index: 1002;',
    '    width: min(84vw, 300px); max-height: none; border: 0; border-radius: 0 14px 14px 0;',
    '    box-shadow: 0 12px 40px rgba(20,32,42,.22);',
    '    transform: translateX(-105%); transition: transform .28s cubic-bezier(.22,1,.36,1);',
    '  }',
    '  body.fig-nav-open .fig-sidenav { transform: none; }',
    '  body.fig-nav-open { overflow: hidden; }',
    '  .fig-sidenav__close { display: inline-flex; align-items: center; justify-content: center; }',
    '  .fig-nav-toggle {',
    '    position: fixed; left: 16px; bottom: 18px; z-index: 970;',
    '    display: inline-flex; align-items: center; gap: 7px;',
    '    padding: 9px 15px; border: 1px solid var(--line, #e5e9ee); border-radius: 999px;',
    '    background: #fff; color: var(--ink, #24292f); box-shadow: 0 6px 22px rgba(36,41,47,.16);',
    '    font: 600 13px/1.2 var(--sans, sans-serif); cursor: pointer;',
    '  }',
    '  .fig-nav-toggle span:first-child { font-size: 14px; color: var(--accent, #0ea5e9); }',
    '  body.fig-nav-open .fig-nav-toggle { opacity: 0; pointer-events: none; }',
    '  .fig-nav-backdrop {',
    '    position: fixed; inset: 0; z-index: 1001; display: block;',
    '    background: rgba(20,32,42,.38); opacity: 0; pointer-events: none; transition: opacity .25s ease;',
    '  }',
    '  body.fig-nav-open .fig-nav-backdrop { opacity: 1; pointer-events: auto; }',
    '}',
    '@media (prefers-reduced-motion: reduce) {',
    '  html { scroll-behavior: auto; }',
    '  .fig-sidenav, .fig-nav-backdrop { transition: none; }',
    '}',
    '@media print {',
    '  .fig-sidenav, .fig-nav-toggle, .fig-nav-backdrop { display: none !important; }',
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
    '<div class="fig-sidenav__head"><span>本页目录<small>' + SECTIONS.length + ' 章节</small></span>' +
    '<button class="fig-sidenav__close" type="button" aria-label="关闭目录">&times;</button></div>' +
    '<div class="fig-sidenav__body"><ul class="fig-sidenav__list"></ul>' +
    '<details class="fig-sidenav__cases"><summary>案例索引<span class="fig-sidenav__count"></span></summary>' +
    '<div class="fig-sidenav__case-groups"></div></details></div>' +
    '<button class="fig-sidenav__top" type="button">↑ 回到顶部</button>';
  document.body.appendChild(aside);
  document.body.classList.add('has-fig-sidenav');

  /* Chapter links */
  var list = aside.querySelector('.fig-sidenav__list');
  var items = [];
  SECTIONS.forEach(function (s) {
    var el = document.getElementById(s.id);
    if (!el) return;
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

  /* Mobile drawer controls */
  var toggle = document.createElement('button');
  toggle.className = 'fig-nav-toggle';
  toggle.type = 'button';
  toggle.setAttribute('aria-label', '打开本页目录');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.innerHTML = '<span aria-hidden="true">☰</span><span>目录</span>';
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
