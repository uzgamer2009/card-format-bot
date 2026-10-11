import asyncio
import os
import re
from html import escape

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CopyTextButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = os.getenv("BOT_TOKEN", "").strip()
# Optional: restrict the bot to your Telegram numeric user ID, e.g. ADMIN_ID=123456789
ADMIN_ID = os.getenv("ADMIN_ID", "").strip()

dp = Dispatcher()
pending = {}  # user_id -> {"step": "...", "card": "...", "recipient": "..."}


def allowed(user_id: int) -> bool:
    return not ADMIN_ID or str(user_id) == ADMIN_ID


def format_card(raw: str) -> str | None:
    digits = re.sub(r"\D", "", raw)
    if not 12 <= len(digits) <= 19:
        return None
    return " ".join(digits[i:i + 4] for i in range(0, len(digits), 4))



def copy_keyboard(card: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📋 Karta raqamini nusxalash",
        copy_text=CopyTextButton(text=card)
    )
    return builder.as_markup()

@dp.message(CommandStart())
async def start(message: Message):
    if not allowed(message.from_user.id):
        return await message.answer("Bu botdan foydalanishga ruxsatingiz yo‘q.")
    await message.answer(
        "Salom! 👋\n\n"
        "Karta ma’lumotlarini chiroyli formatlash uchun /add yuboring.\n"
        "/cancel — jarayonni bekor qilish."
    )


@dp.message(Command("add"))
async def add_card(message: Message):
    if not allowed(message.from_user.id):
        return await message.answer("Bu botdan foydalanishga ruxsatingiz yo‘q.")
    pending[message.from_user.id] = {"step": "card"}
    await message.answer("💳 Karta raqamini yuboring:")


@dp.message(Command("cancel"))
async def cancel(message: Message):
    pending.pop(message.from_user.id, None)
    await message.answer("Jarayon bekor qilindi.")


@dp.message(F.text)
async def collect(message: Message):
    user_id = message.from_user.id
    if not allowed(user_id):
        return
    state = pending.get(user_id)
    if not state:
        return

    text = message.text.strip()
    step = state["step"]

    if step == "card":
        card = format_card(text)
        if not card:
            return await message.answer("Karta raqami 12–19 ta raqamdan iborat bo‘lishi kerak. Qayta yuboring:")
        state["card"] = card
        state["step"] = "recipient"
        await message.answer("👤 Qabul qiluvchining ism-familiyasini yuboring:")
    elif step == "recipient":
        if len(text) > 100:
            return await message.answer("Ism-familiya juda uzun. Qayta yuboring:")
        state["recipient"] = text
        state["step"] = "note"
        await message.answer("📝 Izohni yuboring (masalan, Humo). Izoh bo‘lmasa, — yuboring:")
    elif step == "note":
        note = "—" if text == "—" else text
        card = state["card"]
        recipient = escape(state["recipient"])
        safe_note = escape(note)
        pending.pop(user_id, None)
        await message.answer(
            "🛍️ <b>Savdo</b>\n"
            f"💳 <b>Karta:</b> <code>{escape(card)}</code>\n"
            f"👤 <b>Qabul qiluvchi:</b> {recipient}\n"
            f"📝 <b>Izoh:</b> {safe_note}",
            reply_markup=copy_keyboard(card),
            parse_mode=ParseMode.HTML,
        )


async def main():
    if not TOKEN:
        raise SystemExit(
            "BOT_TOKEN topilmadi. BotFather tokenini BOT_TOKEN muhit o‘zgaruvchisiga kiriting."
        )
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
