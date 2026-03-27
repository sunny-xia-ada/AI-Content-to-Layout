import base64
import os
import re
import urllib.parse
import random
import uuid
import time
import markdown
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="XYLAB // SMART AGENT v4.4")

# Vercel Serverless Absolute Pathing Fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# If the code is running in a different context (like Vercel functions), 
# we ensure the templates and static folders are reached correctly.
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
if not os.path.exists(TEMPLATE_DIR):
    # Fallback to a relative path from the current working directory
    TEMPLATE_DIR = os.path.abspath("templates")

STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    # Fallback to a relative path from the current working directory
    STATIC_DIR = os.path.abspath("static")

# Only mount the static directory if it actually exists in the runtime environment
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"Warning: 'static' directory not found at {STATIC_DIR}. Skipping static mount.")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

LOOPY_PATH = "loopy_asset.png"
def get_base64_asset(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""
LOOPY_DATA_URI = f"data:image/png;base64,{get_base64_asset(LOOPY_PATH)}" if get_base64_asset(LOOPY_PATH) else ""

# The XYLAB Multiverse: 10 Distinct Emotional Themes
THEMES = {
    "loopy": {
        "card": "width: 100%; max-width: 500px; margin: 0 auto; background: #FFFFFF; padding: 60px 25px; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.03); font-family: 'Inter', sans-serif; border: 0;",
        "h2": "font-size: 28px; font-weight: bold; color: #1A1A1A; line-height: 1.3; margin: 40px 0 24px; text-align: left;",
        "h3": "font-size: 18px; font-weight: bold; color: #FEC5D2; margin-top: 40px; letter-spacing: 2px;",
        "p": "font-size: 16px; line-height: 2.0; color: #444; margin: 0 0 2em; text-align: justify;",
        "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px;",
        "img": "max-width: 100%; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); display: block; margin: 25px auto;",
        "accent": "#FEC5D2"
    },
    "executive": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #FFFFFF; background-image: linear-gradient(#F5F5F5 1px, transparent 1px), linear-gradient(90deg, #F5F5F5 1px, transparent 1px); background-size: 40px 40px; padding: 80px 40px 80px 100px; border-radius: 0; font-family: 'Helvetica', 'Inter', sans-serif; border: 1px solid #000; box-shadow: 0 30px 60px rgba(0,0,0,0.03);",
        "h2": "font-size: 26px; font-weight: bold; color: #1A1A1A; border-left: 6px solid #1A1A1A; padding-left: 15px; margin: 50px 0 30px 0; letter-spacing: -0.5px;",
        "h3": "font-size: 16px; font-weight: bold; color: #5A5A5A; text-transform: uppercase; margin-top: 40px; letter-spacing: 2px;",
        "p": "font-size: 15px; line-height: 1.8; color: #333; margin: 0 0 2em; letter-spacing: 0.05em; text-align: justify;",
        "strong": "border-bottom: 2px solid #000; color: #000; font-weight: bold;",
        "img": "max-width: 100%; border: 1px solid #EEE; display: block; margin: 40px auto; filter: grayscale(1);",
        "accent": "#1A1A1A"
    },
    "ethereal": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #FFFFFF; background-image: linear-gradient(rgba(168, 192, 216, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(168, 192, 216, 0.1) 1px, transparent 1px); background-size: 20px 20px; padding: 80px 40px 80px 100px; border-radius: 8px; font-family: 'Inter', sans-serif; border: 1px solid rgba(168, 192, 216, 0.2); box-shadow: 0 10px 100px rgba(168, 192, 216, 0.1);",
        "h2": "font-size: 30px; color: #A8C0D8; text-align: center; font-weight: 300; margin: 60px 0 40px; border: 1px solid rgba(168, 192, 216, 0.3); padding: 15px;",
        "h3": "font-size: 14px; color: #A8C0D8; text-transform: uppercase; letter-spacing: 6px; text-align: center; margin-top: 50px;",
        "p": "font-size: 16px; line-height: 2.2; color: #777; text-align: center; margin-bottom: 3em;",
        "blockquote": "padding: 30px; margin: 40px 0; border: 0.5px solid rgba(168, 192, 216, 0.5); background: rgba(255,255,255,0.7); font-style: italic; color: #555; text-align: center;",
        "strong": "color: #A8C0D8; font-weight: 600;",
        "img": "max-width: 100%; border-radius: 40px; opacity: 0.9; display: block; margin: 40px auto;",
        "accent": "#A8C0D8"
    },
    "techno": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #121212; background-image: radial-gradient(#333 1px, transparent 1px); background-size: 20px 20px; padding: 80px 40px 80px 100px; border-radius: 0; font-family: 'Courier New', monospace; border: 1px solid #333; box-shadow: 0 10px 50px rgba(0, 243, 255, 0.1); color: #E0E0E0;",
        "h2": "font-size: 24px; font-weight: bold; color: #00F3FF; margin: 50px 0 30px 0; letter-spacing: 1px;",
        "h3": "font-size: 16px; font-weight: bold; color: #00F3FF; margin-top: 40px; letter-spacing: 2px; opacity: 0.8;",
        "p": "font-size: 15px; line-height: 1.8; color: #CCC; margin: 0 0 2em; letter-spacing: 0.05em; text-align: left;",
        "strong": "color: #121212; background-color: #00F3FF; padding: 0 4px;",
        "blockquote": "padding: 20px; margin: 40px 0; border-left: 4px solid #00F3FF; background: rgba(0, 243, 255, 0.05); font-style: italic; color: #00F3FF;",
        "img": "max-width: 100%; border: 1px solid #00F3FF; display: block; margin: 40px auto; filter: contrast(1.2); box-shadow: 0 0 15px rgba(0,243,255,0.2);",
        "accent": "#00F3FF"
    },
    "urban": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #FFFFFF; padding: 80px 40px; border-radius: 0; font-family: 'Arial Black', Impact, sans-serif; border: 4px solid #000; box-shadow: 10px 10px 0px #000; color: #000;",
        "h2": "font-size: 32px; font-weight: 900; color: #1A1A1A; text-transform: uppercase; margin: 50px 0 30px 0; text-shadow: 4px 4px 0px #FF69B4; padding-left: 10px; border-left: 8px solid #8A2BE2;",
        "h3": "font-size: 20px; font-weight: 800; color: #8A2BE2; margin-top: 40px; text-transform: uppercase; font-style: italic; text-decoration: underline; text-decoration-color: #FF69B4; text-decoration-thickness: 4px;",
        "p": "font-size: 16px; line-height: 1.6; color: #111; margin: 0 0 2em; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 600;",
        "strong": "color: #FFF; background-color: #FF69B4; padding: 2px 6px; box-shadow: 3px 3px 0px #000; display: inline-block; transform: rotate(-2deg);",
        "blockquote": "padding: 25px; margin: 40px -20px; border: 4px solid #000; background: #FF69B4; font-family: 'Arial Black', Impact, sans-serif; font-size: 18px; color: #FFF; text-transform: uppercase; box-shadow: 8px 8px 0px #8A2BE2; transform: rotate(1deg);",
        "img": "max-width: 100%; border: 4px solid #000; display: block; margin: 40px auto; box-shadow: 10px 10px 0px #000;",
        "accent": "#8A2BE2"
    },
    "wonyoung": {
        "card": "width: 100%; max-width: 500px; margin: 0 auto; background-color: #FFFBFB; background-image: radial-gradient(circle, #FFF 10%, transparent 10%); background-size: 15px 15px; padding: 70px 30px; border-radius: 12px; font-family: 'Playfair Display', serif; border: 1px solid #F5E6E8; box-shadow: 0 20px 50px rgba(224, 176, 255, 0.15); color: #333;",
        "h2": "font-size: 26px; font-weight: 700; color: #E0B0FF; text-align: center; margin: 50px 0 20px 0; font-style: italic;",
        "h3": "font-size: 16px; font-weight: 600; color: #CBAACB; text-align: center; text-transform: uppercase; margin-top: 40px; letter-spacing: 3px;",
        "p": "font-size: 15px; line-height: 2.0; color: #555; text-align: center; margin: 0 0 2em;",
        "strong": "color: #E0B0FF; font-weight: bold;",
        "blockquote": "padding: 20px; margin: 40px 0; border: 1px solid #F5E6E8; border-radius: 8px; font-style: italic; color: #888; text-align: center; background: #FFF;",
        "img": "max-width: 100%; border-radius: 12px; display: block; margin: 30px auto; box-shadow: 0 10px 25px rgba(224, 176, 255, 0.3);",
        "accent": "#E0B0FF"
    },
    "algorithm": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background: linear-gradient(135deg, rgba(255,200,220,0.4), rgba(200,220,255,0.4), rgba(220,200,255,0.4)); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 70px 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 30px 60px rgba(0,0,0,0.05); font-family: 'Inter', sans-serif; color: #222;",
        "h2": "font-size: 28px; font-weight: 800; color: #333; letter-spacing: -1px; margin: 50px 0 24px 0;",
        "h3": "font-size: 14px; font-weight: 700; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-top: 40px;",
        "p": "font-size: 16px; line-height: 1.8; color: #444; margin: 0 0 2em;",
        "strong": "color: #000; border-bottom: 2px solid #333; padding-bottom: 1px;",
        "img": "max-width: 100%; border-radius: 16px; display: block; margin: 40px auto; mix-blend-mode: multiply; opacity: 0.9;",
        "accent": "#A8C0D8"
    },
    "archive": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #EAEAEA; padding: 80px 40px; border-radius: 0; font-family: 'Helvetica', sans-serif; border: 1px solid #CCC; color: #111; position: relative;",
        "h2": "font-size: 22px; font-weight: 800; color: #000; text-transform: uppercase; background: #FFF; display: inline-block; padding: 5px 15px; transform: rotate(-1deg); box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin: 50px 0 30px 0;",
        "h3": "font-size: 14px; font-family: 'Courier New', monospace; font-weight: bold; color: #555; text-transform: uppercase; margin-top: 40px; letter-spacing: 1px;",
        "p": "font-size: 14px; line-height: 1.6; color: #333; margin: 0 0 2em;",
        "strong": "color: #000; background: #D9D9D9; padding: 0 4px;",
        "blockquote": "padding: 20px; margin: 40px 0; border-left: 3px solid #000; font-family: 'Courier New', monospace; font-size: 13px; color: #444; background: #F5F5F5;",
        "img": "max-width: 100%; border: 1px solid #999; display: block; margin: 40px auto; filter: sepia(0.2) contrast(1.1); padding: 10px; background: #FFF;",
        "accent": "#999"
    },
    "solidcore": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #111; background-image: repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(255,255,255,0.03) 50px, rgba(255,255,255,0.03) 51px); padding: 80px 40px; border-radius: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #FFF; box-shadow: 0 20px 40px rgba(0,0,0,0.5);",
        "h2": "font-size: 36px; font-weight: 900; color: #CCFF00; text-transform: uppercase; font-style: italic; margin: 50px 0 20px 0; letter-spacing: -1px;",
        "h3": "font-size: 18px; font-weight: 800; color: #FFF; text-transform: uppercase; font-style: italic; margin-top: 40px; letter-spacing: 1px;",
        "p": "font-size: 16px; line-height: 1.7; color: #CCC; margin: 0 0 2em;",
        "strong": "color: #111; background-color: #CCFF00; padding: 0 5px; font-style: italic;",
        "blockquote": "padding: 20px; margin: 40px 0; border-left: 4px solid #CCFF00; font-weight: bold; font-style: italic; color: #FFF; font-size: 18px;",
        "img": "max-width: 100%; display: block; margin: 40px auto; border: 2px solid #333; filter: grayscale(0.5) contrast(1.2);",
        "accent": "#CCFF00"
    },
    "bottari": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background-color: #F2EEE9; padding: 80px 50px; border-radius: 4px; font-family: 'Georgia', serif; color: #3D3B38; box-shadow: 0 10px 30px rgba(61,59,56,0.08); border: 1px solid #E5DFD5;",
        "h2": "font-size: 24px; font-weight: 400; color: #2C2A28; text-align: center; margin: 50px 0 30px 0; letter-spacing: 1px;",
        "h3": "font-size: 12px; font-weight: normal; color: #7A756C; text-align: center; text-transform: uppercase; margin-top: 40px; letter-spacing: 4px;",
        "p": "font-size: 15px; line-height: 2.2; color: #5C5852; text-align: justify; margin: 0 0 2.5em;",
        "strong": "color: #2C2A28; font-weight: 600;",
        "blockquote": "padding: 30px; margin: 40px 0; border: 1px solid #D1C9C0; font-style: italic; color: #6C6862; text-align: center;",
        "img": "max-width: 100%; display: block; margin: 50px auto; opacity: 0.85; filter: sepia(0.1);",
        "accent": "#D1C9C0"
    }
}

