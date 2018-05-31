from flask import Flask, request, Blueprint

from .basic_auth import requires_auth, configure_auth
from .db.db_manager_abc import DbManagerABC
from .db.mysql_db_manager import MySqlDbManager
from .config import Config, DbConfig
from .main_controller import MainController
from .queue_manager import QueueManager

core = Blueprint('core', __name__)
controller = None


def create_app(app_config=None, auth_config=None, app_name: str = None,
               queue_size: int = 1, queue_timeout=10, db_manager: DbManagerABC = None) -> Flask:
    if app_name is None:
        app_name = Config.PROJECT
    if db_manager is None:
        db_manager = MySqlDbManager(DbConfig)
    if auth_config:
        configure_auth(auth_config)
    queue = QueueManager(queue_size, queue_timeout)
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


@core.route('/api/new_posts', methods=['POST'])
def new_post():
    if request.is_json:
        content = request.get_json()
        for post in content['posts']:
            controller.add_to_queue(post['id'])
        return 'OK'
    return 'FAILED'
