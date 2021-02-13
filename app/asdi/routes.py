from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Publication, Categorie, Like, Historique, Commentaire, Comment, Photo, Album, Fichier
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
import flask_sijax
from ..utilites.utility import ver_enre_article, ver_enre_lu, enr_art, lesvisteurs, title_page, slug_publication, message_historique, date_modification,user_mac
from . import asdi
import timeago
from .forms import FormCommetaire, FormCommetaired



#Time ago
@asdi.context_processor
def utility_processor():
    def timeagos(date_time):
        date_maintenant = datetime.now()
        date_encours=timeago.format(date_time, date_maintenant, 'fr')
        return date_encours
    return dict(timeagos=timeagos)

@asdi.context_processor
def utility_processor():
    def date_french(date_sp):
        date_mois=None
        if date_sp=='01':
            date_mois='Jan'
        elif date_sp=='02':
            date_mois='Fév'
        elif date_sp=='03':
            date_mois='Mar'
        elif date_sp=='04':
            date_mois='Avr'
        elif date_sp=='05':
            date_mois='Mai'
        elif date_sp=='06':
            date_mois='Jui'
        elif date_sp=='07':
            date_mois='Juil'
        elif date_sp=='08':
            date_mois='Aoû'
        elif date_sp=='09':
            date_mois='Sep'
        elif date_sp=='10':
            date_mois='Oct'
        elif date_sp=='11':
            date_mois='Nov'
        else:
            date_mois='Déc'
        return date_mois
    return dict(date_french=date_french)



""" Acceuil """
@asdi.route("/")
def accueil():
    #Titre de l'onglet
    title=title_page('Accueil')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    #Liste des actualités sur la plateforme
    pub=Publication.query.filter(Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.id.asc()).limit(6).all()
    photo=Photo.query.filter(Album.statut==True).order_by(Photo.id.asc()).limit(10).all() #Les photos
    
    return render_template('asdi/index.html',title=title, pub=pub, photos=photo)


""" Article """
@asdi.route('/article/<string:slug>')
def article(slug):
    #Article de verification.
    article_pu=Publication.query.filter_by(slug=slug).first_or_404()
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
        
    if article_pu is not None:
        session["id_pu"] = article_pu.id

    #Nombre des lis de l'article
    article=ver_enre_article(article_pu.id)
    var_lu_art=ver_enre_lu(article_pu.id)
    enr_art(article,var_lu_art,article_pu)
    #Formulaire
    photo=Photo.query.filter(Album.statut==True).order_by(Photo.id.asc()).limit(10).all() #Les photos
    pub_meilleur=Publication.query.filter(Publication.nbr_lu > 10 , Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.nbr_lu.desc()).limit(6).all()
    album=Album.query.filter_by(statut=True).order_by(Album.id.asc()).all()
    #Fichier encours d'éxecution
    fichier_docu=Fichier.query.filter_by(publication_id=article_pu.id).first()
    return render_template('asdi/actua_une.html',title="Actualité", page="Actualité",pub_meilleur=pub_meilleur, une_pub=article_pu, photos=photo, album=album, fichier_docu=fichier_docu)


@asdi.route('/commentaire/<int:id_pub>/<int:id>', methods=['GET','POST'])
def commentaire_secondaire(id_pub,id):
    title=title_page("Actualité")
    #Article de verification.
    article_pu=Publication.query.filter_by(id=id_pub).first_or_404()
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
        
    if article_pu is not None:
        session["id_pu"] = article_pu.id

    #Nombre des lis de l'article
    article=ver_enre_article(article_pu.id)
    var_lu_art=ver_enre_lu(article_pu.id)
    enr_art(article,var_lu_art,article_pu)
    #Formulaire
    form=FormCommetaire()
    comm=FormCommetaired()
    commentaire_pub=Commentaire.query.filter_by(publication_id=article_pu.id, statut=True).order_by(Commentaire.id.desc()).all()
    #COMMENTAIRE SECONDAIRE DE LA PUBLICATION
    article_pu=Publication.query.filter_by(id=id_pub).first_or_404()
    comm=FormCommetaired()
    if comm.validate_on_submit():
        article_pu.nbr_cmt=article_pu.nbr_cmt+1
        comment=Comment(commentaire=comm.commmentaire.data, statut=True, visiteur_id=user_mac(), commentaire_id=id )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('asdi.article', slug=article_pu.slug))

    return render_template('asdi/une_pub.html',comm=comm, title=title, une_pub=article_pu, form=form, commentaire_pub=commentaire_pub)

@asdi.route('/actualites.html')
def actualite():
    #Titre de l'onglet
    title=title_page('Actualités')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    #Liste des actualités sur la plateforme
    page= request.args.get('page', 1, type=int)
    pub=Publication.query.filter(Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.id.desc()).paginate(page=page, per_page=3)
    pub_meilleur=Publication.query.filter(Publication.nbr_lu > 10 , Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.nbr_lu.desc()).limit(6).all()
    photo=Photo.query.filter(Album.statut==True).order_by(Photo.id.asc()).limit(10).all() #Les photos
    return render_template('asdi/actua.html',title=title, pub=pub, pub_meilleur=pub_meilleur, page="Actualités", photos=photo)

@asdi.route('/vision')
def vision():
    #Titre de l'onglet
    title=title_page('Vision')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    return render_template('asdi/vision.html',title=title)

@asdi.route('/contact.html')
def contact():
    #Titre de l'onglet
    title=title_page("Contact")
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()

    return render_template('asdi/contact.html',title=title)

@asdi.route('/galerie.html')
def galerie():
    #Titre de l'onglet
    title=title_page("Gélerie")
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    page="Galerie"
    pub=Publication.query.filter(Publication.statut==True, Categorie.nom=='Actualités', Publication.nbr_lu > 5 ).order_by(Publication.id.asc()).limit(6).all()
    photo=Photo.query.filter(Album.statut==True).order_by(Photo.id.asc()).limit(10).all() #Les photos
    album=Album.query.filter_by(statut=True).order_by(Album.id.asc()).all()
    return render_template('asdi/galerie.html',title=title, page=page, pub=pub, photos=photo, album=album)

@asdi.route('/apropos.html')
def apropos():
    #Titre de l'onglet
    title=title_page('Apropos de nous')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    page="Qui sommes-nous"
    
    return render_template('asdi/about.html',title=title, page=page)

@asdi.route('/<int:id>/galerie.html')
def galerie_trie(id):
    #Titre de l'onglet
    title=title_page("Gélerie")
    #album encours
    nom_al=Album.query.filter_by(id=id).first_or_404()
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    page="Galerie"
    pub=Publication.query.filter(Publication.statut==True, Categorie.nom=='Actualités', Publication.nbr_lu > 5).order_by(Publication.id.asc()).limit(6).all()
    photo=Photo.query.filter(Album.statut==True, Album.id==id).order_by(Photo.id.asc()).all() #Les photos
    album=Album.query.filter(Album.id!=id).order_by(Album.id.asc()).all()
    return render_template('asdi/galerie_trie.html',title=title, page=page,nom_album=nom_al, pub=pub, photos=photo, album=album)

