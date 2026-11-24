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
  var PAGE_WIDTH = 1360;

  var CSS = [
    'html { scroll-behavior: smooth; }',
    ':root { --fig-nav-w: 220px; --fig-nav-h: var(--site-nav-height, 68px); }',
    '@media (min-width: 1320px) {',
    '  body.has-fig-sidenav div.page { max-width: 1360px; padding-left: 272px; }',
    '}',
    '.fig-sidenav {',
    '  position: fixed; top: calc(var(--fig-nav-h) + 22px); left: 16px; z-index: 30;',
    '  display: flex; flex-direction: column; width: var(--fig-nav-w);',
    '  max-height: calc(100vh - var(--fig-nav-h) - 48px);',
    '  max-height: calc(100dvh - var(--fig-nav-h) - 48px);',
    '  overflow: hidden; background: linear-gradient(180deg, #fbfdfe 0, #fff 72px);',
    '  border: 1px solid rgba(229,233,238,.95); border-radius: 14px;',
    '  box-shadow: 0 2px 6px rgba(36,41,47,.03), 0 14px 36px rgba(36,41,47,.07);',
    '  font: 12.5px/1.55 var(--sans, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif);',
    '  color: var(--ink, #24292f);',
    '}',
    '.fig-sidenav::before {',
    '  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;',
    '  background: linear-gradient(90deg, var(--accent, #0ea5e9), var(--accent-deep, #6366f1));',
    '}',
    '@media (min-width: 1360px) {',
    '  .fig-sidenav { left: max(16px, calc((100vw - 1360px) / 2 + 16px)); }',
    '}',
    '.fig-sidenav__head {',
    '  flex: none; display: flex; align-items: center; gap: 8px;',
    '  padding: 14px 13px 12px; border-bottom: 1px solid var(--line, #e5e9ee);',
    '}',
    '.fig-sidenav__title {',
    '  flex: 1; min-width: 0; font: 700 14px/1.3 var(--serif, Georgia, "Songti SC", serif);',
    '  letter-spacing: .01em;',
    '}',
    '.fig-sidenav__title small {',
    '  display: block; margin-top: 3px;',
    '  font: 400 10px/1.3 var(--sans, sans-serif); letter-spacing: .06em;',
    '  color: var(--ink-faint, #8b949e);',
    '}',
    '.fig-sidenav__progress {',
    '  flex: none; padding: 2px 7px; border-radius: 999px;',
    '  background: #eaf6fb; color: #0b7fa8;',
    '  font: 600 10.5px/1.4 var(--mono, Menlo, Consolas, monospace);',
    '  font-variant-numeric: tabular-nums;',
    '}',
    '.fig-sidenav__close {',
    '  display: none; flex: none; width: 30px; height: 30px; padding: 0;',
    '  border: 0; border-radius: 8px;',
    '  background: var(--wash, #f6f8fa); color: var(--ink-soft, #57606a);',
    '  font: 20px/1 var(--sans, sans-serif); cursor: pointer;',
    '}',
    '.fig-sidenav__close:hover { color: var(--ink, #24292f); background: #eef2f5; }',
    '.fig-sidenav__body {',
    '  overflow-y: auto; overscroll-behavior: contain; padding: 6px 5px 10px;',
    '}',
    '.fig-sidenav__body::-webkit-scrollbar { width: 6px; }',
    '.fig-sidenav__body::-webkit-scrollbar-track { background: transparent; }',
    '.fig-sidenav__body::-webkit-scrollbar-thumb {',
    '  background: #dfe6ec; border-radius: 3px;',
    '}',
    '.fig-sidenav ul { list-style: none; margin: 0; padding: 0; }',
    '.fig-sidenav__list { position: relative; }',
    '.fig-sidenav__list::before {',
    '  content: ""; position: absolute; left: 6px; top: 12px; bottom: 8px; width: 1px;',
    '  background: linear-gradient(180deg, transparent, var(--line, #e5e9ee) 6%, var(--line, #e5e9ee) 94%, transparent);',
    '}',
    '.fig-sidenav__group {',
    '  padding: 11px 10px 4px;',
    '  font-size: 10px; font-weight: 700; letter-spacing: .13em;',
    '  color: var(--ink-faint, #8b949e);',
    '}',
    '.fig-sidenav__group:not(:first-child) {',
    '  margin-top: 7px; padding-top: 13px; border-top: 1px dashed var(--line, #e5e9ee);',
    '}',
    '.fig-sidenav a {',
    '  display: block; position: relative; margin: 1px 4px;',
    '  padding: 6px 10px 6px 12px; border-radius: 7px;',
    '  color: var(--ink-soft, #57606a); text-decoration: none;',
    '  transition: background .2s ease, color .2s ease, transform .2s ease;',
    '}',
    '.fig-sidenav a:hover {',
    '  color: var(--ink, #24292f); background: var(--wash, #f6f8fa); transform: translateX(2px);',
    '}',
    '.fig-sidenav a:focus-visible { outline: 2px solid var(--accent, #0ea5e9); outline-offset: 1px; }',
    '.fig-sidenav__list a::before {',
    '  content: ""; position: absolute; left: 0; top: 50%;',
    '  width: 3px; height: 0; border-radius: 2px;',
    '  background: linear-gradient(180deg, var(--accent, #0ea5e9), var(--accent-deep, #6366f1));',
    '  transform: translateY(-50%); transition: height .25s cubic-bezier(.22,1,.36,1);',
    '}',
    '.fig-sidenav__list a[data-level="2"] { padding-left: 22px; }',
    '.fig-sidenav__list a[data-level="3"] {',
    '  padding-left: 32px; font-size: 12px; color: var(--ink-faint, #8b949e);',
    '}',
    '.fig-sidenav__list a.active, .fig-sidenav__list a.active:hover {',
    '  color: #0b7fa8; font-weight: 600; transform: none;',
    '  background: linear-gradient(90deg, rgba(14,165,233,.12), rgba(99,102,241,.03));',
    '}',
    '.fig-sidenav__list a.active::before { height: 17px; }',
    '.fig-sidenav__cases {',
    '  margin: 7px 4px 2px; padding-top: 8px;',
    '  border-top: 1px dashed var(--line, #e5e9ee);',
    '}',
    '.fig-sidenav__cases > summary {',
    '  list-style: none; cursor: pointer; display: flex; align-items: center; gap: 7px;',
    '  padding: 5px 8px; border-radius: 6px;',
    '  font-size: 12px; font-weight: 600; color: var(--ink-soft, #57606a);',
    '}',
    '.fig-sidenav__cases > summary:hover { background: var(--wash, #f6f8fa); }',
    '.fig-sidenav__cases > summary::-webkit-details-marker { display: none; }',
    '.fig-sidenav__cases > summary::before {',
    '  content: ""; width: 0; height: 0;',
    '  border-left: 4px solid var(--ink-faint, #8b949e);',
    '  border-top: 3.5px solid transparent; border-bottom: 3.5px solid transparent;',
    '  transition: transform .2s ease;',
    '}',
    '.fig-sidenav__cases[open] > summary::before { transform: rotate(90deg); }',
    '.fig-sidenav__count {',
    '  margin-left: auto; padding: 1px 7px; border-radius: 999px;',
    '  background: var(--wash, #f6f8fa); color: var(--ink-faint, #8b949e);',
    '  font: 600 10px/1.5 var(--mono, Menlo, Consolas, monospace);',
    '}',
    '.fig-sidenav__case-group { padding: 3px 0 6px; }',
    '.fig-sidenav__case-group b {',
    '  display: block; padding: 7px 10px 3px;',
    '  font-size: 10.5px; font-weight: 600; letter-spacing: .03em;',
    '  color: var(--ink-faint, #8b949e);',
    '}',
    '.fig-sidenav__case-group b::first-letter { color: #0b7fa8; }',
    '.fig-sidenav__case-group a { margin: 0 4px; padding: 4px 8px 4px 18px; font-size: 12px; }',
    '.fig-sidenav__case-group .fnum {',
    '  display: inline-block; min-width: 27px; color: #0b7fa8;',
    '  font: 600 11px/1.4 var(--mono, Menlo, Consolas, monospace);',
    '}',
    '.fig-sidenav__top {',
    '  flex: none; display: flex; align-items: center; justify-content: center; gap: 6px;',
    '  width: 100%; padding: 10px 14px;',
    '  border: 0; border-top: 1px solid var(--line, #e5e9ee); background: #fff;',
    '  color: var(--ink-faint, #8b949e);',
    '  font: 12px/1.4 var(--sans, sans-serif); cursor: pointer;',
    '  transition: color .2s ease, background .2s ease;',
    '}',
    '.fig-sidenav__top::before { content: "↑"; font-size: 13px; }',
    '.fig-sidenav__top:hover { color: #0b7fa8; background: #f8fbfd; }',
    '.fig-nav-toggle, .fig-nav-backdrop { display: none; }',
    '@media (max-width: 1319px) {',
    '  .fig-sidenav {',
    '    top: 0; bottom: 0; left: 0; z-index: 1002;',
    '    width: min(86vw, 310px); max-height: none;',
    '    border: 0; border-radius: 0 16px 16px 0; background: #fff;',
    '    box-shadow: 0 12px 44px rgba(20,32,42,.24);',
    '    transform: translateX(-105%); transition: transform .3s cubic-bezier(.22,1,.36,1);',
    '  }',
    '  .fig-sidenav::before { height: 3px; }',
    '  .fig-sidenav__head { padding: 20px 14px 15px; }',
    '  .fig-sidenav__title { font-size: 16px; }',
    '  body.fig-nav-open .fig-sidenav { transform: none; }',
    '  body.fig-nav-open { overflow: hidden; }',
    '  .fig-sidenav__close { display: inline-flex; align-items: center; justify-content: center; }',
    '  .fig-nav-toggle {',
    '    position: fixed; left: 16px; bottom: 18px; z-index: 970;',
    '    display: inline-flex; align-items: center; gap: 7px;',
    '    padding: 10px 16px; border: 1px solid rgba(229,233,238,.9); border-radius: 999px;',
    '    background: rgba(255,255,255,.96); color: var(--ink, #24292f);',
    '    box-shadow: 0 8px 26px rgba(36,41,47,.18); backdrop-filter: blur(8px);',
    '    font: 600 13px/1.2 var(--sans, sans-serif); cursor: pointer;',
    '  }',
    '  .fig-nav-toggle span:first-child { font-size: 14px; color: var(--accent, #0ea5e9); }',
    '  .fig-nav-toggle:hover { border-color: var(--accent, #0ea5e9); }',
    '  body.fig-nav-open .fig-nav-toggle { opacity: 0; pointer-events: none; }',
    '  .fig-nav-backdrop {',
    '    position: fixed; inset: 0; z-index: 1001; display: block;',
    '    background: rgba(20,32,42,.4); backdrop-filter: blur(2px);',
    '    opacity: 0; pointer-events: none; transition: opacity .25s ease;',
    '  }',
    '  body.fig-nav-open .fig-nav-backdrop { opacity: 1; pointer-events: auto; }',
    '}',
    '@media (prefers-reduced-motion: reduce) {',
    '  html { scroll-behavior: auto; }',
    '  .fig-sidenav, .fig-nav-backdrop, .fig-sidenav a, .fig-sidenav__list a::before { transition: none; }',
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
    '<div class="fig-sidenav__head">' +
    '<div class="fig-sidenav__title">本页目录<small></small></div>' +
    '<span class="fig-sidenav__progress" aria-hidden="true">0%</span>' +
    '<button class="fig-sidenav__close" type="button" aria-label="关闭目录">&times;</button></div>' +
    '<div class="fig-sidenav__body"><ul class="fig-sidenav__list"></ul>' +
    '<details class="fig-sidenav__cases"><summary>案例索引<span class="fig-sidenav__count"></span></summary>' +
    '<div class="fig-sidenav__case-groups"></div></details></div>' +
    '<button class="fig-sidenav__top" type="button">回到顶部</button>';
  document.body.appendChild(aside);
  document.body.classList.add('has-fig-sidenav');

  var headSmall = aside.querySelector('.fig-sidenav__title small');
  var progressEl = aside.querySelector('.fig-sidenav__progress');
  headSmall.textContent = SECTIONS.length + ' 章节';

  /* Chapter links, split into labelled groups */
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
    headSmall.textContent = SECTIONS.length + ' 章节 · ' + caseCount + ' 案例';
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

  /* Scroll spy + reading progress */
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

  function updateProgress() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - doc.clientHeight;
    var pct = max > 0 ? (window.scrollY / max) * 100 : 100;
    progressEl.textContent = Math.max(0, Math.min(100, Math.round(pct))) + '%';
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      var it = currentItem();
      if (it) setActive(it.a);
      updateProgress();
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
    updateProgress();
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
