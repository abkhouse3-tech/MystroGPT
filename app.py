"""
MystroGPT v1 - single-file brain (prototype)
Author: MystroGPT assistant

Purpose:
- A lightweight, extensible Python module that acts as the "v1 brain" for MystroGPT.
- Contains class-based stubs for topic understanding, Hindi script generation (simple everyday Hindi), short creation, SEO pack, thumbnail concept, and organizer.

Usage (prototype):
- This file is a starting point. Each method contains a simple placeholder implementation so you can run and iterate.
- Later, plug in real models (OpenAI/GPT calls), thumbnail image analysis (web.run), video editing hooks, and integrations with your file system or DAW.

Run:
    python mystrogpt_v1.py "topic text here"

Notes:
- Outputs are saved to an `outputs/<sanitized-topic>/` folder.
- Script text is in simple Hindi by default (see `HindiSimpleWriter` rules).
- This is a single-file starting prototype intended for rapid iteration.
"""

import os
import json
import datetime
import textwrap
import argparse
import re
import os
os.environ["PORT"] = os.getenv("PORT", "8080")

def sanitize_folder_name(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\- _]", "", s)
    s = s.replace(" ", "_")
    return s[:120]


class TopicAnalyzer:
    """Extracts core topic and angles from raw input.
    For v1 this is heuristic-based; later replace with an LLM or classifier.
    """

    def analyze(self, raw_text: str) -> dict:
        raw_text = raw_text.strip()
        title = raw_text[:200]
        # simple heuristics to pick angles
        angles = [
            "Case/Timeline",
            "Controversy",
            "Uncovered Facts",
            "What they don't want you to know",
        ]
        return {
            "title": title,
            "canonical_topic": title,
            "angles": angles,
            "raw_text": raw_text,
        }


class HindiSimpleWriter:
    """Generates a voiceover script in simple Hindi.
    v1 uses templates and heuristics to ensure accessibility.
    """

    def __init__(self, persona_name: str = "Narrator"):
        self.persona = persona_name

    def generate_script(self, topic_info: dict) -> str:
        title = topic_info.get("title")
        hook = f"देखिए... {title} — क्या सच सामने आया है या अभी भी पर्दा बाकी है?"
        body = textwrap.dedent(f"""
        पृष्ठभूमि: मैं आपको संक्षेप में बताऊंगा कि ये है क्या और इसके बड़े खिलाड़ी कौन हैं.

        Timeline:
        - शुरुआत: मुख्य घटनाएँ और समयसीमा।
        - विवाद: किन बिंदुओं पर मतभेद हैं।
        - खुलासे: जिन रिपोर्ट्स की बात कर रहा हूँ, उनका सार।

        निष्कर्ष: क्या अब हमें क्या समझना चाहिए और आगे क्या देखने वाली चीज़ें हैं?
        """
        )

        outro = "अगर आप चाहते हैं कि मैं इस्के ऊपर और गहराई से जाँच करूँ, तो बताइये।"

        script = "\n\n".join([hook, body, outro])
        # enforce simple Hindi: here it's a placeholder — later you'd run a simplifier.
        return script


class ShortExtractor:
    """From a full script, pick 3 short ideas (shorts) with timestamps / cut points.
    v1 returns rough cut suggestions (text markers). Later integrate with speech-to-text and editor markers.
    """

    def extract_shorts(self, script_text: str) -> list:
        lines = [l for l in script_text.splitlines() if l.strip()]
        shorts = []
        # pick first 3 strong sentences as short hooks
        candidates = [l.strip() for l in lines if len(l.strip()) > 20]
        for i, c in enumerate(candidates[:3]):
            shorts.append({
                "short_id": i + 1,
                "description": c[:140],
                "suggested_duration_sec": 25,
            })
        return shorts


class SEOPackager:
    """Create title variants, descriptions, and tags.
    v1 uses simple heuristics and templates tuned for YouTube.
    """

    def make_seo_pack(self, topic_info: dict) -> dict:
        title = topic_info.get("title")
        seo_titles = [
            f"{title} — सच क्या है?",
            f"{title} Explained: Timeline और सच",
            f"क्या {title} सच है? (Deep Dive)",
        ]
        description = f"वीडियो में हम {title} की पूरी timeline और विवादों का खुलासा करते हैं."
        tags = [
            "mystrogpt",
            "mystery",
            "explainers",
            re.sub(r"\W+", "", title.split()[0].lower()) if title else "topic",
        ]
        return {"titles": seo_titles, "description": description, "tags": tags}


