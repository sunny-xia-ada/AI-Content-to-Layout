// XYLab XHS Visual Studio - Carousel Generator & Integration Engine

let currentProject = null;
let currentBrief = null;
let activePageIndex = 0;
let styleLockEnabled = true;

// Global overrides
let globalFontPair = ""; // Inherited from theme unless overridden
let globalLogoPosition = "bottom-right";
let globalAccentColor = "";
let globalPageNumberStyle = "classic"; // classic, italic, minimal, none

// Function to generate the Creative Brief from prompt + image
async function generateCreativeBrief(prompt, base64Image = null) {
  try {
    console.log("XHS Generator: Generating Creative Brief...");
    const response = await fetch("/api/xhs/generate-brief", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, image: base64Image })
    });
    if (!response.ok) throw new Error("API Brief generation failed");
    
    currentBrief = await response.json();
    console.log("XHS Generator: Creative Brief Generated:", currentBrief);
    return currentBrief;
  } catch (error) {
    console.error("XHS Generator: Error generating brief, using local mock:", error);
    // Local mock fallback
    currentBrief = {
      detectedTopic: prompt || "未命名创意",
      recommendedFormat: "6-page-carousel",
      suggestedTheme: "XYLab Beauty",
      visualMood: ["clean", "glowy", "soft pink"],
      copyTone: "calm editorial, slightly confident",
      narrativeArc: [
        "Cover: Hook statement for " + (prompt || "aesthetic concept"),
        "Page 01: Core insight breakdown",
        "Page 02: Science or details exploration",
        "Page 03: Routine workflow methodology",
        "Page 04: Visual routine/comparison",
        "Page 05: Summary action review"
      ]
    };
    return currentBrief;
  }
}

// Function to generate the full multi-page carousel from brief & theme
async function generateCarousel(brief, themeKey, pageCount) {
  try {
    console.log(`XHS Generator: Generating Carousel for ${themeKey} with ${pageCount} pages...`);
    const themeName = XYLAB_THEMES[themeKey]?.name || "XYLab Default";
    const response = await fetch("/api/xhs/generate-carousel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ brief, theme: themeName, pageCount })
    });
    if (!response.ok) throw new Error("API Carousel generation failed");
    
    currentProject = await response.json();
    // Inject IDs and numbers if missing
    currentProject.pages.forEach((p, idx) => {
      p.id = p.id || `page_${idx}`;
      p.pageNumber = idx + 1;
      p.imageUrl = p.imageUrl || getCuratedImageForTheme(themeKey, idx);
    });
    activePageIndex = 0;
    console.log("XHS Generator: Carousel Generated:", currentProject);
    return currentProject;
  } catch (error) {
    console.error("XHS Generator: Error generating carousel, using local mock:", error);
    
    // Fallback generator
    const pages = [];
    const layoutSequence = ["magazine-cover", "split-editorial", "info-card", "routine-flow", "before-after", "quote-page", "product-catalog"];
    
    const themeName = XYLAB_THEMES[themeKey]?.name || "XYLab Default";
    const topic = brief.detectedTopic || "Aesthetic Design";
    
    for (let i = 0; i < pageCount; i++) {
      let layout = layoutSequence[i % layoutSequence.length];
      if (i === 0) layout = "magazine-cover";
      else if (i === pageCount - 1) layout = "quote-page";
      
      pages.push({
        id: `page_${i}`,
        pageNumber: i + 1,
        type: i === 0 ? "cover" : "detail",
        headline: i === 0 ? topic : `Core Highlight 0${i}`,
        subheadline: i === 0 ? "XYLAB EDITORIAL LAB" : `CONCEPT HIGHLIGHT 0${i}`,
        body: i === 0 ? "" : `• Detailed explanation point A\n• Detailed explanation point B\n• High-end copy pacing here.`,
        smallNote: i === 0 ? "VOL. 01 / XYLAB WORKPLACE" : `SPECIFICATION ${i}`,
        layout: layout,
        imageRole: i === 0 ? "hero" : "supporting",
        imageUrl: getCuratedImageForTheme(themeKey, i),
        accent: "",
        textAlign: layout === "quote-page" || layout === "magazine-cover" ? "center" : "left",
        density: "medium",
        logoPosition: "bottom-right"
      });
    }
    
    currentProject = {
      projectTitle: topic,
      theme: themeName,
      format: `${pageCount}-page-carousel`,
      visualMood: brief.visualMood || ["editorial"],
      pages: pages,
      caption: `💡 ${topic}\n\nHere is your high-end social media draft.\nDesigned with XYLab premium layout studio.\n\n#visualstorytelling #editorial #design #XYLab`,
      hashtags: [`#${topic}`, "#editorial", "#XYLab"]
    };
    activePageIndex = 0;
    return currentProject;
  }
}

