import multiprocessing

bind = "unix:/home/ubun/sit/gunicorn.sock"
chdir = "/home/ubun/sit"

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4

timeout = 60
graceful_timeout = 30
keepalive = 2

max_requests = 2000
max_requests_jitter = 200

preload_app = True

worker_tmp_dir = "/dev/shm"

user = "ubun"
group = "www-data"
umask = 0o117

loglevel = "info"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"

capture_output = True

raw_env = [
    "DJANGO_SETTINGS_MODULE=sit.settings",
]

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Logging format improvement
def on_starting(server):
    print("Gunicorn is starting...")

def when_ready(server):
    print("Gunicorn is ready!")

def on_exit(server):
    print("Gunicorn is shutting down...")
