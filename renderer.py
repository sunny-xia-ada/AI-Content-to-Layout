import markdown
from bs4 import BeautifulSoup
import base64
import os
import webbrowser
import subprocess

# --- CONFIGURATION ---
INPUT_FILE = "article.md"
OUTPUT_FILE = "output.html"
ASSET_FILE = "loopy_asset.png"

# --- STYLE SYSTEM (Magazine Aesthetics) ---
STYLES = {
    "body_wrapper": "background-color: #F8F8F8; padding: 60px 20px; min-height: 100vh; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center;",
    "card": "background-color: #FFFFFF; width: 100%; max-width: 650px; padding: 50px 40px; border-radius: 20px; box-shadow: 0 15px 45px rgba(0,0,0,0.06);",
    "h2": "font-size: 28px; font-weight: 800; color: #1A1A1A; line-height: 1.3; margin: 40px 0 24px 0; letter-spacing: -0.5px;",
    "h3": "font-size: 18px; font-weight: 700; color: #FEC5D2; border-top: 1px solid #F0F0F0; padding-top: 24px; margin-top: 40px; text-transform: uppercase; letter-spacing: 2px;",
    "p": "font-size: 16px; line-height: 2.0; color: #444444; letter-spacing: 1.0px; margin: 24px 0; text-align: justify; -webkit-font-smoothing: antialiased;",
    "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px; font-weight: 700;",
    "img": "width: 100%; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); margin: 35px 0;",
    "signature_wrap": "text-align: center; margin-top: 60px; padding-top: 40px; border-top: 1px solid #F5F5F5;",
    "signature_img": "max-width: 80px; height: auto;"
}

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def copy_to_clipboard(text):
    """Copies text to clipboard using pbcopy on macOS."""
    try:
        subprocess.run(['pbcopy'], input=text, encoding='utf-8')
        print("✅ HTML Code copied to clipboard!")
    except Exception as e:
        print(f"❌ Failed to copy to clipboard: {e}")

def run_renderer():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found. Please create it first.")
        return

    # 1. Read Markdown
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 2. Convert to HTML
    html_raw = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
    soup = BeautifulSoup(html_raw, "html.parser")

    # 3. Apply Styles & Logic
    # H2 Styling
    for h2 in soup.find_all("h2"):
        h2['style'] = STYLES["h2"]
    
    # H3 Auto-Numbering (01, 02...) & Styling
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        num_prefix = f"{i:02d} "
        h3.string = num_prefix + h3.get_text()
        h3['style'] = STYLES["h3"]

    # P Styling
    for p in soup.find_all("p"):
        p['style'] = STYLES["p"]

    # Strong Styling
    for strong in soup.find_all("strong"):
        strong['style'] = STYLES["strong"]

    # Image Styling
    for img in soup.find_all("img"):
        img['style'] = STYLES["img"]

    # 4. Integrate Loopy Signature
    loopy_b64 = get_base64(ASSET_FILE)
    if loopy_b64:
        sig_div = soup.new_tag("div", style=STYLES["signature_wrap"])
        sig_img = soup.new_tag("img", src=f"data:image/png;base64,{loopy_b64}", style=STYLES["signature_img"])
        sig_div.append(sig_img)
        soup.append(sig_div)

    # 5. Build Final Standalone HTML
    final_content = f"""
    <div style="{STYLES['card']}">
        {soup.decode_contents()}
    </div>
    """
    
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>XYLAB Magazine - Preview</title>
        <style>
            body {{ margin: 0; padding: 0; background-color: #F8F8F8; }}
        </style>
    </head>
    <body>
        <div style="{STYLES['body_wrapper']}">
            {final_content}
        </div>
    </body>
    </html>
    """

    # 6. Save and Automate
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✨ Successfully rendered to {OUTPUT_FILE}")
    
    # Copy to clipboard
    copy_to_clipboard(final_content) # Copying the card content only for WeChat

    # Open in browser
    webbrowser.open(f"file://{os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    run_renderer()
