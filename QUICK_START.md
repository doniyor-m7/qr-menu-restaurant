# 🚀 TEZKOR BOSHLASH YO'RIQNOMASI

## Avtomatik O'rnatish (Tavsiya etiladi)

### Windows uchun:

1. **Loyiha papkasini oching:**
   ```
   d:\Projects\oshhona tizimi
   ```

2. **`setup.bat` faylini ikki marta bosing**
   - Avtomatik ravishda hamma narsani o'rnatadi
   - Virtual muhit yaratadi
   - Kerakli paketlarni o'rnatadi
   - Ma'lumotlar bazasini yaratadi
   - Namunaviy ma'lumotlarni yuklaydi
   - QR kodlarni generatsiya qiladi

3. **Serverni ishga tushirish:**
   - `run.bat` faylini ikki marta bosing
   - Yoki terminal ochib:
   ```bash
   venv\Scripts\activate
   python manage.py runserver
   ```

4. **Brauzerda oching:**
   ```
   http://localhost:8000
   ```

## Qo'lda O'rnatish

Agar avtomatik setup ishlamasa:

```bash
# 1. Virtual muhit yaratish
python -m venv venv

# 2. Aktivlashtirish (Windows)
venv\Scripts\activate

# 3. Paketlarni o'rnatish
pip install -r requirements.txt

# 4. Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# 5. Namunaviy ma'lumotlar
python manage.py populate_sample_data

# 6. QR kodlar
python manage.py generate_qr_codes

# 7. Static fayllar
python manage.py collectstatic --noinput

# 8. Serverni ishga tushirish
python manage.py runserver
```

## 👤 Kirish Ma'lumotlari

| Foydalanuvchi | Username | Parol | URL |
|---------------|----------|-------|-----|
| **Administrator** | admin | admin123 | http://localhost:8000/admin/ |
| **Oshxona** | kitchen | kitchen123 | http://localhost:8000/kitchen/ |
| **Ofitsant** | waiter | waiter123 | http://localhost:8000/waiter/ |

## 📱 Test Qilish

### 1. Mijoz tizimi (QR Menu)
```
http://localhost:8000/menu/?table=5
```
- Taomlarni ko'rish
- Savatga qo'shish
- Buyurtma berish

### 2. Oshxona paneli
```
http://localhost:8000/kitchen/
```
- Login: kitchen / kitchen123
- Yangi buyurtmalarni ko'rish
- Statusni o'zgartirish

### 3. Ofitsant paneli
```
http://localhost:8000/waiter/
```
- Login: waiter / waiter123
- Stollarni boshqarish
- To'lovlarni qabul qilish

### 4. Admin panel
```
http://localhost:8000/admin/
```
- Login: admin / admin123
- Menyu boshqaruvi
- Stollar va QR kodlar
- Hisobotlar

## 🔍 QR Kodlar

QR kodlar avtomatik generatsiya qilinadi va saqlanadi:
```
media/qr_codes/
```

Har bir stol uchun:
- `table_1_qr.png`
- `table_2_qr.png`
- va hokazo...

## 📊 Ma'lumotlar Bazasi

SQLite fayli:
```
db.sqlite3
```

Tozalash va qayta yuklash:
```bash
python manage.py populate_sample_data --clear
```

## ❗ Muammolar

### Import xatosi
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Portni o'zgartirish
```bash
python manage.py runserver 8080
```

### Ma'lumotlar bazasini tiklash
```bash
del db.sqlite3
python manage.py migrate
python manage.py populate_sample_data
```

## 📞 Yordam

Agar muammolar bo'lsa:
1. `setup.bat` faylini qayta ishga tushiring
2. Terminal/CMD da xatolarni o'qing
3. Python versiyasini tekshiring: `python --version` (3.8+)
4. README.md faylini o'qing

## ✅ Tekshirish Ro'yxati

- [ ] Python 3.8+ o'rnatilgan
- [ ] pip ishlamoqda
- [ ] Virtual muhit yaratildi
- [ ] Paketlar o'rnatildi (requirements.txt)
- [ ] Migratsiyalar bajarildi
- [ ] Namunaviy ma'lumotlar yuklandi
- [ ] QR kodlar generatsiya qilindi
- [ ] Server ishga tushdi
- [ ] http://localhost:8000 ochiladi
- [ ] Admin panelga kirish mumkin

## 🎉 Tayyor!

Muvaffaqiyatli o'rnatildi! Endi tizimdan foydalanishingiz mumkin.

**Keyingi qadamlar:**
1. Menyu elementlarini o'zgartiring
2. Stollar sonini sozlang
3. QR kodlarni chop eting
4. Xodimlarni qo'shing
5. Real restoranda sinab ko'ring!

---
**Omad!** 🍽️
