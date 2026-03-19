# XYLAB Smart Agent v4.1

Welcome to **XYLAB Smart Agent**, an intelligent Markdown-to-HTML restructuring and layout tool designed for crafting pristine, highly-aesthetic article layouts (perfect for platforms like WeChat and Notion). 

Version 4.1 introduces the **Zero-Hero Policy**, 10 distinct Emotional Themes from the XYLAB Multiverse, and a robust stateless Shuffle Engine to guarantee massive visual variety.

## ✨ Features

- **Brain-Powered Auto-Layout**: The `smart_restructure` engine automatically parses raw text blocks. It provides "breathing room" by intelligently chunking long paragraphs, elevating short impactful phrases to HTML headers, and applying strategic bold emphasis (`**`) to the focal points of your sentences.
- **The XYLAB Multiverse (10 Themes)**: Render your text in 10 highly-stylized, CSS-injected aesthetic universes.
  - `Loopy Cute` (Pastel, bubbly, soft)
  - `Executive Gray` (Sharp grids, monochromatic)
  - `Ethereal Sky` (Airy, sky blue, dreamy)
  - `Techno Cyber` (Dark mode, neon cyan, circuit grids)
  - `Urban Pulse` (High contrast, skewed shadows, heavy pink/purple)
  - `Wonyoungism` (Glamorous, sparkly, rose gold)
  - `Algorithm Art` (Fluid mesh gradients, glassmorphism)
  - `Archive 2026` (Brutalist concrete, vintage fashion tape borders)
  - `Solidcore` (Kinetic motion blur, electric lime on dark charcoal)
  - `Bottari` (Organic paper textures, earthy minimalist gallery styles)
- **Zero-Hero Aesthetics**: Drops generic hero images entirely. The engine now goes straight into your typography, generating and isolating only *one* atmospheric mid-article Divider pulled dynamically from Flickr based on your active theme's keyword pool.
- **🎲 Stateless Shuffle**: Don't like the divider? Hit **Shuffle**. The app hits a dedicated API endpoint with timestamp cache-busting, retrieves a new image from the global Flickr pool, and safely replaces the markdown natively using localized Regex—without corrupting your current text edits.
- **One-Click Export**: Renders everything directly to an `id="aura-card"` container that you can copy to your clipboard in a single click, ready for pasting into any rich-text editor (like WeChat's Official Account portal).

## 🧭 Workflow

```mermaid
graph TD
    A[Raw Markdown Text] --> B{AI Auto-Layout Engine}
    
    subgraph Text Restructuring
        B --> C[Paragraph Pacing]
        B --> D[Smart Emphasis **]
        B --> E[Header Extraction ##]
    end

    C --> F((Zero-Hero Base))
    D --> F
    E --> F

    F --> G[Divider Image Generation]
    
    subgraph Service Pools
        G --> H[LoremFlickr Single-Tag Pool]
        H -.-> |Cache-Busted Timestamp| I[Shuffle Request API]
    end

    G --> J[HTML Compilation]
    J --> K{Theme Engine}

    subgraph The Multiverse
        K --> L[Ethereal Sky]
        K --> M[Archive 2026]
        K --> N[Solidcore...]
    end

    L --> O([Final WeChat Aura Card])
    M --> O
    N --> O

    I --> G
    O --> P[One-Click Clipboard Copy]
```

## 🚀 Run Locally

Ensure you have Python 3.9+ installed. 

**1. Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install Dependencies**
```bash
pip install fastapi uvicorn beautifulsoup4 markdown python-multipart
```

**3. Boot the Engine**
```bash
python main.py
```
*The agent will launch at `http://localhost:8000` (or `http://0.0.0.0:8000`). If you want to access it from your mobile device, find your computer's local IP address (e.g., `10.0.0.x`) and navigate to `http://10.0.0.x:8000` on your phone.*

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, Uvicorn 
- **Processing**: BeautifulSoup4, Python-Markdown, native RegEx
- **Frontend**: HTML5, Tailwind CSS, Vanilla Javascript

---
*Built by XYLAB // 2026*
