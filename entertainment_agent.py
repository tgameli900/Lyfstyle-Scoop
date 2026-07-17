"""
entertainment_agent.py - Main Orchestrator for the Daily Entertainment News AI Agent.

This script scours regional and global entertainment publications across Ghana, Nigeria,
USA, UK, Canada & West Africa, selects a balanced set of trending stories, uses an LLM
(OpenAI, Anthropic, or Gemini) to generate individual social media post suites, and
delivers the final digest straight to your phone!
"""

import os
import time
import datetime
from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_STORIES_PER_DIGEST
)
from scrapers import get_top_entertainment_news
from prompts import SYSTEM_PROMPT, build_digest_prompt
from notifier import notify_user


def generate_social_media_digest(stories: list) -> str:
    """
    Calls the configured LLM to format the selected news stories into individual
    social media suites. Includes an automatic mock/offline fallback if no API key is set.
    """
    if not stories:
        return "🛑 No recent entertainment stories found within the selected time window today."

    user_prompt = build_digest_prompt(stories)

    # 1. OpenAI Generation
    if LLM_PROVIDER == "openai" and OPENAI_API_KEY and OPENAI_API_KEY != "YOUR_OPENAI_API_KEY":
        try:
            print(f"[*] Generating multi-platform social media digest using OpenAI ({OPENAI_MODEL})...")
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=3500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[!] OpenAI API Error: {e}. Falling back to internal mock/template generator...")

    # 2. Anthropic Generation
    elif LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "YOUR_ANTHROPIC_API_KEY":
        try:
            print(f"[*] Generating multi-platform social media digest using Anthropic ({ANTHROPIC_MODEL})...")
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                system=SYSTEM_PROMPT,
                max_tokens=3500,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"[!] Anthropic API Error: {e}. Falling back to internal mock/template generator...")

    # 3. Google Gemini Generation
    elif LLM_PROVIDER == "gemini" and GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
        try:
            print(f"[*] Generating multi-platform social media digest using Google Gemini ({GEMINI_MODEL})...")
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(user_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[!] Gemini API Error: {e}. Falling back to internal mock/template generator...")

    # 4. Fallback / Mock Generator (Used when testing without API keys)
    print("[*] NOTICE: No active LLM API key detected in environment. Using built-in local template generator...")
    return generate_fallback_digest(stories)


def generate_fallback_digest(stories: list) -> str:
    """
    Generates a beautifully formatted, realistic multi-platform social media digest
    directly from the scraped stories if no LLM API key is present.
    """
    today_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
    output = f"🌟 **DAILY REGIONAL & GLOBAL ENTERTAINMENT SCOOP** 🌟\n📅 *{today_str}*\n"
    output += "Focus Regions: 🇬🇭 Ghana | 🇳🇬 Nigeria | 🇺🇸 USA | 🇬🇧 UK | 🇨🇦 Canada\n\n"
    output += "Here is your ready-to-post social media breakdown across X, Instagram, TikTok, and Facebook:\n\n"
    output += "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"

    for i, story in enumerate(stories, 1):
        title = story.get("title", "Breaking Entertainment News")
        source = story.get("source", "Industry Source")
        region = story.get("region", "Global")
        url = story.get("url", "https://variety.com")
        summary = story.get("summary", "Top industry updates and celebrity news making waves across entertainment today.")
        if len(summary) > 260:
            summary = summary[:257] + "..."

        # Determine regional hashtags based on the region
        reg_tag = "PopCulture"
        if "Ghana" in region:
            reg_tag = "GhanaMusic #Accra #GhanaEnt"
        elif "Nigeria" in region:
            reg_tag = "Afrobeats #Nollywood #Lagos"
        elif "UK" in region or "United Kingdom" in region:
            reg_tag = "UKMusic #London #BritishTV"
        elif "Canada" in region:
            reg_tag = "CanadaMusic #CanadianPop"
        else:
            reg_tag = "Hollywood #EntertainmentNews"

        words = [w for w in title.split() if len(w) > 3 and w.isalnum()]
        tag1 = words[0] if words else "News"
        tag2 = words[1] if len(words) > 1 else "Trending"

        output += f"🎬 **STORY #{i}: {title}**\n"
        output += f"🌍 *Region: {region}* | 📰 *Source: {source}* | 🔗 [Read Original Article]({url})\n\n"

        # 1. X/Threads
        output += f"### 🐦 1. X (Twitter) / Threads Post\n"
        output += f"🚨 BREAKING [{region.upper()}]: {title}!\n\n"
        output += f"Here is the update according to {source}:\n"
        output += f"• {summary}\n"
        output += f"• This is trending right now across social media.\n\n"
        output += f"What are your thoughts on this? 👇\n\n"
        output += f"#{tag1} #{tag2} #{reg_tag}\n\n"

        # 2. Instagram
        output += f"### 📸 2. Instagram Caption / Carousel Copy\n"
        output += f"✨ MAJOR {region.upper()} SCOOP TODAY ✨\n\n"
        output += f"{title} 😱\n\n"
        output += f"Here's the rundown from {source}:\n"
        output += f"{summary}\n\n"
        output += f"💭 Drop your genuine thoughts in the comments below! Did you see this coming or are you completely surprised?\n\n"
        output += f"📌 Save this post & share with a pop culture obsessed friend!\n"
        output += f"•\n•\n•\n"
        output += f"#{tag1} #{tag2} #{reg_tag} #CelebrityNews #PopCulture #Trending #DailyScoop\n\n"

        # 3. TikTok / Reel Script
        output += f"### 📱 3. TikTok / Reel Spoken Video Script\n"
        output += f"**[0:00 - 0:03 | VISUAL HOOK]:** *Green screen over headline graphic of '{title}'. Host points to headline with energy.*\n"
        output += f"**[AUDIO]:** \"If you follow what's happening right now in {region}, stop scrolling because this update from {source} is huge.\"\n\n"
        output += f"**[0:03 - 0:25 | BODY BREAKDOWN]:** *Cut to fast B-roll photos/clips while host narrates text overlay with bullet points.*\n"
        output += f"**[AUDIO]:** \"So according to {source}, {summary} Everyone online is talking about where this goes from here.\"\n\n"
        output += f"**[0:25 - 0:35 | OUTRO & CTA]:** *Host zooms back to full camera with questioning gesture.*\n"
        output += f"**[AUDIO]:** \"Let me know your thoughts in the comments right now, and hit follow for daily updates from Ghana, Nigeria, UK, USA & across the world!\"\n\n"

        # 4. Facebook
        output += f"### 💬 4. Facebook / Community Post\n"
        output += f"📢 Pop Culture & Entertainment Check-In ({region})!\n\n"
        output += f"Did everyone see the major update from {source} regarding {title}?\n\n"
        output += f"{summary}\n\n"
        output += f"Let's get a discussion going — how do you feel about this development? Drop your reactions below! 👇💬\n\n"

        output += f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"

    return output


def save_digest_to_file(digest_text: str, filename: str = "latest_digest.md") -> str:
    """Saves the latest generated digest to a markdown file in the workspace."""
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(digest_text)
    print(f"[+] Saved full daily digest copy to: {filepath}")
    return filepath


def main():
    print("========================================================================")
    print("      🎬 DAILY REGIONAL & GLOBAL ENTERTAINMENT AI AGENT STARTED 🍿      ")
    print("        Focus: Ghana 🇬🇭 | Nigeria 🇳🇬 | USA 🇺🇸 | UK 🇬🇧 | Canada 🇨🇦        ")
    print("========================================================================")
    start_time = time.time()

    # 1. Scour & Fetch Balanced News Stories Across Regions
    stories = get_top_entertainment_news(max_stories=MAX_STORIES_PER_DIGEST)

    # 2. Generate Multi-Platform Social Media Suite
    print("\n[*] Processing stories with AI to generate Social Media suites...")
    digest_text = generate_social_media_digest(stories)

    # 3. Save a persistent copy locally
    save_digest_to_file(digest_text)

    # 4. Notify User on Mobile (Telegram / WhatsApp)
    notify_user(digest_text)

    elapsed = time.time() - start_time
    print(f"\n[✓] Agent execution completed successfully in {elapsed:.2f} seconds.")
    print("========================================================================\n")


if __name__ == "__main__":
    main()
