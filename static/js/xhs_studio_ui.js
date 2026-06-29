// XYLab XHS Visual Studio - Interactive Workspace UI Controller

let selectedThemeKey = "beauty";
let base64DraftImage = null;

// Initialize lists and layout select dropdown
document.addEventListener('DOMContentLoaded', () => {
    renderThemesList();
    renderLayoutSelectDropdown();
    updateStyleLockUI();
});

// Trigger loading layouts into selector option list
function renderLayoutSelectDropdown() {
    const dropdown = document.getElementById('edit-layout');
    if (!dropdown) return;
    dropdown.innerHTML = Object.keys(XYLAB_LAYOUTS).map(key => `
        <option value="${key}">${XYLAB_LAYOUTS[key].name}</option>
    `).join('');
}

// Render themes list toggle cards
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

function selectTheme(key) {
    selectedThemeKey = key;
    renderThemesList();
    
    // Adjust local state if brief suggested different
    if (currentBrief) {
        currentBrief.suggestedTheme = XYLAB_THEMES[key].name;
        renderBriefEditor();
    }
    
    // If project is loaded, reload theme rendering
    if (currentProject) {
        currentProject.theme = XYLAB_THEMES[key].name;
        renderProjectWorkspace();
    }
}

// Draft Image upload handling
function handleDraftImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        base64DraftImage = e.target.result;
        document.getElementById('upload-hint').innerText = "Image Loaded";
    };
    reader.readAsDataURL(file);
}

// Trigger Brief Generation API call
async function triggerBriefGeneration() {
    const prompt = document.getElementById('project-idea-input').value.trim();
    if (!prompt) {
        alert("Please write your idea or paste draft content first.");
        return;
    }

    const overlay = document.getElementById('render-overlay');
    const status = document.getElementById('render-status');
    if (overlay) overlay.style.display = 'flex';
    if (status) status.innerText = "Analyzing idea with AI...";

    try {
        const brief = await generateCreativeBrief(prompt, base64DraftImage);
        renderBriefEditor();
    } catch (err) {
        console.error(err);
    } finally {
        if (overlay) overlay.style.display = 'none';
    }
}

