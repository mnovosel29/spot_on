from flask import Blueprint

bp = Blueprint('users', __name__)

from app.routes.users import routes
