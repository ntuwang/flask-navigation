from app.navigation import blueprint
from flask import render_template


@blueprint.route('/index')
def index():
    return render_template('index.html')


@blueprint.route('/about')
def cn_about():
    return render_template('about.html')

