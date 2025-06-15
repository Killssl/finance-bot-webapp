import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

app = FastAPI()

application = Application.builder().token(BOT_TOKEN).build()

# /start команда
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой финансовый помощник.")

application.add_handler(CommandHandler("start", start))

# Эндпоинт для проверки
@app.get("/")
async def root():
    return {"message": "Finance Bot Backend is working with Telegram Webhook!"}

# Telegram webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    json_data = await req.json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return "ok"

# при запуске приложения
@app.on_event("startup")
async def on_startup():
    await application.initialize()  # <-- вот эта строка ключевая!
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.bot.set_webhook(url=WEBHOOK_URL)
