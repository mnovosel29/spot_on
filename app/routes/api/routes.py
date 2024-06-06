from flask import jsonify, request
from flask_security import roles_required

from app.routes.api import bp
from app.models.auth import User
from sqlalchemy import or_


@bp.route('/users', methods=['POST', 'GET'])
@roles_required('Admin')
def api_users_with_search():
    search = request.json.get('search', '')
    page = request.json.get('page', 1)
    per_page = request.json.get('per_page', 10)
    sort_by = request.json.get('sort_by', 'id')
    sort_direction = request.json.get('sort_direction', 'asc')
    order = getattr(User, sort_by).desc() if sort_direction == 'desc' else getattr(User, sort_by)

    users = User.query.order_by(order).filter(
        or_(User.first_name.ilike(f'%{search}%'), User.last_name.ilike(f'%{search}%'), User.email.ilike(f'%{search}%'))
    ).paginate(page=int(page), per_page=int(per_page))

    return jsonify({
        'items': [user.to_dict() for user in users.items],
        'total': users.total,
        'page': users.page,
        'per_page': users.per_page,
        'pages': users.pages,
    })
