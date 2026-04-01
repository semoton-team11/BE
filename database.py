from supabase import create_client
from functools import lru_cache
import os

@lru_cache
def get_supabase():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])