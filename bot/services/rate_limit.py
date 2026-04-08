from django.core.cache import cache
import time


def is_rate_limited(user_id: str, window=10, rate_limit=5):
    key = f"rate_limit:{user_id}"

    data = cache.get(key, [])
    now = time.time()

    
    data = [t for t in data if now - t < window]

    if len(data) >= rate_limit:
        return True

    data.append(now)
    cache.set(key, data, timeout=window)

    return False