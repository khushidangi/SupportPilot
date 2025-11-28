import os
from supabase import create_client

_url = os.environ.get("SUPABASE_URL")
_key = os.environ.get("SUPABASE_KEY")
_client = None

def get_client():
    global _client
    if _client is None:
        _client = create_client(_url, _key)
    return _client
