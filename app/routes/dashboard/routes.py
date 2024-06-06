from flask import render_template
from app.routes.dashboard import bp


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('admin/dashboard/index.html', name='Mario')
