from .. import db
from ..models import Historique

def title_page(nom="Dashbord"):
    title=f'{nom} | Makunywa Consulting'
    return title

def message_historique(message=None, user=None):
    historique=Historique(message=message, pseudonyme=user)
    db.session.add(historique)
    db.session.commit()
    
    
    