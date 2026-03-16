import streamlit as st
import markdown
from bs4 import BeautifulSoup
import base64
import os

# --- 1. SETUP ---
st.set_page_config(page_title="XYLAB Studio", layout="wide", page_icon="🎀")

# Asset Reference: loopy_asset.png
LOOPY_PATH = "loopy_asset.png"

@st.cache_data
def get_loopy_b64(path):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

LOOPY_B64 = get_loopy_b64(LOOPY_PATH)
LOOPY_DATA_URI = f"data:image/png;base64,{LOOPY_B64}" if LOOPY_B64 else ""

# State Persistence
if "converted_html" not in st.session_state:
    st.session_state.converted_html = ""

# --- 2. STYLE ENGINE (STRICT) ---
STYLES = {
    "card": "width: 100%; margin: 0 auto; background: #FFFFFF; padding: 40px 25px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.05); font-family: 'Helvetica Neue', Arial, sans-serif;",
    "h2": "font-size: 28px; font-weight: bold; color: #1A1A1A; line-height: 1.3; margin: 40px 0 20px 0; text-align: left;",
    "h3": "font-size: 18px; font-weight: bold; color: #FEC5D2; border-top: 1px solid #F0F0F0; padding-top: 20px; margin-top: 35px; letter-spacing: 2px;",
    "p": "font-size: 16px; line-height: 2.0; color: #444444; letter-spacing: 0.8px; margin: 20px 0; text-align: justify;",
    "strong": "background: rgba(254, 197, 210, 0.3); color: #E91E63; padding: 0 4px; border-radius: 4px;",
    "divider_wrap": "text-align: center; margin-top: 50px;",
    "divider_img": "max-width: 80px; display: block; margin: 40px auto;"
}

def render_loopy_final_engine(md_text):
    # Convert Markdown
    raw_html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
    soup = BeautifulSoup(raw_html, "html.parser")

    # Apply Inline Styles
    for h2 in soup.find_all("h2"):
        h2['style'] = STYLES['h2']
    
    # H3 Auto-Numbering (01, 02...)
    for i, h3 in enumerate(soup.find_all("h3"), 1):
        prefix = f"{i:02d} "
        h3.string = prefix + h3.get_text()
        h3['style'] = STYLES['h3']
    
    for p in soup.find_all("p"):
        p['style'] = STYLES['p']
    
    for strong in soup.find_all("strong"):
        strong['style'] = STYLES['strong']

    # Images
    for img in soup.find_all("img"):
        img['style'] = "max-width: 100%; border-radius: 12px; display: block; margin: 25px auto;"

    # Loopy Signature (Center at end)
    if LOOPY_DATA_URI:
        sig_div = soup.new_tag("div", style=STYLES["divider_wrap"])
        sig_img = soup.new_tag("img", src=LOOPY_DATA_URI, style=STYLES["divider_img"])
        sig_div.append(sig_img)
        soup.append(sig_div)
    
    return f'<div style="{STYLES["card"]}">{soup.decode_contents()}</div>'

# --- 3. UI ARCHITECTURE (Side-by-Side) ---
st.title("🎀 XYLAB Contents Editor")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Editor")
    # Bind text_area to session_state with key="md_input_val" for persistence
    md_in = st.text_area(
        "Editor", 
        height=600, 
        key="md_input_val", 
        label_visibility="collapsed",
        placeholder="## Focus Study\n\n**Concentration** is the bridge between goals and accomplishment."
    )
    
    if st.button("🚀 Convert to XYLAB Style", use_container_width=True):
        if md_in.strip():
            st.session_state.converted_html = render_loopy_final_engine(md_in)
        else:
            st.error("Please enter some text on the left first.")

with col2:
    # Preview-First Workflow
    if st.session_state.converted_html:
        # Live Preview at the TOP
        st.markdown("#### ✨ Live Preview")
        st.components.v1.html(st.session_state.converted_html, height=750, scrolling=True)
        
        st.divider()
        
        # HTML Block in an Expander (Hidden for Copying)
        with st.expander("📋 Show HTML Code for Copying"):
            st.code(st.session_state.converted_html, language="html")
            st.success("👆 Copy this code and paste into your WeChat MP Editor.")
    else:
        st.info("The Loopy-fied preview and copy-block will appear here after conversion.")
        if LOOPY_DATA_URI:
            st.markdown(f'<div style="text-align:center;padding:120px 0;"><img src="{LOOPY_DATA_URI}" style="width:100px;opacity:0.2;"></div>', unsafe_allow_html=True)

# sidebar brand Companion
with st.sidebar:
    st.title("XYLAB x Loopy")
    if LOOPY_DATA_URI:
        st.image(LOOPY_DATA_URI, width=60)
    st.markdown("---")
    st.info("Stable focus on magazine-grade layout.")
