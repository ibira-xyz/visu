import katex from "katex";

function renderKatexBlocks() {
  const blocks = document.querySelectorAll(".latex-block");

  blocks.forEach((block) => {
    const htmlBlock = block as HTMLElement;
    if (htmlBlock.dataset.katexRendered === "true") {
      return;
    }
    processKatexBlocks(htmlBlock);
  });
}

function processKatexBlocks(block: HTMLElement): HTMLElement | void {
  const latex = (
    block.dataset.latex ||
    block.textContent ||
    ""
  ).trim();
  const displayMode = block.classList.contains("displayMode");
  
  if (!latex) {
    return;
  }
  try {
    katex.render(latex, block, {
      displayMode: displayMode,
      throwOnError: true,
    });
    block.dataset.katexRendered = "true";
  } catch (error) {
    block.textContent = latex;
    console.warn("Failed to render LaTeX block with KaTeX.", error);
  }
}

if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it("processes LaTeX blocks with data-latex attribute", () => {
    const block = document.createElement("div");
    block.classList.add("latex-block");
    block.dataset.latex = "E=mc^2";
    document.body.appendChild(block);

    processKatexBlocks(block);

    expect(block.dataset.katexRendered).toBe("true");
    expect(block.querySelector(".katex-html")).not.toBeNull(); // Check if KaTeX rendered content is present
  });
  it("processes LaTeX blocks with text content", () => {
    const block = document.createElement("div");
    block.classList.add("latex-block");
    block.textContent = "E=mc^2";
    document.body.appendChild(block);

    processKatexBlocks(block);

    expect(block.dataset.katexRendered).toBe("true");
    expect(block.querySelector(".katex-html")).not.toBeNull(); // Check if KaTeX rendered content is present
  });
  it("processes LaTeX empty", () => {
    const block = document.createElement("div");
    block.classList.add("latex-block");
    document.body.appendChild(block);

    processKatexBlocks(block);

    expect(block.innerHTML).toBe("");
  });
  it("handles invalid LaTeX gracefully", () => {
    const block = document.createElement("div");
    block.classList.add("latex-block");
    block.dataset.latex = "\\invalidLatex{";
    document.body.appendChild(block);

    processKatexBlocks(block);

    expect(block.dataset.katexRendered).toBeUndefined();
    expect(block.textContent).toBe("\\invalidLatex{");
  });
} else {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderKatexBlocks);
  } else {
    renderKatexBlocks();
  }
}