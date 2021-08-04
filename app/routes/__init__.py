from .home import home_bp
from .log_list import log_list_bp

from flask_executor import Executor
executor = Executor()


def init_app(app):
    executor.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(log_list_bp)

    with app.app_context():
        from werobot.contrib.flask import make_view
        from .robot import my_werobot
        app.add_url_rule(rule='/robot/',  # WeRoBot 挂载地址
                         endpoint='werobot',  # Flask 的 endpoint
                         view_func=make_view(my_werobot),
                         methods=['GET', 'POST'])
