import streamlit as st
import os, json
# अगर तेरे पास core file का नाम mystrogpt_v_1.py है तो यह सही रहेगा:
from mystrogpt_v_1 import MystroGPTBrain

BASE = os.path.abspath(os.path.dirname(__file__))
OUTPUTS = os.path.join(BASE, "outputs")
os.makedirs(OUTPUTS, exist_ok=True)

st.set_page_config(page_title="MystroGPT Dashboard", layout="wide")
st.title("🧠 MystroGPT — Local Dashboard")

st.sidebar.header("⚡ Actions")

# नया Topic Input
new_topic = st.sidebar.text_input("नया Topic दर्ज करें:")
if st.sidebar.button("Generate"):
    if not new_topic.strip():
        st.warning("पहले topic डालो फिर Generate दबाओ।")
    else:
        brain = MystroGPTBrain()
        with st.spinner("⏳ Generating..."):
            out = brain.run_pipeline(new_topic)
        st.success(f"✅ Output saved → {out.get('_saved_folder')}")

# Library (पुराने topics)
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Library")
folders = sorted([d for d in os.listdir(OUTPUTS) if os.path.isdir(os.path.join(OUTPUTS, d))])
sel = st.sidebar.selectbox("Select topic:", ["-- choose --"] + folders)

# Main Preview Area
if sel and sel != "-- choose --":
    sel_path = os.path.join(OUTPUTS, sel)
    st.subheader(f"Preview: {sel}")

    # Manifest
    manifest_path = os.path.join(sel_path, "manifest.json")
    if os.path.exists(manifest_path):
        st.markdown("### Manifest")
        with open(manifest_path, "r", encoding="utf-8") as f:
            st.json(json.load(f))

    # Script
    script_path = os.path.join(sel_path, "script_hindi.txt")
    if os.path.exists(script_path):
        st.markdown("### 🎤 Voiceover Script (Hindi)")
        with open(script_path, "r", encoding="utf-8") as f:
            st.text_area("Script", f.read(), height=400)

    # SEO
    seo_path = os.path.join(sel_path, "seo_pack.json")
    if os.path.exists(seo_path):
        st.markdown("### 🔎 SEO Pack")
        with open(seo_path, "r", encoding="utf-8") as f:
            st.write(json.load(f))

    # Shorts
    shorts_path = os.path.join(sel_path, "shorts.json")
    if os.path.exists(shorts_path):
        st.markdown("### 🎬 Shorts")
        with open(shorts_path, "r", encoding="utf-8") as f:
            st.table(json.load(f))

    # Thumbnail
    thumb_path = os.path.join(sel_path, "thumbnail_concept.json")
    if os.path.exists(thumb_path):
        st.markdown("### 🖼️ Thumbnail Concept")
        with open(thumb_path, "r", encoding="utf-8") as f:
            st.write(json.load(f))
else:
    st.info("⬅️ Left sidebar से Topic चुनो या नया generate करो।")