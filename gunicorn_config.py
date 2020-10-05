import os

import gunicorn

workers = os.getenv("WEB_SERVER_WORKERS")
worker_class = os.getenv("WEB_SERVER_WORKER_CLASS")
threads = os.getenv("WEB_SERVER_THREADS")
keepalive = os.getenv("HTTP_KEEP_ALIVE")
bind = "0.0.0.0:5000"
gunicorn.SERVER_SOFTWARE = "None"
