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
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(title="XYLAB // SMART AGENT v7.7.3")

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

# Static Asset Resolution (Local vs Vercel)
STATIC_DIR = os.path.join(BASE_DIR, "public", "static")
if not os.path.exists(STATIC_DIR):
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
    "loopy": ["pastel", "toy"], "executive": ["architecture"], "ethereal": ["sky", "clouds"],
    "techno": ["cyberpunk"], "urban": ["street", "graffiti"], "wonyoung": ["pink", "jewelry"],
    "algorithm": ["mesh", "gradient"], "archive": ["concrete", "vintage"],
    "solidcore": ["fitness", "lime"], "bottari": ["earthy", "minimal"]
}

def smart_restructure(text):
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    final_output = []
    for p in text.split('\n\n'):
        if len(p) < 40 and not p.endswith(('.', '。')):
            final_output.append(f"## {p}")
        else:
            final_output.append(p)
    return "\n\n".join(final_output)

def auto_illustrate(text, theme_id="loopy"):
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text, flags=re.DOTALL).strip()
    tags = LOREM_TAGS.get(theme_id, ["pastel"])
    seed = random.randint(1, 999999)
    divider_url = f"https://loremflickr.com/1000/600/{random.choice(tags)}/all?lock={seed}"
    lines = text.split('\n')
    if lines: lines.insert(len(lines)//2, f"\n\n![Divider]({divider_url})\n\n")
    return "\n\n".join(lines).strip()

def render_aura_engine(md_text, theme_id="loopy"):
    theme = THEMES.get(theme_id, THEMES["loopy"])
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br', 'sane_lists'])
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in ["p", "strong", "h2", "h3", "blockquote"]:
        for el in soup.find_all(tag): el['style'] = theme.get(tag, "")
    for img in soup.find_all("img"): img['style'] = theme.get("img", "")
    return f'<div id="aura-card" style="{theme["card"]}">{soup.decode_contents()}</div>'

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def os_portal(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/wechat", response_class=HTMLResponse)
async def wechat_engine(request: Request):
    return templates.TemplateResponse(request, "wechat.html", {"loopy_uri": LOOPY_DATA_URI})

@app.get("/xhs", response_class=HTMLResponse)
async def xhs_engine(request: Request):
    return templates.TemplateResponse(request, "xhs.html", {"loopy_uri": LOOPY_DATA_URI})

@app.get("/youtube", response_class=HTMLResponse)
async def youtube_engine(request: Request):
    return templates.TemplateResponse(request, "youtube.html", {})

@app.get("/x", response_class=HTMLResponse)
async def x_engine(request: Request):
    return templates.TemplateResponse(request, "x.html", {})

@app.get("/spotify", response_class=HTMLResponse)
async def spotify_engine(request: Request):
    return templates.TemplateResponse(request, "spotify.html", {})

@app.get("/douyin", response_class=HTMLResponse)
async def douyin_engine(request: Request):
    return templates.TemplateResponse(request, "douyin.html", {})

@app.get("/meituan", response_class=HTMLResponse)
async def meituan_engine(request: Request):
    return templates.TemplateResponse(request, "meituan.html", {})

@app.post("/convert")
async def convert(markdown_input: str = Form(...), theme: str = Form("loopy")):
    return {"html": render_aura_engine(markdown_input, theme_id=theme)}

@app.post("/api/vision-magic")
async def vision_magic(request: VisionMagicRequest):
    prompt_text = request.prompt
    try:
        with DDGS() as ddgs:
            refs = list(ddgs.text(f"site:xiaohongshu.com {prompt_text[:20]}", max_results=3))
            refs_text = "\n".join([r.get('body', '') for r in refs])
    except: refs_text = "N/A"

    system_instruction = f"你是顶级小红书博主。参考：{refs_text}\n返回 JSON 结构。"
    contents = [system_instruction, f"User Prompt: {prompt_text}"]
    if request.image:
        img_data = request.image
        if ";base64," in img_data: img_data = img_data.split(";base64,")[1]
        contents.append({"mime_type": "image/jpeg", "data": base64.b64decode(img_data)})

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(contents)
        return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
    except:
        return {"copy": {"title": "HYDRATION DIVE-IN", "hook": "夏日本命!", "body": "Mock Success", "ending": "👇"}}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)