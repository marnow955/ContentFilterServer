from flask import Flask, request, Blueprint

from .db.db_manager_abc import DbManagerABC
from .db.mysql_db_manager import MySqlDbManager
from .config import Config, DbConfig
from .main_controller import MainController
from .queue_manager import QueueManager

core = Blueprint('core', __name__)
controller = None


def create_app(app_config=None, app_name: str = None, queue_size: int = 1, db_manager: DbManagerABC = None) -> Flask:
    if app_name is None:
        app_name = Config.PROJECT
    if db_manager is None:
        db_manager = MySqlDbManager(DbConfig)
    queue = QueueManager(queue_size)
    app = Flask(app_name)
    configure_app(app, app_config)
    app.register_blueprint(core)
    global controller
    controller = MainController(queue, db_manager)
    return app


def configure_app(app: Flask, config=None):
    if config:
        app.config.from_object(config)


@core.route('/')
def index():
    return "Filtering server is working"


@core.route('/api/new_post', methods=['POST'])
def new_post():
    if request.is_json:
        content = request.get_json()
        controller.add_to_queue(content['id'])
        return 'OK'
    return 'FAILED'

# @app.route('/api/get')
# def get():
#     return get_post_by_id(get_from_queue())
# update_post_flag(get_from_queue(), 3)
# return "UPDATED"
