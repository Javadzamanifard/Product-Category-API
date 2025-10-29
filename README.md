# 🛍️ Store API (Django REST Framework)

یک API ساده برای مدیریت محصولات و دسته‌بندی‌ها با استفاده از Django REST Framework، JWT Authentication و Djoser.  
این پروژه برای تمرین و توسعه‌ی ساختار RESTful در جنگو طراحی شده است.

---

## 🚀 ویژگی‌ها

- مدیریت **محصولات** و **دسته‌بندی‌ها**
- احراز هویت با **JWT (SimpleJWT + Djoser)**
- دسترسی‌ها (Permissions):
  - کاربران معمولی: فقط مشاهده‌ی داده‌ها
  - ادمین‌ها: دسترسی کامل (CRUD)
- فیلتر، جست‌وجو و مرتب‌سازی داده‌ها
- صفحه‌بندی (Pagination)
- API استاندارد و قابل استفاده در Frontend یا Mobile App

---

## 🧩 ساختار پروژه

store_api/
├── store/
│ ├── models.py # مدل‌های Product و Category
│ ├── serializers.py # سریالایزرهای DRF
│ ├── views.py # ViewSetها و فیلترها
│ ├── permissions.py # IsAdminOrReadOnly
│ ├── pagination.py # DefaultPagination
│ ├── urls.py # مسیرهای API
│ └── ...
├── config/
│ ├── settings.py # تنظیمات پروژه
│ ├── urls.py # مسیرهای اصلی و Djoser
│ └── serializers.py # Serializerهای کاربر برای Djoser
└── requirements.txt


## ⚙️ نصب و اجرا

### 1️⃣ کلون پروژه
```bash
git clone https://github.com/your-username/store-api.git
cd store-api
2️⃣ ساخت محیط مجازی و نصب پکیج‌ها
bash
Copy code
python -m venv env
source env/bin/activate   # در ویندوز: env\Scripts\activate
pip install -r requirements.txt
3️⃣ اعمال مایگریشن‌ها
bash
Copy code
python manage.py makemigrations
python manage.py migrate
4️⃣ ساخت ادمین
bash
Copy code
python manage.py createsuperuser
5️⃣ اجرای سرور
bash
Copy code
python manage.py runserver
🔐 احراز هویت (Authentication)
پروژه از JWT استفاده می‌کند.
پس از نصب Djoser و SimpleJWT، endpointهای زیر در دسترس هستند:

Endpoint	توضیح
/auth/jwt/create/	دریافت Access و Refresh Token
/auth/jwt/refresh/	تمدید توکن
/auth/users/	ثبت‌نام کاربر جدید
/auth/users/me/	مشاهده اطلاعات کاربر فعلی

نمونه درخواست:

json
Copy code
POST /auth/jwt/create/
{
  "email": "user@example.com",
  "password": "1234"
}
📦 Endpoints اصلی
🛒 محصولات (Products)
متد	آدرس	توضیح
GET	/api/products/	دریافت لیست محصولات
GET	/api/products/{id}/	جزئیات محصول
POST	/api/products/	افزودن محصول جدید (فقط ادمین)
PUT/PATCH	/api/products/{id}/	ویرایش محصول (فقط ادمین)
DELETE	/api/products/{id}/	حذف محصول (فقط ادمین)

🔹 پارامترهای جست‌وجو و فیلتر:

ruby
Copy code
?category_id=1&min_price=10&max_price=100&search=shirt&ordering=-price
🧩 دسته‌بندی‌ها (Categories)
متد	آدرس	توضیح
GET	/api/categories/	لیست دسته‌بندی‌ها
POST	/api/categories/	افزودن دسته‌بندی (فقط ادمین)

🔒 Permissionها
IsAdminOrReadOnly → فقط ادمین‌ها می‌تونن بنویسن (POST/PUT/DELETE)

کاربران عادی فقط می‌تونن بخونن (GET)

🧾 Pagination
پروژه از کلاس صفحه‌بندی سفارشی استفاده می‌کند:

python
Copy code
class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
نمونه خروجی:

json
Copy code
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
⚙️ تنظیمات مهم
settings.py
python
Copy code
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
.gitignore
__pycache__/
env/
media/
*.sqlite3
*.pyc
👨‍💻 توسعه‌دهنده
نام: Javad Zamani
📧 ایمیل :javadzamanii.1374@gmail.com
🌍 ساخته‌شده با Django REST Framework ❤️

