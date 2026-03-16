from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
from bs4 import BeautifulSoup
import base64
import os

app = FastAPI(title="XYLAB // AURA RENDERER")

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

# --- Style System (AURA CORE v2.2 - Refined Indexing) ---
STYLES = {
    "card": "width: 100%; max-width: 500px; margin: 0 auto; background: #FFFFFF; padding: 60px 8% 60px 12%; border-radius: 0; box-shadow: 0 30px 60px rgba(0,0,0,0.03); font-family: 'Helvetica Neue', Arial, sans-serif; border: 0;",
    "h2": "font-size: 28px; font-weight: bold; color: #1A1A1A; line-height: 1.3; margin: 40px 0 24px 0; text-align: left;",
    "h3": "font-size: 18px; font-weight: bold; color: #FEC5D2; padding-top: 0; margin-top: 10px; letter-spacing: 2px;",
    "h3_divider": "border-top: 0.5px solid #E5E5E5; width: 30%; margin: 60px 0 24px 0;",
    "h3_num": "font-family: 'Courier New', Courier, monospace; font-weight: bold; margin-right: 8px;",
    "p": "font-size: 16px; line-height: 2.0; color: #444444; letter-spacing: 0.8px; margin: 0 0 2.5em 0; text-align: justify; text-indent: 0;",
    "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px;",
    "bubble_wrap": "width: 64px; height: 64px; background: #FFFFFF; border-radius: 50%; box-shadow: 0 12px 30px rgba(0,0,0,0.06); margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 1px solid #F5F5F5;",
    "sig_stamp": "text-align: center; margin-top: 50px; padding-top: 40px;",
    "timestamp": "font-size: 10px; color: #BBBBBB; letter-spacing: 3px; margin-top: 20px; font-weight: 300; text-transform: uppercase;"
}

def render_aura_engine(md_text):
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
    soup = BeautifulSoup(raw_html, "html.parser")

    for h2 in soup.find_all("h2"):
        h2['style'] = STYLES['h2']
    
    # H3 Refinement: 30% Hairline + Monospace Numbering
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        # 1. Monospace Numbering
        num_str = f"{i:02d} "
        num_span = soup.new_tag("span", style=STYLES["h3_num"])
        num_span.string = num_str
        
        orig_text = h3.get_text()
        h3.clear()
        h3.append(num_span)
        h3.append(orig_text)
        h3['style'] = STYLES['h3']
        
        # 2. Hairline Divider Injector
        divider = soup.new_tag("div", style=STYLES["h3_divider"])
        h3.insert_before(divider)
    
    for p in soup.find_all("p"):
        p['style'] = STYLES['p']
    
    for strong in soup.find_all("strong"):
        strong['style'] = STYLES['strong']

    for img in soup.find_all("img"):
        img['style'] = "max-width: 100%; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); display: block; margin: 25px auto;"

    # Signature: Floating Bubble + Timestamp
    if LOOPY_DATA_URI:
        sig_container = soup.new_tag("div", style=STYLES["sig_stamp"])
        
        # Loopy Bubble
        bubble = soup.new_tag("div", style=STYLES["bubble_wrap"])
        sig_img = soup.new_tag("img", src=LOOPY_DATA_URI, style="width: 36px; height: auto; display: block; margin: 0 auto;")
        bubble.append(sig_img)
        
        # Timestamp
        ts = soup.new_tag("div", style=STYLES["timestamp"])
        ts.string = "XYLAB // 2026"
        
        sig_container.append(bubble)
        sig_container.append(ts)
        soup.append(sig_container)
    
    return f'<div id="aura-card" style="{STYLES["card"]}">{soup.decode_contents()}</div>'

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "loopy_uri": LOOPY_DATA_URI})

@app.post("/convert")
async def convert(markdown_input: str = Form(...)):
    if not markdown_input.strip():
        return {"html": ""}
    html_output = render_aura_engine(markdown_input)
    return {"html": html_output}

if __name__ == "__main__":
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="0.0.0.0", port=args.port)