// Render Creative Brief edit options
function renderBriefEditor() {
    const container = document.getElementById('brief-editor-container');
    if (!container || !currentBrief) return;

    // Map themes option
    const themeOptions = Object.keys(XYLAB_THEMES).filter(k => k !== 'default').map(k => `
        <option value="${k}" ${XYLAB_THEMES[k].name === currentBrief.suggestedTheme ? 'selected' : ''}>${XYLAB_THEMES[k].name}</option>
    `).join('');

    container.innerHTML = `
        <div class="space-y-3 text-[10px]">
            <div>
                <span class="block text-neutral-400 font-bold mb-1">Detected Topic:</span>
                <input type="text" id="brief-topic" value="${currentBrief.detectedTopic}" class="w-full p-2 bg-white border border-neutral-200 rounded outline-none font-medium">
            </div>
            
            <div class="grid grid-cols-2 gap-2">
                <div>
                    <span class="block text-neutral-400 font-bold mb-1">Theme Sug:</span>
                    <select id="brief-theme-select" onchange="selectTheme(this.value)" class="w-full p-1.5 bg-white border border-neutral-200 rounded font-bold uppercase text-[9px]">
                        ${themeOptions}
                    </select>
                </div>
                <div>
                    <span class="block text-neutral-400 font-bold mb-1">Page Count:</span>
                    <select id="brief-page-count" class="w-full p-1.5 bg-white border border-neutral-200 rounded font-bold text-[9px]">
                        <option value="6" ${currentBrief.recommendedFormat.includes('6') ? 'selected' : ''}>6 Pages (Standard)</option>
                        <option value="8" ${currentBrief.recommendedFormat.includes('8') ? 'selected' : ''}>8 Pages (Longer)</option>
                        <option value="9" ${currentBrief.recommendedFormat.includes('9') ? 'selected' : ''}>9 Pages (Archive)</option>
                    </select>
                </div>
            </div>

            <div>
                <span class="block text-neutral-400 font-bold mb-1">Copy Tone:</span>
                <input type="text" id="brief-tone" value="${currentBrief.copyTone}" class="w-full p-2 bg-white border border-neutral-200 rounded outline-none">
            </div>

            <div>
                <span class="block text-neutral-400 font-bold mb-1">Narrative Arc Guidelines:</span>
                <div class="space-y-1.5" id="narrative-arc-inputs">
                    ${currentBrief.narrativeArc.map((arc, i) => `
                        <input type="text" data-index="${i}" value="${arc}" class="w-full p-1.5 bg-white border border-neutral-100 rounded text-[9px] narrative-step-input">
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

// Trigger Carousel Generation from modified Brief values
async function triggerCarouselGeneration() {
    if (!currentBrief) {
        alert("Please generate a creative brief first.");
        return;
    }

    // Sync modified parameters from user input elements back to currentBrief
    currentBrief.detectedTopic = document.getElementById('brief-topic').value;
    currentBrief.copyTone = document.getElementById('brief-tone').value;
    
    // Sync narrative arc
    const arcInputs = document.querySelectorAll('.narrative-step-input');
    const newArc = [];
    arcInputs.forEach(input => newArc.push(input.value));
    currentBrief.narrativeArc = newArc;

    const pageCount = parseInt(document.getElementById('brief-page-count').value);

    const overlay = document.getElementById('render-overlay');
    const status = document.getElementById('render-status');
    if (overlay) overlay.style.display = 'flex';
    if (status) status.innerText = "Directing AI to compile full carousel pages...";

    try {
        const project = await generateCarousel(currentBrief, selectedThemeKey, pageCount);
        renderProjectWorkspace();
    } catch (err) {
        console.error(err);
    } finally {
        if (overlay) overlay.style.display = 'none';
    }
}

function renderProjectWorkspace() {
    if (!currentProject) return;

    // Header title
    document.getElementById('current-project-title-display').innerText = currentProject.projectTitle.toUpperCase();

    // Caption Text
    document.getElementById('edit-caption-textarea').value = currentProject.caption;

    // Thumbnail strip
    renderThumbnailsDeck();

    // Render active slide
    renderPreviewSlide('master-live-viewport', currentProject.pages[activePageIndex], selectedThemeKey);

    // Populate Page Editor fields
    loadPageEditorData(activePageIndex);
}

function renderThumbnailsDeck() {
    const container = document.getElementById('carousel-thumbnails-container');
    const countLabel = document.getElementById('deck-page-count-label');
    if (!container || !currentProject) return;

    countLabel.innerText = `${currentProject.pages.length} Slides`;

    container.innerHTML = currentProject.pages.map((p, idx) => {
        const isActive = idx === activePageIndex;
        const activeBorder = isActive ? 'border-neutral-900 bg-neutral-50 shadow-sm' : 'border-neutral-200/50 bg-white/40';
        
        return `
            <div onclick="switchActiveSlide(${idx})" class="flex-shrink-0 w-24 p-2.5 border rounded-xl cursor-pointer hover:border-neutral-400 transition-all ${activeBorder} flex flex-col space-y-1.5">
                <div class="flex items-center justify-between text-[8px] font-bold text-neutral-400">
                    <span>SLIDE ${idx+1}</span>
                    <span class="text-[7px] font-light truncate max-w-[40px] uppercase">${p.layout.split('-')[0]}</span>
                </div>
                <div class="w-full aspect-[4/3] rounded bg-neutral-100 overflow-hidden border border-neutral-200/30">
                    ${p.imageUrl ? `<img src="${p.imageUrl}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-[7px] text-gray-400">NO IMG</div>`}
                </div>
                <span class="text-[9px] font-bold truncate max-w-[80px]" style="color: ${XYLAB_THEMES[selectedThemeKey].colors.textPrimary}">${p.headline || "Untitled"}</span>
            </div>
        `;
    }).join('');
}

function switchActiveSlide(index) {
    activePageIndex = index;
    renderProjectWorkspace();
}

// Load active slide details to editor
function loadPageEditorData(index) {
    const page = currentProject.pages[index];
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
}

// Apply edits instantly to rendering state
function handlePageEdit() {
    if (!currentProject || !currentProject.pages[activePageIndex]) return;
    const page = currentProject.pages[activePageIndex];

    page.headline = document.getElementById('edit-headline').value;
    page.subheadline = document.getElementById('edit-subheadline').value;
    page.body = document.getElementById('edit-body').value;
    page.smallNote = document.getElementById('edit-small-note').value;
    page.imageUrl = document.getElementById('edit-image-url').value;
    page.layout = document.getElementById('edit-layout').value;
    page.textAlign = document.getElementById('edit-text-align').value;
    page.accent = document.getElementById('edit-accent').value;
    page.logoPosition = document.getElementById('edit-logo-position').value;

    // Re-render
    renderPreviewSlide('master-live-viewport', page, selectedThemeKey);
    // Refresh slide name in thumbnail
    renderThumbnailsDeck();
}

function handleCaptionEdit() {
    if (currentProject) {
        currentProject.caption = document.getElementById('edit-caption-textarea').value;
    }
}

// Style lock mechanics
function toggleStyleLock() {
    styleLockEnabled = !styleLockEnabled;
    updateStyleLockUI();
    if (currentProject) {
        renderProjectWorkspace();
    }
}

function updateStyleLockUI() {
    const btn = document.getElementById('style-lock-toggle-btn');
    const knob = document.getElementById('style-lock-knob');
    if (styleLockEnabled) {
        btn.className = "w-12 h-6 rounded-full bg-neutral-900 flex items-center px-1 transition-all";
        knob.className = "w-4 h-4 bg-white rounded-full transition-transform translate-x-6";
    } else {
        btn.className = "w-12 h-6 rounded-full bg-neutral-200 flex items-center px-1 transition-all";
        knob.className = "w-4 h-4 bg-white rounded-full transition-transform translate-x-0";
    }
}

// Global Overrides
function applyGlobalFontPair(val) {
    globalFontPair = val;
    if (currentProject) {
        renderProjectWorkspace();
    }
}

function applyGlobalLogoPos(val) {
    globalLogoPosition = val;
    if (currentProject) {
        currentProject.pages.forEach(p => p.logoPosition = val);
        renderProjectWorkspace();
    }
}

function applyGlobalAccentColor(val) {
    globalAccentColor = val;
    if (currentProject) {
        currentProject.pages.forEach(p => p.accent = val);
        renderProjectWorkspace();
    }
}

function clearGlobalAccent() {
    globalAccentColor = "";
    document.getElementById('global-accent-color-picker').value = "#C8C8C8";
    if (currentProject) {
        currentProject.pages.forEach(p => p.accent = "");
        renderProjectWorkspace();
    }
}

// Single page image upload
function handlePageImageUpload(event) {
    const file = event.target.files[0];
    if (!file || !currentProject) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = e.target.result;
        document.getElementById('edit-image-url').value = data;
        handlePageEdit();
    };
    reader.readAsDataURL(file);
}

