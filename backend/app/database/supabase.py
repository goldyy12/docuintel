# Change the first line to this:
from supabase import create_client, Client 

import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# This now uses the function from the official library
supabase: Client = create_client(url, key)