import os
from random import choice
from string import letters, digits

from flask import Flask, g, abort, url_for, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.contrib.fixers import ProxyFix
import redis

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# max upload size (100MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Directory to save files on the server
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), "uploads")

# How long upload files are available
app.config['EXPIRE_SECONDS'] = 60

# Redis connection
app.config['REDIS_URL'] = "redis://localhost:6379/0"

def get_redis():
    try:
        return get_redis.r
    except AttributeError:
        r = get_redis.r = redis.Redis.from_url(app.config['REDIS_URL'])
    return r

@app.before_request
def before_request():
    g.r = get_redis()

def save_file(file):
    filename = secure_filename(file.filename)
    file_id = random_str(20)
    while not g.r.setnx(file_id, filename):
        file_id = random_str(20)

    stored_filename = "-".join([file_id, filename])
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], stored_filename))
    g.r.expire(file_id, app.config['EXPIRE_SECONDS'])
    return file_id, filename


def random_str(length):
    return "".join(choice(letters+digits) for i in xrange(length))


@app.route("/upload", methods=("POST",))
def upload():
    file = request.files['file']
    file_id, filename = save_file(file)
    return url_for('download',
        file_id=file_id, filename=filename, _external=True)


@app.route("/download/<file_id>/<filename>", methods=("GET",))
def download(file_id, filename):
    fname = g.r.get(file_id)
    if not fname or fname != filename:
        abort(404)
    stored_filename = "-".join([file_id, filename])
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               stored_filename)


if __name__ == '__main__':
    app.run(debug=True)

