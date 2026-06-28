import multiprocessing

# Bind
bind = "0.0.0.0:5000"

# Workers — 2-4x CPU cores recommended
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
threads = 2
worker_connections = 1000

# Timeouts
timeout = 120
keepalive = 5
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sms'

# Process naming
proc_name = "rtvoyage"

# Max requests per worker to avoid memory leaks
max_requests = 1000
max_requests_jitter = 100
