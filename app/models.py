from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Droit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False)  
    users = db.relationship('User', backref='user_droit', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    adress = db.Column(db.String(128))
    tel = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    password_onhash = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    avatar=db.Column(db.String(128), default='user.png')
    droit_id = db.Column(db.Integer, db.ForeignKey('droit.id'), nullable=False) 
    medias = db.relationship('Media', backref='user_file', lazy='dynamic')
    publications = db.relationship('Publication', backref='user_publication', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudonyme = db.Column(db.String(128))
    adress_mac = db.Column(db.String(128))
    avatar=db.Column(db.String(128))
    commentaires = db.relationship('Commentaire', backref='visiteur_commentaire', lazy='dynamic')
    medias = db.relationship('Media', backref='visiteur_medias', lazy='dynamic')
    aimers = db.relationship('Aimer', backref='visiteur_aimer', lazy='dynamic')
    comments = db.relationship('Comment', backref='visiteur_comment', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.pseudonyme)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.String(128))
    responsable = db.Column(db.String(128)) 
    mail = db.Column(db.String(128))  
    telephone = db.Column(db.String(128)) 
    logo_file=db.Column(db.String(128), default='client.png')
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow ) 
    publications = db.relationship('Publication', backref='client_publication', lazy='dynamic')
    medias = db.relationship('Media', backref='client_medias', lazy='dynamic')
    offres = db.relationship('Offre', backref='client_offre', lazy='dynamic')
    status = db.Column(db.Boolean, default=False) 
    def __repr__(self):
        return ' {} '.format(self.denomination)

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    plateforme=db.Column(db.String(128))
    pub = db.Column(db.Boolean, default=False)
    rubrique=db.Column(db.String(128))
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    publications = db.relationship('Publication', backref='categorie_publication', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.nom)


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    resume = db.Column(db.Text)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    slug=db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False)
    collabo_id = db.Column(db.Integer) 
    collaborateur = db.Column(db.String(60)) 
    url_img= db.Column(db.String(128))
    rubrique= db.Column(db.String(128))
    pub=db.Column(db.Boolean, default=False)
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    alaune= db.Column(db.Boolean, default=False)
    medias = db.relationship('Media', backref='publication_medias', lazy='dynamic')
    commentaires = db.relationship('Commentaire', backref='publication_commentaire', lazy='dynamic')
    aimers = db.relationship('Aimer', backref='publication_aimer', lazy='dynamic')
    comments = db.relationship('Comment', backref='publication_comment', lazy='dynamic')
    nbr_lu=db.Column(db.Integer, default=0)
    nbr_like=db.Column(db.Integer, default=0)
    nbr_cmt=db.Column(db.Integer, default=0)
    def __repr__(self):
        return ' {} '.format(self.titre)


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    visteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
    comments = db.relationship('Comment', backref='commentaire_comment', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.commentaire)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commentaire = db.Column(db.Text)
    statut = db.Column(db.Boolean, default=False) 
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    visteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaire.id'), nullable=False)

    def __repr__(self):
        return ' {} '.format(self.commentaire)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_img= db.Column(db.String(128))
    url_pdf= db.Column(db.String(128))
    url_video= db.Column(db.String(128))
    user_media=db.Column(db.Boolean, default=False)
    video_article=db.Column(db.Boolean, default=False)
    publication_media=db.Column(db.Boolean, default=False)
    client_media=db.Column(db.Boolean, default=False)
    visiteur_media=db.Column(db.Boolean, default=False)  
    img_one=db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=True)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    date_mod=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
 
    def __repr__(self):
        return ' {} '.format(self.url_img)

class Aimer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=False)
    visiteur_id = db.Column(db.Integer, db.ForeignKey('visiteur.id'), nullable=False)
    def __repr__(self):
        return ' {} '.format(self.like_publication)

class Internaute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_vis = db.Column(db.Integer, default=0)
    date_vist=db.Column(db.Date)
    def __repr__(self):
        return ' {} '.format(self.nombre_v_par)


class Offre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    resume = db.Column(db.Text)
    date_activation=db.Column(db.Date)
    date_limite=db.Column(db.Date)
    url_redierct = db.Column(db.Text)
    statut=db.Column(db.Boolean, default=False)
    default=db.Column(db.Boolean, default=False)
    pdf=db.Column(db.Boolean, default=False)
    url=db.Column(db.Boolean, default=False)
    pdf_nom = db.Column(db.String(255))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    nombre_jrs = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return ' {} '.format(self.titre)
    

