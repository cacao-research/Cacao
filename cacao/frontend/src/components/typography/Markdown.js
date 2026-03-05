/**
 * Markdown component - renders markdown with full prose styling
 *
 * Features:
 * - Prose typography (headings, paragraphs, lists, blockquotes)
 * - Code blocks with copy button
 * - GFM tables, task lists, strikethrough
 * - Callout blocks ([!NOTE], [!WARNING], [!TIP], [!IMPORTANT], [!CAUTION])
 * - Mermaid diagrams (lazy-loaded from CDN)
 * - KaTeX math (lazy-loaded from CDN)
 * - Auto-linking URLs
 * - Optional table of contents
 * - Image sizing via ![alt|WxH](url)
 */

const { createElement: h, useState, useEffect, useRef, useCallback, useMemo } = React;
import { Marked } from 'marked';

// Callout types and their icons/labels
const CALLOUT_TYPES = {
  NOTE: { icon: '\u2139\uFE0F', className: 'callout-note' },
  TIP: { icon: '\uD83D\uDCA1', className: 'callout-tip' },
  IMPORTANT: { icon: '\u2757', className: 'callout-important' },
  WARNING: { icon: '\u26A0\uFE0F', className: 'callout-warning' },
  CAUTION: { icon: '\uD83D\uDED1', className: 'callout-caution' },
};

/**
 * Custom marked extension for callout blocks
 * Transforms blockquotes starting with [!TYPE] into styled callouts
 */
function calloutExtension() {
  return {
    renderer: {
      blockquote(token) {
        const body = this.parser.parse(token.tokens);
        // Check if the blockquote starts with [!TYPE]
        const match = body.match(/^\s*<p>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*<br\s*\/?>\s*/i);
        if (!match) {
          const matchNewline = body.match(/^\s*<p>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*\n/i);
          if (!matchNewline) return `<blockquote>${body}</blockquote>\n`;
          const type = matchNewline[1].toUpperCase();
          const callout = CALLOUT_TYPES[type];
          const content = body.replace(matchNewline[0], '<p>');
          return `<div class="callout ${callout.className}"><div class="callout-title">${callout.icon} ${type.charAt(0) + type.slice(1).toLowerCase()}</div><div class="callout-body">${content}</div></div>\n`;
        }
        const type = match[1].toUpperCase();
        const callout = CALLOUT_TYPES[type];
        const content = body.replace(match[0], '<p>');
        return `<div class="callout ${callout.className}"><div class="callout-title">${callout.icon} ${type.charAt(0) + type.slice(1).toLowerCase()}</div><div class="callout-body">${content}</div></div>\n`;
      }
    }
  };
}

/**
 * Custom renderer for code blocks (copy button + mermaid/math detection)
 */
function codeBlockExtension() {
  return {
    renderer: {
      code(token) {
        const text = token.text;
        const lang = (token.lang || '').trim();

        if (lang === 'mermaid') {
          return `<div class="mermaid-block" data-mermaid="${encodeURIComponent(text)}"><pre class="mermaid-loading"><code>${text}</code></pre></div>`;
        }

        const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return `<div class="prose-code-wrapper"><pre class="c-code language-${lang}"><button class="c-code-copy" aria-label="Copy code">Copy</button><code>${escaped}</code></pre></div>`;
      }
    }
  };
}

/**
 * Custom renderer for images with size syntax: ![alt|WxH](url)
 */
function imageSizeExtension() {
  return {
    renderer: {
      image(token) {
        let alt = token.text || '';
        const src = token.href || '';
        const title = token.title ? ` title="${token.title}"` : '';

        // Check for size syntax: alt|WxH or alt|W
        const sizeMatch = alt.match(/^(.*?)\|(\d+)(?:x(\d+))?$/);
        let style = '';
        if (sizeMatch) {
          alt = sizeMatch[1];
          const width = sizeMatch[2];
          const height = sizeMatch[3];
          style = ` style="width:${width}px${height ? `;height:${height}px` : ''}"`;
        }

        return `<img src="${src}" alt="${alt}"${title}${style} />`;
      }
    }
  };
}

/**
 * Process inline math ($...$) and block math ($$...$$)
 */
function preprocessMath(text) {
  // Block math: $$...$$
  text = text.replace(/\$\$([\s\S]+?)\$\$/g, (_, math) => {
    return `<div class="math-block" data-math="${encodeURIComponent(math.trim())}">$$${math}$$</div>`;
  });
  // Inline math: $...$  (not $$)
  text = text.replace(/(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)/g, (_, math) => {
    return `<span class="math-inline" data-math="${encodeURIComponent(math.trim())}">$${math}$</span>`;
  });
  return text;
}

/**
 * Extract headings from markdown for TOC generation
 */
function extractHeadings(markdown) {
  const headings = [];
  const lines = markdown.split('\n');
  let inCodeBlock = false;

  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    const match = line.match(/^(#{1,6})\s+(.+)/);
    if (match) {
      const level = match[1].length;
      const text = match[2].replace(/[*_`~\[\]]/g, '');
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
      headings.push({ level, text, id });
    }
  }

  return headings;
}

/**
 * Add id attributes to rendered headings for anchor links
 */
function headingIdExtension() {
  return {
    renderer: {
      heading(token) {
        const text = token.text;
        const depth = token.depth;
        const raw = token.raw || text;
        const id = raw.replace(/^#+\s*/, '').replace(/[*_`~\[\]]/g, '').toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
        return `<h${depth} id="${id}">${this.parser.parseInline(token.tokens)}</h${depth}>\n`;
      }
    }
  };
}

