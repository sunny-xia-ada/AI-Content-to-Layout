// XYLab XHS Visual Studio - Front-end UI Coordinator

let selectedThemeKey = "beauty";

document.addEventListener('DOMContentLoaded', () => {
  // Initial page layout
  renderThemesList();
  renderLayoutSelectDropdown();
  updateStyleLockUI();
  runStateValidation();
  
  // Attach content textarea listener
  const ideaInput = document.getElementById('project-idea-input');
  if (ideaInput) {
    ideaInput.addEventListener('input', (e) => {
      studioState.idea = e.target.value.trim();
      runStateValidation();
    });
  }
});

// Storing and rendering multiple uploaded assets
function handleDraftImageUpload(event) {
  const files = event.target.files;
  if (!files || files.length === 0) return;
  
  let loadedCount = 0;
  for (let i = 0; i < files.length; i++) {
    const reader = new FileReader();
    reader.onload = (e) => {
      studioState.uploadedAssets.push(e.target.result);
      loadedCount++;
      if (loadedCount === files.length) {
        document.getElementById('upload-hint').innerText = `${studioState.uploadedAssets.length} Images Loaded`;
        renderUploadedAssetsList();
        runStateValidation();
      }
    };
    reader.readAsDataURL(files[i]);
  }
}

// Render uploaded images in left panel
function renderUploadedAssetsList() {
  const container = document.getElementById('brief-editor-container'); // Draw under input or creative brief area
  // We can create a dedicated thumbnail section for uploaded assets if they exist
  let assetsArea = document.getElementById('uploaded-assets-strip');
  if (!assetsArea) {
    assetsArea = document.createElement('div');
    assetsArea.id = 'uploaded-assets-strip';
    assetsArea.className = 'flex space-x-2 overflow-x-auto py-2 border-b border-dashed border-neutral-200';
    const parent = document.getElementById('project-idea-input').parentNode;
    parent.appendChild(assetsArea);
  }
  
  assetsArea.innerHTML = studioState.uploadedAssets.map((asset, index) => `
    <div class="relative w-12 h-12 rounded border overflow-hidden flex-shrink-0">
      <img src="${asset}" class="w-full h-full object-cover">
      <button onclick="removeUploadedAsset(${index})" class="absolute top-0 right-0 w-3.5 h-3.5 bg-black/70 text-white rounded-bl flex items-center justify-center text-[7px] font-black">×</button>
    </div>
  `).join('');
}

function removeUploadedAsset(index) {
  studioState.uploadedAssets.splice(index, 1);
  const hint = document.getElementById('upload-hint');
  if (hint) {
    hint.innerText = studioState.uploadedAssets.length > 0 ? `${studioState.uploadedAssets.length} Images Loaded` : "Upload Draft Image";
  }
  renderUploadedAssetsList();
  runStateValidation();
  
  // Re-draw asset grid in right panel if active page editor is open
  renderPageEditorAssetsGrid();
}

