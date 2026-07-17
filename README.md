# 🎬 Daily Regional & Global Entertainment News AI Agent 🍿
**Focus Regions:** 🇬🇭 Ghana | 🇳🇬 Nigeria | 🇺🇸 USA | 🇬🇧 UK | 🇨🇦 Canada & West Africa

A fully automated AI Agent that scours breaking entertainment, Afrobeats, Nollywood, and pop-culture news across **Ghana, Nigeria, West Africa, USA, UK, and Canada** daily. It uses an LLM (`OpenAI`, `Anthropic`, or `Google Gemini`) to convert each story into **four individual Social Media Post-ready formats** and delivers the complete suite right to your phone via **Telegram** (or optional WhatsApp/Twilio).

---

## ✨ Regional & Global Coverage

Our balanced scraper (`scrapers.py`) aggregates and round-robin selects top stories daily from:
- **🇬🇭 Ghana & West Africa**: *Ameyaw Debrah*, *Google News Ghana Entertainment*, and *West Africa Pop Culture* feeds (`#GhanaMusic #Accra #GhanaEnt`).
- **🇳🇬 Nigeria & Afrobeats**: *BellaNaija* and *Afrobeats & Nollywood Industry* feeds (`#Afrobeats #Nollywood #Lagos`).
- **🇺🇸 USA & Global Hollywood**: *Variety*, *Deadline Hollywood*, *Billboard*, and *The Hollywood Reporter*.
- **🇬🇧 United Kingdom**: *BBC Entertainment & Arts (UK)* and *UK Pop Culture* feeds (`#UKMusic #London #BritishTV`).
- **🇨🇦 Canada**: *Canadian Pop Culture & Entertainment* feeds (`#CanadaMusic #CanadianPop`).

---

## 📲 Exact Outputs Generated per Story

For every selected regional or global story, the AI outputs four individual copy formats ready for instant posting:
1. **🐦 X (Twitter) / Threads Post**: Regional hook, concise bullet points, character-conscious spacing, and targeted hashtags.
2. **📸 Instagram Caption / Carousel Copy**: Scroll-stopping headline hook, storytelling body, visual emoji bullets, call-to-action (CTA), and dedicated hashtag blocks.
3. **📱 TikTok / Reel Script (30–45 Sec Video)**: Spoken-word video script with stage directions and time-stamped cues (`[0:00 - 0:03 | VISUAL HOOK]`, `[BODY BREAKDOWN]`, `[OUTRO & CTA]`).
4. **💬 Facebook / Community Page Post**: Conversational tone sparking discussion and community debate.

---

## 🛠️ How to Run Your Agent (3 Simple Methods)

### Method 1: Run Right Now on Your Computer (Local Run)

1. **Download / Clone these Workspace Files** to a folder on your computer.
2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Your `.env` Credentials**:
   Copy `.env.example` to `.env` and enter your Telegram bot credentials:
   ```bash
   cp .env.example .env
   ```
4. **Run the Agent**:
   ```bash
   python entertainment_agent.py
   ```
   *The agent will immediately scrape stories across Ghana, Nigeria, USA, UK, and Canada, format them into all 4 social media styles, save a copy to `latest_digest.md`, and ping your phone!*

---

### Method 2: 100% Free Daily Cloud Automation (GitHub Actions)

You can deploy this agent to run automatically every single morning without keeping your personal computer running:

1. **Upload to GitHub**: Create a private repository on [GitHub.com](https://github.com) and push these project files into it.
2. **Add Your Secrets**: Go to your repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**. Add:
   - `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY` / `GEMINI_API_KEY`)
   - `TELEGRAM_BOT_TOKEN` (Your token from `@BotFather`)
   - `TELEGRAM_CHAT_ID` (Your ID from `@userinfobot`)
3. **Automatic Execution**: The included `.github/workflows/daily_news_agent.yml` file automatically wakes up and runs your agent every morning at **08:00 UTC** (08:00 AM Accra / GMT time!).
   - *Want to run it instantly in the cloud?* Go to the **Actions** tab on GitHub, click **🎬 Daily Entertainment News AI Agent**, and click **Run workflow**.

---

### Method 3: Deploy on a 24/7 Cloud Server (VPS / Modal / Railway)

If you prefer running it on a cloud VPS or background worker:
```bash
# Run via cron job every day at 8:00 AM local time on Linux/VPS
0 8 * * * /usr/bin/python3 /path/to/entertainment_agent.py >> /var/log/entertainment_agent.log 2>&1
```

---

## 📲 How to Connect Your Phone via Telegram (Takes 2 Minutes)

Telegram is the recommended delivery channel because it is completely free, supports rich formatting, and pushes instantly to iOS and Android lock screens.

1. **Create your Bot**:
   - Open Telegram and search for **`@BotFather`** (the official Telegram bot creator with the blue checkmark).
   - Send the message `/newbot`.
   - Choose a name (e.g., *Ghana & Afrobeats Daily Scoop*) and username ending in `bot` (e.g., *accra_popculture_bot*).
   - Copy the **HTTP API Token** (`TELEGRAM_BOT_TOKEN`).

2. **Get your Chat ID**:
   - Open Telegram and search for **`@userinfobot`** (or `@IDBot`).
   - Send `/start`. Copy the numeric **Id** it replies with (`TELEGRAM_CHAT_ID`).

3. **Start your Bot**:
   - Open your new bot in Telegram (`@accra_popculture_bot`) and press **Start**. *(Important: Bots cannot message you first unless you initiate the chat!)*

---

## 📁 Project Structure

```text
├── entertainment_agent.py    # Main script: orchestrates scraping, LLM formatting, and delivery
├── scrapers.py               # Region-balanced news aggregator across 12+ Ghana, Nigeria, UK & US feeds
├── prompts.py                # LLM system & user prompts guaranteeing the 4-format output structure
├── notifier.py               # Telegram Bot API client with automatic message splitting + Twilio fallback
├── config.py                 # Central configuration for regional feeds, time windows, and model settings
├── requirements.txt          # Python dependencies (requests, beautifulsoup4, feedparser, openai, etc.)
├── .github/
│   └── workflows/
│       └── daily_news_agent.yml  # Daily cron schedule for automated cloud execution
└── README.md                 # Documentation and setup guide
```
