# ☁️ Cloud Vision API Setup (ไม่ต้องติดตั้ง Tesseract)

## วิธี 1: Google Cloud Vision API (แนะนำ)

Google Vision OCR ดีกว่า Tesseract มาก สำหรับภาษาไทย!

### Step 1: สร้าง Google Cloud Project

1. ไปที่ https://console.cloud.google.com
2. Sign in ด้วย Google account
3. **Create Project** → ตั้งชื่อ (เช่น `thai-ocr`)
4. รอสักแป

### Step 2: Enable Vision API

1. ค้นหา **"Vision API"** ใน search bar
2. Click → **Enable**
3. รอ 30 วินาที

### Step 3: สร้าง Service Account

1. ไปที่ **IAM & Admin** → **Service Accounts**
2. **Create Service Account**:
   - Name: `thai-ocr-service`
   - Click **Create and Continue**
3. ให้ role **"Editor"** (หรือ "Cloud Vision API User")
4. **Continue** → **Done**

### Step 4: สร้าง Key

1. Click service account ที่เพิ่งสร้าง
2. ไปที่ **Keys** tab
3. **Add Key** → **Create new key**
4. เลือก **JSON** → **Create**
5. File `xxx-key.json` ดาวน์โหลดมา

### Step 5: ตั้ง Environment Variable

**macOS/Linux:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/xxx-key.json"
```

**Windows:**
```bash
set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\xxx-key.json"
```

**Permanent (macOS/Linux):** เพิ่มใน `~/.bash_profile`:
```bash
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/xxx-key.json"' >> ~/.bash_profile
source ~/.bash_profile
```

### Step 6: Install Python Package

```bash
pip install google-cloud-vision
```

### Step 7: Test

```bash
python -c "from google.cloud import vision; print('✅ Google Vision ready')"
```

---

## วิธี 2: AWS Textract (เลือกได้)

```bash
pip install boto3
```

Set AWS credentials:
```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="ap-southeast-1"  # Thailand
```

---

## วิธี 3: Hybrid (ใช้ Cloud + Local)

เมื่อติดตั้งอยู่แล้ว code จะ:
1. ลอง Cloud Vision ก่อน (ถ้ามี)
2. ถ้าไม่ได้ → fallback ไป Tesseract
3. ถ้าไม่มี Tesseract → error

---

## 🚀 Run ทันที (ไม่ต้องลง Tesseract!)

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/thai-text-extractor.git
cd thai_ocr_tool

# 2. Virtual env
python3 -m venv venv
source venv/bin/activate

# 3. Install (ไม่มี Tesseract)
pip install flask flask-cors pythainlp PyMuPDF google-cloud-vision

# 4. Set Google credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# 5. Run!
python app.py
# → http://localhost:5000
```

---

## 💰 Cost

**Google Vision:**
- **Free:** 1,000 requests/month
- **Paid:** $1.50 per 1,000 images (OCR)
- ถ้า upload < 30-40 ไฟล์/เดือน → ไม่มีค่า ✨

**AWS Textract:**
- **Free:** 100 pages/month
- **Paid:** $1.50 per 1,000 pages

---

## ❌ Troubleshooting

**"GOOGLE_APPLICATION_CREDENTIALS not found"**
```bash
# Check path
echo $GOOGLE_APPLICATION_CREDENTIALS
ls -la /path/to/key.json
```

**"Vision API not enabled"**
- ไปที่ https://console.cloud.google.com
- Search "Vision API"
- Click **Enable**

**"Permission denied"**
- เปิด key.json
- ตรวจสอบ `type: "service_account"`
- ให้ role เป็น "Editor" หรือ "Cloud Vision API User"

---

## ✅ เสร็จแล้ว!

ไม่ต้องลง Tesseract หรือ Poppler ก็ใช้ได้ 🎉
