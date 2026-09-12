import multiprocessing
import os


# ============================================================
# Application
# ============================================================

# Django project directory.
# Defaults to the current working directory.
chdir = os.environ.get("APP_DIR", os.getcwd())

# Django settings module.
raw_env = [
    "DJANGO_SETTINGS_MODULE=sit.settings",
]


# ============================================================
# Network
# ============================================================

# Azure App Service expects the application to listen on the
# platform-provided port. For a VPS, PORT can be set to 8000.
#
# Example:
#   Azure -> PORT supplied by environment
#   VPS   -> PORT=8000
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"


# ============================================================
# Workers
# ============================================================

# Do not blindly use CPU * 2 + 1 together with many threads.
# Start conservatively and increase after monitoring.
#
# GTHREAD + 4 threads gives good concurrency for Django
# without creating excessive processes on a small server.
workers = int(
    os.environ.get(
        "GUNICORN_WORKERS",
        min(4, multiprocessing.cpu_count() + 1)
    )
)

worker_class = "gthread"

threads = int(os.environ.get("GUNICORN_THREADS", "4"))


# ============================================================
# Timeouts
# ============================================================

timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))

graceful_timeout = int(
    os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30")
)

keepalive = int(
    os.environ.get("GUNICORN_KEEPALIVE", "2")
)


# ============================================================
# Worker lifecycle / stability
# ============================================================

# Restart workers periodically to protect against gradual
# memory growth.
max_requests = 2000
max_requests_jitter = 200

# Load Django before forking workers.
# Usually beneficial for Django because of copy-on-write memory.
preload_app = True

# Linux optimization.
worker_tmp_dir = "/dev/shm"


# ============================================================
# Logging
# ============================================================

# "-" means stdout/stderr.
#
# This is especially important for Azure App Service because
# Azure can collect application output without requiring
# /var/log/gunicorn to exist.
accesslog = "-"
errorlog = "-"

loglevel = os.environ.get(
    "GUNICORN_LOG_LEVEL",
    "info"
)

capture_output = True


# ============================================================
# Request limits
# ============================================================

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190


# ============================================================
# Gunicorn lifecycle logging
# ============================================================

def on_starting(server):
    server.log.info("Gunicorn is starting...")


def when_ready(server):
    server.log.info(
        "Gunicorn is ready - workers=%s, threads=%s",
        workers,
        threads,
    )


def on_exit(server):
    server.log.info("Gunicorn is shutting down...")