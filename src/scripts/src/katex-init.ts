import katex from "katex";

function renderKatexBlocks() {
  const blocks = document.querySelectorAll(".latex-block");

  blocks.forEach((block) => {
    const htmlBlock = block as HTMLElement;
    if (htmlBlock.dataset.katexRendered === "true") {
      return;
    }

    const latex = (
      htmlBlock.dataset.latex ||
      htmlBlock.textContent ||
      ""
    ).trim();
    const displayMode = htmlBlock.classList.contains("displayMode");

    if (!latex) {
      return;
    }

    try {
      katex.render(latex, htmlBlock, {
        displayMode: displayMode,
        throwOnError: true,
      });
      htmlBlock.dataset.katexRendered = "true";
    } catch (error) {
      htmlBlock.textContent = latex;
      console.warn("Failed to render LaTeX block with KaTeX.", error);
    }
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderKatexBlocks);
} else {
  renderKatexBlocks();
}
