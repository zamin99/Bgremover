import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from io import BytesIO

# ===== CONFIGURATION =====
# Read from environment variables (set on Railway)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
REMOVE_BG_API_KEY = os.environ.get("REMOVE_BG_API_KEY", "F2RnX8kEWsjfoAoP1ezQfQgS")  # fallback only
REMOVE_BG_URL = "https://api.remove.bg/v1.0/removebg"

# Your channel and developer info
CHANNEL_LINK = "https://t.me/ZAMINTRICKS"
DEV_CONTACT = "@SIGMAXZAMIN"  # for display
DEV_URL = "https://t.me/SIGMAXZAMIN"  # for button link

# ===== LOGGING =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inline keyboard with channel and dev buttons
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = """
➖➖➖➖➖➖➖➖➖➖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━➤🐉
⊚-----------------------------------⊚🐉

✨ **Welcome to the Ultimate Background Remover Bot!** ✨

I can remove the background from any image you send me.  
Just drop an image and watch the magic happen! 🪄

🚀 **How to use:**
• Send me a photo (as file or picture).
• Wait a few seconds.
• Receive your background‑free image! 🖼️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
➖➖➖➖➖➖➖➖➖➖
"""
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ===== HELP COMMAND =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 **Help Menu**

1️⃣ Send me any image (JPEG, PNG, etc.)  
2️⃣ I'll process it using remove.bg API.  
3️⃣ You'll receive the image with the background removed.

⚠️ **Note:** The bot uses remove.bg free credits. If credits run out, you may need to upgrade your API plan.

For issues, contact my developer: @SIGMAXZAMIN
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ===== PROCESS IMAGES =====
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Notify user that processing has started
    await update.message.reply_text("⏳ Removing background... Please wait.")

    # Get the image file
    photo_file = await update.message.photo[-1].get_file()
    image_data = BytesIO()
    await photo_file.download_to_memory(image_data)
    image_data.seek(0)

    # Call remove.bg API
    try:
        response = requests.post(
            REMOVE_BG_URL,
            files={'image_file': image_data},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API_KEY},
        )
        if response.status_code == 200:
            # Send the result image back to the user
            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
                [InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_photo(
                photo=BytesIO(response.content),
                filename="no_bg.png",
                caption="✅ Background removed successfully!",
                reply_markup=reply_markup
            )
        else:
            # Handle API errors
            error_msg = response.json().get('errors', [{}])[0].get('title', 'Unknown error')
            await update.message.reply_text(f"❌ Background removal failed: {error_msg}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

# ===== MAIN FUNCTION =====
def main():
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        raise ValueError("No BOT_TOKEN found! Please set the BOT_TOKEN environment variable.")

    # Create the Application using the builder pattern (correct for v20+)
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Start the bot
    logger.info("🤖 Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
