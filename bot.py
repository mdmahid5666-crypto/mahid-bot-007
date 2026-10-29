import logging
import base64
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "9095452020:AAEmhuXEeYpHoOINqtjSm8IZLh7w9JnOJ9A"

TEAM_NAME = "MAHID DVP HELP TEAM"
ADMIN_HANDLE = "@DWC_ADMIN_MAHID"
REQUIRED_CHANNELS = ["@NCK_Dev", "@ERRORX404E", "@NCKDEVFreeSC"]

verified_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in verified_users:
        await show_main_menu(update, context)
        return

    keyboard = []
    for ch in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{ch.replace('@', '')}")])
    
    keyboard.append([InlineKeyboardButton("✅ VERIFY", callback_data="verify_join")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "<b>⚠️ চ্যানেলগুলোতে জয়েন করুন!</b>\n\n"
        "বটটি ব্যবহার করতে হলে নিচের চ্যানেলগুলোতে জয়েন করা বাধ্যতামূলক। জয়েন করার পর নিচে <b>VERIFY</b> বাটনে ক্লিক করুন।"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == "verify_join":
        verified_users.add(user_id)
        await query.message.delete()
        await show_main_menu_callback(query, context)
    elif query.data == "main_menu":
        await show_main_menu_callback(query, context)
    elif query.data == "protect_code_menu":
        keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "🛡️ <b>MAHID DVP SECURE OBFUSCATOR</b>\n\n"
            "⏳ <b>Duration:</b> Unlimited\n"
            "💰 <b>Cost:</b> FREE\n"
            "📦 <b>Max size:</b> 50MB\n\n"
            "আপনার প্রটেক্ট করার জন্য যেকোনো <b>HTML কোড (টেক্সট আকারে)</b> অথবা সরাসরি একটি <b>.html ফাইলের</b> ডকুমেন্ট এই চ্যাটে পাঠিয়ে দিন!",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{REQUIRED_CHANNELS[0].replace('@', '')}")],
        [InlineKeyboardButton("🛡️ Protect Code", callback_data="protect_code_menu")],
        [InlineKeyboardButton("👨‍💻 Telegram Admin", url=f"https://t.me/{ADMIN_HANDLE.replace('@', '')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption_text = (
        "✅ <b>VERIFIED!</b>\n\n"
        f"Thank you for joining our channels, {update.effective_user.first_name}!\n\n"
        "💰 Balance: <b>$0</b> | ⭐ Stars: <b>0</b>\n\n"
        "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় কাজটি সিলেক্ট করুন:"
    )
    await update.message.reply_text(caption_text, reply_markup=reply_markup, parse_mode="HTML")

async def show_main_menu_callback(query, context):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{REQUIRED_CHANNELS[0].replace('@', '')}")],
        [InlineKeyboardButton("🛡️ Protect Code", callback_data="protect_code_menu")],
        [InlineKeyboardButton("👨‍💻 Telegram Admin", url=f"https://t.me/{ADMIN_HANDLE.replace('@', '')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption_text = (
        "✅ <b>VERIFIED!</b>\n\n"
        f"Thank you for joining our channels!\n\n"
        "💰 Balance: <b>$0</b> | ⭐ Stars: <b>0</b>\n\n"
        "নিচের অপশনগুলো থেকে আপনার প্রয়োজনীয় কাজটি সিলেক্ট করুন:"
    )
    await query.message.reply_text(caption_text, reply_markup=reply_markup, parse_mode="HTML")

async def process_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in verified_users:
        await update.message.reply_text("⚠️ দয়া করে আগে /start লিখে চ্যানেল ভেরিফাই করুন!")
        return

    raw_code = ""
    if update.message.text:
        raw_code = update.message.text
    elif update.message.document:
        doc = update.message.document
        file = await context.bot.get_file(doc.file_id)
        file_bytes = await file.download_as_bytearray()
        raw_code = file_bytes.decode("utf-8", errors="ignore")
    
    if not raw_code.strip():
        await update.message.reply_text("❌ খালি কোড গ্রহণযোগ্য নয়।")
        return

    processing_msg = await update.message.reply_text("⏳ কোড প্রসেসিং এবং সিকিউরিটি শিল্ড যুক্ত করা হচ্ছে...")

    encoded1 = base64.b64encode(raw_code.encode("utf-8")).decode("utf-8")
    shifted = "".join([chr(ord(c) + 5) for c in encoded1])
    final_payload = base64.b64encode(shifted.encode("utf-8")).decode("utf-8")

    protected_code = f"""<!--
==================================================
🔥 UNBREAKABLE ELITE ANTI-DECODE BY {TEAM_NAME} 🔥
--------------------------------------------------
Obfuscated By: {ADMIN_HANDLE}
Status: MAXIMUM ANTI-DECODER SHIELD & CLOCK LOCK ACTIVE 🛑
==================================================
-->
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>🚫🔥💀 [কোড চোর সনাক্ত হয়েছে! {TEAM_NAME} এর সিকিউরিটি ভেঙে কোড ডিকোড করার ক্ষমতা কারো নাই! ওনার: {ADMIN_HANDLE}] 🔒 ⚡</title>
<script>
    function triggerClockDestruct() {{
        document.open();
        document.write('<!DOCTYPE html><html><head><title>⚠️ CODE DESTROYED - CLOCK LOCK ACTIVE</title><style>body {{ background: #000; color: #00ff66; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: Courier New, monospace; overflow: hidden; text-align: center; margin: 0; }} h1 {{ color: #ff0055; text-shadow: 0 0 15px #ff0055; font-size: 26px; margin-bottom: 10px; }} .clock {{ font-size: 65px; font-weight: bold; color: #00ff66; text-shadow: 0 0 20px #00ff66, 0 0 40px #00ff66; border: 3px solid #00ff66; padding: 20px 40px; border-radius: 15px; background: rgba(0, 255, 102, 0.05); margin: 20px 0; }} p {{ color: #00e5ff; font-size: 16px; margin: 5px 0; }} .admin {{ color: #ff0055; font-weight: bold; }}</style></head><body><h1>🚫 SECURITY BREACH & TAMPER DETECTED! 🚫</h1><p>Code modification attempted! This file has been permanently converted into a clock.</p><div class="clock" id="liveClock">00:00:00</div><p>Owner Admin: <span class="admin">{ADMIN_HANDLE}</span></p><p>Team: {TEAM_NAME}</p><script>function updateClock() {{ const now = new Date(); document.getElementById("liveClock").innerText = now.toLocaleTimeString(); }} setInterval(updateClock, 1000); updateClock();<\\/script></body></html>');
        document.close();
    }}
    window.addEventListener("keydown", function(e) {{
        if (e.keyCode === 123 || (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 67 || e.keyCode === 74)) || (e.ctrlKey && (e.keyCode === 85 || e.keyCode === 83))) {{
            triggerClockDestruct();
            e.preventDefault();
            return false;
        }}
    }}, true);
    window.addEventListener("contextmenu", function(e) {{ triggerClockDestruct(); e.preventDefault(); return false; }}, true);
    window.addEventListener("DOMContentLoaded", function() {{
        try {{
            let step1 = atob("{final_payload}");
            let shifted = "";
            for(let i=0; i<step1.length; i++) {{ shifted += String.fromCharCode(step1.charCodeAt(i) - 5); }}
            let b64_decoded = atob(shifted);
            let real_html = decodeURIComponent(escape(b64_decoded));
            document.open(); document.write(real_html); document.close();
        }} catch(e) {{ triggerClockDestruct(); }}
    }});
</script>
</head>
<body style="margin:0;background:#000;"></body>
</html>"""

    file_filename = "protected_secure_app.html"
    with open(file_filename, "w", encoding="utf-8") as f:
        f.write(protected_code)

    await processing_msg.delete()
    with open(file_filename, "rb") as f:
        await update.message.reply_document(
            document=f,
            filename=file_filename,
            caption=f"✅ **আপনার কোড সফলভাবে সিকিউর করা হয়েছে!**\n🛡️ Powered by {TEAM_NAME}",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_code))
    app.add_handler(MessageHandler(filters.Document.ALL, process_code))

    print("🤖 MAHID DVP Bot is running successfully...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
