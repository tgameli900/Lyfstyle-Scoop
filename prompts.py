"""
prompts.py - LLM System and Generation Prompts for Social Media Formatting.

This module structures the prompt sent to the LLM (OpenAI/Anthropic/Gemini) so that
every regional or global entertainment story is converted into multiple ready-to-post
social media formats tailored for Ghana, Nigeria, USA, UK, Canada & West African fans.
"""

from config import SOCIAL_MEDIA_FORMATS

SYSTEM_PROMPT = """You are a world-class Social Media Editor & Pop Culture Lead specializing in global and African entertainment (with deep expertise in Ghana pop culture, Afrobeats/Lagos/Nollywood, UK Grime/Pop, Canadian culture, and US Hollywood).
Your job is to take raw entertainment news stories and convert EACH individual story into a comprehensive "Social Media Post-Ready Suite".

For every selected news story, you must generate exactly four individual, highly polished formats that the user can copy-paste and publish immediately:
1. 🐦 X (Twitter) / Threads Post
2. 📸 Instagram Caption / Carousel Copy
3. 📱 TikTok / Instagram Reel Spoken Video Script (with visual cues)
4. 💬 Facebook / Community Page Post

GUIDELINES FOR OUTPUT:
- Maintain complete factual accuracy from the source article. Never invent or hallucinate facts or quotes.
- Use engaging, punchy, scroll-stopping hooks tailored to the story's region (e.g., if it's a Ghana or Nigeria story, use authentic energy like "Accra we need to talk about this..." or "Big news for Afrobeats fans right now...").
- Format clearly with clean spacing, emojis, and visual dividers.
- Output clean Markdown formatting so it renders beautifully when sent to the user's phone via Telegram/mobile notification.
"""

def build_digest_prompt(stories: list) -> str:
    """
    Builds the user prompt containing the top trending regional and global
    entertainment stories to be formatted into individual social media suites.
    """
    prompt = (
        f"Below are the top {len(stories)} trending entertainment and pop culture news stories "
        "scraped from major regional and global industry publications today across Ghana, Nigeria, USA, UK, and Canada.\n\n"
        "For EACH story, produce the full, individual 'Social Media Post-Ready Suite' containing all 4 formats: "
        "(1) X/Threads, (2) Instagram Caption, (3) TikTok/Reel Script, and (4) Facebook Community Post.\n\n"
        "====================================================\n"
        "RAW STORIES DATA:\n"
        "====================================================\n\n"
    )

    for i, story in enumerate(stories, 1):
        prompt += (
            f"STORY #{i}: {story.get('title')}\n"
            f"Region/Focus: {story.get('region')} | Source: {story.get('source')}\n"
            f"Published: {story.get('published')} | URL: {story.get('url')}\n"
            f"Summary/Excerpt:\n{story.get('summary')}\n\n"
            f"----------------------------------------------------\n\n"
        )

    prompt += (
        "\n====================================================\n"
        "REQUIRED OUTPUT FORMAT (Markdown):\n"
        "====================================================\n"
        "Output each story clearly using the structure below so it splits nicely on mobile screens:\n\n"
        "🎬 **STORY #1: [Catchy Headline]**\n"
        "🌍 *Region: [Region]* | 📰 *Source: [Source Name]* | 🔗 [Read Original Article](URL)\n\n"
        "### 🐦 1. X (Twitter) / Threads Post\n"
        "[Insert ready-to-post X/Threads content with bullet points and 2-3 regional/trending hashtags]\n\n"
        "### 📸 2. Instagram Caption / Carousel Copy\n"
        "[Insert ready-to-post Instagram caption with hook, emojis, body, CTA, and hashtag block]\n\n"
        "### 📱 3. TikTok / Reel Spoken Video Script\n"
        "**[0:00 - 0:03 | VISUAL HOOK]:** [Visual cue or text overlay description]\n"
        "**[AUDIO]:** [Spoken hook line]\n\n"
        "**[0:03 - 0:25 | BODY BREAKDOWN]:** [Visual cuts/B-roll instructions]\n"
        "**[AUDIO]:** [Spoken explanation of what happened & quotes]\n\n"
        "**[0:25 - 0:35 | OUTRO & CTA]:** [Visual cue]\n"
        "**[AUDIO]:** [Engaging question to viewers]\n\n"
        "### 💬 4. Facebook / Community Post\n"
        "[Insert conversational community post prompting discussion and reactions]\n\n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
        "Repeat this exact structure for all selected stories. Make the writing sharp, viral-worthy, and ready to post!"
    )

    return prompt
