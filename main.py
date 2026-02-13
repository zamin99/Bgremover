import os
import logging
import asyncio
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

# ===== WELCOME MESSAGE =====
WELCOME_TEXT = """
╭━━━━━━━━━━━━━━━━━━━━━━╮
      🚀 PRO BG REMOVER
╰━━━━━━━━━━━━━━━━━━━━━━╯

➤ Send Any Image  
➤ AI Detects Subject  
➤ Background Removed Instantly  
➤ Get Transparent HD PNG  

━━━━━━━━━━━━━━━━━━━━━━
⚡ Fast • Clean • Professional
━━━━━━━━━━━━━━━━━━━━━━

➤ Type /help for commands
"""

# ===== HELP MESSAGE =====
HELP_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          ⚡ HELP CENTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 COMMANDS
➜ /start  » Activate Bot
➜ /help   » View Help Menu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 HOW IT WORKS
➜ Send any image
➜ AI removes background
➜ Get HD transparent PNG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 FEATURES
➜ Clean Edge Detection
➜ Fast Processing
➜ High-Quality Output
➜ Secure & Private

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 REQUIREMENTS
➜ Max Size: 20MB
➜ Formats: JPG • PNG • WEBP
➜ Use high-resolution images

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍💻 SUPPORT
➜ Developer: @SIGMAXZAMIN
➜ Channel: @ZAMINTRICKS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ===== BOT NETWORK MESSAGE =====
BOT_NETWORK_TEXT = """
█▓▒░  OFFICIAL BOT NETWORK  ░▒▓█
        DARK • CYBER • PRO
━━━━━━━━━━━━━━━━━━━━━━━
⚠ POWERED TELEGRAM BOTS ⚠
━━━━━━━━━━━━━━━━━━━━━━━

⟢ @ALL_SOCIAL_DOWLODEDRBOT
⟿ ALL SOCIAL MEDIA DOWNLOADER

⟢ @GOOGLEXPLAYSZAMINBOT
⟿ GOOGLE PLAY TOOLS & INFO

⟢ @CYBERXTOOLKITBOT
⟿ CYBER & HACKER UTILITIES

⟢ @URLXSHORTNERBOT
⟿ FAST & SECURE URL SHORTENER

⟢ @IMAGEXHOSTERBOT
⟿ IMAGE UPLOAD & HOSTING

⟢ @INSTAXDOWLODERBOT
⟿ INSTAGRAM MEDIA DOWNLOADER

⟢ @Thumbnailxdowloderbot
⟿ YOUTUBE THUMBNAIL GRABBER

⟢ @Tikdowloderbot
⟿ TIKTOK NO-WATERMARK VIDEOS

⟢ @ForwardxTagremoverbot
⟿ FORWARD TAG REMOVER

⟢ @Githubrepo_to_zipdowloderbot
⟿ GITHUB REPO DOWLODER

⟢ @EDITING_MODS_APKSBOT
⟿ MODS EDITING APPS BOT
━━━━━━━━━━━━━━━━━━━━━━━
⚙ STATUS : ACTIVE
⚙ MODE   : DARK CYBER
⚙ MORE   : COMING SOON
━━━━━━━━━━━━━━━━━━━━━━━

☠ CREATED BY ➜ @ZAMINTRICKS
⚡ JOIN • USE • DOMINATE
━━━━━━━━━━━━━━━━━━━━━━━
"""

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖼️ Remove Background", callback_data="remove_bg")],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🤖 More Bots", callback_data="show_network")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# ===== HELP COMMAND =====
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👨‍💻 Contact Developer", url=DEV_URL)],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(HELP_TEXT, reply_markup=reply_markup)

# ===== CALLBACK HANDLER =====
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "remove_bg":
        await query.edit_message_text(
            "📸 **Send me an image** and I'll remove its background instantly!\n\n👇 Just upload a photo.",
            parse_mode="Markdown"
        )
    
    elif query.data == "show_network":
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🖼️ Remove Background", callback_data="remove_bg")],
            [InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(BOT_NETWORK_TEXT, reply_markup=reply_markup)

# ===== PROGRESS SIMULATION FUNCTION =====
async def update_progress(message, percent, step_text):
    # Progress bar with gradient style (█ = full, ░ = empty)
    filled = percent // 10  # 10% per block, total 10 blocks
    bar = "█" * filled + "░" * (10 - filled)
    text = f"""🤖 Processing your request...

[{bar}] {percent}%
Step {percent//25 + 1} of 4: {step_text}"""
    await message.edit_text(text)

# ===== PROCESS IMAGES WITH ANIMATED PROGRESS =====
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send initial progress message
    progress_msg = await update.message.reply_text(
        "🤖 Processing your request...\n\n[██░░░░░░░░░] 10%\nStep 1 of 4: Uploading image..."
    )

    # Define progress stages: (percent, step_text, delay)
    stages = [
        (10, "Uploading image...", 0.8),
        (25, "Analyzing image...", 0.8),
        (50, "Processing data...", 0.8),
        (75, "Enhancing result...", 0.8),
        (90, "Finalizing...", 0.8),
        (100, "Completed", 0.8),
    ]

    # Start the background API call
    photo_file = await update.message.photo[-1].get_file()
    image_data = BytesIO()
    await photo_file.download_to_memory(image_data)
    image_data.seek(0)

    # Create a task for API call
    api_task = asyncio.create_task(call_remove_bg_api(image_data))

    # Simulate progress
    for percent, step_text, delay in stages:
        if percent > 10:  # Already sent 10% initially
            await asyncio.sleep(delay)
            await update_progress(progress_msg, percent, step_text)

    # Progress reached 100%, now wait for API result if not finished
    response = await api_task

    # Delete or edit progress message to fade out (delete it)
    await progress_msg.delete()

    if response and response.status_code == 200:
        caption = (
            "✔ Process Completed Successfully\n\n"
            "Your background-free image is ready.\n"
            "Clean cut. High quality. Zero compromise.\n\n"
            "Stay connected:\n"
            f"Developer — {DEV_CONTACT}\n"
            f"Channel — @ZAMINTRICKS"
        )
        keyboard = [
            [InlineKeyboardButton("🔄 Remove Another", callback_data="remove_bg")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(
            photo=BytesIO(response.content),
            filename="no_bg.png",
            caption=caption,
            reply_markup=reply_markup
        )
    else:
        error_msg = "Unknown error"
        if response and response.status_code != 200:
            try:
                error_msg = response.json().get('errors', [{}])[0].get('title', 'Unknown error')
            except:
                pass
        await update.message.reply_text(f"❌ Failed: {error_msg}")

# ===== API CALL FUNCTION =====
async def call_remove_bg_api(image_data):
    loop = asyncio.get_event_loop()
    # Run requests.post in a thread to avoid blocking
    return await loop.run_in_executor(None, lambda: requests.post(
        REMOVE_BG_URL,
        files={'image_file': image_data},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    ))

# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("🤖 Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
