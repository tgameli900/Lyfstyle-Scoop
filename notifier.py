"""
notifier.py - Mobile Delivery & Notification Engine (Telegram & WhatsApp/Twilio).

Handles delivering the generated social media digest straight to the user's phone.
Automatically handles long message splitting (Telegram limit is 4096 chars per message)
and gracefully falls back to mock/log output if API keys are not yet configured.
"""

import requests
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_FROM_NUMBER,
    TWILIO_TO_NUMBER
)


def split_message(text: str, max_length: int = 4000) -> list:
    """
    Splits a long message cleanly at story dividers (`➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖` or double newlines)
    so that each piece fits comfortably inside Telegram's 4096 character limit.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    # Try splitting by our story divider line first
    divider = "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
    if divider in text:
        parts = text.split(divider)
        current_chunk = ""
        for part in parts:
            part_stripped = part.strip()
            if not part_stripped:
                continue
            # If adding this part exceeds max_length, push current_chunk and start new
            if len(current_chunk) + len(part_stripped) + len(divider) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip() + f"\n\n{divider}")
                current_chunk = part_stripped
            else:
                if current_chunk:
                    current_chunk += f"\n\n{divider}\n\n" + part_stripped
                else:
                    current_chunk = part_stripped
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    # Fallback: split by paragraphs
    paragraphs = text.split("\n\n")
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk) + len(p) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = p
        else:
            current_chunk = (current_chunk + "\n\n" + p).strip()
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def send_telegram_message(text: str, bot_token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID) -> bool:
    """
    Sends text to the user's Telegram chat via Bot API.
    Splits message into clean chunks if over limit.
    """
    if not bot_token or not chat_id or bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
        print("[!] Telegram Bot Token or Chat ID not configured. Skipping live Telegram dispatch.")
        return False

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    chunks = split_message(text)
    success = True

    print(f"[*] Sending digest to Telegram ({len(chunks)} message chunks required)...")
    for i, chunk in enumerate(chunks, 1):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }
        try:
            resp = requests.post(api_url, json=payload, timeout=15)
            if resp.status_code != 200:
                # If Markdown parsing fails (due to unescaped characters in raw text), retry without parse_mode
                print(f"[!] Markdown parse error chunk {i} ({resp.text}). Retrying as plain text...")
                payload["parse_mode"] = ""
                resp_plain = requests.post(api_url, json=payload, timeout=15)
                if resp_plain.status_code != 200:
                    print(f"[!] Error sending Telegram chunk {i}: {resp_plain.text}")
                    success = False
                else:
                    print(f"[+] Chunk {i}/{len(chunks)} sent successfully (plain text fallback).")
            else:
                print(f"[+] Chunk {i}/{len(chunks)} sent successfully (Markdown).")
        except Exception as e:
            print(f"[!] Exception while sending to Telegram: {e}")
            success = False

    return success


def send_whatsapp_message(text: str) -> bool:
    """
    Optional: Sends via Twilio WhatsApp API.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_FROM_NUMBER or not TWILIO_TO_NUMBER:
        return False

    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        chunks = split_message(text, max_length=1500) # WhatsApp has shorter limits per message cleanly
        for chunk in chunks:
            message = client.messages.create(
                from_=TWILIO_FROM_NUMBER,
                body=chunk,
                to=TWILIO_TO_NUMBER
            )
            print(f"[+] WhatsApp message sent: {message.sid}")
        return True
    except Exception as e:
        print(f"[!] Error sending WhatsApp message: {e}")
        return False


def notify_user(digest_text: str) -> bool:
    """
    Primary notification handler: Attempts Telegram first, falls back to WhatsApp or local print.
    """
    print("\n========================================================================")
    print("                      DELIVERING DAILY DIGEST                           ")
    print("========================================================================")
    
    sent = send_telegram_message(digest_text)
    
    if not sent and TWILIO_ACCOUNT_SID:
        print("[*] Attempting fallback delivery via Twilio WhatsApp...")
        sent = send_whatsapp_message(digest_text)

    if not sent:
        print("[*] NOTICE: No live notification credentials (TELEGRAM_BOT_TOKEN / CHAT_ID) found.")
        print("[*] The generated digest is saved to file and displayed in the terminal below:\n")
        print("------------------------------------------------------------------------")
        print(digest_text)
        print("------------------------------------------------------------------------")
    
    return sent
