from flask import Blueprint

blueprint = Blueprint(
    'nav_blueprint',
    __name__,
    url_prefix='/nav',
    template_folder='templates',
    static_folder='static'
)