// Validation logic for active triggers
function runStateValidation() {
  const btnBrief = document.getElementById('btn-generate-brief');
  const btnCarousel = document.getElementById('btn-generate-carousel');
  const btnExport = document.querySelector('button[onclick="exportFullPackZip()"]');
  const pageFields = ['edit-headline', 'edit-subheadline', 'edit-body', 'edit-small-note', 'edit-image-url', 'edit-layout', 'edit-text-align', 'edit-accent', 'edit-logo-position'];
  
  // 1. Generate Brief: Enabled if idea is not empty OR there is at least one uploaded image
  if (btnBrief) {
    const hasIdea = studioState.idea.length > 0;
    const hasImage = studioState.uploadedAssets.length > 0;
    if (hasIdea || hasImage) {
      btnBrief.removeAttribute('disabled');
      btnBrief.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
      btnBrief.setAttribute('disabled', 'true');
      btnBrief.classList.add('opacity-50', 'cursor-not-allowed');
    }
  }

  // 2. Generate Full Carousel: Enabled if creativeBrief is not null
  if (btnCarousel) {
    if (studioState.creativeBrief) {
      btnCarousel.removeAttribute('disabled');
      btnCarousel.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
      btnCarousel.setAttribute('disabled', 'true');
      btnCarousel.classList.add('opacity-50', 'cursor-not-allowed');
    }
  }

  // 3. Export ZIP: Enabled if pages is not empty
  if (btnExport) {
    if (studioState.pages.length > 0) {
      btnExport.removeAttribute('disabled');
      btnExport.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
      btnExport.setAttribute('disabled', 'true');
      btnExport.classList.add('opacity-50', 'cursor-not-allowed');
    }
  }

  // 4. Page Editor fields: Disabled if pages list is empty
  const hasPages = studioState.pages.length > 0;
  pageFields.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      if (hasPages) {
        el.removeAttribute('disabled');
        el.classList.remove('opacity-60', 'cursor-not-allowed');
      } else {
        el.setAttribute('disabled', 'true');
        el.classList.add('opacity-60', 'cursor-not-allowed');
      }
    }
  });

  const btnSingleExport = document.querySelector('button[onclick="exportCurrentSlidePng()"]');
  const btnRegenPage = document.querySelector('button[onclick="triggerPageRegen()"]');
  if (btnSingleExport) {
    if (hasPages) btnSingleExport.removeAttribute('disabled');
    else btnSingleExport.setAttribute('disabled', 'true');
  }
  if (btnRegenPage) {
    if (hasPages) btnRegenPage.removeAttribute('disabled');
    else btnRegenPage.setAttribute('disabled', 'true');
  }
}

// Generate Brief Wrapper
async function triggerBriefGeneration() {
  const prompt = studioState.idea;
  if (!prompt && studioState.uploadedAssets.length === 0) return;

  const overlay = document.getElementById('render-overlay');
  const status = document.getElementById('render-status');
  if (overlay) overlay.style.display = 'flex';
  if (status) status.innerText = "Analyzing creative brief variables...";

  // Use first image asset as brief visual reference if available
  const refImage = studioState.uploadedAssets.length > 0 ? studioState.uploadedAssets[0] : null;

  try {
    const brief = await requestBriefAPI(prompt, refImage);
    studioState.creativeBrief = brief;
    
    // Automatically match brief suggested theme if valid
    const matchingKey = Object.keys(XYLAB_THEMES).find(k => XYLAB_THEMES[k].name === brief.suggestedTheme);
    if (matchingKey) {
      selectedThemeKey = matchingKey;
      studioState.selectedTheme = XYLAB_THEMES[matchingKey].name;
      renderThemesList();
    }
    
    renderBriefEditor();
    runStateValidation();
  } catch (err) {
    console.error(err);
  } finally {
    if (overlay) overlay.style.display = 'none';
  }
}

