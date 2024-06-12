from flask import Blueprint

bp = Blueprint('seat', __name__)

from app.routes.seat import routes