// Function to regenerate a single page contextually
async function regenerateSinglePage(pageIndex, themeKey, brief) {
  if (!currentProject || !currentProject.pages[pageIndex]) return;
  try {
    console.log(`XHS Generator: Regenerating slide ${pageIndex}...`);
    const themeName = XYLAB_THEMES[themeKey]?.name || "XYLab Default";
    const response = await fetch("/api/xhs/regenerate-page", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pageIndex,
        theme: themeName,
        brief,
        pages: currentProject.pages
      })
    });
    if (!response.ok) throw new Error("API page regeneration failed");
    
    const newPage = await response.json();
    newPage.imageUrl = newPage.imageUrl || getCuratedImageForTheme(themeKey, pageIndex);
    currentProject.pages[pageIndex] = newPage;
    return newPage;
  } catch (error) {
    console.error("XHS Generator: Fallback page regeneration locally:", error);
    const page = currentProject.pages[pageIndex];
    page.headline = page.headline + " ✨";
    page.body = (page.body || "") + "\n• Enhanced detail description point.";
    return page;
  }
}

// Helper to resolve high-quality preset background images for themes
function getCuratedImageForTheme(themeKey, index) {
  const theme = XYLAB_THEMES[themeKey] || XYLAB_THEMES.default;
  if (theme.presets && theme.presets.length > 0) {
    return theme.presets[index % theme.presets.length];
  }
  // Standard fallbacks based on tags
  const defaultPresets = [
    "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1608248597481-496100c80836?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
  ];
  return defaultPresets[index % defaultPresets.length];
}

// Render the active preview slide
function renderPreviewSlide(containerId, page, themeKey) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const baseTheme = XYLAB_THEMES[themeKey] || XYLAB_THEMES.default;
  
  // Clone baseTheme to avoid modifications
  const theme = JSON.parse(JSON.stringify(baseTheme));
  
  // Apply style lock constraints
  if (styleLockEnabled) {
    const lockRules = XYLAB_THEMES.default;
    // Overwrite with default fonts and core aesthetic constraints
    theme.fonts = lockRules.fonts;
    theme.colors.background = theme.colors.background || lockRules.colors.background;
    theme.colors.textPrimary = lockRules.colors.textPrimary;
    theme.colors.textSecondary = lockRules.colors.textSecondary;
  }

  // Apply Global Overrides if set
  if (globalFontPair) {
    // Expect formats like "cormorant-inter" or similar
    if (globalFontPair === "serif-sans") {
      theme.fonts.display = "'Cormorant Garamond', 'Playfair Display', serif";
      theme.fonts.sans = "'Inter', 'Helvetica Neue', sans-serif";
    } else if (globalFontPair === "sans-sans") {
      theme.fonts.display = "'Inter', sans-serif";
      theme.fonts.sans = "'Inter', sans-serif";
    }
  }
  if (globalAccentColor) {
    theme.colors.accent = globalAccentColor;
  }

  const renderPage = { ...page };
  if (globalLogoPosition) {
    renderPage.logoPosition = globalLogoPosition;
  }
  
  // Resolve layout renderer
  const layoutKey = renderPage.layout || "magazine-cover";
  const layout = XYLAB_LAYOUTS[layoutKey] || XYLAB_LAYOUTS["magazine-cover"];
  
  // Custom wrappers around layout rendering to handle logo positions and page numbers consistently
  let layoutHtml = layout.render(renderPage, theme, styleLockEnabled);
  
  // Render html
  container.innerHTML = layoutHtml;
}
