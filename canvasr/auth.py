import logging

from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from argon2 import PasswordHasher

from canvasr import store

bp = Blueprint('auth', __name__)
ph = PasswordHasher()

log = logging.getLogger('flask.app.auth')
log.setLevel(logging.DEBUG)


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(msg='missing request data'), 400

    data = request.get_json()
    if 'user' not in data:
        return jsonify(msg='missing user in request'), 400
    if 'pasw' not in data:
        return 'missing pasw in request', 400

    user = data['user']
    pasw = data['pasw']

    hash = store.get(f'hash:{user}')

    if not hash:
        return jsonify(msg="user doesn't exists"), 404

    try:
        ph.verify(hash, pasw)
    except:
        return jsonify(msg='wrong pasw'), 401

    log.debug(hash)

    if ph.check_needs_rehash(hash.decode('utf-8')):
        hash = ph.hash(pasw)
        store.set(f'hash:{user}', hash)

    return jsonify(cooldown=app.config['CD_TIME'], access_token=create_access_token(user)), 200


@bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify(msg='missing request data'), 400

    data = request.get_json()
    if 'user' not in data:
        return jsonify(msg='missing user in request'), 400
    if 'pasw' not in data:
        return jsonify(msg='missing pasw in request'), 400

    user = data['user']
    if store.get(f'hash:{user}'):
        return jsonify(msg='user already exists'), 403

    pasw = data['pasw']

    if len(user) > 64:
        return jsonify(msg='username too long'), 400
    if len(pasw) > 64:
        return jsonify(msg='password too long, max 64'), 400
    if len(pasw) < 8:
        return jsonify(msg='password too short, min 8'), 400

    hash = ph.hash(pasw)

    store.set(f'hash:{user}', hash)

    return jsonify(cooldown=app.config['CD_TIME'], access_token=create_access_token(user)), 200

