import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Backend FastAPI API
API_BASE = "http://web:8000"  # inside Docker network
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ------------------- Commands -------------------

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # extract user info
    user = update.effective_user
    chat_id = str(user.id)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    # try to register/upsert user on the API
    try:
        resp = requests.post(
            f"{API_BASE}/register_user",
            params={
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            },
            timeout=5,
        )
        if resp.status_code in (200, 201):
            # optional: log resp.json()
            pass
        else:
            # not fatal — but log / notify in container logs
            print("Register user failed:", resp.status_code, resp.text)
    except Exception as e:
        print("Register user error:", e)

    # send welcome message back to user
    await update.message.reply_text(
        "👋 Hello! I'm EUR Currency Bot.\n\n"
        "⚠️ Note: This bot is a demo project. This is a beta version, so bugs may exist.\n\n"
        "Currently Supported currencies: USD, GBP\n\n"
        "Available commands:\n"
        "• /rate EUR [Target Currency] → get latest exchange rate\n   ==> ex. /rate EUR USD\n"
        "• /subscribe EUR [Target Currency] → subscribe to daily updates\n  ==> ex. /subscribe EUR USD\n"
        "• /unsubscribe EUR [Target Currency] → remove subscription\n ==> ex. /unsubscribe EUR USD\n"
        "• /subscriptions → list your current subscriptions"
    )


# /rate EUR USD
async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("⚠️ Usage: /rate EUR USD")
        return

    base, target = [arg.upper() for arg in context.args]
    try:
        resp = requests.get(f"{API_BASE}/currency/{base}/{target}")
        if resp.status_code == 200:
            data = resp.json()
            rate_value = data.get("rate")
            await update.message.reply_text(f" 1 {base} = {rate_value} {target}")
        else:
            await update.message.reply_text("❌ Rate not found. Try again later.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# /subscribe EUR USD
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("⚠️ Usage: /subscribe EUR USD")
        return

    base, target = [arg.upper() for arg in context.args]
    user_id = str(update.effective_user.id)

    try:
        resp = requests.post(
            f"{API_BASE}/subscribe",
            params={"user_id": user_id, "base": base, "target": target},
        )
        if resp.status_code == 200:
            await update.message.reply_text(f"✅ Subscribed to {base}/{target}")
        else:
            await update.message.reply_text(f"❌ Failed to subscribe: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")
        
# /unsubscribe EUR USD
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /unsubscribe EUR USD")
        return

    base, target = context.args
    user_id = update.effective_user.id

    try:
        resp = requests.delete(
            f"{API_BASE}/unsubscribe",
            params={"user_id": user_id, "base": base.upper(), "target": target.upper()},
        )
        if resp.status_code == 200:
            await update.message.reply_text(resp.json().get("message"))
        else:
            await update.message.reply_text(f"❌ Failed to unsubscribe: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# /subscriptions
async def subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    try:
        resp = requests.get(f"{API_BASE}/subscriptions/{user_id}")
        if resp.status_code == 200:
            subs = resp.json().get("subscriptions", [])
            if not subs:
                await update.message.reply_text("ℹ️ You have no active subscriptions.")
                return

            msg = "📌 Your subscriptions:\n"
            for sub in subs:
                msg += f"- {sub['base']}/{sub['target']}\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"❌ Failed to fetch subscriptions: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# ------------------- Main -------------------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("subscriptions", subscriptions))

    app.run_polling()

if __name__ == "__main__":
    main()
