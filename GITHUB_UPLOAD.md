# 📤 Step-by-Step: Upload ขึ้น GitHub

## Step 1: สร้าง GitHub Account + Repository

1. ไปที่ **https://github.com**
2. Sign Up ถ้ายังไม่มี account
3. **Create new repository**:
   - Repository name: `thai-text-extractor`
   - Description: "Thai OCR Text Extractor for Translators"
   - Public (ให้ทุกคน download ได้)
   - ❌ ไม่ต้อง tick "Initialize with README" (เรามีแล้ว)
4. Click **Create repository** → จะขึ้นคำสั่ง command

---

## Step 2: Install Git

**macOS:**
```bash
brew install git
```

**Ubuntu/Debian:**
```bash
sudo apt install git
```

**Windows:**
- ดาวน์โหลด: https://git-scm.com/download/win
- Install โดยกด Next ตลอด

---

## Step 3: ตั้งค่า Git (ครั้งแรกเท่านั้น)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

ตัวอย่าง:
```bash
git config --global user.name "Somchai Developer"
git config --global user.email "somchai@example.com"
```

---

## Step 4: Upload โปรเจกต์

### 4.1 ไปที่ folder project

```bash
cd /path/to/thai_ocr_tool
# ตัวอย่าง:
# macOS: cd ~/thai_ocr_tool
# Windows: cd C:\Users\YourName\thai_ocr_tool
```

### 4.2 Initialize Git repository

```bash
git init
git add .
git commit -m "Initial commit: Thai Text Extractor for Translators"
```

### 4.3 เพิ่ม remote URL

GitHub จะให้คำสั่ง หลังจากสร้าง repository (ดูหน้า repository):

```bash
git remote add origin https://github.com/YOUR_USERNAME/thai-text-extractor.git
git branch -M main
git push -u origin main
```

**ตัวอย่าง:**
```bash
git remote add origin https://github.com/somchai2025/thai-text-extractor.git
git branch -M main
git push -u origin main
```

### 4.4 ป้อน GitHub Credentials

ครั้งแรกจะขอ credentials:

**Option A: Personal Access Token (แนะนำ)**
1. ไปที่ GitHub Settings → **Developer settings** → **Personal access tokens**
2. Click **Generate new token**:
   - Name: `thai-ocr-upload`
   - Expiration: 90 days
   - ✅ Tick `repo` (full control of private repositories)
   - Click **Generate token**
3. Copy token → paste ใน terminal เมื่อขอ password

**Option B: ใช้ GitHub CLI (ง่ายสุด)**
```bash
# Install GitHub CLI
# macOS: brew install gh
# Ubuntu: sudo apt install gh
# Windows: choco install gh (ต้องติดตั้ง chocolatey ก่อน)

gh auth login
# เลือก GitHub.com → HTTPS → Y → paste browser link
```

---

## Step 5: ตรวจสอบ Upload สำเร็จ

ไปที่ https://github.com/YOUR_USERNAME/thai-text-extractor

ควรเห็น:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `templates/index.html`
- ✅ `README.md`
- ✅ `CLOUD_SETUP.md`
- ✅ `.gitignore`

---

## ⚡ ถ้าอยากทำแก้ไขใหม่

### Update code และ push ใหม่:

```bash
# 1. แก้ไขไฟล์
# (เช่น แก้ bug ใน app.py)

# 2. Add + Commit
git add .
git commit -m "Fix: [อธิบายว่าแก้ไขอะไร]"

# 3. Push
git push origin main
```

**ตัวอย่าง:**
```bash
git add app.py
git commit -m "Fix: Improve Thai tokenization accuracy"
git push origin main
```

---

## 🎯 สำเร็จแล้ว!

ตอนนี้ใครก็สามารถ clone repo ได้:

```bash
git clone https://github.com/YOUR_USERNAME/thai-text-extractor.git
cd thai-text-extractor
pip install -r requirements.txt
python app.py
```

---

## 🆘 Troubleshooting

**"fatal: remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/thai-text-extractor.git
```

**"Permission denied (publickey)"**
```bash
# ใช้ HTTPS แทน SSH
git remote set-url origin https://github.com/YOUR_USERNAME/thai-text-extractor.git
```

**"failed to push some refs"**
```bash
# Pull ก่อน Push
git pull origin main
git push origin main
```

**"fatal: branch 'main' does not exist"**
```bash
# ใช้ master แทน
git branch -M master
git push -u origin master
```
