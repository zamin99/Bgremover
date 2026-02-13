import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests
import replicate
from io import BytesIO

# ===== CONFIGURATION =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
REMOVE_BG_API_KEY = os.environ.get("REMOVE_BG_API_KEY", "F2RnX8kEWsjfoAoP1ezQfQgS")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")  # Get from replicate.com
REMOVE_BG_URL = "https://api.remove.bg/v1.0/removebg"

CHANNEL_LINK = "https://t.me/ZAMINTRICKS"
DEV_CONTACT = "@SIGMAXZAMIN"
DEV_URL = "https://t.me/SIGMAXZAMIN"

# ===== LOGGING =====
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== MESSAGES (Your Designs) =====
WELCOME_TEXT = """
╭━━━━━━━━━━━━━━━━━━━━━━╮
      🚀 PRO IMAGE TOOLS
╰━━━━━━━━━━━━━━━━━━━━━━╯

➤ Choose a tool below to enhance your image!
➤ AI-powered processing • Fast & Free

━━━━━━━━━━━━━━━━━━━━━━
⚡ Colorize • RemoveBG • Restore • Upscale
━━━━━━━━━━━━━━━━━━━━━━

➤ Type /help for commands
"""

HELP_TEXT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          ⚡ HELP CENTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 COMMANDS
➜ /start  » Show main menu
➜ /help   » View this help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ AVAILABLE TOOLS
➜ 🎨 Colorize – Add color to B&W photos
➜ 🧹 RemoveBG – Remove image background
➜ 🔄 Restore – Fix old/damaged photos (faces)
➜ 📈 Upscale – Increase resolution 4x

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 HOW TO USE
1️⃣ Click a tool button
2️⃣ Send an image
3️⃣ Wait for AI processing
4️⃣ Get enhanced result

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👨‍💻 SUPPORT
➜ Developer: @SIGMAXZAMIN
➜ Channel: @ZAMINTRICKS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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

# ===== USER STATE (to remember selected tool) =====
# We'll use context.user_data to store the chosen tool for each user

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 Colorize", callback_data="tool_colorize"),
         InlineKeyboardButton("🧹 RemoveBG", callback_data="tool_removebg")],
        [InlineKeyboardButton("🔄 Restore", callback_data="tool_restore"),
         InlineKeyboardButton("📈 Upscale", callback_data="tool_upscale")],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
         InlineKeyboardButton("🤖 More Bots", callback_data="show_network")]
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

    data = query.data

    if data.startswith("tool_"):
        # Store selected tool in user_data
        tool = data.replace("tool_", "")
        context.user_data["selected_tool"] = tool
        tool_names = {
            "colorize": "🎨 Colorize",
            "removebg": "🧹 Remove Background",
            "restore": "🔄 Restore Photo",
            "upscale": "📈 Upscale Image"
        }
        await query.edit_message_text(
            f"🖼️ Send me an image for **{tool_names.get(tool, tool)}**.\n\n👇 Just upload a photo and I'll process it.",
            parse_mode="Markdown"
        )

    elif data == "show_network":
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🖼️ Back to Tools", callback_data="back_to_menu")],
            [InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(BOT_NETWORK_TEXT, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("🎨 Colorize", callback_data="tool_colorize"),
             InlineKeyboardButton("🧹 RemoveBG", callback_data="tool_removebg")],
            [InlineKeyboardButton("🔄 Restore", callback_data="tool_restore"),
             InlineKeyboardButton("📈 Upscale", callback_data="tool_upscale")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
             InlineKeyboardButton("🤖 More Bots", callback_data="show_network")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(WELCOME_TEXT, reply_markup=reply_markup)

# ===== PROCESS IMAGES =====
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if user selected a tool
    tool = context.user_data.get("selected_tool")
    if not tool:
        await update.message.reply_text("❌ Please select a tool first using the buttons.")
        return

    # Notify user
    await update.message.reply_text("⏳ Processing image...\nAI magic in progress. Please wait...")

    # Get image file
    photo_file = await update.message.photo[-1].get_file()
    image_data = BytesIO()
    await photo_file.download_to_memory(image_data)
    image_data.seek(0)

    # Process based on tool
    try:
        if tool == "removebg":
            result_image = await remove_background(image_data)
        elif tool == "colorize":
            result_image = await colorize_image(image_data)
        elif tool == "restore":
            result_image = await restore_image(image_data)
        elif tool == "upscale":
            result_image = await upscale_image(image_data)
        else:
            await update.message.reply_text("❌ Unknown tool.")
            return

        if result_image:
            # Success caption
            caption = (
                "✔ Process Completed Successfully\n\n"
                "Your enhanced image is ready.\n"
                "Clean cut. High quality. Zero compromise.\n\n"
                "Stay connected:\n"
                f"Developer — {DEV_CONTACT}\n"
                f"Channel — @ZAMINTRICKS"
            )
            # Buttons after processing: Process Another + Join Channel
            keyboard = [
                [InlineKeyboardButton("🔄 Process Another", callback_data="back_to_menu")],
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_photo(
                photo=result_image,
                filename="output.png",
                caption=caption,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text("❌ Processing failed. Please try again later.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

    # Clear selected tool so user must choose again
    context.user_data.pop("selected_tool", None)

# ===== TOOL FUNCTIONS =====
async def remove_background(image_data):
    response = requests.post(
        REMOVE_BG_URL,
        files={'image_file': image_data},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
    )
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None

async def colorize_image(image_data):
    # Use Replicate's DDColor model
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    # Save image to temporary file or pass as URL? Replicate can accept file uploads.
    # We'll upload to a temporary hosting or use bytes. For simplicity, we'll use a temporary file.
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_data.getvalue())
        tmp_path = tmp.name
    try:
        output = client.run(
            "cjwb0/ddcolor:dee7a1f7e6f8c7e7c8f8c7e7c8f8c7e7c8f8c7e7",
            input={"image": open(tmp_path, "rb")}
        )
        # output is a file URL
        if output:
            response = requests.get(output)
            if response.status_code == 200:
                return BytesIO(response.content)
    finally:
        os.unlink(tmp_path)
    return None

async def restore_image(image_data):
    # GFPGAN for face restoration
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_data.getvalue())
        tmp_path = tmp.name
    try:
        output = client.run(
            "tencentarc/gfpgan:9283608cc6b7be6b65a8e449c8d6c7c9e5a9a5e9",
            input={"img": open(tmp_path, "rb")}
        )
        if output:
            response = requests.get(output)
            if response.status_code == 200:
                return BytesIO(response.content)
    finally:
        os.unlink(tmp_path)
    return None

async def upscale_image(image_data):
    # Real-ESRGAN upscaling
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_data.getvalue())
        tmp_path = tmp.name
    try:
        output = client.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05f0",
            input={"image": open(tmp_path, "rb")}
        )
        if output:
            response = requests.get(output)
            if response.status_code == 200:
                return BytesIO(response.content)
    finally:
        os.unlink(tmp_path)
    return None

# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set!")
    if not REPLICATE_API_TOKEN:
        logger.warning("REPLICATE_API_TOKEN not set. Colorize, Restore, Upscale will not work.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("🤖 Multi‑Tool Image Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
