import os

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
    WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"
