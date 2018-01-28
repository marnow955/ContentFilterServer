from flask import Flask, request
from app.queue_manager import *

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
        print(content['id'])
        return 'OK'
    return 'FAILED'


@app.route('/api/get')
def get():
    return get_from_queue()