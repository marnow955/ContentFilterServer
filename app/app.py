from flask import Flask, request
from app.queue_manager import *
from app.db.db_manager import *

app = Flask(__name__)


def create_app():
    return app


@app.route('/')
def index():
    return "Hello World"


@app.route('/api/new_post', methods=['POST'])
def new_post():
    if request.is_json:
        content = request.get_json()
        add_to_queue(content['id'])
        return 'OK'
    return 'FAILED'


@app.route('/api/get')
def get():
    return get_post_by_id(get_from_queue())
    # update_post_flag(get_from_queue(), 3)
    # return "UPDATED"
