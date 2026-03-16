/**
 * XYLAB 'STANCE CORE' Markdown Converter
 * Converts standard Markdown to architectural HTML/CSS structure.
 */

const STANCE_CORE_CONVERTER = {
    convert: function (markdown) {
        let html = markdown;

        // 1. Blockquotes with XYLAB watermark
        html = html.replace(/^>\s?(.*)$/gm, '<blockquote class="xylabs-blockquote">$1</blockquote>');

        // 2. Images with lightbox glow
        html = html.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="lightbox-img">');

        // 3. Process blocks (Lists, Snippets, Headers, Paragraphs)
        const blocks = html.split('\n\n');
        html = blocks.map(block => {
            const trimmed = block.trim();

            // Skip already processed images/blockquotes
            if (trimmed.startsWith('<img') || trimmed.startsWith('<blockquote')) {
                return block;
            }

            // A. Luxury Snippets (Lines starting with !! or simple Python-like lines if we want to be fancy)
            // For simplicity, let's look for markdown code blocks or a prefix
            if (trimmed.startsWith('```python') || trimmed.startsWith('!!')) {
                const content = trimmed.replace(/```python|```|!!/g, '').trim();
                return `<div class="luxury-snippet">${content}</div>`;
            }

            // B. Ordered Lists (01, 02 markers)
            if (/^\d+\.\s/.test(trimmed)) {
                const items = trimmed.split('\n').filter(i => /\d+\.\s/.test(i));
                const listHtml = items.map(item => `<li>${item.replace(/^\d+\.\s/, '')}</li>`).join('');
                return `<ol class="ordered-list-0x">${listHtml}</ol>`;
            }

            // C. Headers
            if (trimmed.startsWith('#')) {
                const level = (trimmed.match(/^#+/) || ['#'])[0].length;
                const content = trimmed.replace(/^#+\s?/, '');
                const fontStyle = level === 1 ? 'font-family: var(--font-serif); font-size: 4rem;' : 'font-weight: 300;';
                return `<h${level} style="${fontStyle} margin-bottom: 2rem;">${content}</h${level}>`;
            }

            // D. Paragraphs with Word count logic for asymmetric flow
            if (trimmed.length === 0) return '';
            const wordCount = trimmed.split(/\s+/).length;
            const alignmentClass = wordCount < 50 ? 'align-right' : '';
            return `<p class="premium-p ${alignmentClass}">${trimmed}</p>`;
        }).join('\n\n');

        return html;
    }
};

// Example usage and dynamic loading for the demo
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        const contentArea = document.getElementById('stances-content');
        if (contentArea) {
            const rawMarkdown = contentArea.textContent.trim();
            contentArea.innerHTML = STANCE_CORE_CONVERTER.convert(rawMarkdown);
            contentArea.style.opacity = 1;
        }
    });
}