LOREM_TAGS = {
    "loopy": ["pastel", "toy"],
    "executive": ["architecture", "office"],
    "ethereal": ["sky", "clouds"],
    "techno": ["cyberpunk", "circuit"],
    "urban": ["street", "graffiti"],
    "wonyoung": ["pink", "diamonds", "jewelry"],
    "algorithm": ["mesh", "gradient", "fluid"],
    "archive": ["concrete", "sneaker", "vintage"],
    "solidcore": ["fitness", "lime", "dark"],
    "bottari": ["earthy", "canvas", "minimal"]
}

def smart_restructure(text):
    # Rule 0: Clean Slate Headers (Prevent #### accumulation)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Rule 1: Breathing Room (max 3 sentences)
    paragraphs = text.split('\n\n')
    new_paras = []
    
    for p in paragraphs:
        sentences = re.split(r'([.!?。！？])', p.strip())
        if len(sentences) > 6:
            for i in range(0, len(sentences)-1, 6):
                chunk = "".join(sentences[i:i+6]).strip()
                if chunk: new_paras.append(chunk)
        else:
            new_paras.append(p.strip())
            
    # Rule 2: Hierarchy & Rule 3: Emphasis
    final_output = []
    for p in new_paras:
        if len(p) < 40 and not p.endswith(('.', '。', '!', '！', '?', '？')):
            if len(p) < 15: final_output.append(f"## {p}")
            else: final_output.append(f"### {p}")
        elif p.startswith(('"', "'", "“", "「")) and p.endswith(('"', "'", "”", "」")):
            final_output.append(f"> {p}")
        else:
            words = p.split()
            if len(words) > 10:
                mid = len(words) // 2
                words[mid] = f"**{words[mid]}**"
                if mid + 1 < len(words): words[mid+1] = f"**{words[mid+1]}**"
                p = " ".join(words)
            final_output.append(p)
            
    return "\n\n".join(final_output)