class ThumbnailConceptor:
    """Generates a short textual concept for thumbnails (you'll later analyze trends).
    v1 gives the creative direction and suggested text overlays.
    """

    def concept(self, topic_info: dict) -> dict:
        title = topic_info.get("title")
        idea = {
            "headline": f"सच सामने आया?",
            "composition": "बाएँ: चौकाने वाली इमेज (close-up), दायाँ: बड़ा टेक्स्ट, नीचे-छोड़ा ब्रांडिंग",
            "text_overlay": ["सच क्या है?", "Timeline Revealed"],
            "color_direction": "high-contrast, bold text, cinematic shadows",
        }
        return idea


class Organizer:
    """Saves all outputs into a clean folder structure for a topic.
    """

    def __init__(self, base_dir: str = "outputs"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save(self, topic: str, payload: dict) -> str:
        folder = os.path.join(self.base_dir, sanitize_folder_name(topic))
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.datetime.utcnow().isoformat()
        manifest = {
            "topic": topic,
            "timestamp_utc": timestamp,
            "items": list(payload.keys()),
        }
        # write each item
        for k, v in payload.items():
            fn = os.path.join(folder, f"{k}.json")
            with open(fn, "w", encoding="utf-8") as f:
                json.dump(v, f, ensure_ascii=False, indent=2)
        # manifest
        with open(os.path.join(folder, "manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        return folder


class MystroGPTBrain:
    def __init__(self, persona_name: str = "MystroGPT"):
        self.analyzer = TopicAnalyzer()
        self.writer = HindiSimpleWriter(persona_name=persona_name)
        self.shorter = ShortExtractor()
        self.seo = SEOPackager()
        self.thumb = ThumbnailConceptor()
        self.org = Organizer()

    def run_pipeline(self, raw_topic_text: str) -> dict:
        # 1. Analyze topic
        topic_info = self.analyzer.analyze(raw_topic_text)
        # 2. Generate script
        script = self.writer.generate_script(topic_info)
        # 3. Extract shorts
        shorts = self.shorter.extract_shorts(script)
        # 4. Create SEO pack
        seo_pack = self.seo.make_seo_pack(topic_info)
        # 5. Thumbnail concept
        thumb = self.thumb.concept(topic_info)
        # 6. Organize and save
        payload = {
            "topic_info": topic_info,
            "script_hindi": script,
            "shorts": shorts,
            "seo_pack": seo_pack,
            "thumbnail_concept": thumb,
        }
        folder = self.org.save(topic_info.get("title", "untitled_topic"), payload)
        payload["_saved_folder"] = folder
        return payload


# --- Streamlit UI wrapper (replace your top-level argparse/demo block with this) ---
import streamlit as st

# Page config
st.set_page_config(page_title="MystroGPT", layout="wide")
st.title("MystroGPT")
st.markdown("Enter a topic and click **Run pipeline** to generate outputs (script, shorts, thumbnail concept, SEO pack, etc.).")

# Input
topic_input = st.text_input("Topic / Title", value="default topic")

if st.button("Run pipeline"):
    if not topic_input or topic_input.strip() == "":
        st.warning("Please enter a topic/title first.")
    else:
        with st.spinner("Running pipeline (this may take a minute)..."):
            try:
                # Import/create your brain — adjust if your class is in a different module
                brain = MystroGPTBrain(persona_name="MystroGPT")

                # Run pipeline (use the same signature your code expects)
                out = brain.run_pipeline(topic_input.strip())

                # Show success + where files were saved
                saved_folder = out.get("_saved_folder", "outputs/default")
                st.success(f"Done — generated outputs saved to: {saved_folder}")

                # Show available keys (filter internal/private keys)
                filtered = {k: v for k, v in out.items() if not k.startswith("__")}
                st.subheader("Generated items (preview)")
                st.json(filtered)

                # Optional: show links / quick downloads if outputs are files inside outputs/
                # Example: if your pipeline creates outputs/<folder>/script_hindi.json etc.
                try:
                    import os
                    outdir = os.path.join("outputs", saved_folder) if not os.path.isabs(saved_folder) else saved_folder
                    if os.path.exists(outdir):
                        st.write("Files in output folder:")
                        for f in sorted(os.listdir(outdir)):
                            st.write(f"- " + f)
                except Exception:
                    pass

            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                # also show traceback in expander
                import traceback
                with st.expander("Show error details"):
                    st.text(traceback.format_exc())



