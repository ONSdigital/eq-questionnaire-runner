import gunicorn
import os


workers = os.getenv("GUNICORN_WORKERS")
worker_class = "gevent"
keep_alive = os.getenv("GUNICORN_KEEP_ALIVE")
bind = "0.0.0.0:5000"
gunicorn.SERVER_SOFTWARE = "None"
