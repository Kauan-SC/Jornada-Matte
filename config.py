from dotenv import load_dotenv
import os

load_dotenv()

# Click Up
CLICKUP_API_KEY = os.environ["CLICKUP_API_KEY"]
CLICKUP_TEAM_ID = os.environ["CLICKUP_TEAM_ID"]
CLICKUP_LIST_ID = os.environ["CLICKUP_LIST_ID"]

# Supabase
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

# Discord
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
DISCORD_WEBHOOK_URL_ACOMPANHAMENTO = os.environ.get("DISCORD_WEBHOOK_URL_ACOMPANHAMENTO")