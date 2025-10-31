from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from textblob import TextBlob
from dotenv import load_dotenv
import google.generativeai as genai
import json
from datetime import datetime, timedelta
import os, schedule, time, threading, asyncio, re
from pathlib import Path
from langdetect import detect
from telegram.helpers import escape_markdown
from flask import Flask

# optional deep-translator import
try:
    from deep_translator import GoogleTranslator
    translator = GoogleTranslator()
except Exception as e:
    print(f"Warning: translation unavailable, disabled: {e}")
    translator = None


# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv(dotenv_path=Path("/home/mathncode-sid/green-wells-ai-support-platform/.env"))

def _clean_env_var(key, alt=None):
    raw = os.getenv(key)
    if not raw and alt:
        raw = os.getenv(alt)
    if raw is None:
        return None
    raw = str(raw).strip()
    if "#" in raw:
        raw = raw.split("#", 1)[0].strip()
    if len(raw) >= 2 and ((raw[0] == raw[-1]) and raw[0] in ("'", '"')):
        raw = raw[1:-1]
    return raw


# --- CONFIGURATION ---
TOKEN = _clean_env_var("TELEGRAM_BOT_TOKEN", alt="TOKEN")
ADMIN_CHAT_ID_RAW = _clean_env_var("ADMIN_CHAT_ID")
GEMINI_API_KEY = _clean_env_var("GEMINI_API_KEY")

ADMIN_CHAT_ID = None
if ADMIN_CHAT_ID_RAW:
    try:
        ADMIN_CHAT_ID = int(ADMIN_CHAT_ID_RAW)
    except ValueError:
        print(f"Warning: ADMIN_CHAT_ID value '{ADMIN_CHAT_ID_RAW}' is not an integer.")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not set; AI features will be limited.")


