import os
import secrets
from PIL import Image
from flask import redirect, session, url_for
from functools import wraps
from .. import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


def upload_acif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        return f(*args, **kwargs)
      else:
        return redirect(url_for('album.ajoutalbm'))
    return wrap

def upload_inactif(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'album' in session:
        session.pop('album', None)
        return f(*args, **kwargs)
      else:
        return f(*args, **kwargs)
    return wrap


def save_picture_thumb(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

