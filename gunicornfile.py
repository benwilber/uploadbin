import os
import multiprocessing

bind = "localhost:5010"
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048

worker_class = "gevent"
pidfile = "/tmp/gunicorn.pid"

if os.path.isdir("/var/log/apps"):
    logdir = "/var/log/apps"
else:
    logdir = "/tmp"

logfile = os.path.join(logdir, "gunicorn.log")
accesslog = os.path.join(logdir, 'access.log')
errorlog = os.path.join(logdir, 'error.log')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(T)s/%(D)s'