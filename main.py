import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests
from io import BytesIO

# ===== CONFIGURATION =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
REMOVE_BG_API_KEY = os.environ.get("REMOVE_BG_API_KEY", "F2RnX8kEWsjfoAoP1ezQfQgS")
REMOVE_BG_URL = "https://api.remove.bg/v1.0/removebg"

CHANNEL_LINK = "https://t.me/ZAMINTRICKS"
DEV_CONTACT = "@SIGMAXZAMIN"
DEV_URL = "https://t.me/SIGMAXZAMIN"

# ===== LOGGING =====
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== WELCOME MESSAGE (Pro Developer Style) =====
WELCOME_TEXT = """
╔══════════════════════════════╗
║   🔥 **PRO BACKGROUND REMOVER** 🔥  ║
║       ✨ **DEVELOPER EDITION** ✨    ║
╠══════════════════════════════╣
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║                               ║
║  🚀 **Send any image**         ║
║  🎯 **Remove background**       ║
║  ⚡ **Instant result**           ║
║                               ║
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║                               ║
║  👨‍💻 **Developer:** @SIGMAXZAMIN ║
║  📢 **Channel:** @ZAMINTRICKS   ║
║                               ║
║  💡 **Type /help for assistance** ║
╚══════════════════════════════╝
"""

# ===== HELP MESSAGE =====
HELP_TEXT = """
╔══════════════════════════════╗
║        🆘 **HELP MENU**        ║
╠══════════════════════════════╣
║                               ║
║  **🤖 Bot Commands:**          ║
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║  • /start - Start the bot     ║
║  • /help - Show this menu     ║
║                               ║
║  **📸 How to Use:**            ║
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║  1️⃣ Click "Start Removing"     ║
║  2️⃣ Send any image             ║
║  3️⃣ Get background-free result ║
║                               ║
║  **👨‍💻 Contact Developer:**     ║
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║  • Telegram: @SIGMAXZAMIN     ║
║  • Channel: @ZAMINTRICKS      ║
║  • For issues, bugs, or       ║
║    suggestions, DM developer  ║
║                               ║
║  **⚡ Quick Tips:**             ║
║  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰   ║
║  • Send high-quality images    ║
║  • Max size: 20MB             ║
║  • Formats: JPG, PNG, WEBP    ║
║                               ║
╚══════════════════════════════╝
"""

# ===== BOT NETWORK MESSAGE (Cyber Style) =====
BOT_NETWORK_TEXT = """
╔══════════════════════════════╗
║   🤖 **OFFICIAL BOT NETWORK**   ║
║        DARK • CYBER • PRO      ║
╠══════════════════════════════╣
║ @CYBERXTOOLKITBOT            ║
║  ➤ CYBER & HACKER UTILITIES  ║
║                              ║
║ @URLXSHRTNERBOT              ║
║  ➤ FAST & SECURE URL SHORTENER║
║                              ║
║ @IMAGEXHOSTERBOT             ║
║  ➤ IMAGE UPLOAD & HOSTING     ║
║                              ║
║ @INSTAXDOWLODERBOT           ║
║  ➤ INSTAGRAM MEDIA DOWNLOADER ║
║                              ║
║ @Thumbnailxdownloaderbot     ║
║  ➤ YOUTUBE THUMBNAIL GRABBER  ║
║                              ║
║ @Tikdowloderbot              ║
║  ➤ TIKTOK NO-WATERMARK VIDEOS ║
║                              ║
║ @ForwardxTagremoverbot       ║
║  ➤ FORWARD TAG REMOVER        ║
║                              ║
║ @Githubrepo_to_zipdowloderbot║
║  ➤ GITHUB REPO DOWNLOADER     ║
║                              ║
║ @EDITING_MODS_APKSBOT        ║
║  ➤ MODS EDITING APPS BOT      ║
╠══════════════════════════════╣
║ ⚡ **STATUS:** ACTIVE          ║
║ 🌑 **MODE:** DARK CYBER        ║
║ 🔜 **MORE:** COMING SOON       ║
╠══════════════════════════════╣
║ ✨ **CREATED BY**              ║
║    → @ZAMINTRICKS            ║
╚══════════════════════════════╝
"""

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🖼️ Start Removing", callback_data="remove_bg")],
        [InlineKeyboardButton("🤖 More Bots", callback_data="show_network")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup, parse_mode="Markdown")

# ===== HELP COMMAND =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💻 Contact Developer", url=DEV_URL)],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(HELP_TEXT, reply_markup=reply_markup, parse_mode="Markdown")

# ===== CALLBACK HANDLER =====
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "remove_bg":
        await query.edit_message_text("📸 **Send me the next image to remove background!**\n\n👇 Just upload a photo and I'll do the rest.", parse_mode="Markdown")
    
    elif query.data == "show_network":
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🖼️ Start Removing", callback_data="remove_bg")],
            [InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(BOT_NETWORK_TEXT, reply_markup=reply_markup, parse_mode="Markdown")

# ===== PROCESS IMAGES =====
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Notify user
    await update.message.reply_text("⏳ **Removing background...** Please wait.", parse_mode="Markdown")

    # Get image
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
            # Buttons after successful removal: Remove Another + Join Channel
            keyboard = [
                [InlineKeyboardButton("🔄 Remove Another", callback_data="remove_bg")],
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_photo(
                photo=BytesIO(response.content),
                filename="no_bg.png",
                caption=f"╔══════════════════════════════╗\n║   ✅ **BACKGROUND REMOVED**   ║\n╠══════════════════════════════╣\n║ 👨‍💻 Dev: @SIGMAXZAMIN        ║\n║ 📢 Channel: @ZAMINTRICKS     ║\n╚══════════════════════════════╝",
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        else:
            error_msg = response.json().get('errors', [{}])[0].get('title', 'Unknown error')
            await update.message.reply_text(f"❌ **Failed:** {error_msg}", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ **An error occurred.** Please try again later.", parse_mode="Markdown")

# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set! Please add it as environment variable.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("🤖 Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
