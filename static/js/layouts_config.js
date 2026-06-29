// XYLab XHS Visual Studio - Layouts Configuration
const XYLAB_LAYOUTS = {
  "magazine-cover": {
    name: "Magazine Cover",
    description: "Large hero image, strong title, small English subtitle, volume label.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const textStyle = styleLock ? 'letter-spacing: 0.05em;' : '';
      const headlineStyle = styleLock 
        ? `font-family: ${displayFont}; font-weight: 300; font-size: 2.5rem; text-transform: uppercase; color: ${textPrimary};`
        : `font-family: ${displayFont}; font-weight: 800; font-size: 2.8rem; color: ${textPrimary};`;
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont}; ${textStyle}">
          <!-- Header Volume Info -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.3em] uppercase opacity-85 border-b pb-3" style="border-color: ${border}; color: ${textSecondary};">
            <div>XYLAB STUDIO // VOL. ${String(page.pageNumber || 1).padStart(2, '0')}</div>
            <div style="color: ${accent}; font-family: ${displayFont}; font-style: italic;">CREATIVE DIRECTION</div>
          </div>

          <!-- Hero Image & Headline Stack -->
          <div class="my-auto flex flex-col items-center relative py-6">
            ${page.imageUrl ? `
              <div class="w-full aspect-[4/3] rounded-2xl overflow-hidden mb-6 shadow-sm border" style="border-color: ${border}">
                <img src="${page.imageUrl}" class="w-full h-full object-cover grayscale-[20%]" style="${styleLock ? 'filter: contrast(95%) brightness(102%) saturate(85%);' : ''}">
              </div>
            ` : `
              <div class="w-full aspect-[4/3] rounded-2xl bg-gray-100 flex items-center justify-center mb-6 border border-dashed border-gray-300">
                <span class="text-xs text-gray-400">NO IMAGE</span>
              </div>
            `}

            <!-- Text Content -->
            <div class="w-full text-center px-2">
              <h1 class="leading-[1.15] mb-2 tracking-tighter" style="${headlineStyle}">
                ${page.headline || "UNTITLED COVER"}
              </h1>
              <p class="text-[10px] tracking-[0.25em] uppercase opacity-75 mt-3" style="color: ${textSecondary}; font-family: ${displayFont}; font-style: italic;">
                ${page.subheadline || "visual storytelling project"}
              </p>
            </div>
          </div>

          <!-- Footer Branding -->
          <div class="flex justify-between items-end border-t pt-3" style="border-color: ${border};">
            <div class="flex flex-col">
              <span class="text-[7px] tracking-widest opacity-60" style="color: ${textSecondary};">XYLAB OS Matrix</span>
              <span class="text-[9px] font-bold tracking-wider" style="color: ${textPrimary};">BY XYLAB MUSE</span>
            </div>
            <div class="text-[14px] font-thin opacity-80" style="font-family: ${displayFont}; color: ${accent}; font-style: italic;">
              No. ${page.pageNumber || 1}
            </div>
          </div>
        </div>
      `;
    }
  },
  "split-editorial": {
    name: "Split Editorial",
    description: "Image on one side, text on the other. Good for beauty, gems, fragrance, travel.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const isRightImage = page.pageNumber % 2 === 0;

      const titleStyle = `font-family: ${displayFont}; font-weight: ${styleLock ? '300' : '700'}; color: ${textPrimary};`;

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>${page.subheadline || "INSIGHTS"}</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Split Container -->
          <div class="my-auto grid grid-cols-2 gap-4 items-center py-4">
            ${!isRightImage && page.imageUrl ? `
              <div class="h-full aspect-[3/4] rounded-xl overflow-hidden shadow-sm border" style="border-color: ${border}">
                <img src="${page.imageUrl}" class="w-full h-full object-cover" style="${styleLock ? 'filter: saturate(80%) contrast(98%);' : ''}">
              </div>
            ` : ''}

            <div class="flex flex-col justify-center space-y-3 ${isRightImage ? 'pr-2' : 'pl-2'}">
              <span class="text-[8px] uppercase tracking-widest opacity-60" style="color: ${accent}; font-family: ${displayFont}; font-style: italic;">NOTE ${page.pageNumber}</span>
              <h2 class="text-lg leading-tight" style="${titleStyle}">
                ${page.headline || "Untitled"}
              </h2>
              <div class="h-[1px] w-8" style="background-color: ${accent}"></div>
              <p class="text-[11px] leading-[1.7] text-justify whitespace-pre-wrap opacity-95" style="color: ${textSecondary};">
                ${page.body || ""}
              </p>
              ${page.smallNote ? `
                <p class="text-[9px] italic opacity-70 border-l pl-2" style="border-color: ${accent}; color: ${textSecondary};">
                  ${page.smallNote}
                </p>
              ` : ''}
            </div>

            ${isRightImage && page.imageUrl ? `
              <div class="h-full aspect-[3/4] rounded-xl overflow-hidden shadow-sm border" style="border-color: ${border}">
                <img src="${page.imageUrl}" class="w-full h-full object-cover" style="${styleLock ? 'filter: saturate(80%) contrast(98%);' : ''}">
              </div>
            ` : ''}
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Aesthetic Workspace</div>
            <div class="uppercase tracking-widest">© XYLAB 2026</div>
          </div>
        </div>
      `;
    }
  },
  "info-card": {
    name: "Info Card",
    description: "Clean knowledge card. Good for skincare, ingredients, gems, haircare.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;
      
      const items = (page.body || "").split('\n').filter(i => i.trim().length > 0);
      const itemsHtml = items.map((item, idx) => `
        <div class="flex items-start space-x-3 py-2 border-b last:border-0" style="border-color: ${border}">
          <span class="text-[10px] font-bold tracking-tighter opacity-80" style="color: ${accent}; font-family: ${displayFont};">
            0${idx+1}
          </span>
          <span class="text-[11px] leading-[1.6] opacity-90" style="color: ${textSecondary};">${item}</span>
        </div>
      `).join('');

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>${page.subheadline || "TECHNICAL BREAKDOWN"}</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Info Box Box -->
          <div class="my-auto flex flex-col space-y-4">
            <!-- Headline block -->
            <div>
              <h2 class="text-xl font-bold tracking-tight mb-1" style="font-family: ${displayFont}; color: ${textPrimary};">
                ${page.headline || "Ingredients Focus"}
              </h2>
              ${page.smallNote ? `<p class="text-[9px] uppercase tracking-widest opacity-60" style="color: ${accent};">${page.smallNote}</p>` : ''}
            </div>

            <!-- Content Card -->
            <div class="p-5 rounded-2xl border" style="background-color: ${cardBg}; border-color: ${border};">
              <div class="flex flex-col divide-y divide-gray-100">
                ${itemsHtml || `<div class="text-xs text-gray-400">No content details available</div>`}
              </div>
            </div>

            ${page.imageUrl ? `
              <div class="w-full h-24 rounded-xl overflow-hidden shadow-inner border" style="border-color: ${border}">
                <img src="${page.imageUrl}" class="w-full h-full object-cover grayscale-[30%]" style="${styleLock ? 'filter: saturate(80%);' : ''}">
              </div>
            ` : ''}
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Lab Analysis</div>
            <div>CONFIDENTIAL WORKPRINT</div>
          </div>
        </div>
      `;
    }
  },
  "moodboard-archive": {
    name: "Moodboard Archive",
    description: "Grid or collage layout. Good for fantasy visuals, travel, gems, AI visual collections.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>MOODBOARD ARCHIVE</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Collage Content -->
          <div class="my-auto flex flex-col space-y-4 py-2">
            <div class="grid grid-cols-3 gap-2">
              <div class="col-span-2 aspect-[4/3] rounded-xl overflow-hidden border shadow-sm" style="border-color: ${border}">
                ${page.imageUrl ? `
                  <img src="${page.imageUrl}" class="w-full h-full object-cover">
                ` : `<div class="w-full h-full bg-gray-100 flex items-center justify-center text-xs text-gray-400">HERO</div>`}
              </div>
              <div class="aspect-[3/4] rounded-xl overflow-hidden border shadow-sm bg-gray-50 flex items-center justify-center p-3 text-center" style="border-color: ${border}">
                <p class="text-[9px] italic leading-tight" style="font-family: ${displayFont}; color: ${textSecondary};">
                  "${page.subheadline || "Aesthetic vision"}"
                </p>
              </div>
            </div>

            <!-- Bottom details card -->
            <div class="p-4 rounded-xl border flex flex-col space-y-2" style="background-color: ${cardBg}; border-color: ${border};">
              <h3 class="text-xs uppercase font-bold tracking-wider" style="color: ${textPrimary}; font-family: ${displayFont};">
                ${page.headline || "Selected Mood"}
              </h3>
              <p class="text-[10px] leading-relaxed opacity-85" style="color: ${textSecondary};">
                ${page.body || ""}
              </p>
              ${page.smallNote ? `
                <div class="text-[8px] uppercase tracking-widest opacity-50" style="color: ${accent};">
                  ${page.smallNote}
                </div>
              ` : ''}
            </div>
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>Collection Archives // XYLab OS</div>
            <div>VERIFIED 2026</div>
          </div>
        </div>
      `;
    }
  },
  "routine-flow": {
    name: "Routine Flow",
    description: "Step-by-step flow. Good for skincare routine, makeup breakdown, workout sequence.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;
      
      const steps = (page.body || "").split('\n').filter(i => i.trim().length > 0);
      const stepsHtml = steps.map((step, idx) => `
        <div class="flex items-center space-x-3 bg-white p-3 rounded-xl border shadow-sm" style="border-color: ${border}; background-color: ${cardBg};">
          <div class="w-6 h-6 rounded-full flex items-center justify-center text-[9px] font-bold text-white shadow-sm" style="background-color: ${accent};">
            ${idx+1}
          </div>
          <div class="flex-1">
            <span class="text-[11px] leading-[1.5] block font-medium" style="color: ${textPrimary};">${step}</span>
          </div>
        </div>
      `).join('');

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>ROUTINE & METHODOLOGY</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Routine Body -->
          <div class="my-auto flex flex-col space-y-4 py-2">
            <div>
              <h2 class="text-xl font-bold tracking-tight mb-1" style="font-family: ${displayFont}; color: ${textPrimary};">
                ${page.headline || "Step-by-Step Guide"}
              </h2>
              <p class="text-[10px] tracking-wide opacity-80" style="color: ${textSecondary};">
                ${page.subheadline || "Follow the structured algorithm below"}
              </p>
            </div>

            <!-- Steps Stack -->
            <div class="flex flex-col space-y-2">
              ${stepsHtml || `<div class="text-xs text-gray-400">No step instructions provided</div>`}
            </div>

            ${page.smallNote ? `
              <div class="text-[9px] p-3 rounded-lg border border-dashed text-center opacity-80 italic" style="border-color: ${accent}; color: ${textSecondary};">
                💡 Note: ${page.smallNote}
              </div>
            ` : ''}
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Personal Routine Guide</div>
            <div>EXPORT WORKFLOW</div>
          </div>
        </div>
      `;
    }
  },
  "before-after": {
    name: "Before / After",
    description: "Comparison layout. Good for makeup, hair, skin, body transformation.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>COMPARISON STUDIES</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Before / After Grid -->
          <div class="my-auto flex flex-col space-y-4 py-2">
            <div>
              <h2 class="text-xl font-bold tracking-tight" style="font-family: ${displayFont}; color: ${textPrimary};">
                ${page.headline || "Transformation Analysis"}
              </h2>
              <p class="text-[10px] opacity-75" style="color: ${textSecondary};">${page.subheadline || "Direct physical comparison evaluation"}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col space-y-1">
                <div class="aspect-[3/4] rounded-xl overflow-hidden border shadow-sm bg-gray-50 flex items-center justify-center relative" style="border-color: ${border}">
                  ${page.imageUrl ? `
                    <img src="${page.imageUrl}" class="w-full h-full object-cover saturate-50 brightness-90">
                  ` : `<span class="text-xs text-gray-400">NO IMG</span>`}
                  <span class="absolute top-2 left-2 text-[8px] font-black bg-black/60 text-white px-2 py-0.5 rounded tracking-widest">BEFORE</span>
                </div>
              </div>
              <div class="flex flex-col space-y-1">
                <div class="aspect-[3/4] rounded-xl overflow-hidden border shadow-sm bg-gray-50 flex items-center justify-center relative" style="border-color: ${border}">
                  ${page.imageUrl ? `
                    <img src="${page.imageUrl}" class="w-full h-full object-cover">
                  ` : `<span class="text-xs text-gray-400">NO IMG</span>`}
                  <span class="absolute top-2 left-2 text-[8px] font-black bg-white/80 text-black px-2 py-0.5 rounded tracking-widest" style="color: ${textPrimary};">AFTER</span>
                </div>
              </div>
            </div>

            <!-- Notes card -->
            <div class="p-4 rounded-xl border" style="background-color: ${cardBg}; border-color: ${border};">
              <p class="text-[11px] leading-relaxed" style="color: ${textSecondary};">
                ${page.body || "Direct side-by-side verification reveals distinct improvement."}
              </p>
              ${page.smallNote ? `<p class="text-[9px] mt-1 italic font-bold opacity-80" style="color: ${accent};">${page.smallNote}</p>` : ''}
            </div>
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Lab Trial #2026</div>
            <div>VERIFIED ARCHIVE</div>
          </div>
        </div>
      `;
    }
  },
  "quote-page": {
    name: "Quote / Thought Page",
    description: "One strong thought with generous whitespace. Good for reading, cultural salon, personal growth.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>THOUGHT REPOSITORY</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Quote Block -->
          <div class="my-auto flex flex-col space-y-6 px-4">
            <span class="text-5xl font-serif leading-none" style="color: ${accent}; font-family: ${displayFont}; opacity: 0.8;">“</span>
            
            <h1 class="text-xl leading-[1.7] text-justify font-light" style="font-family: ${displayFont}; color: ${textPrimary};">
              ${page.body || page.headline || "Write your core insights here."}
            </h1>
            
            <div class="flex items-center space-x-2 pt-2">
              <div class="h-[1px] w-8" style="background-color: ${accent}"></div>
              <span class="text-[9px] uppercase tracking-[0.25em]" style="color: ${textSecondary};">
                — ${page.subheadline || "XYLAB SALON DIARIES"}
              </span>
            </div>
            
            ${page.smallNote ? `
              <p class="text-[8px] tracking-widest uppercase opacity-55 pt-2" style="color: ${textSecondary};">
                Category // ${page.smallNote}
              </p>
            ` : ''}
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Cultural Dialogues</div>
            <div>2026 EDITION</div>
          </div>
        </div>
      `;
    }
  },
  "product-catalog": {
    name: "Product Catalog",
    description: "Product matrix layout. Good for beauty products, fragrances, jewelry, outfits.",
    render: (page, theme, styleLock) => {
      const displayFont = theme.fonts.display;
      const sansFont = theme.fonts.sans;
      const textPrimary = theme.colors.textPrimary;
      const textSecondary = theme.colors.textSecondary;
      const accent = theme.colors.accent;
      const border = theme.colors.border;
      
      const containerBg = theme.colors.background;
      const cardBg = theme.colors.card;

      const items = (page.body || "").split('\n').filter(i => i.trim().length > 0);
      const itemsHtml = items.map((item, idx) => {
        const parts = item.split(':');
        const key = parts[0] || 'Spec';
        const val = parts[1] || 'Value';
        return `
          <div class="flex justify-between items-center py-1.5 border-b border-dashed last:border-0" style="border-color: ${border}">
            <span class="text-[10px] opacity-75" style="color: ${textSecondary};">${key}</span>
            <span class="text-[10px] font-bold" style="color: ${textPrimary};">${val}</span>
          </div>
        `;
      }).join('');

      return `
        <div class="w-full h-full p-8 flex flex-col justify-between" style="background-color: ${containerBg}; font-family: ${sansFont};">
          <!-- Page Header -->
          <div class="flex justify-between items-center text-[9px] tracking-[0.2em] uppercase opacity-75 border-b pb-2" style="border-color: ${border}; color: ${textSecondary};">
            <div>PRODUCT SPECIFICATION</div>
            <div>PAGE 0${page.pageNumber}</div>
          </div>

          <!-- Catalog Details -->
          <div class="my-auto flex flex-col space-y-4 py-2">
            <div class="grid grid-cols-5 gap-3 items-center">
              <div class="col-span-3 aspect-[3/4] rounded-xl overflow-hidden border shadow-sm bg-gray-50" style="border-color: ${border}">
                ${page.imageUrl ? `
                  <img src="${page.imageUrl}" class="w-full h-full object-cover">
                ` : `<div class="w-full h-full flex items-center justify-center text-xs text-gray-400">PRODUCT</div>`}
              </div>
              <div class="col-span-2 flex flex-col space-y-2 pr-1">
                <span class="text-[8px] uppercase tracking-widest opacity-60" style="color: ${accent}; font-family: ${displayFont}; font-style: italic;">
                  ${page.smallNote || "RECOMMENDED"}
                </span>
                <h3 class="text-sm font-bold leading-tight" style="color: ${textPrimary}; font-family: ${displayFont};">
                  ${page.headline || "Product Name"}
                </h3>
                <p class="text-[9px] leading-relaxed opacity-75" style="color: ${textSecondary};">
                  ${page.subheadline || "Premium luxury series."}
                </p>
              </div>
            </div>

            <!-- Specs list card -->
            <div class="p-4 rounded-xl border" style="background-color: ${cardBg}; border-color: ${border};">
              <div class="flex flex-col">
                ${itemsHtml || `
                  <div class="flex justify-between py-1 border-b last:border-0" style="border-color: ${border}">
                    <span class="text-[10px] text-gray-400">Ingredients</span>
                    <span class="text-[10px] font-bold">100% Organic</span>
                  </div>
                `}
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex justify-between items-center text-[8px] opacity-60" style="color: ${textSecondary}; border-top: 1px solid ${border}; pt-2">
            <div>XYLab Catalog Index</div>
            <div>VERIFIED ARCHIVE</div>
          </div>
        </div>
      `;
    }
  }
};
