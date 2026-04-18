import os
import re
import csv
import json
import uuid
import unicodedata
from io import StringIO, BytesIO
from pathlib import Path
from collections import Counter
from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import pythainlp
from pythainlp.tokenize import word_tokenize

# ✅ OPTIONAL: OCR (skip if not needed)
try:
    import fitz  # PyMuPDF - for PDF text extraction ONLY
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# ─── Thai Text Normalization ──────────────────────────────────────────────────

def normalize_thai_text(text: str) -> str:
    """
    Normalize Thai text:
    - Fix NFC unicode normalization
    - Remove stray/duplicate diacritics
    - Fix common OCR misreads
    """
    if not text:
        return text

    # NFC normalize
    text = unicodedata.normalize('NFC', text)

    # Fix common Thai misreads
    ocr_fixes = {
        'ํา': 'ำ',
        '\u0e4d\u0e32': '\u0e33',
        'เแ': 'แ',
        'เเ': 'แ',
        '่่': '่',
        '้้': '้',
        '๊๊': '๊',
        '๋๋': '๋',
        '็็': '็',
    }
    for wrong, right in ocr_fixes.items():
        text = text.replace(wrong, right)

    # Remove zero-width chars
    text = text.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    text = text.replace('\ufeff', '')

    # Collapse multiple spaces/newlines
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def split_into_segments(text: str) -> list[str]:
    """Split normalized Thai text into translation segments."""
    pattern = re.compile(
        r'(?<=[ๆ\.\!\?\u0e2f\u0e5a\u0e5b])\s+'
        r'|(?<=\n)'
        r'|\n'
    )
    raw = pattern.split(text)
    segments = []
    for seg in raw:
        seg = seg.strip()
        if seg and len(seg) > 1:
            segments.append(seg)
    return segments


def extract_glossary(segments: list[str], top_n: int = 50, min_len: int = 2, min_freq: int = 2) -> list[dict]:
    """Extract frequently repeated Thai words/phrases."""
    thai_char = re.compile(r'[\u0e00-\u0e7f]')
    all_tokens = []
    
    for seg in segments:
        tokens = word_tokenize(seg, engine='newmm', keep_whitespace=False)
        for tok in tokens:
            tok = tok.strip()
            if (len(tok) >= min_len
                    and thai_char.search(tok)
                    and tok not in ('ๆ', 'ฯ', 'และ', 'หรือ', 'ใน', 'ที่', 'ของ', 'การ',
                                     'ให้', 'เป็น', 'ได้', 'จาก', 'โดย', 'มี', 'กับ')):
                all_tokens.append(tok)

    freq = Counter(all_tokens)
    glossary = [
        {"term": term, "frequency": count, "translation": ""}
        for term, count in freq.most_common(top_n)
        if count >= min_freq
    ]
    return glossary


# ─── PDF Text Extraction (NO OCR needed) ──────────────────────────────────────

def extract_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF - text layer only (no OCR)."""
    if not PYMUPDF_AVAILABLE:
        raise RuntimeError("PyMuPDF not installed. Install: pip install PyMuPDF")

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text_parts = []

    for page in doc:
        text = page.get_text("text")
        if text.strip():
            full_text_parts.append(text)

    doc.close()
    return "\n\n".join(full_text_parts)


# ─── CSV Generation ───────────────────────────────────────────────────────────

def segments_to_csv(segments: list[str], filename: str) -> str:
    """Generate CAT-tool-ready CSV from segments."""
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["ID", "Source (TH)", "Target", "Notes"])
    for i, seg in enumerate(segments, 1):
        writer.writerow([f"{filename}_{i:04d}", seg, "", ""])
    return output.getvalue()


def glossary_to_csv(glossary: list[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["Term (TH)", "Frequency", "Translation", "Notes"])
    for item in glossary:
        writer.writerow([item["term"], item["frequency"], item["translation"], ""])
    return output.getvalue()


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    try:
        with open("templates/index.html", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({"error": "index.html not found"}), 404


@app.route("/api/extract", methods=["POST"])
def extract():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No filename provided"}), 400
    
    filename = file.filename
    ext = Path(filename).suffix.lower()
    file_bytes = file.read()
    
    if not file_bytes:
        return jsonify({"error": "Empty file"}), 400

    try:
        if ext == ".pdf":
            raw_text = extract_from_pdf(file_bytes)
        else:
            return jsonify({
                "error": f"❌ This version supports PDF only. For PNG/JPG, install Google Cloud Vision API. See CLOUD_SETUP.md"
            }), 400

        if not raw_text.strip():
            return jsonify({
                "error": "No text found in PDF. Try uploading a text-based PDF (not scanned)."
            }), 400

        normalized = normalize_thai_text(raw_text)
        segments = split_into_segments(normalized)
        
        if not segments:
            return jsonify({
                "error": "No Thai text segments found after processing."
            }), 400
        
        glossary = extract_glossary(segments)

        # Save files
        session_id = str(uuid.uuid4())[:8]
        base_name = Path(filename).stem

        seg_csv = segments_to_csv(segments, base_name)
        glo_csv = glossary_to_csv(glossary)

        seg_path = OUTPUT_FOLDER / f"{session_id}_segments.csv"
        glo_path = OUTPUT_FOLDER / f"{session_id}_glossary.csv"

        seg_path.write_text(seg_csv, encoding="utf-8-sig")
        glo_path.write_text(glo_csv, encoding="utf-8-sig")

        return jsonify({
            "session_id": session_id,
            "filename": filename,
            "raw_preview": normalized[:2000],
            "segment_count": len(segments),
            "segments": segments[:100],
            "glossary": glossary[:30],
            "seg_csv_id": session_id,
        })

    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500


@app.route("/api/download/segments/<session_id>")
def download_segments(session_id):
    path = OUTPUT_FOLDER / f"{session_id}_segments.csv"
    if not path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_file(str(path), as_attachment=True,
                     download_name="segments.csv", mimetype="text/csv")


@app.route("/api/download/glossary/<session_id>")
def download_glossary(session_id):
    path = OUTPUT_FOLDER / f"{session_id}_glossary.csv"
    if not path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_file(str(path), as_attachment=True,
                     download_name="glossary.csv", mimetype="text/csv")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "pymupdf": PYMUPDF_AVAILABLE,
        "pythainlp": True,
        "mode": "PDF Text Extraction Only (Lightweight)"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