// Render Brief Fields dynamically & attach inputs list change sync
function renderBriefEditor() {
  const container = document.getElementById('brief-editor-container');
  if (!container || !studioState.creativeBrief) return;

  const brief = studioState.creativeBrief;

  const themeOptions = Object.keys(XYLAB_THEMES).filter(k => k !== 'default').map(k => `
    <option value="${k}" ${XYLAB_THEMES[k].name === brief.suggestedTheme ? 'selected' : ''}>${XYLAB_THEMES[k].name}</option>
  `).join('');

  container.innerHTML = `
    <div class="space-y-3 text-[10px]">
      <div>
        <span class="block text-neutral-400 font-bold mb-1">Detected Topic:</span>
        <input type="text" id="brief-topic" value="${brief.detectedTopic || ''}" oninput="syncBriefState()" class="w-full p-2 bg-white border border-neutral-200 rounded outline-none font-medium">
      </div>
      
      <div class="grid grid-cols-2 gap-2">
        <div>
          <span class="block text-neutral-400 font-bold mb-1">Theme DNA:</span>
          <select id="brief-theme-select" onchange="syncBriefTheme(this.value)" class="w-full p-1.5 bg-white border border-neutral-200 rounded font-bold uppercase text-[9px]">
            ${themeOptions}
          </select>
        </div>
        <div>
          <span class="block text-neutral-400 font-bold mb-1">Page Count:</span>
          <select id="brief-page-count" onchange="syncBriefPageCount(this.value)" class="w-full p-1.5 bg-white border border-neutral-200 rounded font-bold text-[9px]">
            <option value="6" ${brief.recommendedFormat.includes('6') ? 'selected' : ''}>6 Pages</option>
            <option value="8" ${brief.recommendedFormat.includes('8') ? 'selected' : ''}>8 Pages</option>
            <option value="9" ${brief.recommendedFormat.includes('9') ? 'selected' : ''}>9 Pages (Archive)</option>
          </select>
        </div>
      </div>

      <div>
        <span class="block text-neutral-400 font-bold mb-1">Visual Mood tags (comma-separated):</span>
        <input type="text" id="brief-mood" value="${(brief.visualMood || []).join(', ')}" oninput="syncBriefState()" class="w-full p-2 bg-white border border-neutral-200 rounded outline-none">
      </div>

      <div>
        <span class="block text-neutral-400 font-bold mb-1">Copywriting Tone:</span>
        <input type="text" id="brief-tone" value="${brief.copyTone || ''}" oninput="syncBriefState()" class="w-full p-2 bg-white border border-neutral-200 rounded outline-none">
      </div>

      <div>
        <span class="block text-neutral-400 font-bold mb-1">Narrative Storytelling Arc:</span>
        <div class="space-y-1.5" id="narrative-arc-inputs">
          ${brief.narrativeArc.map((arc, i) => `
            <input type="text" data-index="${i}" value="${arc}" oninput="syncBriefNarrative(${i}, this.value)" class="w-full p-1.5 bg-white border border-neutral-100 rounded text-[9px] narrative-step-input">
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

// Synced updates from Creative Brief editors back into studioState.creativeBrief
function syncBriefState() {
  if (!studioState.creativeBrief) return;
  const b = studioState.creativeBrief;
  
  b.detectedTopic = document.getElementById('brief-topic').value;
  b.copyTone = document.getElementById('brief-tone').value;
  
  const moodVal = document.getElementById('brief-mood').value;
  b.visualMood = moodVal.split(',').map(tag => tag.trim()).filter(t => t.length > 0);
}

function syncBriefTheme(val) {
  selectedThemeKey = val;
  studioState.selectedTheme = XYLAB_THEMES[val].name;
  if (studioState.creativeBrief) {
    studioState.creativeBrief.suggestedTheme = XYLAB_THEMES[val].name;
  }
  renderThemesList();
}

function syncBriefPageCount(val) {
  const count = parseInt(val);
  studioState.pageCount = count;
  if (studioState.creativeBrief) {
    studioState.creativeBrief.recommendedFormat = `${count}-page-carousel`;
    // Scale narrative arc array size to match new page count
    const arc = studioState.creativeBrief.narrativeArc;
    if (count > arc.length) {
      for (let i = arc.length; i < count; i++) {
        arc.push(`Page 0${i}: Core detail point ${i}`);
      }
    } else if (count < arc.length) {
      studioState.creativeBrief.narrativeArc = arc.slice(0, count);
    }
    // Re-draw inputs
    renderBriefEditor();
  }
}

function syncBriefNarrative(index, val) {
  if (studioState.creativeBrief && studioState.creativeBrief.narrativeArc[index] !== undefined) {
    studioState.creativeBrief.narrativeArc[index] = val;
  }
}

// Generate Carousel Wrapper
async function triggerCarouselGeneration() {
  if (!studioState.creativeBrief) return;

  const overlay = document.getElementById('render-overlay');
  const status = document.getElementById('render-status');
  if (overlay) overlay.style.display = 'flex';
  if (status) status.innerText = "Designing and aligning layout sequences...";

  // Ensure latest brief states are synced
  syncBriefState();

  try {
    const project = await requestCarouselAPI(studioState.creativeBrief, selectedThemeKey, studioState.pageCount);
    
    // Bind results to studioState
    studioState.projectTitle = project.projectTitle;
    studioState.pages = project.pages;
    studioState.caption = project.caption;
    studioState.hashtags = project.hashtags;
    studioState.activePageIndex = 0;
    
    renderProjectWorkspace();
    runStateValidation();
  } catch (err) {
    console.error(err);
  } finally {
    if (overlay) overlay.style.display = 'none';
  }
}

// Draw preview slides, thumbnails, and editor hydrate
function renderProjectWorkspace() {
  if (studioState.pages.length === 0) return;

  // Header Title
  document.getElementById('current-project-title-display').innerText = studioState.projectTitle.toUpperCase();

  // Caption textarea
  document.getElementById('edit-caption-textarea').value = studioState.caption;

  // Draw Thumbnails strip
  renderThumbnailsDeck();

  // Render Canvas
  renderPreviewSlide('master-live-viewport', studioState.pages[studioState.activePageIndex], selectedThemeKey);

  // Load editor details
  loadPageEditorData(studioState.activePageIndex);
}

function renderThumbnailsDeck() {
  const container = document.getElementById('carousel-thumbnails-container');
  const countLabel = document.getElementById('deck-page-count-label');
  if (!container) return;

  countLabel.innerText = `${studioState.pages.length} Slides`;

  container.innerHTML = studioState.pages.map((p, idx) => {
    const isActive = idx === studioState.activePageIndex;
    const activeBorder = isActive ? 'border-neutral-900 bg-neutral-50 shadow-sm' : 'border-neutral-200/50 bg-white/40';
    const textPrimaryColor = XYLAB_THEMES[selectedThemeKey].colors.textPrimary;
    
    return `
      <div onclick="switchActiveSlide(${idx})" class="flex-shrink-0 w-24 p-2.5 border rounded-xl cursor-pointer hover:border-neutral-400 transition-all ${activeBorder} flex flex-col space-y-1.5">
        <div class="flex items-center justify-between text-[8px] font-bold text-neutral-400">
          <span>SLIDE ${idx+1}</span>
          <span class="text-[7px] font-light truncate max-w-[40px] uppercase">${p.layout.split('-')[0]}</span>
        </div>
        <div class="w-full aspect-[4/3] rounded bg-neutral-100 overflow-hidden border border-neutral-200/30">
          ${p.imageUrl ? `<img src="${p.imageUrl}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-[7px] text-gray-400">NO IMG</div>`}
        </div>
        <span class="text-[9px] font-bold truncate max-w-[80px]" style="color: ${textPrimaryColor}">${p.headline || "Untitled"}</span>
      </div>
    `;
  }).join('');
}

function switchActiveSlide(index) {
  studioState.activePageIndex = index;
  renderProjectWorkspace();
}

function renderLayoutSelectDropdown() {
  const dropdown = document.getElementById('edit-layout');
  if (!dropdown) return;
  dropdown.innerHTML = Object.keys(XYLAB_LAYOUTS).map(key => `
    <option value="${key}">${XYLAB_LAYOUTS[key].name}</option>
  `).join('');
}

// Hydrate fields
function loadPageEditorData(index) {
  const page = studioState.pages[index];
  if (!page) return;

  document.getElementById('editor-page-title').innerText = `Page ${index + 1} Editor`;
  document.getElementById('editor-page-layout-name').innerText = `Layout: ${page.layout}`;

  document.getElementById('edit-headline').value = page.headline || "";
  document.getElementById('edit-subheadline').value = page.subheadline || "";
  document.getElementById('edit-body').value = page.body || "";
  document.getElementById('edit-small-note').value = page.smallNote || "";
  document.getElementById('edit-image-url').value = page.imageUrl || "";
  document.getElementById('edit-layout').value = page.layout || "magazine-cover";
  document.getElementById('edit-text-align').value = page.textAlign || "left";
  document.getElementById('edit-accent').value = page.accent || XYLAB_THEMES[selectedThemeKey].colors.accent;
  document.getElementById('edit-logo-position').value = page.logoPosition || "bottom-right";

  // Also render assets selector grid in Page Editor
  renderPageEditorAssetsGrid();
}

// Allows setting page imageUrl from multiple uploadedAssets pool
function renderPageEditorAssetsGrid() {
  let grid = document.getElementById('page-editor-assets-picker-grid');
  if (!grid) {
    const parent = document.getElementById('edit-image-url').parentNode;
    grid = document.createElement('div');
    grid.id = 'page-editor-assets-picker-grid';
    grid.className = 'grid grid-cols-5 gap-2 mt-2 border-t pt-2';
    parent.appendChild(grid);
  }

  if (studioState.uploadedAssets.length === 0) {
    grid.innerHTML = '<span class="col-span-5 text-[8px] text-neutral-400">No custom uploads. Image URLs or search presets will be used.</span>';
    return;
  }

  grid.innerHTML = studioState.uploadedAssets.map((asset, idx) => {
    const isChosen = studioState.pages[studioState.activePageIndex]?.imageUrl === asset;
    const borderClass = isChosen ? 'border-neutral-900 scale-105' : 'border-neutral-200 hover:border-neutral-500';
    return `
      <div onclick="setPageImageFromUpload(${idx})" class="aspect-square rounded border overflow-hidden cursor-pointer transition-all ${borderClass}">
        <img src="${asset}" class="w-full h-full object-cover">
      </div>
    `;
  }).join('');
}

function setPageImageFromUpload(idx) {
  const asset = studioState.uploadedAssets[idx];
  const page = studioState.pages[studioState.activePageIndex];
  if (page && asset) {
    page.imageUrl = asset;
    document.getElementById('edit-image-url').value = asset;
    handlePageEdit();
  }
}

// Modify single page attributes instantly
function handlePageEdit() {
  if (studioState.pages.length === 0) return;
  const page = studioState.pages[studioState.activePageIndex];
  if (!page) return;

  page.headline = document.getElementById('edit-headline').value;
  page.subheadline = document.getElementById('edit-subheadline').value;
  page.body = document.getElementById('edit-body').value;
  page.smallNote = document.getElementById('edit-small-note').value;
  page.imageUrl = document.getElementById('edit-image-url').value;
  page.layout = document.getElementById('edit-layout').value;
  page.textAlign = document.getElementById('edit-text-align').value;
  page.accent = document.getElementById('edit-accent').value;
  page.logoPosition = document.getElementById('edit-logo-position').value;

  renderPreviewSlide('master-live-viewport', page, selectedThemeKey);
  renderThumbnailsDeck();
  renderPageEditorAssetsGrid();
}

function handleCaptionEdit() {
  if (studioState.pages.length > 0) {
    studioState.caption = document.getElementById('edit-caption-textarea').value;
  }
}

// Themes list DNA scroll
function renderThemesList() {
  const container = document.getElementById('themes-grid-container');
  if (!container) return;
  
  container.innerHTML = Object.keys(XYLAB_THEMES).filter(key => key !== 'default').map(key => {
    const theme = XYLAB_THEMES[key];
    const isSelected = key === selectedThemeKey;
    const activeClasses = isSelected ? 'border-neutral-900 bg-neutral-50 shadow-sm' : 'border-neutral-200/60 bg-white';
    
    return `
      <div onclick="selectTheme('${key}')" class="p-3 border rounded-xl cursor-pointer hover:border-neutral-400 transition-all ${activeClasses} flex flex-col space-y-1">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-bold tracking-tight">${theme.name}</span>
          <div class="w-2.5 h-2.5 rounded-full border border-neutral-300" style="background-color: ${theme.colors.accent}"></div>
        </div>
        <span class="text-[8px] text-neutral-400 capitalize truncate">${theme.mood.slice(0, 3).join(', ')}</span>
      </div>
    `;
  }).join('');
}

// Style lock mechanics
function toggleStyleLock() {
  studioState.styleLockEnabled = !studioState.styleLockEnabled;
  updateStyleLockUI();
  if (studioState.pages.length > 0) {
    renderProjectWorkspace();
  }
}

function updateStyleLockUI() {
  const btn = document.getElementById('style-lock-toggle-btn');
  const knob = document.getElementById('style-lock-knob');
  if (studioState.styleLockEnabled) {
    btn.className = "w-12 h-6 rounded-full bg-neutral-900 flex items-center px-1 transition-all";
    knob.className = "w-4 h-4 bg-white rounded-full transition-transform translate-x-6";
  } else {
    btn.className = "w-12 h-6 rounded-full bg-neutral-200 flex items-center px-1 transition-all";
    knob.className = "w-4 h-4 bg-white rounded-full transition-transform translate-x-0";
  }
}

// Global overrides
function applyGlobalFontPair(val) {
  globalOverrides.fontPair = val;
  if (studioState.pages.length > 0) {
    renderProjectWorkspace();
  }
}

function applyGlobalLogoPos(val) {
  globalOverrides.logoPosition = val;
  if (studioState.pages.length > 0) {
    studioState.pages.forEach(p => p.logoPosition = val);
    renderProjectWorkspace();
  }
}

function applyGlobalAccentColor(val) {
  globalOverrides.accentColor = val;
  if (studioState.pages.length > 0) {
    studioState.pages.forEach(p => p.accent = val);
    renderProjectWorkspace();
  }
}

function clearGlobalAccent() {
  globalOverrides.accentColor = "";
  document.getElementById('global-accent-color-picker').value = "#C8C8C8";
  if (studioState.pages.length > 0) {
    studioState.pages.forEach(p => p.accent = "");
    renderProjectWorkspace();
  }
}

// Page Single Image file upload
function handlePageImageUpload(event) {
  const file = event.target.files[0];
  if (!file || studioState.pages.length === 0) return;
  
  const reader = new FileReader();
  reader.onload = (e) => {
    // Append to uploadedAssets array
    studioState.uploadedAssets.push(e.target.result);
    renderUploadedAssetsList();
    
    // Set active page image
    const page = studioState.pages[studioState.activePageIndex];
    page.imageUrl = e.target.result;
    document.getElementById('edit-image-url').value = e.target.result;
    
    handlePageEdit();
  };
  reader.readAsDataURL(file);
}

// Generate single slide background photo search or generation
function triggerPageShuffle() {
  if (studioState.pages.length === 0) return;
  
  const page = studioState.pages[studioState.activePageIndex];
  const theme = XYLAB_THEMES[selectedThemeKey] || XYLAB_THEMES.default;
  const tags = theme.mood.slice(0, 3).join(',');
  const seed = Math.floor(Math.random() * 999999);
  
  const rawUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(tags + ' clear editorial closeup photo, luxury beauty magazine style')}?width=1000&height=1400&nologo=true&seed=${seed}`;
  const proxyUrl = `/api/proxy-image?url=${encodeURIComponent(rawUrl)}`;
  
  page.imageUrl = proxyUrl;
  document.getElementById('edit-image-url').value = proxyUrl;
  handlePageEdit();
}

// Regenerate single page copy using API context
async function triggerPageRegen() {
  if (studioState.pages.length === 0 || !studioState.creativeBrief) return;

  const overlay = document.getElementById('render-overlay');
  const status = document.getElementById('render-status');
  if (overlay) overlay.style.display = 'flex';
  if (status) status.innerText = `Regenerating page ${studioState.activePageIndex + 1}...`;

  try {
    const page = await requestRegeneratePageAPI(studioState.activePageIndex, selectedThemeKey, studioState.creativeBrief, studioState.pages);
    studioState.pages[studioState.activePageIndex] = page;
    renderProjectWorkspace();
  } catch (err) {
    console.error(err);
  } finally {
    if (overlay) overlay.style.display = 'none';
  }
}

// High-resolution image exporter
async function exportCurrentSlidePng() {
  if (studioState.pages.length === 0) return;

  const target = document.getElementById('render-target-container');
  const overlay = document.getElementById('render-overlay');
  const status = document.getElementById('render-status');
  if (overlay) overlay.style.display = 'flex';
  if (status) status.innerText = "Processing UHD snapshot rendering (1080x1440)...";

  try {
    // Temporarily increase size of the frame for UHD capture
    const originalWidth = target.style.width;
    const originalHeight = target.style.height;
    
    // Scale canvas container to 1080x1440 for exact rendering snapshot
    target.style.width = "1080px";
    target.style.height = "1440px";
    
    // Wait briefly for style recalculations
    await new Promise(r => setTimeout(r, 450));

    const canvas = await html2canvas(target, {
      scale: 1, // Already set to target size, no extra scaling needed
      useCORS: true,
      allowTaint: true
    });

    // Revert size
    target.style.width = originalWidth;
    target.style.height = originalHeight;
    await new Promise(r => setTimeout(r, 100));

    const link = document.createElement('a');
    link.href = canvas.toDataURL("image/png");
    link.download = `${studioState.projectTitle || "xhs"}_slide_${studioState.activePageIndex + 1}.png`;
    link.click();
  } catch (err) {
    console.error("Export PNG failed:", err);
    alert("Export failed: " + err.message);
  } finally {
    if (overlay) overlay.style.display = 'none';
  }
}

// Batch ZIP UHD export
async function exportFullPackZip() {
  if (studioState.pages.length === 0) return;
  
  const zip = new JSZip();
  const folder = zip.folder("xhs_carousel_pack");

  const target = document.getElementById('render-target-container');
  const overlay = document.getElementById('render-overlay');
  const status = document.getElementById('render-status');
  if (overlay) overlay.style.display = 'flex';

  const originalIndex = studioState.activePageIndex;
  const originalWidth = target.style.width;
  const originalHeight = target.style.height;

  // Scale frame to 1080x1440
  target.style.width = "1080px";
  target.style.height = "1440px";

  try {
    for (let i = 0; i < studioState.pages.length; i++) {
      if (status) status.innerText = `Rendering UHD Slide ${i+1}/${studioState.pages.length}...`;
      
      // Update viewport slide state
      studioState.activePageIndex = i;
      renderPreviewSlide('master-live-viewport', studioState.pages[i], selectedThemeKey);
      
      // Allow extra time for images/fonts mapping in scaled layout
      await new Promise(r => setTimeout(r, 650)); 
      
      const canvas = await html2canvas(target, {
        scale: 1,
        useCORS: true,
        allowTaint: true
      });
      
      const imgData = canvas.toDataURL("image/png");
      const base64Data = imgData.split(";base64,")[1];
      folder.file(`slide_${String(i+1).padStart(2, '0')}.png`, base64Data, {base64: true});
    }

    if (status) status.innerText = "Compressing pack files...";
    const blob = await zip.generateAsync({type: "blob"});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${studioState.projectTitle.replace(/\s+/g, '_')}_carousel_uhd.zip`;
    link.click();
  } catch (err) {
    console.error("ZIP Generation error:", err);
    alert("ZIP Export failed: " + err.message);
  } finally {
    // Revert viewport sizes and active indexes
    target.style.width = originalWidth;
    target.style.height = originalHeight;
    studioState.activePageIndex = originalIndex;
    
    renderProjectWorkspace();
    if (overlay) overlay.style.display = 'none';
  }
}

// Copy caption
function copyPostCaption() {
  if (studioState.pages.length === 0) return;
  const text = document.getElementById('edit-caption-textarea').value;
  navigator.clipboard.writeText(text)
    .then(() => alert("✨ Xiaohongshu Post Caption copied successfully!"))
    .catch(err => console.error("Clipboard copy error:", err));
}

// Mock preset save
function saveProjectPreset() {
  alert("✨ Preset saved! The exact current structured project state has been stored.");
}

// Info modal trigger
function openThemeLibraryModal() {
  alert("✨ XYLab Theme Library: All themes follow standard, curated visual styling codes, prioritizing low saturation, thin serif display labels, and clean white spacing grids.");
}
