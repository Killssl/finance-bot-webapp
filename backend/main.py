import os
from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = FastAPI()

# Простая проверка API
@app.get("/")
async def root():
    return {"message": "Finance Bot Backend is working with Telegram!"}

# Базовый обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой финансовый помощник.")

# Подключаем Telegram бота при запуске FastAPI
@app.on_event("startup")
async def startup():
    app_bot_token = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(app_bot_token).build()

    application.add_handler(CommandHandler("start", start))

    # Запускаем бота в отдельном процессе
    application.run_polling()
