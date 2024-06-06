from flask import render_template
from flask_security import roles_required

from app.routes.home import bp


@bp.route('/')
def index():
    return render_template('home/index.html')