def auto_illustrate(text, theme_id="loopy"):
    # Step 1: The Nuclear Wipe (Aesthetic Sanitization)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text, flags=re.DOTALL)
    text = text.strip()

    # Step 2: Simplified Illustration Logic (Zero-Hero Policy)
    DIVIDER_TAGS = {
        "loopy": "pastel,gradient,soft",
        "executive": "monochrome,grid,minimal",
        "ethereal": "light,blur,airy",
        "techno": "circuit,matrix,dark",
        "urban": "neon,blur,texture",
        "wonyoung": "sparkle,diamond,pink",
        "algorithm": "mesh,fluid,gradient",
        "archive": "concrete,texture,industrial",
        "solidcore": "motion,blur,lime",
        "bottari": "paper,earthy,texture"
    }

    divider_tags = DIVIDER_TAGS.get(theme_id, "pastel,gradient,soft")
    tag_list = [t.strip() for t in divider_tags.split(",")]
    chosen_tag = random.choice(tag_list)
    
    seed = random.randint(1, 999999)
    divider_url = f"https://loremflickr.com/1000/600/{chosen_tag}/all?lock={seed}"

    # Step 3: Strict Markdown Syntax Insertion
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    if lines:
        mid = len(lines) // 2
        # Critical Requirement: exactly two newlines before and after image
        lines.insert(mid, f"\n\n![Divider]({divider_url})\n\n")

    return "\n\n".join(lines).strip()

