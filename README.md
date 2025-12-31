# QR Menu - Restaurant & Fast-Food Ordering System

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

Zamonaviy restoran va tez ovqatlanish joylar uchun QR-kod asosida buyurtma boshqaruv tizimi.

## 🎯 Xususiyatlar

### Mijozlar uchun
- ✅ QR kod orqali menyuga kirish
- ✅ Kategoriya bo'yicha taomlarni ko'rish
- ✅ Savatga qo'shish va buyurtma berish
- ✅ Real-time hisob ko'rish
- ✅ Mobil qurilmalarga moslashtirilgan

### Oshxona uchun
- ✅ Yangi buyurtmalarni real-time ko'rish
- ✅ Buyurtma statuslarini boshqarish (Kutilmoqda → Tayyorlanmoqda → Tayyor)
- ✅ Kunlik statistika
- ✅ Auto-refresh

### Ofitsantlar uchun
- ✅ Stollar va sessiyalarni boshqarish
- ✅ Har bir stol bo'yicha hisob
- ✅ To'lov qabul qilish
- ✅ Sessiyalarni yopish

### Admin uchun
- ✅ Menyu CRUD (qo'shish, o'zgartirish, o'chirish)
- ✅ Kategoriya boshqaruvi
- ✅ Stol va etaj boshqaruvi
- ✅ QR kod generatsiya qilish
- ✅ Buyurtmalar va to'lovlar statistikasi
- ✅ Xodimlarni boshqarish

## 🚀 O'rnatish

### Talablar
- Python 3.8 yoki yuqori
- pip
- virtualenv (tavsiya etiladi)

### 1. Loyihani yuklab oling
```bash
cd "d:\Projects\oshhona tizimi"
```

### 2. Virtual muhit yarating
```bash
python -m venv venv
```

### 3. Virtual muhitni faollashtiring
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Kerakli paketlarni o'rnating
```bash
pip install -r requirements.txt
```

### 5. Ma'lumotlar bazasini yarating
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Namunaviy ma'lumotlarni yuklang
```bash
python manage.py populate_sample_data
```

Bu buyruq quyidagilarni yaratadi:
- 5 ta kategoriya
- 20+ ta menyu elementi
- 25 ta stol (3 etaj)
- 3 ta foydalanuvchi (admin, kitchen, waiter)

### 7. QR kodlarni generatsiya qiling
```bash
python manage.py generate_qr_codes
```

### 8. Serverni ishga tushiring
```bash
python manage.py runserver
```

Brauzerda ochish: http://localhost:8000

## 👥 Kirish ma'lumotlari

Default foydalanuvchilar:

| Rol | Username | Parol | URL |
|-----|----------|-------|-----|
| Admin | admin | admin123 | /admin/ |
| Oshxona | kitchen | kitchen123 | /kitchen/ |
| Ofitsant | waiter | waiter123 | /waiter/ |

## 📱 Foydalanish

### Mijoz sifatida:
1. Stolingizdagi QR kodni skanerlang
2. Menyu avtomatik ochiladi (masalan: `/menu/?table=5`)
3. Taomlarni tanlang va savatga qo'shing
4. "Buyurtma berish" tugmasini bosing
5. Hisobni `/bill/?table=5` orqali ko'ring

### Oshpaz sifatida:
1. `/kitchen/` ga kiring
2. Yangi buyurtmalarni ko'ring
3. "Boshlash" tugmasini bosib tayyorlashni boshlang
4. "Tayyor" tugmasini bosing

### Ofitsant sifatida:
1. `/waiter/` ga kiring
2. Faol stollarni ko'ring
3. Har bir stolning hisobini ko'ring
4. To'lovni qabul qiling
5. Sessiyani yoping

## 📂 Loyiha tuzilmasi

```
oshhona tizimi/
├── qrmenu/                 # Main project folder
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── restaurant/             # Restaurant app
│   ├── models.py           # Database models
│   ├── views.py            # Views (logic)
│   ├── urls.py             # App URLs
│   ├── admin.py            # Admin configuration
│   ├── management/         # Custom commands
│   │   └── commands/
│   │       ├── populate_sample_data.py
│   │       └── generate_qr_codes.py
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── restaurant/         # Restaurant templates
│       ├── menu.html
│       ├── cart.html
│       ├── bill.html
│       ├── kitchen_panel.html
│       └── waiter_panel.html
├── static/                 # Static files (CSS, JS)
├── media/                  # Uploaded files (images, QR codes)
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## 🔧 Sozlash

### BASE_URL o'zgartirish (Production uchun)
`qrmenu/settings.py` da:
```python
BASE_URL = 'https://yourdomain.com'
```

### Ma'lumotlar bazasini o'zgartirish
Default: SQLite  
Production uchun PostgreSQL tavsiya etiladi:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qrmenu_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🛠 Qo'shimcha buyruqlar

### Yangi superuser yaratish
```bash
python manage.py createsuperuser
```

### Ma'lumotlar bazasini tozalash
```bash
python manage.py populate_sample_data --clear
```

### QR kodlarni qayta generatsiya qilish
```bash
python manage.py generate_qr_codes --force
```

### Testlarni ishga tushirish
```bash
python manage.py test restaurant
```

## 📊 API Endpoints

| URL | Method | Description |
|-----|--------|-------------|
| `/menu/?table=X` | GET | Menyu sahifasi |
| `/cart/?table=X` | GET | Savat |
| `/order/submit/` | POST | Buyurtma berish |
| `/bill/?table=X` | GET | Hisob |
| `/order/update-status/` | POST | Status o'zgartirish |
| `/kitchen/orders/` | GET | Buyurtmalar (JSON) |

## 🔐 Xavfsizlik

- ✅ CSRF himoya
- ✅ Django auth tizimi
- ✅ User roles va permissions
- ✅ SQL injection himoya (Django ORM)
- ✅ XSS himoya

**Production uchun:**
1. `DEBUG = False` qiling
2. `SECRET_KEY` ni o'zgartiring
3. `ALLOWED_HOSTS` ni sozlang
4. HTTPS ishlatishni yoqing

## 📝 Kelajakda qo'shilishi mumkin

- [ ] WebSocket real-time updates
- [ ] Click/Payme to'lov integratsiyasi
- [ ] SMS xabarnomalar
- [ ] Multi-language support
- [ ] Telegram bot integratsiyasi
- [ ] Hisobot PDF export
- [ ] Mahsulotlar inventarizatsiyasi
- [ ] Xodimlar ish vaqti hisobi

## 📞 Yordam

Muammolar yoki savollar bo'lsa:
1. GitHub Issues bo'limiga murojaat qiling
2. Django docs: https://docs.djangoproject.com/
3. Bootstrap docs: https://getbootstrap.com/

## 📄 Litsenziya

MIT License - bepul foydalanish va o'zgartirish mumkin.

## 👨‍💻 Muallif

QR Menu System - Restaurant Ordering Platform
Version 1.0 - MVP

---
**⭐ Loyiha yoqsa, GitHub'da star bering!**
