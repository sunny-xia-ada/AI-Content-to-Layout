from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from bs4 import BeautifulSoup
import base64
import os
import re
import urllib.parse

app = FastAPI(title="XYLAB // SMART LAYOUT AGENT")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Asset Reference
LOOPY_PATH = "loopy_asset.png"

def get_base64_asset(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

LOOPY_B64 = get_base64_asset(LOOPY_PATH)
LOOPY_DATA_URI = f"data:image/png;base64,{LOOPY_B64}" if LOOPY_B64 else ""

# --- Multi-Theme Engine (AURA CORE v3.0) ---
THEMES = {
    "loopy": {
        "card": "width: 100%; max-width: 500px; margin: 0 auto; background: #FFFFFF; padding: 60px 8% 60px 12%; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.03); font-family: 'Helvetica Neue', Arial, sans-serif; border: 0;",
        "h2": "font-size: 28px; font-weight: bold; color: #1A1A1A; line-height: 1.3; margin: 40px 0 24px 0; text-align: left;",
        "h3": "font-size: 18px; font-weight: bold; color: #FEC5D2; padding-top: 0; margin-top: 10px; letter-spacing: 2px;",
        "p": "font-size: 16px; line-height: 2.0; color: #444444; letter-spacing: 0.8px; margin: 0 0 2.5em 0; text-align: justify; text-indent: 0;",
        "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px;",
        "img": "max-width: 100%; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); display: block; margin: 25px auto;",
        "accent": "#FEC5D2"
    },
    "executive": {
        "card": "width: 100%; max-width: 500px; margin: 0 auto; background: #FFFFFF; padding: 60px 8% 60px 12%; border-radius: 0; box-shadow: 0 30px 60px rgba(0,0,0,0.03); font-family: 'Georgia', serif; border: 0;",
        "h2": "font-size: 26px; font-weight: bold; color: #1A1A1A; border-left: 4px solid #1A1A1A; padding-left: 15px; margin: 50px 0 30px 0;",
        "h3": "font-size: 16px; font-weight: bold; color: #5A5A5A; text-transform: uppercase; margin-top: 40px;",
        "p": "font-size: 15px; line-height: 1.8; color: #333333; margin: 0 0 2em 0; text-align: left;",
        "strong": "border-bottom: 2px solid #5A5A5A; font-weight: bold;",
        "img": "max-width: 100%; border: 1px solid #EFEFEF; box-shadow: none; display: block; margin: 30px auto;",
        "accent": "#5A5A5A"
    },
    "ethereal": {
        "card": "width: 100%; max-width: 550px; margin: 0 auto; background: rgba(255,255,255,0.9); padding: 80px 10%; border-radius: 8px; box-shadow: 0 10px 100px rgba(168, 192, 216, 0.1); font-family: 'Inter', sans-serif; border: 1px solid rgba(168, 192, 216, 0.2);",
        "h2": "font-size: 30px; color: #A8C0D8; text-align: center; font-weight: 300; margin: 60px 0 40px 0; border: 1px solid rgba(168, 192, 216, 0.3); padding: 15px;",
        "h3": "font-size: 14px; color: #A8C0D8; text-transform: uppercase; letter-spacing: 4px; text-align: center; margin-top: 50px;",
        "p": "font-size: 16px; line-height: 2.2; color: #666666; font-weight: 300; margin: 0 0 3em 0; text-align: center;",
        "strong": "color: #A8C0D8; font-weight: 600;",
        "img": "max-width: 100%; border-radius: 30px; opacity: 0.9; display: block; margin: 40px auto;",
        "accent": "#A8C0D8"
    }
}

def render_aura_engine(md_text, theme_id="loopy"):
    theme = THEMES.get(theme_id, THEMES["loopy"])
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
    soup = BeautifulSoup(raw_html, "html.parser")

    for h2 in soup.find_all("h2"):
        h2['style'] = theme['h2']
    
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        if theme_id == "loopy":
            num_span = soup.new_tag("span", style="font-family: 'Courier New', monospace; font-weight: bold; margin-right: 8px;")
            num_span.string = f"{i:02d} "
            orig_text = h3.get_text()
            h3.clear()
            h3.append(num_span)
            h3.append(orig_text)
            divider = soup.new_tag("div", style=f"border-top: 0.5px solid #E5E5E5; width: 30%; margin: 60px 0 24px 0;")
            h3.insert_before(divider)
        h3['style'] = theme['h3']
    
    for p in soup.find_all("p"):
        p['style'] = theme['p']
    
    for strong in soup.find_all("strong"):
        strong['style'] = theme['strong']

    for img in soup.find_all("img"):
        # Apply strict premium styling to all images
        img['style'] = "max-width: 100%; height: auto; display: block; margin: 30px auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);"

    # Signature logic based on theme
    if LOOPY_DATA_URI and theme_id == "loopy":
        sig_container = soup.new_tag("div", style="text-align: center; margin-top: 50px; padding-top: 40px;")
        bubble = soup.new_tag("div", style="width: 64px; height: 64px; background: #FFFFFF; border-radius: 50%; box-shadow: 0 12px 30px rgba(0,0,0,0.06); margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 1px solid #F5F5F5;")
        sig_img = soup.new_tag("img", src=LOOPY_DATA_URI, style="width: 36px; height: auto; display: block; margin: 0 auto;")
        bubble.append(sig_img)
        ts = soup.new_tag("div", style="font-size: 10px; color: #BBBBBB; letter-spacing: 3px; margin-top: 20px; font-weight: 300; text-transform: uppercase;")
        ts.string = "XYLAB // 2026"
        sig_container.append(bubble)
        sig_container.append(ts)
        soup.append(sig_container)
    elif theme_id == "executive":
        sig_container = soup.new_tag("div", style="text-align: left; margin-top: 100px; border-top: 2px solid #1A1A1A; padding-top: 20px;")
        ts = soup.new_tag("div", style="font-size: 12px; color: #1A1A1A; font-weight: bold; text-transform: uppercase; letter-spacing: 2px;")
        ts.string = "XYLAB EXECUTIVE CORE // 2026"
        sig_container.append(ts)
        soup.append(sig_container)

    return f'<div id="aura-card" style="{theme["card"]}">{soup.decode_contents()}</div>'

# --- AI Intelligence Logic ---
def smart_restructure(text):
    # Rule 1: Breathing Room (Max 3 sentences per paragraph)
    paragraphs = text.split('\n\n')
    new_paras = []
    
    for p in paragraphs:
        # Split sentences while keeping punctuation
        sentences = re.split(r'([.!?。！？])', p.strip())
        if len(sentences) > 6: # More than 3 full sentences
            chunks = []
            for i in range(0, len(sentences)-1, 6): # 2 items (sentence + punct) * 3 = 6
                chunk = "".join(sentences[i:i+6]).strip()
                if chunk: chunks.append(chunk)
            new_paras.extend(chunks)
        else:
            new_paras.append(p.strip())
    
    # Rule 2: Hierarchy (Identify lines that look like titles)
    restructured = []
    for p in new_paras:
        if len(p) < 40 and not p.endswith(('.', '。', '!', '！', '?', '？')):
            # Short lines without punctuation are likely headings
            if len(p) < 15: restructured.append(f"## {p}")
            else: restructured.append(f"### {p}")
        else:
            restructured.append(p)
    
    # Rule 3: Emphasis (Quotes to Blockquotes & Bolding)
    final_output = []
    for p in restructured:
        # Identify quotes (simplified)
        if p.startswith(('"', "'", "“", "「")) and p.endswith(('"', "'", "”", "」")):
            final_output.append(f"> {p}")
        else:
            # Auto-Bold 2nd or 3rd sentence if not a heading
            if not p.startswith('#'):
                words = p.split()
                if len(words) > 10:
                    mid = len(words) // 2
                    words[mid] = f"**{words[mid]}**"
                    if mid + 1 < len(words): words[mid+1] = f"**{words[mid+1]}**"
                    p = " ".join(words)
            final_output.append(p)
            
    return "\n\n".join(final_output)

def auto_illustrate(text):
    # Rule: Use Pollinations AI for no-auth reliable image generation
    # Extracting meaningful visual keywords
    keywords = ["minimalist", "modern", "aesthetic", "future", "luxury", "essence"]
    extracted = re.findall(r'\b[A-Za-z]{6,}\b', text)
    top_keywords = list(set(extracted))[:3] if extracted else keywords[:3]
    
    lines = text.split('\n\n')
    
    def get_pollination_url(prompt):
        encoded = urllib.parse.quote(prompt)
        return f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=500&nologo=true"

    # Injection: Hero and Divider images
    if len(lines) > 2:
        hero_prompt = f"{top_keywords[0]} luxury cinematic aesthetic"
        lines.insert(0, f"![Hero]({get_pollination_url(hero_prompt)})")
        
        if len(lines) > 5:
            mid_prompt = f"{top_keywords[1]} minimalist clean background"
            lines.insert(len(lines)//2 + 1, f"![Divider]({get_pollination_url(mid_prompt)})")
            
    return "\n\n".join(lines)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "loopy_uri": LOOPY_DATA_URI})

@app.post("/convert")
async def convert(markdown_input: str = Form(...), theme: str = Form("loopy")):
    if not markdown_input.strip():
        return {"html": ""}
    html_output = render_aura_engine(markdown_input, theme_id=theme)
    return {"html": html_output}

@app.post("/ai-process")
async def ai_process(markdown_input: str = Form(...)):
    restructured = smart_restructure(markdown_input)
    illustrated = auto_illustrate(restructured)
    return {"markdown": illustrated}

if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="0.0.0.0", port=args.port)
