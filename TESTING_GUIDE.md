# 🧪 TEST VA ISHGA TUSHIRISH BO'YICHA TO'LIQ YO'RIQNOMA

## ⚡ TEZKOR ISHGA TUSHIRISH (5 DAQIQA)

### Windows foydalanuvchilari uchun:

1. **PowerShell yoki CMD ochib, loyiha papkasiga o'ting:**
```powershell
cd "d:\Projects\oshhona tizimi"
```

2. **Avtomatik setup skriptini ishga tushiring:**
```powershell
setup.bat
```

3. **Serverni ishga tushiring:**
```powershell
run.bat
```

4. **Brauzerda oching:**
```
http://localhost:8000
```

✅ **TAYYOR!** Tizim ishga tushdi!

---

## 📋 QADAMMA-QADAM O'RNATISH

### Boshlash Talablari

Quyidagilar o'rnatilgan bo'lishi kerak:
- ✅ Python 3.8 yoki yuqori ([python.org](https://python.org))
- ✅ pip (Python bilan birga keladi)
- ✅ Git (ixtiyoriy)

**Python versiyasini tekshirish:**
```bash
python --version
# yoki
python3 --version
```

### 1-Qadam: Virtual Muhit Yaratish

```bash
# Virtual muhit yaratish
python -m venv venv

# Aktivlashtirish (Windows)
venv\Scripts\activate

# Aktivlashtirish (Linux/Mac)
source venv/bin/activate
```

✅ **Muvaffaqiyatli:** Terminalda `(venv)` ko'rinishi kerak

### 2-Qadam: Kerakli Paketlarni O'rnatish

```bash
pip install -r requirements.txt
```

**O'rnatilayotgan paketlar:**
- Django 4.2.9
- Pillow 10.1.0
- qrcode 7.4.2
- python-dateutil 2.8.2

⏱️ **Vaqt:** ~2-3 daqiqa

### 3-Qadam: Ma'lumotlar Bazasini Yaratish

```bash
# Migratsiya fayllarini yaratish
python manage.py makemigrations

# Ma'lumotlar bazasini yaratish
python manage.py migrate
```

✅ **Natija:** `db.sqlite3` fayli paydo bo'ladi

### 4-Qadam: Namunaviy Ma'lumotlarni Yuklash

```bash
python manage.py populate_sample_data
```

**Yaratiladi:**
- 👤 3 ta foydalanuvchi (admin, kitchen, waiter)
- 📁 5 ta kategoriya
- 🍽️ 20+ ta menyu elementi
- 🪑 25 ta stol (3 etaj)

**Foydalanuvchilar:**
| Username | Parol | Rol |
|----------|-------|-----|
| admin | admin123 | Administrator |
| kitchen | kitchen123 | Oshxona xodimi |
| waiter | waiter123 | Ofitsant |

### 5-Qadam: QR Kodlarni Generatsiya Qilish

```bash
python manage.py generate_qr_codes
```

**Natija:** 
- `media/qr_codes/` papkasida 25 ta QR kod PNG fayl

### 6-Qadam: Static Fayllarni Yig'ish

```bash
python manage.py collectstatic --noinput
```

### 7-Qadam: Serverni Ishga Tushirish

```bash
python manage.py runserver
```

✅ **Muvaffaqiyatli!** Server ishlamoqda: `http://127.0.0.1:8000/`

---

## 🧪 TIZIMNI TEST QILISH

### Test 1: Bosh Sahifa
```
URL: http://localhost:8000/
```
**Kutilgan natija:** Bosh sahifa ochiladi, 3 ta karta ko'rinadi

---

### Test 2: Admin Panel

```
URL: http://localhost:8000/admin/
Login: admin / admin123
```

**Test qilinadigan funksiyalar:**
1. ✅ Login sahifasi ochiladi
2. ✅ Admin dashboard ko'rinadi
3. ✅ Categories bo'limiga kirish
4. ✅ Menu Items ro'yxati
5. ✅ Tables ro'yxati va QR kodlar
6. ✅ Sessions va Orders

**Test script:**
```
1. Admin panelga kiring
2. "Menu Items" ga bosing
3. Yangi taom qo'shing:
   - Name: Test Taom
   - Category: Osh va suyuq taomlar
   - Price: 15000
   - Save
4. Taom ro'yxatda ko'rinishini tekshiring
```

---

### Test 3: Mijoz Interfeysi (QR Menu)

```
URL: http://localhost:8000/menu/?table=5
```

**Test qilinadigan funksiyalar:**
1. ✅ Menyu sahifasi ochiladi
2. ✅ Stol raqami ko'rinadi (Stol #5)
3. ✅ Kategoriyalar filteri ishlaydi
4. ✅ Taomlarni ko'rish mumkin
5. ✅ Miqdor oshirish/kamaytirish (+/-)
6. ✅ "Savatga qo'shish" tugmasi ishlaydi
7. ✅ Savat hisoblagichi yangilanadi

**Test script:**
```
1. /menu/?table=5 ga o'ting
2. "Osh" taomini toping
3. Miqdorni 2 ga o'zgartiring
4. "Savatga qo'shish" bosing
5. "Savat (2)" ko'rinishini tekshiring
6. Savat tugmasini bosing
```

---

### Test 4: Savat (Cart)

```
URL: http://localhost:8000/cart/?table=5
```

**Test qilinadigan funksiyalar:**
1. ✅ Qo'shilgan taomlar ko'rinadi
2. ✅ Miqdorni o'zgartirish mumkin
3. ✅ O'chirish tugmasi ishlaydi
4. ✅ Jami summa to'g'ri hisoblanadi
5. ✅ "Buyurtma berish" tugmasi ishlaydi

**Test script:**
```
1. Savatda 2 ta Osh borligini tekshiring
2. Miqdorni 3 ga oshiring
3. Jami: 75,000 so'm bo'lishini tekshiring
4. "Buyurtma berish" bosing
5. "Buyurtma muvaffaqiyatli qabul qilindi" xabari
```

---

### Test 5: Hisob (Bill)

```
URL: http://localhost:8000/bill/?table=5
```

**Test qilinadigan funksiyalar:**
1. ✅ Buyurtmalar ro'yxati
2. ✅ Har bir taom statusi (pending/cooking/done)
3. ✅ Jami summa to'g'ri
4. ✅ "Qo'shimcha buyurtma berish" tugmasi
5. ✅ "Chop etish" tugmasi

---

### Test 6: Oshxona Paneli

```
URL: http://localhost:8000/kitchen/
Login: kitchen / kitchen123
```

**Test qilinadigan funksiyalar:**
1. ✅ Login sahifasi
2. ✅ Dashboard ochiladi
3. ✅ Yangi buyurtmalar ko'rinadi
4. ✅ "Boshlash" tugmasi (pending → cooking)
5. ✅ "Tayyor" tugmasi (cooking → done)
6. ✅ Auto-refresh (10 soniya)

**Test script:**
```
1. Kitchen panelga kiring
2. "Kutilmoqda" bo'limida buyurtmani toping
3. "Boshlash" tugmasini bosing
4. Buyurtma "Tayyorlanmoqda" ga o'tdi
5. "Tayyor" tugmasini bosing
6. Buyurtma "Tayyor" ga o'tdi
```

---

### Test 7: Ofitsant Paneli

```
URL: http://localhost:8000/waiter/
Login: waiter / waiter123
```

**Test qilinadigan funksiyalar:**
1. ✅ Barcha stollar ko'rinadi
2. ✅ Faol stollar ajralib turadi
3. ✅ Har bir stolning summasi
4. ✅ "Ko'rish" tugmasi - session details
5. ✅ "Yopish" tugmasi - sessiyani yopish

**Test script:**
```
1. Waiter panelga kiring
2. Stol #5 ni toping (faol)
3. "Ko'rish" tugmasini bosing
4. Session detailsda buyurtmalarni ko'ring
5. "To'lov qabul qilish" bosing
6. To'lov turini tanlang: Naqd
7. Summani kiriting: 75000
8. "Tasdiqlash" bosing
9. "Sessiyani yopish" bosing
```

---

## 📊 LOAD TESTING (Yuklanishni test qilish)

### Bir vaqtda ko'p foydalanuvchilar

**Test 1: 10 ta tab ochish**
```
1. Brauzerda 10 ta yangi tab oching
2. Har birida turli stol raqamlari:
   - /menu/?table=1
   - /menu/?table=2
   - ...
   - /menu/?table=10
3. Har birida taom qo'shing va buyurtma bering
```

**Kutilgan natija:**
- ✅ Barcha tablar normal ishlaydi
- ✅ Buyurtmalar oshxonaga tushadi
- ✅ Savat har bir tab uchun alohida

---

## 🐛 DEBUGGING (Xatolarni tuzatish)

### Umumiy xatolar va yechimlar

#### 1. Import Error
```
ERROR: No module named 'django'
```
**Yechim:**
```bash
pip install -r requirements.txt
```

#### 2. Database Error
```
ERROR: no such table: restaurant_category
```
**Yechim:**
```bash
python manage.py migrate
```

#### 3. Static Files 404
```
ERROR: GET /static/css/... 404
```
**Yechim:**
```bash
python manage.py collectstatic --noinput
```

#### 4. Port Already in Use
```
ERROR: Port 8000 already in use
```
**Yechim:**
```bash
python manage.py runserver 8080
```

#### 5. Permission Denied
```
ERROR: Permission denied
```
**Yechim:**
```bash
# Windows: Administrator sifatida ishga tushiring
# Linux/Mac:
sudo python manage.py runserver
```

---

## 🔍 LOG VA MONITORING

### Django Development Server Logs

Serverdan keladigan loglarni kuzating:
```bash
python manage.py runserver
```

**Kutilgan loglar:**
```
[30/Dec/2025 10:00:00] "GET /menu/?table=5 HTTP/1.1" 200 15234
[30/Dec/2025 10:00:05] "POST /order/submit/ HTTP/1.1" 200 89
[30/Dec/2025 10:00:10] "GET /kitchen/ HTTP/1.1" 200 12456
```

### Database Queries

Qancha query bajarilayotganini ko'rish:
```python
# settings.py ga qo'shing (development faqat):
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## ✅ YAKUNIY TEST CHECKLIST

Quyidagi testlarning barchasini bajaring:

### Mijoz Tizimi
- [ ] QR link orqali menyu ochiladi
- [ ] Kategoriya filtri ishlaydi
- [ ] Taomni savatga qo'shish mumkin
- [ ] Savat hisoblagichi to'g'ri
- [ ] Buyurtma yuboriladi
- [ ] Hisob ko'rinadi

### Oshxona Paneli
- [ ] Login qilish mumkin
- [ ] Yangi buyurtmalar ko'rinadi
- [ ] Status o'zgartirish ishlaydi
- [ ] Auto-refresh ishlaydi
- [ ] Statistika to'g'ri

### Ofitsant Paneli
- [ ] Login qilish mumkin
- [ ] Barcha stollar ko'rinadi
- [ ] Faol sessiyalar ajralib turadi
- [ ] To'lov qabul qilish mumkin
- [ ] Sessiyani yopish ishlaydi

### Admin Panel
- [ ] Login qilish mumkin
- [ ] Kategoriya qo'shish/o'zgartirish
- [ ] Menyu elementi qo'shish/o'zgartirish
- [ ] Stol qo'shish/o'zgartirish
- [ ] QR kod ko'rinadi
- [ ] Buyurtmalar ro'yxati
- [ ] To'lovlar hisoboti

---

## 🎯 KEYINGI QADAMLAR

Testlar muvaffaqiyatli o'tgandan keyin:

1. ✅ **Production sozlamalari:**
   - DEBUG = False
   - ALLOWED_HOSTS sozlash
   - SECRET_KEY o'zgartirish
   - PostgreSQL ga o'tish

2. ✅ **Qo'shimcha xususiyatlar:**
   - WebSocket (real-time)
   - To'lov API integratsiya
   - SMS notifications
   - Email reports

3. ✅ **Deployment:**
   - VPS/Cloud server tanlash
   - Nginx konfiguratsiya
   - SSL sertifikat
   - Domain sozlash

---

## 📞 YORDAM

Agar testlarda muammo bo'lsa:

1. **Loglarni tekshiring:** Terminal/CMD output
2. **README.md ni o'qing:** To'liq hujjatlar
3. **QUICK_START.md:** Tezkor yo'riqnoma
4. **Django docs:** https://docs.djangoproject.com/

---

## ✨ OMAD!

Tizim to'liq test qilindi va ishga tayyor! 🎉

Agar barcha testlar muvaffaqiyatli o'tsa, siz tayyor production tizimga egasiz!
