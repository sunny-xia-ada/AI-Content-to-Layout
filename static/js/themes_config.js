// XYLab XHS Visual Studio - Themes Configuration DNA
const XYLAB_THEMES = {
  default: {
    name: "XYLab Default",
    mood: ["editorial", "minimalist", "low saturation", "clean"],
    colors: {
      background: "#F7F4EF",
      card: "#FFFFFF",
      textPrimary: "#171717",
      textSecondary: "#5F5A54",
      accent: "#C8C8C8",
      border: "rgba(23, 23, 23, 0.08)"
    },
    fonts: {
      display: "'Cormorant Garamond', 'Playfair Display', Georgia, serif",
      sans: "'Inter', 'Helvetica Neue', 'PingFang SC', sans-serif"
    },
    layouts: ["magazine-cover", "split-editorial", "info-card", "moodboard-archive", "routine-flow", "before-after", "quote-page", "product-catalog"],
    copyTone: ["precise", "quiet luxury", "calm intelligence"],
    avoid: ["Canva-like stickers", "cheap gradients", "crowded layout", "childish fonts", "gaming-CG look", "overly cute treatment", "heavy decorative effects", "generic AI SaaS look"]
  },
  muse: {
    name: "XYLab Muse",
    mood: ["pearl", "fantasy", "soft glow", "editorial", "dreamy"],
    colors: {
      background: "#F8F6F2",
      card: "#FFFFFF",
      textPrimary: "#1A1917",
      textSecondary: "#6E6B64",
      accent: "#D7B7C8", // Accent pink
      border: "rgba(215, 183, 200, 0.2)"
    },
    fonts: {
      display: "'Cormorant Garamond', serif",
      sans: "'Inter', sans-serif"
    },
    layouts: ["magazine-cover", "split-editorial", "moodboard-archive", "quote-page"],
    copyTone: ["healing", "becoming", "poetic", "confident"],
    avoid: ["cheap gradients", "neon grids", "high saturation", "gaming-CG look"],
    presets: [
      "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80"
    ]
  },
  beauty: {
    name: "XYLab Beauty",
    mood: ["clean", "glowy", "korean editorial", "refined"],
    colors: {
      background: "#FAF7F2",
      card: "#FFFFFF",
      textPrimary: "#1A1A1A",
      textSecondary: "#5A5450",
      accent: "#EBD3DB", // Soft glowy pink/rose
      border: "rgba(235, 211, 219, 0.3)"
    },
    fonts: {
      display: "'Cormorant Garamond', 'Playfair Display', serif",
      sans: "'Inter', sans-serif"
    },
    layouts: ["magazine-cover", "split-editorial", "info-card", "routine-flow", "before-after", "product-catalog"],
    copyTone: ["precise", "soft", "slightly confident"],
    avoid: ["too cute", "too Canva", "too crowded", "cheap gradients"],
    presets: [
      "https://images.unsplash.com/photo-1608248597481-496100c80836?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80"
    ]
  },
  stage: {
    name: "XYLab Stage",
    mood: ["motion", "flash", "city lights", "stylish"],
    colors: {
      background: "#121212",
      card: "#1E1E1E",
      textPrimary: "#FFFFFF",
      textSecondary: "#A0A0A0",
      accent: "#B8C7D9", // Accent blue/silver
      border: "rgba(255, 255, 255, 0.08)"
    },
    fonts: {
      display: "'Playfair Display', Georgia, serif",
      sans: "'Inter', sans-serif"
    },
    layouts: ["magazine-cover", "split-editorial", "moodboard-archive", "before-after"],
    copyTone: ["confident", "sharp", "stylish"],
    avoid: ["childish fonts", "pastel colors", "quiet luxury", "earthy textures"],
    presets: [
      "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"
    ]
  },
  gems: {
    name: "XYLab Gems",
    mood: ["museum catalog", "gemstone archive", "precious"],
    colors: {
      background: "#F5F3EE",
      card: "#FFFFFF",
      textPrimary: "#1F1D1A",
      textSecondary: "#6E695F",
      accent: "#C9B68A", // Accent gold
      border: "rgba(201, 182, 138, 0.25)"
    },
    fonts: {
      display: "'Cormorant Garamond', serif",
      sans: "'Inter', sans-serif"
    },
    layouts: ["magazine-cover", "info-card", "moodboard-archive", "product-catalog"],
    copyTone: ["elegant", "precious", "informative"],
    avoid: ["cheap gradients", "gaming-CG look", "childish fonts", "too cute"],
    presets: [
      "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80"
    ]
  },
  salon: {
    name: "XYLab Salon",
    mood: ["quiet luxury", "serif typography", "calm intelligence"],
    colors: {
      background: "#FAF9F5",
      card: "#FFFFFF",
      textPrimary: "#1E1E1E",
      textSecondary: "#605C56",
      accent: "#8C8275", // Earthy neutral
      border: "rgba(140, 130, 117, 0.15)"
    },
    fonts: {
      display: "'Cormorant Garamond', serif",
      sans: "'Inter', sans-serif"
    },
    layouts: ["magazine-cover", "split-editorial", "info-card", "quote-page"],
    copyTone: ["calm", "intelligent", "reflective"],
    avoid: ["stickers", "too cute", "cheap gradients", "overly bright colors"],
    presets: [
      "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=800&q=80"
    ]
  },
  wonyoungism: {
    name: "Wonyoungism",
    mood: ["glamorous", "sparkly", "rose gold", "princess"],
    colors: {
      background: "#FFF5FA",
      card: "#FFFFFF",
      textPrimary: "#2A1820",
      textSecondary: "#7A5E6B",
      accent: "#FFBBEF",
      border: "rgba(255, 187, 239, 0.3)"
    },
    fonts: { display: "'Cormorant Garamond', serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "moodboard-archive", "routine-flow"],
    copyTone: ["charming", "glamorous", "encouraging"],
    avoid: ["dark charcoal", "neon", "brutalist"],
    presets: ["https://images.unsplash.com/photo-1596436889106-be35e843f974?auto=format&fit=crop&w=800&q=80"]
  },
  solidcore: {
    name: "Solidcore Burn",
    mood: ["kinetic", "athletic", "electric", "dark charcoal"],
    colors: {
      background: "#111111",
      card: "#1C1C1C",
      textPrimary: "#FFFFFF",
      textSecondary: "#8A8A8A",
      accent: "#CCFF00", // Electric Lime
      border: "rgba(204, 255, 0, 0.15)"
    },
    fonts: { display: "'Inter', sans-serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "routine-flow", "before-after"],
    copyTone: ["high-energy", "factual", "sharp"],
    avoid: ["serif displays", "soft pinks", "vintage tapes", "museum catalog"],
    presets: ["https://images.unsplash.com/photo-1541701494587-cb58502866ab?auto=format&fit=crop&w=800&q=80"]
  },
  urban: {
    name: "Urban Pulse",
    mood: ["high contrast", "street style", "brutalist shadow"],
    colors: {
      background: "#EAE7E1",
      card: "#FFFFFF",
      textPrimary: "#0D0D0D",
      textSecondary: "#524F4A",
      accent: "#8A2BE2",
      border: "rgba(138, 43, 226, 0.2)"
    },
    fonts: { display: "'Playfair Display', serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "moodboard-archive"],
    copyTone: ["edgy", "expressive", "bold"],
    avoid: ["too cute", "soft gradients", "pastel pink", "delicate serif"],
    presets: ["https://images.unsplash.com/photo-1515621061946-eff1c2a352bd?auto=format&fit=crop&w=800&q=80"]
  },
  bottari: {
    name: "Bottari Scent",
    mood: ["organic paper", "earthy minimalist", "gallery"],
    colors: {
      background: "#EBE6DE",
      card: "#FFFFFF",
      textPrimary: "#332F2A",
      textSecondary: "#736C63",
      accent: "#D1C9C0",
      border: "rgba(209, 201, 192, 0.4)"
    },
    fonts: { display: "'Cormorant Garamond', serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "info-card", "product-catalog"],
    copyTone: ["sensory", "earthy", "understated"],
    avoid: ["neons", "liquid metal", "technology", "bold shadows"],
    presets: ["https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=800&q=80"]
  },
  nomad: {
    name: "Solo Nomad",
    mood: ["travel", "golden hour", "warm sand", "freedom"],
    colors: {
      background: "#EFEBE4",
      card: "#FFFFFF",
      textPrimary: "#2E2822",
      textSecondary: "#6E6256",
      accent: "#F4A460",
      border: "rgba(244, 164, 96, 0.2)"
    },
    fonts: { display: "'Cormorant Garamond', serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "moodboard-archive"],
    copyTone: ["adventurous", "nostalgic", "free"],
    avoid: ["neon grids", "chrome", "cute emojis"],
    presets: ["https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80"]
  },
  algorithm: {
    name: "Algorithm Art",
    mood: ["fluid mesh", "glassmorphism", "clean logic"],
    colors: {
      background: "#EBF1F5",
      card: "rgba(255, 255, 255, 0.7)",
      textPrimary: "#1E2A38",
      textSecondary: "#627387",
      accent: "#B8C7D9",
      border: "rgba(184, 199, 217, 0.4)"
    },
    fonts: { display: "'Inter', sans-serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "info-card", "split-editorial", "product-catalog"],
    copyTone: ["analytical", "structured", "cool"],
    avoid: ["vintage paper", "retro fonts", "organic textures"],
    presets: ["https://images.unsplash.com/photo-1633167606207-d840b5070fc2?auto=format&fit=crop&w=800&q=80"]
  },
  y2k: {
    name: "Y2K Archive",
    mood: ["brutalist tape", "liquid chrome", "retro digital"],
    colors: {
      background: "#EFEFEF",
      card: "#FFFFFF",
      textPrimary: "#000000",
      textSecondary: "#555555",
      accent: "#FFFF00",
      border: "rgba(0, 0, 0, 0.15)"
    },
    fonts: { display: "'Inter', sans-serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "moodboard-archive", "split-editorial"],
    copyTone: ["raw", "retro-futuristic", "playful"],
    avoid: ["quiet luxury", "elegant serif", "soft pastel pinks"],
    presets: ["https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?auto=format&fit=crop&w=800&q=80"]
  },
  posh: {
    name: "Posh Resale",
    mood: ["fashion tape", "minimal luxury", "curated closet"],
    colors: {
      background: "#F2EFEB",
      card: "#FFFFFF",
      textPrimary: "#1A1A1A",
      textSecondary: "#5A5753",
      accent: "#C8C8C8",
      border: "rgba(200, 200, 200, 0.3)"
    },
    fonts: { display: "'Playfair Display', serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "split-editorial", "product-catalog", "before-after"],
    copyTone: ["sophisticated", "exclusive", "concise"],
    avoid: ["Canva stickers", "neons", "cheap gradients"],
    presets: ["https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80"]
  },
  techno: {
    name: "Techno Cyber",
    mood: ["dark mode", "neon cyan", "circuit grid"],
    colors: {
      background: "#08080C",
      card: "#101016",
      textPrimary: "#FFFFFF",
      textSecondary: "#7A8293",
      accent: "#00F3FF",
      border: "rgba(0, 243, 255, 0.15)"
    },
    fonts: { display: "'Inter', sans-serif", sans: "'Inter', sans-serif" },
    layouts: ["magazine-cover", "info-card", "moodboard-archive"],
    copyTone: ["technological", "cold", "futuristic"],
    avoid: ["warm palettes", "paper texture", "soft curves"],
    presets: ["https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"]
  }
};
