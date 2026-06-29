// XYLab XHS Visual Studio - Carousel Generator & State Manager

// Single source of truth for the project state
const studioState = {
  projectTitle: "",
  idea: "",
  uploadedAssets: [], // Array of data URLs
  creativeBrief: null,
  selectedTheme: "beauty",
  styleLockEnabled: true,
  pageCount: 6,
  activePageIndex: 0,
  pages: [],
  caption: "",
  hashtags: []
};

// Global style overrides
const globalOverrides = {
  fontPair: "",       // "serif-sans", "sans-sans"
  logoPosition: "bottom-right", // "bottom-right", "bottom-left", "top-right", "top-left", "none"
  accentColor: ""     // Hex color
};

// Wrap external image URLs in CORS proxy
function ensureProxyUrl(url) {
  if (!url) return "";
  if (url.startsWith("data:") || url.startsWith("/api/proxy-image") || url.startsWith("http://localhost") || url.startsWith("/")) {
    return url;
  }
  return `/api/proxy-image?url=${encodeURIComponent(url)}`;
}

// Local mock brief generator fallback
function mockGenerateBrief(prompt) {
  return {
    detectedTopic: prompt || "清冷秋季日常妆",
    recommendedFormat: "6-page-carousel",
    suggestedTheme: "XYLab Beauty",
    visualMood: ["platinum", "soft pink", "clean editorial"],
    copyTone: "calm editorial, slightly confident",
    recommendedLayoutPack: "Magazine Cover",
    narrativeArc: [
      "Cover: 白金发色之后的清冷妆容公式 ❄️",
      "Page 01: 核心洞察：为什么发色越浅，结构感越重要",
      "Page 02: 避坑指南：告别廉价低俗感，降低面部饱和度",
      "Page 03: 步骤拆解：高光与阴影修容的精准定位",
      "Page 04: 好物推荐：适合冷皮的修容与眼影单品",
      "Page 05: 总结与互动：评论区留下你的发色"
    ]
  };
}

// Local mock carousel generator fallback
function mockGenerateCarousel(brief, themeKey, pageCount) {
  const topic = brief.detectedTopic || "清冷美学";
  const mood = brief.visualMood || ["clean", "glowy"];
  const layouts = ["magazine-cover", "split-editorial", "info-card", "routine-flow", "before-after", "quote-page", "product-catalog"];
  
  const pages = [];
  for (let i = 0; i < pageCount; i++) {
    let layout = layouts[i % layouts.length];
    if (i === 0) layout = "magazine-cover";
    else if (i === pageCount - 1) layout = "quote-page";
    
    // Choose fallback image from theme presets or static library
    const theme = XYLAB_THEMES[themeKey] || XYLAB_THEMES.default;
    let img = "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80";
    if (studioState.uploadedAssets.length > 0) {
      img = studioState.uploadedAssets[i % studioState.uploadedAssets.length];
    } else if (theme.presets && theme.presets.length > 0) {
      img = theme.presets[i % theme.presets.length];
    }

    pages.push({
      id: `page_${i}`,
      pageNumber: i + 1,
      type: i === 0 ? "cover" : (i === pageCount - 1 ? "summary" : "detail"),
      headline: i === 0 ? topic : `${brief.narrativeArc[i] || '干货分享 ' + i}`,
      subheadline: i === 0 ? "XYLAB EDITORIAL LAB" : `CONCEPT HIGHLIGHT // 0${i}`,
      body: i === 0 ? "" : `• 降低妆容饱和度，避免色彩冲突。\n• 用冷灰色调修容勾勒面部轮廓。\n• 选择哑光质地的眼影和腮红。`,
      smallNote: i === 0 ? "VOL. 01 / XYLAB MUSE" : `AESTHETIC ANALYSIS ${i}`,
      layout: layout,
      imageRole: i === 0 ? "hero" : "supporting",
      imageUrl: img,
      accent: theme.colors.accent || "",
      textAlign: layout === "quote-page" || layout === "magazine-cover" ? "center" : "left",
      density: "medium",
      logoPosition: globalOverrides.logoPosition
    });
  }

  return {
    projectTitle: topic,
    theme: themeKey,
    format: `${pageCount}-page-carousel`,
    visualMood: mood,
    pages: pages,
    caption: `💡 ${topic}\n\n这套内容是根据您的创作想法生成的完整小红书卡片大纲。\n\n包含核心卖点和详细步骤拆解，排版极具杂志高级感。\n\n#小红书排版 #高级感 #审美提升 #XYLab #清冷妆容`,
    hashtags: [`#${topic.replace(/\s+/g, '')}`, "#小红书排版", "#高级感", "#XYLab"]
  };
}

