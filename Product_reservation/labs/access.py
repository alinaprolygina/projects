from flask import session, current_app, render_template
from functools import wraps
from flask import request


def group_validation(sess: session) -> bool:
    group = session.get('group_name', None)
    if group is not None and group != '':
        return True
    return False


def group_permission_validation(config: dict, sess: session) -> bool:
    group = sess.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint
    print(target_app, "-", group)
    if group in config and target_app in config[group]:
        return True
    return False


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation(session):
            return f(*args, **kwargs)
        return render_template("permision.html")
    return wrapper


def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return render_template("denied.html")
    return wrapper
