# api.py (lazy import safe version)
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import importlib

app = Flask(__name__)
CORS(app)

def get_generate_callable():
    """
    Try to import a generate() function from app.py (or another module).
    Import is done lazily to avoid Streamlit running at import time.
    Returns callable or None.
    """
    try:
        mod = importlib.import_module("app")
        gen = getattr(mod, "generate", None)
        if callable(gen):
            return gen
    except Exception:
        # import failed (probably because app.py runs Streamlit UI on import)
        return None
    return None

def fallback_generate(prompt: str):
    return {"title": "MystroGPT (local - placeholder)", "text": f"Processed prompt (placeholder): {prompt}"}

@app.route("/run", methods=["POST"])
def run_route():
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "")
        generate_fn = get_generate_callable()
        if generate_fn:
            try:
                out = generate_fn(prompt)
            except Exception:
                return jsonify({"ok": False, "error": "generate() failed", "trace": traceback.format_exc()}), 500
        else:
            out = fallback_generate(prompt)

        if isinstance(out, str):
            out = {"title": "Result", "text": out}
        return jsonify({"ok": True, "result": out})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
