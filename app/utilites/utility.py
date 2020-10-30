from .. import db
from ..models import Historique
from slugify import slugify
from datetime import datetime

#Titre
def title_page(nom="Dashbord"):
    title=f'{nom} | ASDI'
    return title

#Historique
def message_historique(message=None, user=None):
    historique=Historique(message=message, pseudonyme=user)
    db.session.add(historique)
    db.session.commit()

#Slug de l'article
def slug_publication(titre=None):
    return slugify(titre)

#Date de la modification
def date_modification():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string
    

    