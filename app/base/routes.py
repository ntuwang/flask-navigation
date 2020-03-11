from bcrypt import checkpw
from flask import jsonify, render_template, redirect, request, url_for
from app.base import blueprint


@blueprint.route('/')
def route_default():
    return redirect(url_for('nav_blueprint.index'))
