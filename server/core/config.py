import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

settings = Settings()
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)