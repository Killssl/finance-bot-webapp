import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

app = FastAPI()

# создаем приложение Telegram
application = Application.builder().token(BOT_TOKEN).build()

# обработчик /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой финансовый помощник.")

application.add_handler(CommandHandler("start", start))

# FastAPI endpoint для проверки
@app.get("/")
async def root():
    return {"message": "Finance Bot Backend is working with Telegram Webhook!"}

# FastAPI endpoint для Telegram webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    json_data = await req.json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return "ok"

# запуск Webhook при старте
@app.on_event("startup")
async def on_startup():
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.bot.set_webhook(url=WEBHOOK_URL)
