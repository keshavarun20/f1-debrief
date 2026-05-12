import fastf1
import os

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", ".cache")

os.makedirs(CACHE_DIR, exist_ok=True)

fastf1.Cache.enable_cache(CACHE_DIR)