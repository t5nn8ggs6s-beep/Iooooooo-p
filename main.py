import asyncio
import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = "8625476937:AAHXIk5bn4K1f8kTrZ9D5MUd2o0PRFqndrg"
CHANNEL_LINK = "https://t.me/+GQvYBe-YqAcyYjBl"

logging.basicConfig(level=logging.INFO)

users = {}

menu_keyboard = ReplyKeyboardMarkup(
    [["🔑 Ввести код"], ["ℹ️ Как получить код"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users[user_id] = datetime.now()

    await update.message.reply_text(
        "🎬 Добро пожаловать в КиноТочка!\n\n"
        "Получи доступ к эксклюзивным фильмам 👇",
        reply_markup=menu_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🔑 Ввести код":
        await update.message.reply_text("Введи код из TikTok 👇")

    elif text == "ℹ️ Как получить код":
        await update.message.reply_text(
            "📱 Найди наше видео в TikTok\n"
            "🔢 Скопируй код из описания\n"
            "⬅️ Вернись сюда"
        )

    elif text.isdigit():
        code = int(text)

        msg = await update.message.reply_text("⏳ Проверяю код...")
        await asyncio.sleep(1)

        await msg.edit_text("🔍 Ищу фильм...")
        await asyncio.sleep(1)

        await msg.edit_text("📡 Подключаю доступ...")
        await asyncio.sleep(1)

        if 300 <= code <= 3000:
            await msg.edit_text(
                f"✅ Доступ открыт!\n\n"
                f"🎬 Смотреть фильм:\n{CHANNEL_LINK}"
            )

            print(f"USER {user_id} ENTERED VALID CODE {code}")

        else:
            await msg.edit_text("❌ Код не найден\n\nПопробуй ещё раз")

    else:
        await update.message.reply_text("❗ Используй кнопки ниже")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("BOT STARTED...")
app.run_polling()
