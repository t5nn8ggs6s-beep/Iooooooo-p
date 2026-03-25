import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Получаем токен из переменных окружения
TOKEN = "8625476937:AAHXIk5bn4K1f8kTrZ9D5MUd2o0PRFqndrg"
if not TOKEN:
    raise ValueError("TOKEN не найден! Добавь его в Railway Variables")

CHANNEL_LINK = "https://t.me/+GQvYBe-YqAcyYjBl"

# Клавиатура меню
menu_keyboard = ReplyKeyboardMarkup(
    [["🔑 Ввести код"], ["ℹ️ Как получить код"]],
    resize_keyboard=True
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Добро пожаловать в КиноТочка!\n\n"
        "Получи доступ к эксклюзивным фильмам 👇",
        reply_markup=menu_keyboard
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await msg.edit_text(f"✅ Код принят!\n\n🎬 Смотреть фильм:\n{CHANNEL_LINK}")
        else:
            await msg.edit_text("❌ Неверный код\n\nПопробуй ещё раз")
    else:
        await update.message.reply_text("❗ Используй кнопки ниже")

# Создаём приложение и запускаем
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("BOT STARTED...")
app.run_polling()
