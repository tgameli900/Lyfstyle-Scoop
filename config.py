"""
config.py - Configuration & Settings for the Daily Entertainment News AI Agent.

Handles environment variables, RSS feeds of top global and regional entertainment
publications (Ghana, Nigeria, West Africa, USA, UK, and Canada), default schedule
settings, and target social media format definitions.
"""

import os
from dotenv import load_dotenv

# Load local .env file if running locally or in test mode
load_dotenv()

# ==========================================
# 1. API & NOTIFICATION CONFIGURATION
# ==========================================

# LLM Provider selection: 'openai', 'anthropic', or 'gemini'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# LLM Model choices
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Telegram Bot Credentials (Primary Delivery Method)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Optional WhatsApp/Twilio Fallback
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
TWILIO_TO_NUMBER = os.getenv("TWILIO_TO_NUMBER", "")


# ==========================================
# 2. NEWS SCRAPING & FEED CONFIGURATION
# ==========================================

# Maximum number of top trending stories to process per daily digest
# Default is set to 6 to allow balanced representation across Ghana, Nigeria, USA, UK, Canada & West Africa
MAX_STORIES_PER_DIGEST = int(os.getenv("MAX_STORIES_PER_DIGEST", "6"))

# Time window in hours to check for news articles (default: last 24 hours)
HOURS_WINDOW = int(os.getenv("HOURS_WINDOW", "24"))

# Region-Categorized Entertainment & Pop Culture RSS Feeds
ENTERTAINMENT_RSS_FEEDS = [
    # --- 🇬🇭 GHANA & WEST AFRICA ---
    {
        "name": "Ameyaw Debrah (Ghana)",
        "url": "https://ameyawdebrah.com/feed/",
        "region": "Ghana & West Africa",
        "category": "Ghanaian Celebrity & Pop Culture"
    },
    {
        "name": "Google News: Ghana Entertainment",
        "url": "https://news.google.com/rss/search?q=Ghana+entertainment+music+celebrity&hl=en-US&gl=US&ceid=US:en",
        "region": "Ghana & West Africa",
        "category": "Ghana Music, Movies & Stars"
    },
    {
        "name": "Google News: West Africa Pop Culture",
        "url": "https://news.google.com/rss/search?q=West+Africa+music+entertainment+celebrity&hl=en-US&gl=US&ceid=US:en",
        "region": "Ghana & West Africa",
        "category": "Pan-West African Entertainment"
    },

    # --- 🇳🇬 NIGERIA (AFROBEATS & NOLLYWOOD) ---
    {
        "name": "BellaNaija",
        "url": "https://www.bellanaija.com/feed/",
        "region": "Nigeria & Afrobeats",
        "category": "African Lifestyle, Nollywood & Celebrities"
    },
    {
        "name": "Google News: Nigeria Afrobeats & Nollywood",
        "url": "https://news.google.com/rss/search?q=Nigeria+Afrobeats+Nollywood+entertainment&hl=en-US&gl=US&ceid=US:en",
        "region": "Nigeria & Afrobeats",
        "category": "Afrobeats Music & Nollywood Industry"
    },

    # --- 🇺🇸 USA & GLOBAL HOLLYWOOD ---
    {
        "name": "Variety",
        "url": "https://variety.com/feed/",
        "region": "USA & Global",
        "category": "Hollywood Film & TV Industry"
    },
    {
        "name": "Deadline Hollywood",
        "url": "https://deadline.com/feed/",
        "region": "USA & Global",
        "category": "Breaking Hollywood & Box Office News"
    },
    {
        "name": "Billboard",
        "url": "https://www.billboard.com/feed/",
        "region": "USA & Global",
        "category": "Global Music Charts & Industry"
    },
    {
        "name": "The Hollywood Reporter",
        "url": "https://www.hollywoodreporter.com/feed/",
        "region": "USA & Global",
        "category": "Film/TV Industry News"
    },

    # --- 🇬🇧 UNITED KINGDOM ---
    {
        "name": "BBC Entertainment & Arts (UK)",
        "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        "region": "United Kingdom",
        "category": "British TV, Music & Culture"
    },
    {
        "name": "Google News: UK Entertainment",
        "url": "https://news.google.com/rss/search?q=UK+entertainment+music+celebrity&hl=en-GB&gl=GB&ceid=GB:en",
        "region": "United Kingdom",
        "category": "UK Pop Culture & Celebrities"
    },

    # --- 🇨🇦 CANADA ---
    {
        "name": "Google News: Canada Entertainment",
        "url": "https://news.google.com/rss/search?q=Canada+entertainment+music+celebrity&hl=en-CA&gl=CA&ceid=CA:en",
        "region": "Canada",
        "category": "Canadian Music, Film & Pop Culture"
    }
]


# ==========================================
# 3. SOCIAL MEDIA FORMAT DEFINITIONS
# ==========================================

SOCIAL_MEDIA_FORMATS = [
    {
        "key": "x_threads",
        "title": "🐦 X (Twitter) / Threads Post",
        "description": "Short, punchy, high-engagement hook. Bullet points for quick reading. Character-conscious. Includes 2-3 trending region/topic hashtags."
    },
    {
        "key": "instagram_caption",
        "title": "📸 Instagram Caption / Carousel Copy",
        "description": "Engaging hook on the first line. Storytelling body explaining what happened and why it matters. Emojis for visual spacing. Call-to-action (CTA) asking followers a question to boost engagement. Separated hashtag block at the bottom (5-8 relevant tags including regional tags like #GhanaMusic #Afrobeats #Nollywood #Hollywood etc.)."
    },
    {
        "key": "tiktok_reel_script",
        "title": "📱 TikTok / Instagram Reel Script (30-45 Sec Video)",
        "description": "Spoken-word video script with visual cues. Format: [VISUAL/HOOK], [BODY/GOSSIP BREAKDOWN], [OUTRO/CTA]. Exact time stamps or stage directions included."
    },
    {
        "key": "facebook_community",
        "title": "💬 Facebook / Community Page Post",
        "description": "Conversational, relatable tone tailored for entertainment fans or pop-culture community groups. Encourages debate and opinion-sharing."
    }
]
