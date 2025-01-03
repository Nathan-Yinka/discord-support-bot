from dotenv import load_dotenv
load_dotenv()

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_ROLE_NAME = "Support Team"
CLOSED_CATEGORY_NAME = "CLOSED TICKET"
TICKET_CATEGORY_NAME = "OPENED TICKETS"
TRANSCRIPT_CATEGORY_NAME = "TRANSCRIPTS"
OPEN_TICKET_CHANNEL_NAME = "🎫︱open-ticket"
TEXT_CATEGORY_NAME = "Text Channels"
