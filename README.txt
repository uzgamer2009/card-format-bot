# Telegram Card Format Bot

Reklamasiz, karta ma'lumotlarini siz kiritadigan oddiy Telegram bot.

## 1. Talablar
- Python 3.10 yoki undan yangi
- Telegram'da @BotFather orqali yaratilgan bot tokeni

## 2. O'rnatish (Windows PowerShell)
Papka ichida terminal oching:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Tokenni sozlash
BotFather'dan token oling. Uni hech kimga yubormang.

Faqat joriy PowerShell oynasi uchun:
```powershell
$env:BOT_TOKEN="BOTFATHER_TOKENINGIZ"
```

Tavsiya: bot faqat siz ishlatishingiz uchun Telegram numeric ID'ingizni ham belgilang:
```powershell
$env:ADMIN_ID="TELEGRAM_NUMERIC_ID"
```

## 4. Ishga tushirish
```powershell
.\.venv\Scripts\python.exe bot.py
```

Terminal oynasi ochiq turganda bot ishlaydi. To'xtatish uchun `Ctrl+C`.

## Buyruqlar
- `/start` — boshlash
- `/add` — karta, qabul qiluvchi, izoh kiritish
- `/cancel` — bekor qilish

Bot tokeni yoki karta ma'lumotlarini ommaga ulashmang. Bu oddiy formatlovchi bot; u pul o'tkazmaydi va karta balansiga kira olmaydi.
