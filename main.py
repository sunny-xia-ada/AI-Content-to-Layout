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
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import json
from duckduckgo_search import DDGS

# Initialize the LLM (Requires GEMINI_API_KEY environment variable)
genai.configure(api_key="AIzaSyBIsVN0XhvYWxkGDmBQwm2l8mLNfQnl-QU")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="XYLAB // SMART AGENT v7.7.3")

# Add CORS Middleware to support local file access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class XhsMagicRequest(BaseModel):
    prompt: str

class VisionMagicRequest(BaseModel):
    prompt: str
    image: Optional[str] = None  # Base64 image data

# XHS Native Template Engine (Viral Frameworks v5.0)
XHS_TEMPLATES = [
    {
        "id": "shopping_selection_logic",
        "category": {"primary": "shopping_brand_discovery", "secondary": "lifestyle_mood", "confidence": 0.96},
        "copy": {
            "title": "在韩国逛街，我只留下这3类品牌🛍️",
            "hook": "有些品牌只是过客，有些才能进我生活。",
            "body": "这几天在汉南洞和圣水洞走走停停，比起那些需要排长队的人气品牌，我更在意哪些能让我真正想带回家。\n\n我筛选的标准其实挺直接的：\n\n1. 看面料和质地。我更偏爱那种有呼吸感、有颗粒感的自然材质，这种质感才值得长久陪伴。\n2. 看店里的氛围感。真正好的品牌，店里应该是安静、有留白的，能让人在忙碌的行程里稍微停下来喘口气。\n3. 看穿搭的实穿度。我会想这件衣服和我衣柜里已有的衣服怎么搭，不想为了那点所谓的新鲜感买单。",
            "ending": "与其说是筛选品牌，不如说是在理清我到底想要什么样的日常吧。",
            "tags": ["韩国逛街", "汉南洞", "圣水洞", "我的生活方式", "小众品牌"]
        },
        "visual": {"theme": "bottari", "mode": "rednote_feed", "layout": "inner", "image_prompt": "Realistic lifestyle photography of a minimalist Hannam-dong boutique interior, soft natural light from a side window, a simple wooden clothing rack with linen textures, iPhone photo feel, subtle shadows, clean 3:4 composition, negative space at top."},
        "quality": {"score_total": 88, "hook_strength": 82, "save_value": 92, "authenticity": 90, "specificity": 88, "xhs_fit": 86, "elegance": 80}
    },
    {
        "id": "tech_minimalist_workflow",
        "category": {"primary": "tech_desk_setup", "secondary": "productivity", "confidence": 0.92},
        "copy": {
            "title": "这就是我想要的代码避难所⌨️",
            "hook": "拒绝复杂，回归最高效的简法工作流。",
            "body": "深夜写码的时候，我发现能让我专注的从来不是昂贵的设备，而是这种极致的清爽感。\n\n我的桌搭逻辑其实就这几点：\n\n1. 极简布线。桌面上看不到一根多余的线，这种视觉上的无序感最消耗专注力。\n2. 纯粹质感。比起RGB灯带，我更喜欢冷色光的颗粒感，能让我更冷静地思考。\n3. 触感先行。键盘的反馈和鼠标的丝滑，是我和代码对话的唯一触媒。",
            "ending": "效率不是加法，而是把多余的噪音彻底关掉。",
            "tags": ["我的桌搭", "程序员日常", "极简生活", "生产力工具"]
        },
        "visual": {"theme": "techno", "mode": "rednote_feed", "layout": "cover", "image_prompt": "Realistic photography of a minimalist coding setup, dark aesthetic, single monitor with green code, mechanical keyboard, dark wood desk, natural moonlight shadow, iPhone photo feel, sharp textures, high contrast."},
        "quality": {"score_total": 85, "hook_strength": 80, "save_value": 88, "authenticity": 85, "specificity": 82, "xhs_fit": 84, "elegance": 88}
    }
]

# Vercel Serverless Absolute Pathing Fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
if not os.path.exists(TEMPLATE_DIR): TEMPLATE_DIR = os.path.abspath("templates")