def render_aura_engine(md_text, theme_id="loopy"):
    theme = THEMES.get(theme_id, THEMES["loopy"])
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br', 'sane_lists'])
    soup = BeautifulSoup(raw_html, "html.parser")

    for h2 in soup.find_all("h2"):
        if theme_id == "executive":
            num_span = soup.new_tag("span", style="font-family: 'Courier New', monospace; font-size: 0.7em; color: #888; font-weight: normal; margin-right: 10px;")
            num_span.string = "[SECTION.SC]"
            orig_text = h2.get_text()
            h2.clear()
            h2.append(num_span); h2.append(f" {orig_text}")
        elif theme_id == "techno":
            num_span = soup.new_tag("span", style="color: #00F3FF; margin-right: 10px; opacity: 0.6;")
            num_span.string = "// SYSTEM_LOG"
            orig_text = h2.get_text()
            h2.clear()
            h2.append(num_span); h2.append(f" {orig_text}")
        elif theme_id == "wonyoung":
            orig_text = h2.get_text()
            h2.string = f"{orig_text} ✨"
        h2['style'] = theme['h2']
    
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        if theme_id == "loopy":
            num_span = soup.new_tag("span", style="font-family: 'Courier New', monospace; font-weight: bold; margin-right: 8px;")
            num_span.string = f"{i:02d} "
            orig_text = h3.get_text()
            h3.clear()
            h3.append(num_span); h3.append(orig_text)
            divider = soup.new_tag("div", style="border-top: 0.5px solid #E5E5E5; width: 30%; margin: 60px 0 24px 0;")
            h3.insert_before(divider)
        elif theme_id == "bottari":
            orig_text = h3.get_text()
            h3.string = f"[ Scent Notes: {orig_text} ]"
        h3['style'] = theme['h3']
    
    for tag in ["p", "strong", "blockquote"]:
        if tag in theme or (tag == "blockquote" and "blockquote" in theme):
            for el in soup.find_all(tag): el['style'] = theme.get(tag, "")

    for img in soup.find_all("img"):
        img['style'] = theme.get("img", "max-width: 100%; height: auto; display: block; margin: 30px auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);")
        img['data-w'] = "100%"
        
        # Divider specific styling
        if img.get("alt") == "Divider":
            color = theme.get("accent", "#CCC")
            container = soup.new_tag("div", style=f"margin: 60px 0 40px; padding-bottom: 15px; border-bottom: 1px solid {color}; background-image: linear-gradient(90deg, {color} 1px, transparent 1px); background-size: 10px 6px; background-repeat: repeat-x; background-position: bottom;")
            
            if theme_id == "solidcore":
                # Motion blur effect on solidcore divider
                img['style'] += " filter: blur(1px) contrast(1.5); transform: skewX(-5deg);"
            
            img.wrap(container)
        
        # Hero specific styling    
        if img.get("alt") == "Hero":
            if theme_id == "archive":
                cert_badge = soup.new_tag("div", style="position: absolute; top: -10px; right: -10px; background: #000; color: #FFF; font-family: 'Courier New', monospace; font-size: 10px; font-weight: bold; padding: 5px 10px; transform: rotate(5deg); border: 1px solid #FFF;")
                cert_badge.string = "CERTIFIED AUTHENTIC"
                wrapper = soup.new_tag("div", style="position: relative; display: inline-block; width: 100%;")
                img.wrap(wrapper)
                wrapper.append(cert_badge)

    # Footer Bubble Signature
    footer = soup.new_tag("div", style="text-align: center; margin-top: 60px; padding-bottom: 20px;")
    
    if LOOPY_DATA_URI and theme_id == "loopy":
        bubble = soup.new_tag("div", style="width: 60px; height: 60px; background: #FFF; border-radius: 50%; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 1px solid #F5F5F5;")
        bubble.append(soup.new_tag("img", src=LOOPY_DATA_URI, style="width: 32px; height: auto;"))
        footer.append(bubble)
    elif LOOPY_DATA_URI and theme_id == "ethereal":
        bubble = soup.new_tag("div", style="width: 60px; height: 60px; background: transparent; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(168, 192, 216, 0.4);")
        bubble.append(soup.new_tag("img", src=LOOPY_DATA_URI, style="width: 32px; height: auto; opacity: 0.6;"))
        footer.append(bubble)
    elif LOOPY_DATA_URI and theme_id == "urban":
        bubble = soup.new_tag("div", style="width: 80px; height: 80px; background: #000; border-radius: 50%; box-shadow: 0 0 30px #FF69B4, inset 0 0 20px #8A2BE2; margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 4px solid #FFF;")
        bubble.append(soup.new_tag("img", src=LOOPY_DATA_URI, style="width: 50px; height: auto; filter: drop-shadow(0 0 5px #FFF);"))
        footer.append(bubble)
        
    if theme_id == "executive":
        ts = soup.new_tag("div", style="font-size: 12px; font-weight: bold; letter-spacing: 2px; color: #1A1A1A; text-transform: uppercase; margin-top: 15px;")
        ts.string = "XYLAB STANCE CORE // 2026"
        footer['style'] = "margin-top: 80px; border-top: 2px solid #000; padding-top: 20px; text-align: left;"
        footer.append(ts)
    elif theme_id == "ethereal":
        ts = soup.new_tag("div", style="font-size: 10px; font-weight: 300; letter-spacing: 6px; color: #A8C0D8; text-transform: uppercase; margin-top: 15px;")
        ts.string = "XYLAB STANCE CORE // 2026"
        footer['style'] = "margin-top: 80px; padding-top: 20px; text-align: center;"
        footer.append(ts)
    elif theme_id == "techno":
        ts = soup.new_tag("div", style="font-size: 12px; font-weight: bold; letter-spacing: 2px; color: #00F3FF; font-family: 'Courier New', monospace; opacity: 0.8; margin-top: 15px;")
        ts.string = ">> XYLAB.TECHNO_CORE.SYS // 2026"
        footer['style'] = "margin-top: 80px; padding-top: 20px; text-align: left; border-top: 1px dashed #00F3FF;"
        footer.append(ts)
    elif theme_id == "urban":
        ts = soup.new_tag("div", style="font-size: 14px; font-weight: 900; letter-spacing: 2px; color: #1A1A1A; font-family: 'Arial Black', sans-serif; background: #FF69B4; display: inline-block; padding: 5px 15px; transform: skewX(-10deg); box-shadow: 4px 4px 0px #000; margin-top: 20px; text-transform: uppercase;")
        ts.string = "XYLAB STANCE CORE // 2026"
        footer['style'] = "margin-top: 80px; padding-top: 40px; text-align: center; border-top: 8px solid #8A2BE2; background: linear-gradient(180deg, transparent 0%, rgba(255,105,180,0.1) 100%);"
        footer.append(ts)
    elif theme_id == "wonyoung":
        ts = soup.new_tag("div", style="font-size: 12px; font-weight: bold; letter-spacing: 3px; color: #E0B0FF; font-family: 'Playfair Display', serif; margin-top: 15px; text-transform: uppercase; font-style: italic;")
        ts.string = "Y/X Center Stage"
        footer['style'] = "margin-top: 60px; padding-top: 20px; text-align: center; border-top: 1px solid #F5E6E8;"
        footer.append(ts)
    elif theme_id == "algorithm":
        ts = soup.new_tag("div", style="font-size: 10px; font-weight: bold; letter-spacing: 5px; color: #555; font-family: 'Inter', sans-serif; margin-top: 15px; text-transform: uppercase;")
        ts.string = "DATA_SC X ART"
        footer['style'] = "margin-top: 60px; padding-top: 20px; text-align: right; border-top: 1px solid rgba(0,0,0,0.1);"
        footer.append(ts)
    elif theme_id == "archive":
        ts = soup.new_tag("div", style="font-size: 11px; font-weight: bold; letter-spacing: 2px; color: #111; font-family: 'Courier New', monospace; margin-top: 15px; text-transform: uppercase; background: #D9D9D9; display: inline-block; padding: 2px 8px;")
        ts.string = "ARCHIVE: 2026"
        footer['style'] = "margin-top: 60px; padding-top: 20px; text-align: left; border-top: 2px dashed #999;"
        footer.append(ts)
    elif theme_id == "solidcore":
        ts = soup.new_tag("div", style="font-size: 16px; font-weight: 900; letter-spacing: -1px; color: #111; font-family: 'Helvetica', sans-serif; margin-top: 15px; text-transform: uppercase; font-style: italic; background: #CCFF00; display: inline-block; padding: 5px 20px; transform: skewX(-15deg);")
        ts.string = "XYLAB KINETIC"
        footer['style'] = "margin-top: 60px; padding-top: 40px; text-align: center; border-top: 4px solid #CCFF00;"
        footer.append(ts)
    elif theme_id == "bottari":
        ts = soup.new_tag("div", style="font-size: 12px; font-weight: normal; letter-spacing: 6px; color: #7A756C; font-family: 'Georgia', serif; margin-top: 15px; text-transform: uppercase;")
        ts.string = "XYLAB FRAGRANCE LAB"
        footer['style'] = "margin-top: 80px; padding-top: 30px; text-align: center; border-top: 1px solid #D1C9C0;"
        footer.append(ts)
    elif theme_id == "loopy":
        ts = soup.new_tag("div", style="font-size: 10px; color: #888; letter-spacing: 4px; margin-top: 15px; text-transform: uppercase;")
        ts.string = "XYLAB STANCE CORE // 2026"
        footer.append(ts)
    
    soup.append(footer)

    return f'<div id="aura-card" style="{theme["card"]}">{soup.decode_contents()}</div>'

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "loopy_uri": LOOPY_DATA_URI})

@app.post("/convert")
async def convert(markdown_input: str = Form(...), theme: str = Form("loopy")):
    return {"html": render_aura_engine(markdown_input, theme_id=theme)}

@app.post("/ai-process")
async def ai_process(markdown_input: str = Form(...), theme: str = Form('loopy')):
    res = smart_restructure(markdown_input)
    res = auto_illustrate(res, theme_id=theme)
    return {"markdown": res}

@app.post("/shuffle-image")
async def shuffle_image(theme: str = Form("loopy")):
    tags = LOREM_TAGS.get(theme, LOREM_TAGS["loopy"])
    chosen_tag = random.choice(tags)
    
    seed = random.randint(1, 999999)
    timestamp = int(time.time() * 1000)
    url = f"https://loremflickr.com/1000/600/{chosen_tag}/all?lock={seed}&t={timestamp}"
    return {"new_image_markdown": f"![Divider]({url})"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)