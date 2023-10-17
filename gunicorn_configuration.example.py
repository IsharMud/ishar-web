from multiprocessing import cpu_count


bind = "127.0.0.1:8000"
worker_class = 'gthread'
workers = cpu_count() * 2 + 1
threads = 2
keepalive = 300
capture_output = True
accesslog = errorlog = "/var/www/isharmud.com/gunicorn.log"
