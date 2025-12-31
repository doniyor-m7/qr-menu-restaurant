# 🚨 MUAMMOLARNI HAL QILISH

## Eng ko'p uchraydigan xatolar va yechimlar

### 1. Permission Denied (Ruxsat rad etildi)

**Xato:**
```
Error: [Errno 13] Permission denied
```

**Yechimlar:**

#### A) Eski venv ni o'chirish
```powershell
cd "d:\Projects\oshhona tizimi"
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
python -m venv venv
```

#### B) Administrator sifatida ishga tushirish
1. PowerShell ni o'ng tugma → "Run as Administrator"
2. Keyin setup.ps1 ni ishga tushiring

#### C) Execution Policy o'zgartirish
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 2. PowerShell Script Execution

**Xato:**
```
cannot be loaded because running scripts is disabled
```

**Yechim:**
```powershell
# PowerShell da:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Keyin:
.\setup.ps1
```

---

### 3. Python topilmadi

**Xato:**
```
'python' is not recognized as an internal or external command
```

**Yechim:**
1. Python o'rnatilganligini tekshiring: https://python.org
2. PATH ga qo'shilganini tekshiring
3. Qaytadan o'rnating va "Add to PATH" ni belgilang

---

### 4. Port band

**Xato:**
```
Port 8000 already in use
```

**Yechim:**
```powershell
# Boshqa portdan ishga tushiring:
python manage.py runserver 8080

# Yoki eski jarayonni o'chiring:
Get-Process -Name python | Stop-Process -Force
```

---

### 5. Import Error

**Xato:**
```
ModuleNotFoundError: No module named 'django'
```

**Yechim:**
```powershell
# Virtual environment faollashtirilganligini tekshiring:
.\venv\Scripts\Activate.ps1

# Paketlarni qayta o'rnating:
pip install -r requirements.txt
```

---

### 6. Database Locked

**Xato:**
```
database is locked
```

**Yechim:**
```powershell
# Barcha Python jarayonlarini to'xtating:
Get-Process -Name python | Stop-Process -Force

# Database faylini o'chiring va qayta yarating:
Remove-Item db.sqlite3
python manage.py migrate
python manage.py populate_sample_data
```

---

### 7. Static Files 404

**Xato:**
```
GET /static/... 404
```

**Yechim:**
```powershell
python manage.py collectstatic --noinput
```

---

## 🔄 TO'LIQ QAYTA O'RNATISH

Agar hech narsa ishlamasa, boshidan boshlang:

```powershell
cd "d:\Projects\oshhona tizimi"

# 1. Hamma narsani tozalash
Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force media -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force staticfiles -ErrorAction SilentlyContinue

# 2. Yangi venv
python -m venv venv

# 3. Aktivlashtirish
.\venv\Scripts\Activate.ps1

# 4. Paketlar
pip install --upgrade pip
pip install -r requirements.txt

# 5. Database
python manage.py makemigrations restaurant
python manage.py migrate

# 6. Data
python manage.py populate_sample_data

# 7. QR
python manage.py generate_qr_codes

# 8. Static
python manage.py collectstatic --noinput

# 9. Run
python manage.py runserver
```

---

## 💡 MASLAHATLAR

### PowerShell vs CMD

**PowerShell ishlamasa, CMD dan foydalaning:**
1. CMD (Command Prompt) ochish
2. `cd "d:\Projects\oshhona tizimi"`
3. `setup.bat` (eski batch file)

### Virtual Environment faollashtirilganligini tekshirish

Terminal boshida `(venv)` ko'rinishi kerak:
```
(venv) PS D:\Projects\oshhona tizimi>
```

### Python versiyasini tekshirish

```powershell
python --version
# Natija: Python 3.8 yoki yuqori bo'lishi kerak
```

---

## 🆘 TEZKOR YECHIMLAR

### Eng oddiy yechim (tavsiya etiladi):

```powershell
# 1. Eski venv ni o'chirish
cd "d:\Projects\oshhona tizimi"
Remove-Item -Recurse -Force venv

# 2. Yangi setup
.\setup.ps1

# 3. Run
.\run.ps1
```

### Agar setup.ps1 ishlamasa:

```powershell
# Execution policy o'zgartirish
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Qaytadan urinish
.\setup.ps1
```

### Agar hali ham ishlamasa:

```powershell
# Qo'lda birin-ketin
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install Django Pillow qrcode python-dateutil
python manage.py migrate
python manage.py populate_sample_data
python manage.py runserver
```

---

## 📞 YORDAM

Agar bu yechimlar ishlamasa:

1. **Python versiyasini tekshiring:** `python --version`
2. **Pip versiyasini tekshiring:** `pip --version`
3. **Administrator huquqida ishlating**
4. **Antivirus ni vaqtincha o'chiring**
5. **Path nomidagi bo'shliqlarni tekshiring**

---

## ✅ TEKSHIRISH RO'YXATI

Agar muammo bo'lsa, quyidagilarni tekshiring:

- [ ] Python 3.8+ o'rnatilgan
- [ ] Python PATH ga qo'shilgan
- [ ] pip ishlayapti
- [ ] PowerShell Execution Policy to'g'ri
- [ ] Eski venv o'chirilgan
- [ ] Disk bo'sh joyi yetarli (1GB+)
- [ ] Antivirus blokirovka qilmayapti
- [ ] Administrator huquqi bor

---

## 🎯 ENG TEZKOR YECHIM

Agar hech narsa ishlamasa, quyidagi 3 ta buyruqni ishga tushiring:

```powershell
cd "d:\Projects\oshhona tizimi"
Remove-Item -Recurse -Force venv
.\setup.ps1
```

Bu 99% holatlarda ishlaydi! ✅
