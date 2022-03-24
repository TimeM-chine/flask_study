from functools import wraps
from flask import g, redirect, url_for


def login_verify(func):
    @wraps(func)
    def wrapper(*args, **ss):
        if hasattr(g, "user"):
            return func(*args, **ss)
        else:
            return redirect(url_for("user.login"))

    return wrapper
