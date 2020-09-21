import os

import gunicorn

workers = os.getenv("WEB_SERVER_WORKERS")
threads = os.getenv("WEB_SERVER_THREADS")
worker_class = "gthread"
keepalive = os.getenv("GUNICORN_KEEP_ALIVE")
bind = "0.0.0.0:5000"
gunicorn.SERVER_SOFTWARE = "None"
