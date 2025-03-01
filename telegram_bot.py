import subprocess
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ✅ Yahan apna Telegram Bot Token daal
BOT_TOKEN = "123456789:ABCDEF..."  

# ✅ Teri binary ka path
BINARY_PATH = "./raja_patched"

# ✅ Process store karne ke liye variable
running_process = None

# ✅ Attack start karne ka function
def start_attack(update: Update, context: CallbackContext):
    global running_process
    
    if len(context.args) == 0:
        update.message.reply_text("Usage: /start_attack <time_in_min>")
        return
    
    try:
        duration = int(context.args[0]) * 60
        update.message.reply_text(f"🔥 Attack started for {context.args[0]} minutes!")

        # ✅ Binary execute karna
        running_process = subprocess.Popen([BINARY_PATH])
        
        # ✅ Diye gaye time tak wait karna, phir stop karna
        time.sleep(duration)
        if running_process:
            running_process.terminate()
            update.message.reply_text("✅ Attack stopped automatically!")
            running_process = None
    except ValueError:
        update.message.reply_text("❌ Invalid time format! Example: /start_attack 5")

# ✅ Attack stop karne ka function
def stop_attack(update: Update, context: CallbackContext):
    global running_process
    if running_process:
        running_process.terminate()
        update.message.reply_text("⛔ Attack stopped manually!")
        running_process = None
    else:
        update.message.reply_text("❌ No attack is running!")

# ✅ Bot setup karna
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start_attack", start_attack, pass_args=True))
    dp.add_handler(CommandHandler("stop_attack", stop_attack))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
