(() => {
  const button = document.getElementById('post-language');
  const body = document.getElementById('post-body');
  const original = document.getElementById('post-original');
  const headings = [...document.querySelectorAll(".post-heading [data-original]")];
  const englishHeadings = headings.map(heading => heading.textContent);
  const english = document.createDocumentFragment();
  let showingOriginal = false;

  button.addEventListener('click', () => {
    showingOriginal = !showingOriginal;
    if (showingOriginal) {
      english.append(...body.childNodes);
      body.replaceChildren(original.content.cloneNode(true));
    } else {
      body.replaceChildren(english);
    }
    const language = showingOriginal ? 'zh-CN' : 'en';
    body.lang = language;
    headings.forEach((heading, index) => {
      heading.lang = language;
      heading.textContent = showingOriginal ? heading.dataset.original : englishHeadings[index];
    });
    button.textContent = showingOriginal ? 'Read in English' : '查看中文原文';
    button.lang = showingOriginal ? 'en' : 'zh-CN';
    if (typeof generateCatalog === 'function') {
      document.querySelector('.catalog-body').replaceChildren();
      generateCatalog('.catalog-body');
    }
  });
  button.lang = 'zh-CN';
  button.hidden = false;
})();
