#  Green Wells AI Support Platform

An intelligent Telegram bot for customer support and feedback management, powered by Google's Gemini AI. This platform provides multilingual support, sentiment analysis, automated categorization, and visual analytics for customer feedback.

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Telegram Bot API](https://img.shields.io/badge/telegram--bot--api-20.5-blue.svg)

---

##  Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Analytics Dashboard](#analytics-dashboard)
- [Scheduled Tasks](#scheduled-tasks)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

##  Features

###  AI-Powered Support
- **Gemini AI Integration**: Intelligent responses using Google's Gemini 1.5 Flash model
- **Context-Aware Replies**: AI considers recent feedback history for personalized responses
- **Fallback Responses**: Graceful degradation when AI is unavailable

###  Multilingual Support
- **Auto-Detection**: Automatically detects user's language using `langdetect`
- **Real-Time Translation**: Translates messages using `deep-translator`
- **Supported Languages**: 100+ languages via Google Translate API
- **Bidirectional Translation**: Translates user messages to English for processing, then translates responses back

###  Sentiment Analysis
- **Real-Time Analysis**: Uses TextBlob for sentiment scoring
- **Three-Level Classification**:
  -  **Positive** (score > 0.1)
  -  **Neutral** (-0.1 to 0.1)
  -  **Negative** (score < -0.1)
- **Persistent Storage**: All feedback stored with sentiment metadata

###  Automatic Categorization
AI-powered categorization of feedback into:
- **Service Quality** - Customer service experiences
- **Product Issues** - Product-related problems
- **Billing** - Payment and billing inquiries
- **Technical Support** - Technical difficulties
- **General Inquiry** - General questions
- **Other** - Uncategorized feedback

###  Visual Analytics
- **Interactive Dashboard**: HTML dashboard with Chart.js visualizations
- **Bar Chart**: Feedback count by category
- **Pie Chart**: Category distribution percentages
- **Statistics Cards**: Total, Positive, Neutral, and Negative feedback counts
- **Recent Feedback Table**: Last 10 feedback entries with full details
- **Responsive Design**: Mobile-friendly layout

###  Automated Reporting
- **Daily Summaries**: Automated summary generation every day at 7 PM
- **AI-Generated Insights**: Gemini analyzes trends and patterns
- **Admin Notifications**: Summaries sent directly to admin via Telegram
- **Manual Triggers**: On-demand summary generation via `/summary` command

###  Interactive Feedback Collection
- **Inline Keyboards**: Quick sentiment selection buttons
- **Conversation Flow**: Guided feedback submission process
- **Admin Review**: All feedback forwarded to admin chat
- **User Confirmation**: Feedback receipt acknowledgment

---

##  Architecture

```
┌─────────────┐
│   Telegram  │
│    Users    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Telegram Bot API  │
│  (python-telegram)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│          Green Wells Bot Core           │
│  ┌───────────────────────────────────┐  │
│  │  Message Handler                  │  │
│  │  • Language Detection             │  │
│  │  • Translation                    │  │
│  │  • Sentiment Analysis             │  │
│  │  • Category Assignment            │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │  AI Response Generator (Gemini)   │  │
│  │  • Context-aware replies          │  │
│  │  • Summary generation             │  │
│  └───────────────────────────────────┘  │
│                                          │
│  ┌───────────────────────────────────┐  │
│  │  Scheduler (APScheduler)          │  │
│  │  • Daily summaries (7 PM)         │  │
│  └───────────────────────────────────┘  │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│   Data Storage      │
│  • feedback.json    │
│  • dashboard.html   │
└─────────────────────┘
```

---

##  Prerequisites

- **Python**: 3.12 or higher
- **Telegram**: A Telegram account and bot token
- **API Keys**:
  - Telegram Bot Token (from [@BotFather](https://t.me/botfather))
  - Google Gemini API Key (from [Google AI Studio](https://makersuite.google.com/app/apikey))

---

##  Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/green-wells-ai-support-platform.git
cd green-wells-ai-support-platform
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

---

##  Configuration

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If example exists, or create manually
```

### 2. Configure Environment Variables

Edit `.env` with your credentials:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
# Legacy name also supported:
# TOKEN="your_telegram_bot_token_here"

# Admin Configuration
ADMIN_CHAT_ID=your_telegram_user_id  # Get from @userinfobot

# AI Configuration
GEMINI_API_KEY="your_gemini_api_key_here"
```

**How to Get Your Credentials:**

1. **Telegram Bot Token**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the token provided

2. **Admin Chat ID**:
   - Message [@userinfobot](https://t.me/userinfobot) on Telegram
   - Copy your numeric user ID

3. **Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create new API key
   - Copy the key

### 3. Security Best Practices

```bash
# Add .env to .gitignore (should already be there)
echo ".env" >> .gitignore

# Set proper permissions
chmod 600 .env
```

---

##  Usage

### Starting the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Run the bot
python bot.py
```

You should see:
```
Bot is running...
```

### Stopping the Bot

Press `Ctrl+C` to gracefully shutdown.

---

## 📱 Commands

### User Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and show welcome message | `/start` |

### Admin Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/summary` | Generate and view daily feedback summary | `/summary` |
| `/dashboard` | Receive HTML analytics dashboard | `/dashboard` |
| `/test_summary` | Test summary generation without scheduling | `/test_summary` |

---

##  Project Structure

```
green-wells-ai-support-platform/
│
├── bot.py                  # Main bot application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── data/                  # Data storage directory
│   ├── feedback.json      # Feedback database
│   └── dashboard.html     # Generated analytics dashboard
│
└── venv/                  # Virtual environment (created during setup)
```

---

##  How It Works

### 1. User Interaction Flow

```
User sends message
    ↓
Language Detection (langdetect)
    ↓
Translation to English (deep-translator)
    ↓
Sentiment Analysis (TextBlob)
    ↓
AI Categorization (Gemini)
    ↓
Store in feedback.json
    ↓
Generate AI Response (Gemini)
    ↓
Translate Response back to user's language
    ↓
Send to user + Forward to admin
```

### 2. Feedback Data Structure

```json
{
  "timestamp": "2025-10-31T14:30:00",
  "name": "John Doe",
  "message": "Great service!",
  "sentiment": "positive",
  "category": "Service Quality",
  "user_id": 123456789
}
```

### 3. Sentiment Scoring

```python
# TextBlob returns polarity score: -1.0 to 1.0
score = TextBlob(text).sentiment.polarity

if score > 0.1:
    sentiment = "positive"    
elif score < -0.1:
    sentiment = "negative"    
else:
    sentiment = "neutral"     
```

---

##  Analytics Dashboard

The HTML dashboard (`data/dashboard.html`) provides:

### Statistics Cards
- **Total Feedback**: All-time count
- **Positive**: Green card with count
- **Neutral**: Orange card with count  
- **Negative**: Red card with count

### Visualizations

#### Bar Chart
- X-axis: Categories
- Y-axis: Feedback count
- Color-coded bars
- Hover for exact values

#### Pie Chart
- Category distribution
- Percentage labels
- Interactive slices
- Same color scheme as bar chart

### Recent Feedback Table
- Last 10 entries
- Columns: Name, Message, Sentiment, Category
- Color-coded sentiment badges
- Responsive layout

### Accessing the Dashboard

```bash
# Open in browser (Linux)
xdg-open data/dashboard.html

# Or request via Telegram
# Send /dashboard to the bot as admin
```

---

##  Scheduled Tasks

### Daily Summary (7 PM)

Automatically runs every day at 19:00 (7 PM) local time:

1. Analyzes last 24 hours of feedback
2. Generates AI summary with Gemini
3. Creates updated HTML dashboard
4. Sends summary + dashboard to admin via Telegram

### Manual Triggering

```bash
# In Telegram (as admin)
/summary        # Generate and send summary now
/test_summary   # Test without affecting schedule
```

---

##  Development

### Adding New Categories

Edit `categorize_feedback()` in `bot.py`:

```python
def categorize_feedback(text):
    prompt = f"""
    Categorize this feedback into ONE category:
    - Service Quality
    - Product Issues
    - Billing
    - Technical Support
    - General Inquiry
    - Your New Category  # Add here
    - Other

    Feedback: {text}
    Category:
    """
    # ... rest of function
```

### Customizing Scheduled Time

Edit `run_scheduler()` in `bot.py`:

```python
def run_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: asyncio.run(send_daily_summary(app)),
        'cron',
        hour=19,  # Change hour here (0-23)
        minute=0   # Change minute here (0-59)
    )
    scheduler.start()
```

### Modifying Dashboard Styling

Edit `generate_html_dashboard()` in `bot.py` to customize:
- Colors
- Chart types
- Layout
- Additional statistics

---

##  Troubleshooting

### Common Issues

#### 1. "Missing one or more environment variables"

**Solution**: Check your `.env` file:
```bash
cat .env
```
Ensure all required variables are set:
- `TELEGRAM_BOT_TOKEN` or `TOKEN`
- `ADMIN_CHAT_ID`
- `GEMINI_API_KEY` (optional but recommended)

#### 2. "Can't parse entities" Error

**Cause**: MarkdownV2 formatting issue

**Solution**: Already handled by `sanitize_and_escape_for_markdown()` function. If you still see this, ensure you're using the latest version of `bot.py`.

#### 3. Translation Not Working

**Check**:
```bash
pip show deep-translator langdetect
```

**Reinstall if needed**:
```bash
pip install --upgrade deep-translator langdetect
```

#### 4. Charts Not Displaying

**Solution**: Ensure internet connection (Chart.js loads from CDN). For offline use, download Chart.js:

```bash
mkdir -p static/js
curl https://cdn.jsdelivr.net/npm/chart.js -o static/js/chart.js
```

Then update the script tag in `generate_html_dashboard()`.

#### 5. Permission Denied Errors

**Solution**:
```bash
# Set proper permissions for data directory
chmod 755 data/
chmod 644 data/feedback.json
chmod 644 .env
```

---

##  Testing

### Unit Tests

Create `tests/test_bot.py`:

```python
import pytest
from bot import sanitize_and_escape_for_markdown, categorize_feedback

def test_markdown_escaping():
    text = "Test (with) special | characters"
    result = sanitize_and_escape_for_markdown(text)
    assert "\\" in result  # Should have escape characters

def test_categorization():
    feedback = "Your product is broken"
    category = categorize_feedback(feedback)
    assert category in ["Service Quality", "Product Issues", 
                       "Billing", "Technical Support", 
                       "General Inquiry", "Other"]
```

Run tests:
```bash
pytest tests/
```

### Manual Testing

```bash
# Test environment loading
python -c "from bot import TOKEN, ADMIN_CHAT_ID; print('OK')"

# Test Gemini integration
python -c "from bot import gemini_generate_reply; print(gemini_generate_reply('test'))"

# Test translation
python -c "from bot import detect_and_translate; print(detect_and_translate('Bonjour'))"
```

---

##  Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Use type hints where appropriate

---

##  License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Green Wells AI Support Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

- **Telegram Bot API** - Python Telegram Bot library
- **Google Gemini** - AI-powered responses and analysis
- **TextBlob** - Sentiment analysis
- **Deep Translator** - Multilingual support
- **Chart.js** - Interactive data visualizations
- **APScheduler** - Task scheduling

---

## Support

For issues, questions, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/mathncode-sid/green-wells-ai-support-platform/issues)
- **Email**: sidneybarakamuriuki1@gmail.com
- **Telegram**: @sidneybm7

---


*Making customer support intelligent, multilingual, and insightful.*
