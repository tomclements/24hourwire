import os

# Production memory reasoning:
#   Prod peak ~180 MB RSS (master + 1 worker) on a 512 MB starter plan.
#   An idle worker is ~50 MB and a busy one ~80-155 MB, so 2 workers fit with
#   headroom.  Threads add little memory and let /healthz and fast pages through
#   while slow pages render.
#   8 threads per worker (16 total) keeps a free thread for /healthz during
#   ~10-request crawler bursts (load test: /healthz max 0.53s at 2x8 vs ~3s at 2x4).
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
worker_class = "gthread"
workers = int(os.environ.get("WEB_CONCURRENCY", 2))
threads = int(os.environ.get("GUNICORN_THREADS", 8))
timeout = 120
graceful_timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
