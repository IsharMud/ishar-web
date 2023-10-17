from multiprocessing import cpu_count

bind = "127.0.0.1:8001"
worker_class = 'gthread'

# The following value was decided based on the Gunicorn documentation and configuration example:
# http://docs.gunicorn.org/en/stable/configure.html#configuration-file
workers = cpu_count() * 2 + 1
threads = 8
keepalive = 300
capture_output = True
worker_tmp_dir = '/dev/shm'
