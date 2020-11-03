from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    publications = db.relationship('Publication', backref='cat_pub', lazy='dynamic')
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    statut = db.Column(db.Boolean, default=False)  
    def __repr__(self):
        return ' {} '.format(self.nom)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    resume = db.Column(db.Text)
    slug=db.Column(db.String(255))
    statut = db.Column(db.Boolean, default=False)
    url_img= db.Column(db.String(128))
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nbr_lu=db.Column(db.Integer, default=0)
    nbr_like=db.Column(db.Integer, default=0)
    nbr_cmt=db.Column(db.Integer, default=0)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    fichiers = db.relationship('Fichier', backref='pub_fic', lazy='dynamic')
    commentaires = db.relationship('Commentaire', backref='pub_com', lazy='dynamic')
    likes = db.relationship('Like', backref='like_pub', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.titre)

class Sondage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    description = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False)  
    date_debut=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_fin=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    resultats = db.relationship('Resultat', backref='sond_resul', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.titre)

class Resultat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nbr_obtenu = db.Column(db.Integer, default=0)
    sondage_id = db.Column(db.Integer, db.ForeignKey('sondage.id'), nullable=False) 
    condidat_id = db.Column(db.Integer, db.ForeignKey('candidat.id'), nullable=False) 
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False) 
    def __repr__(self):
        return ' {} '.format(self.nbr_obtenu)

class Candidat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    parti_politique = db.Column(db.String(128))
    parti_regroupement = db.Column(db.String(128))
    description = db.Column(db.Text)
    url_img= db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    resultats = db.relationship('Resultat', backref='cond_resul', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Fichier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_img= db.Column(db.String(128))
    url_pdf= db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False) 
    def __repr__(self):
        return ' {} '.format(self.url_img)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    role = db.Column(db.String(128))
    password_onhash = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar=db.Column(db.String(128), default='user.png')
    publications = db.relationship('Publication', backref='user_pub', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Internaute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_vis = db.Column(db.Integer, default=0)
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_vist=db.Column(db.Date)
    def __repr__(self):
        return ' {} '.format(self.nombre_v_par)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_publication=db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False) 
    visteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False) 
    def __repr__(self):
        return ' {} '.format(self.nombre_v_par)



class Visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudonyme = db.Column(db.String(128))
    adress_mac = db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar=db.Column(db.String(128))
    resultats = db.relationship('Resultat', backref='user_pub', lazy='dynamic')
    likes = db.relationship('Like', backref='like_vis', lazy='dynamic')
    commentaires = db.relationship('Commentaire', backref='vis_com', lazy='dynamic')
    comments = db.relationship('Comment', backref='vis_comment', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.pseudonyme)

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    primaire = db.Column(db.Boolean, default=False) 
    secondaire = db.Column(db.Boolean, default=False) 
    id_primaire = db.Column(db.Integer) 
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False) 
    vist_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False) 
    comments = db.relationship('Comment', backref='comment_com', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.commentaire)

class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    pseudonyme = db.Column(db.String(128))
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return ' {} '.format(self.message)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False) 
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaire.id'), nullable=False) 
    def __repr__(self):
        return ' {} '.format(self.commentaire)





    