# --- GEMINI HELPER ---
def gemini_generate_reply(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return "I'm here to help. Could you please clarify a bit more?"
    except Exception as e:
        print(f"Gemini error: {e}")
        return None


def sanitize_and_escape_for_markdown(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"[\x00-\x1f\x7f]", "", str(text))
    try:
        return escape_markdown(text, version=2)
    except Exception:
        return re.sub(r"[\[\]\(\)\`\\]", "", text)


# --- MULTILINGUAL HELPER ---
def detect_and_translate(text):
    try:
        lang = detect(text)
        if lang != "en" and translator:
            translated = translator.translate(text, source=lang, target='en')
            return translated, lang
        return text, lang if lang else "en"
    except Exception:
        return text, "en"


# --- FEEDBACK UTILITIES ---
def categorize_feedback(text):
    try:
        categories = ["LPG & Refills", "Station Service", "Pricing & Billing",
                      "Delivery & Logistics", "Complaints", "Other"]
        keyword_map = {
            "lpg": "LPG & Refills", "gas": "LPG & Refills",
            "fuel": "Pricing & Billing", "price": "Pricing & Billing",
            "cost": "Pricing & Billing", "station": "Station Service",
            "car wash": "Station Service", "delivery": "Delivery & Logistics",
            "truck": "Delivery & Logistics", "complaint": "Complaints",
            "rude": "Complaints", "bad": "Complaints"
        }
        for word, cat in keyword_map.items():
            if word in text.lower():
                return cat
        prompt = f"Classify this feedback into one of the following categories: {', '.join(categories)}.\nFeedback: {text}"
        ai_reply = gemini_generate_reply(prompt)
        for c in categories:
            if c.lower() in ai_reply.lower():
                return c
        return "Other"
    except Exception:
        return "Other"


def log_feedback(user, message, sentiment, category):
    data_file = "data/feedback.json"
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            json.dump([], f)
    with open(data_file, "r") as f:
        feedback_data = json.load(f)
    feedback_data.append({
        "user_id": user.id,
        "name": user.first_name,
        "message": message,
        "sentiment": sentiment,
        "category": category,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(data_file, "w") as f:
        json.dump(feedback_data, f, indent=4)


def generate_html_dashboard():
    data_file = "data/feedback.json"
    if not os.path.exists(data_file):
        return
    with open(data_file, "r") as f:
        data = json.load(f)
    if not data:
        return
    total = len(data)
    pos = len([d for d in data if d["sentiment"] == "Positive"])
    neg = len([d for d in data if d["sentiment"] == "Negative"])
    neu = len([d for d in data if d["sentiment"] == "Neutral"])
    categories = {}
    for d in data:
        categories[d.get("category", "Other")] = categories.get(d.get("category", "Other"), 0) + 1
    category_labels = list(categories.keys())
    category_counts = list(categories.values())
    html = f"""<!DOCTYPE html>
    <html><head>
        <title>Green Wells Energies Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 40px; }}
            .card {{ background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            h1 {{ color: #2e7d32; }}
            canvas {{ max-width: 600px; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <h1>🛢️ Green Wells Energies - Feedback Dashboard</h1>
        <div class="card">
            <h3>Feedback Summary</h3>
            <p><b>Total Feedback:</b> {total}</p>
            <p><b>Positive:</b> {pos} | <b>Neutral:</b> {neu} | <b>Negative:</b> {neg}</p>
        </div>
        <div class="card">
            <h3>Feedback by Category</h3>
            <canvas id="barChart"></canvas>
        </div>
        <div class="card">
            <h3>Category Distribution</h3>
            <canvas id="pieChart"></canvas>
        </div>
        <script>
            const labels = {json.dumps(category_labels)};
            const counts = {json.dumps(category_counts)};
            new Chart(document.getElementById('barChart'), {{
                type: 'bar',
                data: {{ labels: labels, datasets: [{{ label: 'Feedback Count', data: counts, backgroundColor: 'rgba(46,125,50,0.7)' }}] }},
                options: {{ responsive: true }}
            }});
            new Chart(document.getElementById('pieChart'), {{
                type: 'pie',
                data: {{ labels: labels, datasets: [{{ data: counts, backgroundColor: ['#2e7d32','#66bb6a','#81c784','#a5d6a7','#c8e6c9'] }}] }},
                options: {{ responsive: true }}
            }});
        </script>
    </body></html>"""
    with open("data/dashboard.html", "w") as f:
        f.write(html)


# --- DAILY SUMMARY ---
def summarize_feedback():
    data_file = "data/feedback.json"
    if not os.path.exists(data_file):
        return "No feedback data available yet."
    with open(data_file, "r") as f:
        data = json.load(f)
    if not data:
        return "No feedback data to summarize."
    now = datetime.now()
    last_24h = [d for d in data if datetime.strptime(
        d["timestamp"], "%Y-%m-%d %H:%M:%S") >= now - timedelta(hours=24)]
    if not last_24h:
        return "No feedback received in the last 24 hours."
    total = len(last_24h)
    pos = len([d for d in last_24h if d["sentiment"] == "Positive"])
    neg = len([d for d in last_24h if d["sentiment"] == "Negative"])
    neu = len([d for d in last_24h if d["sentiment"] == "Neutral"])
    prompt = (
        f"You are a customer insights analyst for Green Wells Energies. "
        f"Here is customer feedback from the past 24 hours:\n\n{json.dumps(last_24h[-30:], indent=2)}\n\n"
        f"Write a short, professional summary including key trends, sentiment, and recommendations."
    )
    ai_summary = gemini_generate_reply(prompt)
    ai_summary = sanitize_and_escape_for_markdown(ai_summary) if ai_summary else None
    generate_html_dashboard()
    summary_text = (
        r"*Daily Feedback Summary \(Last 24 Hours\)*" + "\n\n"
        f"Total feedback: {total}\n"
        f"Positive: {pos} \\| Neutral: {neu} \\| Negative: {neg}\n\n"
        f"AI Summary:\n{ai_summary if ai_summary else 'No AI summary available\\.'}"
    )
    return summary_text


async def send_daily_summary_via_app(app):
    summary_text = summarize_feedback()
    await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary_text)
    dashboard_path = "data/dashboard.html"
    if os.path.exists(dashboard_path):
        await app.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=open(dashboard_path, "rb"),
            filename="GreenWells_Dashboard.html",
            caption="📊 Daily Analytics Dashboard"
        )


def run_scheduler(app):
    async def job():
        await send_daily_summary_via_app(app)
    def sync_job():
        asyncio.run(job())
    schedule.every().day.at("19:00").do(sync_job)
    while True:
        schedule.run_pending()
        time.sleep(60)


# --- TELEGRAM HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Green Wells Energies Support.\n\n"
        "I am here to assist you with LPG, fuel, or station services.\n"
        "Type your message below, and I will respond shortly or connect you to a live agent."
    )


