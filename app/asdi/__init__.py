from flask import Blueprint

asdi = Blueprint('asdi', __name__, url_prefix='/')
# never forget 
from . import routes