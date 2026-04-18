# ไทยอักษร · Thai Text Extractor

> เครื่องมือสกัดข้อความภาษาไทยจาก PDF/PNG/JPG สำหรับนักแปลมืออาชีพ  
> Thai OCR + NLP pipeline → CAT-ready CSV output

---

## ✨ Features

| Feature | Details |
|---|---|
| 📄 **File Support** | PDF, PNG, JPG, JPEG, WEBP, TIFF, BMP |
| 🔤 **Thai Normalization** | สระไม่ลอย, แก้ OCR misread, NFC unicode |
| 📝 **Segment Export** | CSV พร้อม ID สำหรับ CAT Tools (OmegaT, memoQ, Trados) |
| 📚 **Glossary Extraction** | สกัดคำที่พบซ้ำบ่อยอัตโนมัติด้วย PyThaiNLP |
| 🌐 **Web UI** | Editorial design, drag-and-drop upload |
| ⬇️ **Download** | segments.csv + glossary.csv (UTF-8 BOM) |

---

## 🚀 Quick Start (1 นาที!)

**ไม่ต้องลง Tesseract หรือ Poppler**

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/thai-text-extractor.git
cd thai-text-extractor

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download PyThaiNLP corpus (first time only)
python -c "import pythainlp; pythainlp.corpus.download('best')"

# 5. Run!
python app.py

# ✨ Open: http://localhost:5000
```

---

## ✨ Features (Built-in)

- ✅ **PDF Text Extraction** (ไม่ต้องลง Tesseract)
- ✅ **Thai Text Normalizer** (สระไม่ลอย, แก้ Unicode)
- ✅ **Segment Splitter** (แบ่งประโยค)
- ✅ **Glossary Extractor** (คำซ้ำบ่อย)
- ✅ **CAT-ready CSV Export** (สำหรับ OmegaT, memoQ, Trados)
- ✅ **Beautiful Web UI** (Editorial Design)

---

## 📸 ต้องการ OCR (PNG/JPG/Scanned PDF)?

ใช้ **Google Cloud Vision API** (ดีกว่า Tesseract มาก!)

👉 ดูรายละเอียด → **`CLOUD_SETUP.md`**

---

## 📂 Project Structure

```
thai-text-extractor/
├── app.py                  # Flask backend + Thai NLP pipeline
├── templates/
│   └── index.html          # Web UI
├── uploads/                # Temp upload storage (auto-created)
├── outputs/                # Generated CSV files (auto-created)
├── requirements.txt
└── README.md
```

---

## 🔧 How It Works

### Text Extraction Pipeline

```
Input File (PDF/IMG)
       │
       ▼
┌──────────────────┐
│  File Type Check │
└────────┬─────────┘
         │
    ┌────▼──────────────────────┐
    │ PDF → PyMuPDF text layer  │
    │       (if has Thai text)  │
    │       else → page render  │
    │       + Tesseract OCR     │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │   Image → Tesseract OCR   │
    │   lang: tha+eng, psm 6    │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │  Thai Text Normalizer     │
    │  - NFC unicode            │
    │  - Fix ํา → ำ (sara am)  │
    │  - Fix เเ → แ (sara ae)  │
    │  - Remove ZWJ/ZWNJ        │
    │  - Dedupe tone marks      │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │  Segment Splitter         │
    │  (sentence boundary)      │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │  Glossary Extractor       │
    │  PyThaiNLP newmm tokenizer│
    │  → Counter → top N        │
    └────────────┬──────────────┘
                 │
         ┌───────┴────────┐
         ▼                ▼
   segments.csv      glossary.csv
   (CAT import)      (term base)
```

### CSV Format — segments.csv

```csv
"ID","Source (TH)","Target","Notes"
"doc_0001","ข้อความภาษาไทย","",""
"doc_0002","ประโยคที่สอง","",""
```

### CSV Format — glossary.csv

```csv
"Term (TH)","Frequency","Translation","Notes"
"สินค้า",42,"",""
"ราคา",38,"",""
```

---

## ⚙️ Configuration

Edit top of `app.py` to tune:

```python
# Glossary settings
top_n    = 50    # max glossary terms
min_len  = 2     # min character length of term
min_freq = 2     # min occurrences to include
```

---

## 🛠️ CAT Tool Import Guide

### OmegaT
1. Create project → set source language: `th`
2. Import segments.csv as TMX or copy text
3. Import glossary.csv via **Glossary → Edit Glossary**

### memoQ
1. **Import** → CSV → map columns to Source / Target
2. Glossary: **Term Base** → Import → CSV

### SDL Trados
1. **Open Package** → import bilingual CSV
2. Termbase: **SDL MultiTerm** → import CSV → map fields

---

## 🧩 Dependencies

| Package | Purpose |
|---|---|
| Flask | Web framework |
| flask-cors | Cross-origin requests |
| PyMuPDF (fitz) | PDF text extraction + render |
| pytesseract | Tesseract OCR wrapper |
| Pillow | Image processing |
| pdf2image | PDF → image for OCR fallback |
| pythainlp | Thai tokenization + corpus |

---

## 📝 License

MIT License — free for commercial and personal use.

---

## 🤝 Contributing

PRs welcome! Ideas:
- [ ] Batch upload (multiple files)
- [ ] Translation Memory (TM) matching
- [ ] Named entity recognition (NER) for Thai
- [ ] Export to XLIFF / TMX format
- [ ] Docker container