async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    summary_text = summarize_feedback()
    await update.message.reply_text(summary_text)
    dashboard_path = "data/dashboard.html"
    if os.path.exists(dashboard_path):
        await update.message.reply_document(open(dashboard_path, "rb"), filename="GreenWells_Dashboard.html")


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_CHAT_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    dashboard_path = "data/dashboard.html"
    if not os.path.exists(dashboard_path):
        await update.message.reply_text("No dashboard yet. Run /summary first.")
        return
    await update.message.reply_document(open(dashboard_path, "rb"), filename="GreenWells_Dashboard.html")


# --- Handle Messages & Admin Replies ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text, user_lang = detect_and_translate(update.message.text)
    polarity = TextBlob(text).sentiment.polarity

    if "refill" in text.lower():
        response = "You can refill your LPG cylinder at any Green Wells station near you, including Kisumu, Ugunja, or Mbita."
    elif "location" in text.lower():
        response = "We currently operate in Kisumu, Ugunja, and Mbita."
    elif "price" in text.lower() or "cost" in text.lower():
        response = "Fuel prices vary by location. Please visit your nearest Green Wells station for accurate pricing."
    elif polarity < -0.2 or any(w in text.lower() for w in ["bad", "poor", "rude", "slow", "terrible", "complaint"]):
        response = "I'm sorry to hear that. I will notify our support team right away."

        keyboard = [[InlineKeyboardButton(f"Reply to {user.first_name}", callback_data=f"reply_{user.id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"🚨 New negative feedback from {user.first_name} (id: {user.id}):\n\n{text}",
            reply_markup=reply_markup
        )
    else:
        prompt = (
            f"You are Green Wells Energies' virtual support assistant. "
            f"Respond naturally and professionally to this customer message as the company would. "
            f"Provide only one short, friendly message — do not list options or meta commentary.\n\n"
            f"Customer message: {text}\n\n"
            f"Tone: warm, concise, confident, and helpful."
        )
        ai_reply = gemini_generate_reply(prompt)
        response = ai_reply if ai_reply else "Thank you for your message."

    sentiment = "Positive" if polarity > 0.2 else "Negative" if polarity < -0.2 else "Neutral"
    category = categorize_feedback(text)
    log_feedback(user, text, sentiment, category)

    if user_lang != "en" and translator:
        try:
            response = translator.translate(response, source='en', target=user_lang)
        except Exception:
            pass

    await update.message.reply_text(response)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("reply_"):
        user_id = int(query.data.split("_")[1])
        context.user_data["reply_to_id"] = user_id
        await query.message.reply_text(
            f"Please type your reply below starting with /send. Example:\n\n/send Your message here"
        )


async def send_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == ADMIN_CHAT_ID:
        if "reply_to_id" not in context.user_data:
            await update.message.reply_text("Please click a 'Reply to user' button first.")
            return

        user_id = context.user_data["reply_to_id"]
        msg = update.message.text.replace("/send", "", 1).strip()

        await context.bot.send_message(user_id, f"Support Agent: {msg}")
        await update.message.reply_text("✅ Message sent to user.")
        del context.user_data["reply_to_id"]


# --- MAIN APP ---
def main():
    if not TOKEN or not ADMIN_CHAT_ID:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN/TOKEN or ADMIN_CHAT_ID in .env file.")
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set; AI features will be limited.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("summary", summary))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("send", send_reply))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    threading.Thread(target=run_scheduler, args=(app,), daemon=True).start()

    web_app = Flask(__name__)

    @web_app.route('/')
    def health():
        return "✅ Green Wells Energies AI Bot is running!", 200

    def run_flask():
        port = int(os.environ.get("PORT", 8080))
        web_app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask, daemon=True).start()

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
