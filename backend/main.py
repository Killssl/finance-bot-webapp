import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler
from backend.handlers import start
from backend.config import Config

app = FastAPI()
application = Application.builder().token(Config.BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start.start))

@app.get("/")
async def root():
    return {"message": "Finance Bot Backend is working!"}

@app.post(Config.WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    json_data = await req.json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return "ok"

@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.bot.set_webhook(url=Config.WEBHOOK_URL)