// Single page shuffle image
function triggerPageShuffle() {
    if (!currentProject) return;
    const page = currentProject.pages[activePageIndex];
    const theme = XYLAB_THEMES[selectedThemeKey];
    const tags = theme.mood.slice(0, 3).join(',');
    const seed = Math.floor(Math.random() * 999999);
    const rawUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(tags + ' clear editorial close-up realistic aesthetic')}?width=1000&height=1400&nologo=true&seed=${seed}`;
    
    const proxyUrl = `/api/proxy-image?url=${encodeURIComponent(rawUrl)}`;
    
    document.getElementById('edit-image-url').value = proxyUrl;
    handlePageEdit();
}

// Regenerate this page
async function triggerPageRegen() {
    if (!currentProject || !currentBrief) return;
    
    const overlay = document.getElementById('render-overlay');
    const status = document.getElementById('render-status');
    if (overlay) overlay.style.display = 'flex';
    if (status) status.innerText = `Regenerating page ${activePageIndex + 1}...`;

    try {
        await regenerateSinglePage(activePageIndex, selectedThemeKey, currentBrief);
        renderProjectWorkspace();
    } catch (err) {
        console.error(err);
    } finally {
        if (overlay) overlay.style.display = 'none';
    }
}

// Export current slide as PNG
async function exportCurrentSlidePng() {
    if (!currentProject) {
        alert("Please generate a project first.");
        return;
    }

    const target = document.getElementById('render-target-container');
    const overlay = document.getElementById('render-overlay');
    const status = document.getElementById('render-status');
    if (overlay) overlay.style.display = 'flex';
    if (status) status.innerText = "Generating PNG file...";

    try {
        await new Promise(r => setTimeout(r, 300));
        
        const canvas = await html2canvas(target, {
            scale: 3,
            useCORS: true,
            allowTaint: true
        });

        const link = document.createElement('a');
        link.href = canvas.toDataURL("image/png");
        link.download = `slide_${activePageIndex + 1}.png`;
        link.click();
    } catch (err) {
        console.error("Export Error:", err);
        alert("Export failed: " + err.message);
    } finally {
        if (overlay) overlay.style.display = 'none';
    }
}

// Export full pack ZIP
async function exportFullPackZip() {
    if (!currentProject) {
        alert("Please generate a carousel first.");
        return;
    }
    const zip = new JSZip();
    const folder = zip.folder("xhs_carousel");
    
    // Show rendering overlay
    const overlay = document.getElementById('render-overlay');
    const status = document.getElementById('render-status');
    if (overlay) overlay.style.display = 'flex';
    
    // Cache original index
    const originalIndex = activePageIndex;
    
    try {
        for (let i = 0; i < currentProject.pages.length; i++) {
            if (status) status.innerText = `Rendering Slide ${i+1}/${currentProject.pages.length}...`;
            
            // Select the slide to render it in the canvas DOM
            activePageIndex = i;
            loadPageEditorData(i);
            renderPreviewSlide('master-live-viewport', currentProject.pages[i], selectedThemeKey);
            
            // Wait for image loading & layouts redraw
            await new Promise(r => setTimeout(r, 600)); 
            
            const target = document.getElementById('render-target-container');
            const canvas = await html2canvas(target, {
                scale: 2.5,
                useCORS: true,
                allowTaint: true
            });
            
            const imgData = canvas.toDataURL("image/png");
            const base64Data = imgData.split(";base64,")[1];
            folder.file(`slide_${String(i+1).padStart(2, '0')}.png`, base64Data, {base64: true});
        }
        
        if (status) status.innerText = "Compressing ZIP file...";
        const content = await zip.generateAsync({type:"blob"});
        
        // Download zip
        const link = document.createElement('a');
        link.href = URL.createObjectURL(content);
        link.download = `${currentProject.projectTitle.replace(/\s+/g, '_')}_pack.zip`;
        link.click();
    } catch (err) {
        console.error("ZIP Generation error:", err);
        alert("Export failed: " + err.message);
    } finally {
        // Restore
        activePageIndex = originalIndex;
        loadPageEditorData(originalIndex);
        renderPreviewSlide('master-live-viewport', currentProject.pages[originalIndex], selectedThemeKey);
        if (overlay) overlay.style.display = 'none';
        renderThumbnailsDeck();
    }
}

// Copy Post caption clipboard
function copyPostCaption() {
    if (!currentProject) return;
    const caption = document.getElementById('edit-caption-textarea').value;
    navigator.clipboard.writeText(caption)
        .then(() => alert("✨ Caption copied to clipboard!"))
        .catch(err => console.error("Clipboard write error:", err));
}

// Save preset mockup
function saveProjectPreset() {
    alert("✨ XYLab Visual Studio: Current project configuration saved successfully as custom preset!");
}

// Dummy modal trigger
function openThemeLibraryModal() {
    alert("✨ XYLab Theme Library: All themes follow standard, curated visual styling codes, prioritizing low saturation, thin serif display labels, and clean white spacing grids.");
}
