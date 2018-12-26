import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, current_app, send_from_directory
from flask_collect import Collect
from flask_redis import FlaskRedis
from werkzeug.local import LocalProxy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import os


store = FlaskRedis()
log = LocalProxy(lambda: current_app.logger)
jwt = JWTManager()
collect = Collect()
socket = SocketIO()

def create_app(**kwargs):
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.update(**kwargs)

    # cors
    cors = CORS(app)

    # custom loggin
    from canvasr import logging
    logging.init_app(app)

    # static file collection
    collect.init_app(app)

    # redis store
    store.init_app(app)
    store.setnx('pixel:id',0)

    # jwt manager
    jwt.init_app(app)

    # socket
    socket.init_app(app, message_queue=app.config['REDIS_URL'], channel=f"canvas:{app.config['APP_STAGE']}")


    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/greet')
    def greeting():
        return 'Hello, World!'


    from canvasr import auth, pixel
    app.register_blueprint(auth.bp)
    app.register_blueprint(pixel.bp)


    return app





