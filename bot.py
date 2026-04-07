import asyncio
import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from main import identify_car

load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # e.g. https://your-app.azurecontainerapps.io
PORT = int(os.environ.get("PORT", 8443))


_START_MESSAGE = (
    "👋 Welcome to Car Price Estimator!\n\n"
    "📸 Send me a car photo — I'll identify its make and model.\n\n"
    "⚠️ Limitations:\n"
    "- Make & model only (no trim or year)\n"
    "- Photos only — videos are ignored\n"
    "- Price estimation coming soon"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(_START_MESSAGE)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]  # largest available size
    file = await context.bot.get_file(photo.file_id)

    async def keep_typing():
        while True:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            await asyncio.sleep(4)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        typing_task = asyncio.create_task(keep_typing())
        try:
            result = await asyncio.get_event_loop().run_in_executor(None, identify_car, tmp.name)
        finally:
            typing_task.cancel()

    if result.get("error"):
        await update.message.reply_text(f"Could not identify car: {result['error']}")
    else:
        make = result.get("make") or "unknown"
        model = result.get("model") or "unknown"
        await update.message.reply_text(f"Make: {make}\nModel: {model}")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="/webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
    )


if __name__ == "__main__":
    main()
