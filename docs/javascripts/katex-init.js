/* KaTeX auto-render 配置：渲染 arithmatex 输出的 \( \) / \[ \] 与 $$ 定界公式。
   脚本由 mkdocs 按 extra_javascript 顺序在 auto-render 之后加载。
   解锁系统注入新内容后，可调用 window.renderBookMath(el) 对局部重渲染。 */
(function () {
  var OPTS = {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
    throwOnError: false,
    errorColor: "#cc0000",
  };

  window.renderBookMath = function (el) {
    if (typeof renderMathInElement !== "function") return;
    renderMathInElement(el || document.body, OPTS);
  };

  function renderMath() {
    if (typeof renderMathInElement !== "function") return;
    window.renderBookMath(document.body);
    document.body.dataset.mathRendered = "1";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderMath);
  } else {
    renderMath();
  }
})();
