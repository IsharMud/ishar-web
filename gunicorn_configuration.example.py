from multiprocessing import cpu_count
from pathlib import Path


chdir = str(Path(Path(__file__).resolve().parent, "ishar-web"))
bind = "127.0.0.1:8000"
worker_class = "gthread"
workers = cpu_count() * 2 + 1
threads = 2
keepalive = 300
capture_output = True
access_log_format = '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = str(Path(Path(__file__).resolve().parent, "logs/gunicorn_access.log"))
errorlog = str(Path(Path(__file__).resolve().parent, "logs/gunicorn_error.log"))
