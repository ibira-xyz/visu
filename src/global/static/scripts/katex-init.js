function renderKatexBlocks() {
  if (!window.katex) {
    return;
  }

  const blocks = document.querySelectorAll('.latex-block');

  blocks.forEach((block) => {
    if (block.dataset.katexRendered === 'true') {
      return;
    }

    const latex = (block.dataset.latex || block.textContent || '').trim();
    const displayMode = block.classList.contains('displayMode');

    if (!latex) {
      return;
    }

    try {
      window.katex.render(latex, block, {
        displayMode: displayMode,
        throwOnError: true,
      });
      block.dataset.katexRendered = 'true';
    } catch (error) {
      block.textContent = latex;
      console.warn('Failed to render LaTeX block with KaTeX.', error);
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderKatexBlocks);
} else {
  renderKatexBlocks();
}