# Static Asset Resolution
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.abspath("static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

# --- Media & Assets ---
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

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def os_portal(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/wechat", response_class=HTMLResponse)
@app.get("/wechat.html", response_class=HTMLResponse)
async def wechat_engine(request: Request):
    return templates.TemplateResponse(request, "wechat.html", {"loopy_uri": LOOPY_DATA_URI})

@app.get("/xhs", response_class=HTMLResponse)
@app.get("/xhs.html", response_class=HTMLResponse)
async def xhs_engine(request: Request):
    return templates.TemplateResponse(request, "xhs.html", {"loopy_uri": LOOPY_DATA_URI})

@app.get("/youtube", response_class=HTMLResponse)
@app.get("/youtube.html", response_class=HTMLResponse)
async def youtube_engine(request: Request):
    return templates.TemplateResponse(request, "youtube.html", {})

@app.get("/x", response_class=HTMLResponse)
@app.get("/x.html", response_class=HTMLResponse)
async def x_engine(request: Request):
    return templates.TemplateResponse(request, "x.html", {})

@app.get("/spotify", response_class=HTMLResponse)
@app.get("/spotify.html", response_class=HTMLResponse)
async def spotify_engine(request: Request):
    return templates.TemplateResponse(request, "spotify.html", {})

@app.get("/douyin", response_class=HTMLResponse)
@app.get("/douyin.html", response_class=HTMLResponse)
async def douyin_engine(request: Request):
    return templates.TemplateResponse(request, "douyin.html", {})

@app.get("/meituan", response_class=HTMLResponse)
@app.get("/meituan.html", response_class=HTMLResponse)
async def meituan_engine(request: Request):
    return templates.TemplateResponse(request, "meituan.html", {})

@app.get("/api/proxy-image")
async def proxy_image(url: str):
    import httpx
    from fastapi import Response
    import random
    
    decoded_url = urllib.parse.unquote(url)
    if not decoded_url.startswith(("http://", "https://")):
        return Response(status_code=400, content="Invalid URL scheme")
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(decoded_url, headers=headers)
            if resp.status_code == 200:
                return Response(
                    content=resp.content,
                    media_type=resp.headers.get("content-type", "image/jpeg"),
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Cache-Control": "public, max-age=86400"
                    }
                )
            print(f"Proxy main request returned status {resp.status_code} for {decoded_url}")
    except Exception as e:
        print(f"Proxy main request exception for {decoded_url}: {e}")

    # Fallback: Curated high-quality backgrounds that support CORS
    FALLBACKS = [
        "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1000&q=80"
    ]
    
    fallback_url = random.choice(FALLBACKS)
    print(f"Proxy falling back to curated image: {fallback_url}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(fallback_url, headers=headers)
            if resp.status_code == 200:
                return Response(
                    content=resp.content,
                    media_type=resp.headers.get("content-type", "image/jpeg"),
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Cache-Control": "public, max-age=86400"
                    }
                )
    except Exception as fallback_err:
        print(f"Proxy fallback request exception: {fallback_err}")
        
    return Response(status_code=500, content="Proxy Error")

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

@app.post("/api/vision-magic")
async def vision_magic(request: VisionMagicRequest):
    prompt_text = request.prompt
    try:
        with DDGS() as ddgs:
            refs = list(ddgs.text(f"site:xiaohongshu.com {prompt_text[:20]}", max_results=3))
            refs_text = "\n".join([r.get('body', '') for r in refs])
    except: refs_text = "N/A"

    system_instruction = (
        f"你是顶级小红书与美妆护肤博主。参考：{refs_text}\n"
        "根据用户提示与可能上传的商品图，生成多张极其种草、爆款的小红书轮播图分镜卡片文案（限制在 2 到 6 张卡片内）。\n"
        "文案必须按页面顺序拆分：\n"
        "1. 第一张卡片（数组第1项）必须是封面标题页（Cover Page），标题要极其吸睛、有冲击力，Hook为引流句，Core Copy列出产品最核心的 2-3 个爆炸卖点（如：5D复合玻尿酸、15分钟极速补水退红）。\n"
        "2. 第二张及之后的卡片为细节干货页（Detail Page），包含具体的使用体验、成分拆解、保姆级敷法步骤、避坑指南等，排版列点清晰，字数精简适合手机卡片阅读。\n"
        "必须返回且仅返回一个干净的 JSON 对象（不包含 ``` 标记），结构必须为：\n"
        "{\n"
        "  \"scenes\": [\n"
        "    {\n"
        "      \"title\": \"本页标题（如：这面膜太神了 / 🔍成分深度拆解）\",\n"
        "      \"hook\": \"本页Hook/引流句（如：敷完脸上掐得出水💦）\",\n"
        "      \"body\": \"本页干货内容（分行列出 2-3 点，使用换行符号或 Emoji）\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )
    contents = [system_instruction, f"User Prompt: {prompt_text}"]
    if request.image:
        img_data = request.image
        if ";base64," in img_data: img_data = img_data.split(";base64,")[1]
        contents.append({"mime_type": "image/jpeg", "data": base64.b64decode(img_data)})

    # Try multiple models to find one with quota
    candidate_models = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-2.5-pro',
        'models/gemini-pro-latest'
    ]
    
    last_error = ""
    for model_name in candidate_models:
        try:
            print(f"Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            last_error = str(e)
            print(f"Model {model_name} failed: {last_error}")
            continue # Try next model
            
    # If all models fail
    if "429" in last_error:
        return {
            "scenes": [{
                "title": "🚦 创作配额受限", 
                "hook": "检测到 API 额度异常", 
                "body": f"虽然你今天没用过，但 Google 返回了配额错误：{last_error}\n这通常是因为：\n1. 网络代理所在地区受限\n2. 该 Key 尚未在 AI Studio 激活预览权限"
            }]
        }
    
    return {
        "scenes": [{
            "title": "GENERATION FAILED", 
            "hook": "API Error", 
            "body": f"所有尝试的模型均失败。最后报错: {last_error}"
        }]
    }

# --- XHS STUDIO NEW ARCHITECTURE ENDPOINTS ---

class BriefRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

class CarouselRequest(BaseModel):
    brief: dict
    theme: str
    pageCount: int

class RegenerateRequest(BaseModel):
    pageIndex: int
    theme: str
    brief: dict
    pages: list

def mock_generate_brief(prompt: str):
    return {
        "detectedTopic": prompt or "美妆日常",
        "recommendedFormat": "6-page-carousel",
        "suggestedTheme": "XYLab Beauty",
        "visualMood": ["clean", "glowy", "soft pink"],
        "copyTone": "calm editorial, slightly confident",
        "narrativeArc": [
            "Cover: emotional hook about " + (prompt[:15] if prompt else "Aesthetics"),
            "Page 01: core insight on why this matters",
            "Page 02: detail breakdown or ingredients analysis",
            "Page 03: routine steps or methodology",
            "Page 04: direct results or comparisons",
            "Page 05: final review & call to action"
        ]
    }

def mock_generate_carousel(brief: dict, theme: str, page_count: int = 6):
    topic = brief.get("detectedTopic", "Aesthetic Idea")
    mood = brief.get("visualMood", ["editorial", "clean"])
    
    layouts = ["magazine-cover", "split-editorial", "info-card", "routine-flow", "before-after", "quote-page", "product-catalog"]
    
    # Map theme presets
    presets_map = {
        "XYLab Muse": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=800&q=80",
        "XYLab Beauty": "https://images.unsplash.com/photo-1608248597481-496100c80836?auto=format&fit=crop&w=800&q=80",
        "XYLab Stage": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
        "XYLab Gems": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=800&q=80",
        "XYLab Salon": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80"
    }
    
    img_url = presets_map.get(theme, "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80")
    
    pages = []
    # cover
    pages.append({
        "id": "page_0",
        "pageNumber": 1,
        "type": "cover",
        "headline": f"{topic}",
        "subheadline": "XYLab Editorial Concept",
        "body": "A curated visual storytelling project exploring modern styling dynamics.",
        "smallNote": "VOL. 01 / XYLAB MUSE",
        "layout": "magazine-cover",
        "imageRole": "hero",
        "imageUrl": img_url,
        "accent": "",
        "textAlign": "center",
        "density": "medium",
        "logoPosition": "bottom-right"
    })
    
    # inner
    for i in range(1, page_count):
        lay = layouts[i % len(layouts)]
        if i == page_count - 1:
            lay = "quote-page"
            
        headline = f"Core Insight 0{i}"
        body = f"Detail point A for this section.\nDetail point B showing logical breakdown.\nKeep paragraphs spaced nicely."
        
        pages.append({
            "id": f"page_{i}",
            "pageNumber": i + 1,
            "type": "insight" if i < 3 else "detail",
            "headline": headline,
            "subheadline": f"AESTHETIC ANALYSIS // 0{i}",
            "body": body,
            "smallNote": f"SPECIFICATION {i}",
            "layout": lay,
            "imageRole": "supporting",
            "imageUrl": img_url,
            "accent": "",
            "textAlign": "left" if lay != "quote-page" else "center",
            "density": "medium",
            "logoPosition": "bottom-right"
        })
        
    return {
        "projectTitle": topic,
        "theme": theme,
        "format": f"{page_count}-page-carousel",
        "visualMood": mood,
        "pages": pages,
        "caption": f"💡 {topic}\n\n这里是为您自动生成的精彩小红书文案！\n包含核心卖点和详细步骤拆解，排版极具杂志高级感。\n\n#小红书排版 #高级感 #审美提升 #XYLab",
        "hashtags": [f"#{topic}", "#小红书排版", "#高级感", "#XYLab"]
    }

@app.post("/api/xhs/generate-brief")
async def api_generate_brief(request: BriefRequest):
    prompt_text = request.prompt
    
    system_instruction = (
        "You are a top Xiaohongshu (XHS) creator and editorial director.\n"
        "Analyze the user's idea or rough draft and output a structured creative brief.\n"
        "You must return ONLY a valid JSON object matching this schema (do not include markdown block wrappers):\n"
        "{\n"
        "  \"detectedTopic\": \"Detected theme or core idea (e.g., 白金发之后的妆容逻辑)\",\n"
        "  \"recommendedFormat\": \"Format like '6-page-carousel', '8-page-carousel', or '9-page-archive-carousel'\",\n"
        "  \"suggestedTheme\": \"Name of the theme matching the style DNA (e.g. XYLab Beauty)\",\n"
        "  \"visualMood\": [\"Color accent or key visual words (e.g., soft pink, clean editorial)\"],\n"
        "  \"copyTone\": \"Copywriter writing tone (e.g., calm editorial, slightly confident)\",\n"
        "  \"narrativeArc\": [\n"
        "    \"Cover: hook statement\",\n"
        "    \"Page 01: insight statement\",\n"
        "    \"Page 02: detail/concept statement\",\n"
        "    ...\n"
        "  ]\n"
        "}"
    )
    
    contents = [system_instruction, f"User Idea/Draft: {prompt_text}"]
    if request.image:
        img_data = request.image
        if ";base64," in img_data: img_data = img_data.split(";base64,")[1]
        contents.append({"mime_type": "image/jpeg", "data": base64.b64decode(img_data)})

    candidate_models = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-2.5-pro',
        'models/gemini-pro-latest'
    ]
    
    for model_name in candidate_models:
        try:
            print(f"Brief generation using: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Model {model_name} failed for brief: {e}")
            continue
            
    # Fallback
    return mock_generate_brief(prompt_text)

@app.post("/api/xhs/generate-carousel")
async def api_generate_carousel(request: CarouselRequest):
    brief = request.brief
    theme = request.theme
    page_count = request.pageCount
    
    system_instruction = (
        f"You are a premium editorial director for Xiaohongshu. Based on the provided Creative Brief, selected Theme ({theme}), and requested page count ({page_count}), generate a full multi-page carousel project.\n"
        "Generate carousel data as structured JSON, then return ONLY a valid JSON object matching this schema (do not wrap in markdown tags):\n"
        "{\n"
        "  \"projectTitle\": \"Title of the project\",\n"
        "  \"theme\": \"Chosen theme\",\n"
        "  \"format\": \"Format e.g., 6-page-carousel\",\n"
        "  \"visualMood\": [\"Color accent or key visual words\"],\n"
        "  \"pages\": [\n"
        "    {\n"
        "      \"id\": \"page_0\",\n"
        "      \"pageNumber\": 1,\n"
        "      \"type\": \"cover\",\n"
        "      \"headline\": \"Cover headline (punchy, high hook)\",\n"
        "      \"subheadline\": \"English subtitle for editorial feeling\",\n"
        "      \"body\": \"\",\n"
        "      \"smallNote\": \"Refined small label or issue name\",\n"
        "      \"layout\": \"magazine-cover\",\n"
        "      \"imageRole\": \"hero\",\n"
        "      \"imageUrl\": \"curated image URL based on theme visual mood\",\n"
        "      \"accent\": \"Hex color string like #D7B7C8 or empty\",\n"
        "      \"textAlign\": \"center\",\n"
        "      \"density\": \"medium\",\n"
        "      \"logoPosition\": \"bottom-right\"\n"
        "    },\n"
        "    {\n"
        "      \"id\": \"page_1\",\n"
        "      \"pageNumber\": 2,\n"
        "      \"type\": \"insight\",\n"
        "      \"headline\": \"Page headline\",\n"
        "      \"subheadline\": \"English small category header\",\n"
        "      \"body\": \"Detailed body content - use line breaks (\\n) and bullets if needed\",\n"
        "      \"smallNote\": \"Refined small annotation\",\n"
        "      \"layout\": \"split-editorial\",\n"
        "      \"imageRole\": \"supporting\",\n"
        "      \"imageUrl\": \"curated image URL\",\n"
        "      \"accent\": \"\",\n"
        "      \"textAlign\": \"left\",\n"
        "      \"density\": \"medium\",\n"
        "      \"logoPosition\": \"bottom-right\"\n"
        "    }\n"
        "  ],\n"
        "  \"caption\": \"Xiaohongshu post text caption (engaging, emojis, bullet points)\",\n"
        "  \"hashtags\": [\"#hashtag1\", \"#hashtag2\"]\n"
        "}\n\n"
        "Use these layout names where appropriate: 'magazine-cover' (mandatory for Cover), 'split-editorial', 'info-card', 'moodboard-archive', 'routine-flow', 'before-after', 'quote-page', 'product-catalog'."
    )
    
    contents = [system_instruction, f"Creative Brief: {json.dumps(brief)}"]
    
    candidate_models = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-2.5-pro'
    ]
    
    for model_name in candidate_models:
        try:
            print(f"Carousel generation using: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Model {model_name} failed for carousel: {e}")
            continue
            
    # Fallback
    return mock_generate_carousel(brief, theme, page_count)

