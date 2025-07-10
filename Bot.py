import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("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")
BOT_TOKEN = os.getenv("7731721054:AAG8TSf_JpbSAzYbWJIHRRn9mJURjop1esQ")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm your English Communication coach.\n\n"
        "You can use these commands:\n"
        "/correct <sentence> – Grammar correction\n"
        "/fluency <sentence> - More fluent version\n"
        "/tip - Daily English tip\n"
        "/chat <message> - Practice conversation"
    )

# Grammar Correction
async def correct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please send a sentence after /correct")
        return

    user_text = ' '.join(context.args)
    prompt = f"Correct this sentence for grammar and spelling errors: '{user_text}' and explain the corrections."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    corrected = response['choices'][0]['message']['content']
    await update.message.reply_text(f"✅ Grammar Correction:\n{corrected}")

# Fluency Improvement
async def fluency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please send a sentence after /fluency")
        return

    user_text = ' '.join(context.args)
    prompt = f"Rewrite this sentence to sound more fluent and natural: '{user_text}'"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    fluent = response['choices'][0]['message']['context']
    await update.message.reply_text(f"💬 Fluent Version:\n{fluent}")

# Daily English Tip
async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = "Give a simple English speaking tip."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    english_tip = response['choices'][0]['message']['content']  # ✅ renamed variable
    await update.message.reply_text(f"🧠 English Tip:\n{english_tip}")

# Conversation practice
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please type a message after /chat to start a conversation.")
        return

    user_text = ' '.join(context.args)
    prompt = f"Talk to the user in simple English and help improve their communication. User said: '{user_text}'"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

# Bot Setup
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("correct", correct))
    app.add_handler(CommandHandler("fluency", fluency))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("chat", chat))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