/**
 * Create a configured marked instance
 */
function createMarkedInstance() {
  const marked = new Marked();
  marked.use({ gfm: true, breaks: true });
  marked.use(headingIdExtension());
  marked.use(calloutExtension());
  marked.use(codeBlockExtension());
  marked.use(imageSizeExtension());
  return marked;
}

// Singleton marked instance
let markedInstance = null;
function getMarked() {
  if (!markedInstance) {
    markedInstance = createMarkedInstance();
  }
  return markedInstance;
}

/**
 * Initialize mermaid diagrams in a container
 */
async function initMermaid(container) {
  const blocks = container.querySelectorAll('.mermaid-block');
  if (blocks.length === 0) return;

  // Lazy-load mermaid from CDN
  if (!window.mermaid) {
    try {
      await new Promise((resolve, reject) => {
        if (document.querySelector('script[data-mermaid]')) {
          // Already loading, wait for it
          const check = setInterval(() => {
            if (window.mermaid) { clearInterval(check); resolve(); }
          }, 100);
          setTimeout(() => { clearInterval(check); reject(new Error('Mermaid load timeout')); }, 10000);
          return;
        }
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
        script.setAttribute('data-mermaid', 'true');
        script.onload = () => {
          window.mermaid.initialize({
            startOnLoad: false,
            theme: document.documentElement.getAttribute('data-theme') === 'light' ? 'default' : 'dark',
            securityLevel: 'loose',
          });
          resolve();
        };
        script.onerror = reject;
        document.head.appendChild(script);
      });
    } catch (e) {
      console.warn('Failed to load mermaid:', e);
      return;
    }
  }

  for (const block of blocks) {
    const code = decodeURIComponent(block.dataset.mermaid);
    try {
      const id = 'mermaid-' + Math.random().toString(36).slice(2, 9);
      const { svg } = await window.mermaid.render(id, code);
      block.innerHTML = svg;
      block.classList.add('mermaid-rendered');
    } catch (e) {
      console.warn('Mermaid render error:', e);
    }
  }
}

/**
 * Initialize KaTeX math in a container
 */
async function initKaTeX(container) {
  const mathBlocks = container.querySelectorAll('.math-block, .math-inline');
  if (mathBlocks.length === 0) return;

  // Lazy-load KaTeX from CDN
  if (!window.katex) {
    try {
      await new Promise((resolve, reject) => {
        if (document.querySelector('link[data-katex]')) {
          const check = setInterval(() => {
            if (window.katex) { clearInterval(check); resolve(); }
          }, 100);
          setTimeout(() => { clearInterval(check); reject(new Error('KaTeX load timeout')); }, 10000);
          return;
        }
        // Load CSS
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css';
        link.setAttribute('data-katex', 'true');
        document.head.appendChild(link);
        // Load JS
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    } catch (e) {
      console.warn('Failed to load KaTeX:', e);
      return;
    }
  }

  for (const el of mathBlocks) {
    const math = decodeURIComponent(el.dataset.math);
    const isBlock = el.classList.contains('math-block');
    try {
      el.innerHTML = window.katex.renderToString(math, {
        displayMode: isBlock,
        throwOnError: false,
      });
      el.classList.add('math-rendered');
    } catch (e) {
      console.warn('KaTeX render error:', e);
    }
  }
}

/**
 * Attach copy button handlers to code blocks
 */
function attachCopyHandlers(container) {
  const buttons = container.querySelectorAll('.c-code-copy');
  for (const btn of buttons) {
    btn.addEventListener('click', () => {
      const code = btn.closest('pre').querySelector('code');
      if (!code) return;
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      }).catch(() => {
        btn.textContent = 'Failed';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      });
    });
  }
}

export function Markdown({ props }) {
  const { content, toc = false } = props;
  const containerRef = useRef(null);

  // Parse markdown
  const { html, headings } = useMemo(() => {
    if (!content) return { html: '', headings: [] };
    const md = getMarked();
    const processed = preprocessMath(content);
    const rendered = md.parse(processed);
    const heads = toc ? extractHeadings(content) : [];
    return { html: rendered, headings: heads };
  }, [content, toc]);

  // Post-render: init mermaid, katex, copy buttons
  useEffect(() => {
    if (!containerRef.current) return;
    attachCopyHandlers(containerRef.current);
    initMermaid(containerRef.current);
    initKaTeX(containerRef.current);
  }, [html]);

  const handleTocClick = useCallback((e) => {
    const id = e.target.dataset.tocId;
    if (!id) return;
    e.preventDefault();
    const el = containerRef.current?.querySelector(`#${CSS.escape(id)}`);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }, []);

  if (toc && headings.length > 0) {
    return h('div', { className: 'prose-with-toc' }, [
      h('nav', {
        key: 'toc',
        className: 'prose-toc',
        onClick: handleTocClick
      }, [
        h('div', { key: 'toc-title', className: 'prose-toc-title' }, 'Contents'),
        ...headings.map((heading, i) =>
          h('a', {
            key: i,
            href: `#${heading.id}`,
            className: `prose-toc-item prose-toc-level-${heading.level}`,
            'data-toc-id': heading.id,
          }, heading.text)
        )
      ]),
      h('div', {
        key: 'content',
        ref: containerRef,
        className: 'prose',
        dangerouslySetInnerHTML: { __html: html }
      })
    ]);
  }

  return h('div', {
    ref: containerRef,
    className: 'prose',
    dangerouslySetInnerHTML: { __html: html }
  });
}