@app.post("/api/xhs/regenerate-page")
async def api_regenerate_page(request: RegenerateRequest):
    page_index = request.pageIndex
    theme = request.theme
    brief = request.brief
    current_pages = request.pages
    
    if page_index < 0 or page_index >= len(current_pages):
        return {"error": "Invalid page index"}
        
    page_to_regen = current_pages[page_index]
    
    system_instruction = (
        f"You are a premium editorial director for Xiaohongshu. Regenerate this single page (index: {page_index}) in a multi-page carousel project.\n"
        f"Selected Theme: {theme}\n"
        f"Brief: {json.dumps(brief)}\n"
        f"Current Slide Content: {json.dumps(page_to_regen)}\n"
        "Improve the copywriting, headlines, subheadlines, or structure to make it punchier and look more like an editorial magazine.\n"
        "Return ONLY a valid JSON object matching the single page schema (do not wrap in markdown tags):\n"
        "{\n"
        "  \"id\": \"page_id\",\n"
        "  \"pageNumber\": number,\n"
        "  \"type\": \"page type\",\n"
        "  \"headline\": \"...\",\n"
        "  \"subheadline\": \"...\",\n"
        "  \"body\": \"...\",\n"
        "  \"smallNote\": \"...\",\n"
        "  \"layout\": \"...\",\n"
        "  \"imageRole\": \"...\",\n"
        "  \"imageUrl\": \"...\",\n"
        "  \"accent\": \"...\",\n"
        "  \"textAlign\": \"...\",\n"
        "  \"density\": \"...\",\n"
        "  \"logoPosition\": \"...\"\n"
        "}"
    )
    
    candidate_models = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest'
    ]
    
    for model_name in candidate_models:
        try:
            print(f"Regenerating page {page_index} using: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([system_instruction])
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Model {model_name} failed for page regen: {e}")
            continue
            
    # Fallback: simple text enhancement
    page_to_regen["headline"] = page_to_regen.get("headline", "") + " ✨"
    page_to_regen["body"] = page_to_regen.get("body", "") + "\n(Regenerated copy details)"
    return page_to_regen

if __name__ == "__main__":

    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)