from flask import Blueprint, current_app

favicon_blueprint = Blueprint("favicon", __name__)


@favicon_blueprint.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.png")
