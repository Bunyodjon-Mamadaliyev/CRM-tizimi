# 🧠 Django CRM Export API - Rendererlar bilan

🎯 **Loyiha maqsadi**

Bu loyiha CRM (Customer Relationship Management) tizimi uchun Django REST Framework asosida turli formatlarda ma'lumotlarni eksport qilish imkoniyatini beradi. Ma'lumotlar quyidagi formatlarda chiqarilishi mumkin:

* 🟡 JSON (standart format)
* 🟩 CSV (Excelda ochish uchun qulay)
* 🟦 Excel (.xlsx)
* 🔴 PDF (hisobot shaklida)

## 📦 Funktsiyalar

✅ CRM ma'lumotlarini eksport qilish: JSON, CSV, Excel, PDF
✅ Content Negotiation: `Accept` header asosida avtomatik format tanlash
✅ Custom JSON wrapper: Har bir javob ma'lumotlari belgilangan struktura bilan qaytariladi
✅ Hisobotlar: Kompaniya, Bitim, Aktivlik, Sotuvlar bo'yicha eksport qilinadigan hisobotlar

---

## 🏗️ O'rnatish

```bash
# 1. Loyihani klonlash
$ git clone https://github.com/Bunyodjon-Mamadaliyev/CRM-tizimi.git
$ cd CRM-tizimi

# 2. Virtual muhit yaratish
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Talab qilinadigan kutubxonalarni o'rnatish
$ pip install -r requirements.txt

# 4. Migratsiyalarni qo'llash
$ python manage.py migrate

# 5. Admin foydalanuvchi yaratish
$ python manage.py createsuperuser

# 6. Serverni ishga tushirish
$ python manage.py runserver
```

---

## 🔌 API Endpointlar

| Endpoint                   | Tavsif                | Formatlar             |
| -------------------------- | --------------------- | --------------------- |
| `/api/companies/`          | Kompaniyalar ro'yxati | JSON, CSV, Excel, PDF |
| `/api/contacts/`           | Kontaktlar ro'yxati   | JSON, CSV, Excel, PDF |
| `/api/deals/`              | Bitimlar ro'yxati     | JSON, CSV, Excel, PDF |
| `/api/activities/`         | Aktivliklar ro'yxati  | JSON, CSV, Excel, PDF |
| `/api/reports/sales/`      | Sotuvlar hisoboti     | JSON, CSV, Excel, PDF |
| `/api/reports/activities/` | Aktivliklar hisoboti  | JSON, CSV, Excel, PDF |
| `/api/reports/companies/`  | Kompaniyalar hisoboti | JSON, CSV, Excel, PDF |
| `/api/reports/deals/`      | Bitimlar hisoboti     | JSON, CSV, Excel, PDF |

📥 Format tanlash uchun `Accept` headerdan foydalaning:

```http
Accept: application/json        # JSON (standart)
Accept: text/csv                # CSV
Accept: application/vnd.ms-excel  # Excel
Accept: application/pdf         # PDF
```

---

### 📄 CSVRenderer

* Har bir model uchun ustunlar nomlari bilan CSV fayl yaratadi.
* Masalan: `companies.csv`

### 📄 ExcelRenderer

* `.xlsx` formatda javob beradi.
* Pandas kutubxonasi orqali hosil qilinadi.

### 📄 PDFRenderer

* PDF hisobotlar `ReportLab` yoki `WeasyPrint` orqali yaratiladi.
* Har bir hisobot sahifasi tartibli va dizaynlangan bo'ladi.

---

## 📊 Hisobotlar

| Hisobot      | Endpoint                   | Tavsif                          |
| ------------ | -------------------------- | ------------------------------- |
| Sotuvlar     | `/api/reports/sales/`      | Bitimlar asosida savdo hisoboti |
| Aktivliklar  | `/api/reports/activities/` | Faoliyat bo'yicha xulosalar     |
| Kompaniyalar | `/api/reports/companies/`  | Kompaniyalar holati haqida      |
| Bitimlar     | `/api/reports/deals/`      | Bitim bosqichlari bo'yicha      |

---

## ✅ Testlash

### Unit testlar:

* Har bir renderer uchun alohida test yozilgan: JSON, CSV, Excel, PDF

### Integration testlar:

* Rendererlar endpointlar orqali to'g'ri ishlashini tekshiradi

### Edge-case testlar:

* Bo'sh queryset
* Katta ma'lumotlar to'plami
* Xatolik yuz bergan holatlar

---

## 📖 Hujjatlar

* Swagger: `http://localhost:8000/swagger/`
* ReDoc: `http://localhost:8000/redoc/`

---

## 🛡️ Qo'shimcha imkoniyatlar

* 📦 Streaming: Katta fayllar uchun
* 🔐 Xavfsizlik: Exportda faqat ruxsat berilgan ma'lumotlar ko'rsatiladi
* ⚙️ Sozlamalar: Rendererlarni sozlash uchun konfiguratsiya imkoniyati mavjud (`settings.py`)

---

## 👨‍💻 Muallif

> Loyihani yaratdi: **Mamadaliyev Bunyodjon**
> Django REST Framework orqali ko'p formatli javoblarni yetkazib berish

---

## 🌟 Foydali bo'lsa yulduzcha qo'ying!

Agar loyiha sizga foydali bo'lgan bo'lsa, GitHub sahifasida ⭐ bosing va boshqalar bilan bo'lishing! 🎉
