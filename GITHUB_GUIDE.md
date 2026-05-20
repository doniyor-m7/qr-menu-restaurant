# GitHub'ga Yuklash Yo'riqnomasi

## 🚀 Loyihani GitHub'ga Yuklash

### 1-Qadam: GitHub'da Repository Yaratish

1. **GitHub'ga kiring:** https://github.com
2. **"+" belgisini bosing** (yuqori o'ng burchakda)
3. **"New repository"** ni tanlang
4. **Repository ma'lumotlarini kiriting:**
   - Repository name: `qr-menu-restaurant`
   - Description: `QR-based Restaurant & Fast-Food Ordering System`
   - Visibility: **Public** yoki **Private**
   - ❌ **README, .gitignore, license qo'shMANG** (bizda allaqachon bor)
5. **"Create repository"** tugmasini bosing

### 2-Qadam: Remote Repository Qo'shish

GitHub'dagi yangi repository sahifasida sizga buyruqlar ko'rsatiladi. Quyidagilarni bajaring:

#### Windows PowerShell:

```powershell
cd "d:\Projects\oshhona tizimi"

# GitHub username va repository nomini o'zgartiring!
git remote add origin https://github.com/YOUR_USERNAME/qr-menu-restaurant.git

# Asosiy branch nomini o'zgartirish
git branch -M main

# GitHub'ga yuklash
git push -u origin main
```

### 3-Qadam: GitHub Login

Birinchi marta push qilganda GitHub login so'raydi:

**Ikkita variant:**

#### A) Personal Access Token (Tavsiya etiladi)
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" (classic)
3. Scope: `repo` ni belgilang
4. Token yarating va nusxalang
5. Push qilganda:
   - Username: sizning GitHub username
   - Password: token (parol emas!)

#### B) GitHub CLI
```powershell
# GitHub CLI o'rnatilgan bo'lsa
gh auth login
```

### 4-Qadam: Push Qilish

```powershell
git push -u origin main
```

## 📝 Keyingi O'zgarishlar Uchun

Kelajakda o'zgarishlar kiritganda:

```powershell
# O'zgarishlarni ko'rish
git status

# Barcha o'zgarishlarni qo'shish
git add .

# Commit yaratish
git commit -m "Yangi funksiya qo'shildi"

# GitHub'ga yuklash
git push
```

## 🔒 Maxfiy Ma'lumotlarni Himoya Qilish

**MUHIM:** Quyidagi fayllar `.gitignore` da mavjud (GitHub'ga yuklanmaydi):

- `db.sqlite3` - Database
- `venv/` - Virtual environment
- `media/` - Yuklangan fayllar
- `*.pyc` - Python cache
- `.env` - Environment variables

**Production uchun:**

SECRET_KEY va boshqa maxfiy ma'lumotlarni environment variables da saqlang:

```python
# settings.py
import os
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

## 📊 Repository Tuzilishi

GitHub'da quyidagicha ko'rinadi:

```
qr-menu-restaurant/
├── .gitignore
├── README.md
├── QUICK_START.md
├── PROJECT_SUMMARY.md
├── TESTING_GUIDE.md
├── TROUBLESHOOTING.md
├── requirements.txt
├── manage.py
├── setup.bat / setup.ps1
├── run.bat / run.ps1
├── qrmenu/
├── restaurant/
├── templates/
└── static/
```

## 🎯 To'liq Namuna

```powershell
# 1. Remote qo'shish (faqat bir marta)
git remote add origin https://github.com/YOUR_USERNAME/qr-menu-restaurant.git

# 2. Branch nomini o'zgartirish
git branch -M main

# 3. Yuklash
git push -u origin main

# 4. O'zgarishlarni tekshirish
git status

# 5. Yangi commit
git add .
git commit -m "Bug fixes"
git push
```

## 🌐 GitHub Pages (Ixtiyoriy)

Static demo sahifa uchun:

1. Repository → Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → /docs yoki /root
4. Save

## 📱 GitHub Desktop (Osonroq variant)

Agar terminal qiyin bo'lsa:

1. **GitHub Desktop yuklab oling:** https://desktop.github.com/
2. **File → Add Local Repository**
3. **Publish repository** tugmasini bosing
4. Keyingi o'zgarishlar uchun GUI orqali commit va push qiling

## ✅ Tayyor!

Sizning loyihangiz endi GitHub'da! 

**Repository URL:**
```
https://github.com/YOUR_USERNAME/qr-menu-restaurant
```

**Clone qilish (boshqa kompyuterda):**
```powershell
git clone https://github.com/YOUR_USERNAME/qr-menu-restaurant.git
cd qr-menu-restaurant
.\setup.ps1
```

## 🆘 Muammolar

**"remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/qr-menu-restaurant.git
```

**"Permission denied"**
- Personal Access Token ishlatilganligini tekshiring
- Token `repo` scopega ega bo'lishi kerak

**"rejected - non-fast-forward"**
```powershell
git pull origin main --rebase
git push origin main
```

---

**Omad!** 🎉
