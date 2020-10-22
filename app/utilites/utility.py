from .. import db
from ..models import Historique
from slugify import slugify

#Titre
def title_page(nom="Dashbord"):
    title=f'{nom} | Makunywa Consulting'
    return title

#Historique
def message_historique(message=None, user=None):
    historique=Historique(message=message, pseudonyme=user)
    db.session.add(historique)
    db.session.commit()

#Slug de l'article
def slug_publication(titre=None):
    return slugify(titre)
    

    