// API: Generate brief
async function requestBriefAPI(prompt, base64Image = null) {
  try {
    const response = await fetch("/api/xhs/generate-brief", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, image: base64Image })
    });
    if (!response.ok) throw new Error();
    return await response.json();
  } catch (err) {
    console.warn("XHS Generator: Brief API failed, using mock.");
    return mockGenerateBrief(prompt);
  }
}

// API: Generate full project
async function requestCarouselAPI(brief, themeKey, pageCount) {
  try {
    const themeName = XYLAB_THEMES[themeKey]?.name || "XYLab Default";
    const response = await fetch("/api/xhs/generate-carousel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ brief, theme: themeName, pageCount })
    });
    if (!response.ok) throw new Error();
    const project = await response.json();
    
    // Validate project schema
    project.pages.forEach((p, idx) => {
      p.id = p.id || `page_${idx}`;
      p.pageNumber = idx + 1;
      p.imageUrl = p.imageUrl || getCuratedImageForTheme(themeKey, idx);
      p.accent = p.accent || XYLAB_THEMES[themeKey]?.colors?.accent || "";
      p.textAlign = p.textAlign || (p.layout === "quote-page" || p.layout === "magazine-cover" ? "center" : "left");
      p.logoPosition = p.logoPosition || globalOverrides.logoPosition;
    });
    return project;
  } catch (err) {
    console.warn("XHS Generator: Carousel API failed, using mock.");
    return mockGenerateCarousel(brief, themeKey, pageCount);
  }
}

// API: Regenerate single page
async function requestRegeneratePageAPI(pageIndex, themeKey, brief, pages) {
  try {
    const themeName = XYLAB_THEMES[themeKey]?.name || "XYLab Default";
    const response = await fetch("/api/xhs/regenerate-page", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pageIndex, theme: themeName, brief, pages })
    });
    if (!response.ok) throw new Error();
    return await response.json();
  } catch (err) {
    console.warn("XHS Generator: Page Regen API failed, fallback locally.");
    const page = { ...pages[pageIndex] };
    page.headline = page.headline + " (AI Optimized) ✨";
    page.body = page.body + "\n• 精准重构核心论点\n• 提升文字修辞";
    return page;
  }
}

// Helper to resolve preset images
function getCuratedImageForTheme(themeKey, index) {
  const theme = XYLAB_THEMES[themeKey] || XYLAB_THEMES.default;
  if (studioState.uploadedAssets.length > 0) {
    return studioState.uploadedAssets[index % studioState.uploadedAssets.length];
  }
  if (theme.presets && theme.presets.length > 0) {
    return theme.presets[index % theme.presets.length];
  }
  const defaults = [
    "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1608248597481-496100c80836?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80"
  ];
  return defaults[index % defaults.length];
}

// CSS & style DNA injection function
function renderPreviewSlide(containerId, page, themeKey) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const baseTheme = XYLAB_THEMES[themeKey] || XYLAB_THEMES.default;
  const theme = JSON.parse(JSON.stringify(baseTheme));
  
  // Style Lock Logic: merge XYLab Default properties
  if (studioState.styleLockEnabled) {
    const lockRules = XYLAB_THEMES.default;
    theme.fonts = lockRules.fonts;
    theme.colors.background = lockRules.colors.background;
    theme.colors.textPrimary = lockRules.colors.textPrimary;
    theme.colors.textSecondary = lockRules.colors.textSecondary;
  }

  // Apply Global Overrides
  if (globalOverrides.fontPair === "serif-sans") {
    theme.fonts.display = "'Cormorant Garamond', 'Playfair Display', serif";
    theme.fonts.sans = "'Inter', 'Helvetica Neue', sans-serif";
  } else if (globalOverrides.fontPair === "sans-sans") {
    theme.fonts.display = "'Inter', sans-serif";
    theme.fonts.sans = "'Inter', sans-serif";
  }

  if (globalOverrides.accentColor) {
    theme.colors.accent = globalOverrides.accentColor;
  }

  // Render using layout module
  const pageToRender = { ...page };
  if (pageToRender.imageUrl) {
    pageToRender.imageUrl = ensureProxyUrl(pageToRender.imageUrl);
  }
  if (globalOverrides.logoPosition) {
    pageToRender.logoPosition = globalOverrides.logoPosition;
  }

  const layoutKey = pageToRender.layout || "magazine-cover";
  const layout = XYLAB_LAYOUTS[layoutKey] || XYLAB_LAYOUTS["magazine-cover"];
  
  // Call layout template renderer
  container.innerHTML = layout.render(pageToRender, theme, studioState.styleLockEnabled);
}
