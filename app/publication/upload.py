import os
import secrets
from .. import create_app




config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)



#Enregistrement du fichier pdf
def publication_doc(document):
    if document is None:
        return None
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(document.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    document.save(picture_path)
    return picture_fn