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

# --- Style System (AURA CORE v2.1 - Floating Gallery) ---
STYLES = {
    "card": "width: 100%; max-width: 500px; margin: 0 auto; background: #FFFFFF; padding: 60px 8% 60px 12%; border-radius: 0; box-shadow: 0 30px 60px rgba(0,0,0,0.03); font-family: 'Helvetica Neue', Arial, sans-serif; border: 0;",
    "h2": "font-size: 28px; font-weight: bold; color: #1A1A1A; line-height: 1.3; margin: 40px 0 24px 0; text-align: left;",
    "h3": "font-size: 18px; font-weight: bold; color: #FEC5D2; border-top: 1px solid #F0F0F0; padding-top: 24px; margin-top: 45px; letter-spacing: 2px;",
    "p": "font-size: 16px; line-height: 2.0; color: #444444; letter-spacing: 0.8px; margin: 0 0 2.5em 0; text-align: justify; text-indent: 0;",
    "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px;",
    "divider_wrap": "text-align: center; margin-top: 60px;",
    "divider_img": "max-width: 80px; display: block; margin: 40px auto;"
}

def render_aura_engine(md_text):
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
    soup = BeautifulSoup(raw_html, "html.parser")

    for h2 in soup.find_all("h2"):
        h2['style'] = STYLES['h2']
    
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        num = f"{i:02d} "
        h3.string = num + h3.get_text()
        h3['style'] = STYLES['h3']
    
    for p in soup.find_all("p"):
        p['style'] = STYLES['p']
    
    for strong in soup.find_all("strong"):
        strong['style'] = STYLES['strong']

    for img in soup.find_all("img"):
        img['style'] = "max-width: 100%; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); display: block; margin: 25px auto;"

    if LOOPY_DATA_URI:
        sig_div = soup.new_tag("div", style=STYLES["divider_wrap"])
        sig_img = soup.new_tag("img", src=LOOPY_DATA_URI, style=STYLES["divider_img"])
        sig_div.append(sig_img)
        soup.append(sig_div)
    
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
