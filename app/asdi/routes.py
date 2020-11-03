from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User, Publication, Categorie, Like, Historique, Commentaire, Comment
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
    return render_template('asdi/index.html',title=title, pub=pub)


""" Article """
@flask_sijax.route(asdi, '/article/<string:slug>')
def article(slug):
    def like_page(obj_response, arg1):
        title=title_page("Actualité")
        #Enregistrement de luke
        pub_art=Publication.query.filter_by(id=arg1).first_or_404()
        # L'utilisateur en cours
        mac_utilisateur=user_mac()
        #Like article
        like=Like.query.filter_by(visteur_id=mac_utilisateur, id_publication=arg1).first()
        if like is None:
            pub_art.nbr_like=pub_art.nbr_like+1
            like_une=Like(id_publication=arg1, visteur_id=mac_utilisateur)
            db.session.add(like_une)
            db.session.commit()
        else:
            pub_art.nbr_like=pub_art.nbr_like-1
            db.session.delete(like)
            db.session.commit()
        #Envoie des données
        pub_one=render_template('sijax/page_stat.html', une_pub=pub_art)
        obj_response.html('#page_stat',pub_one)
    
    def commentaire(obj_response, commentaire):
        form=FormCommetaire(data=commentaire)
        article_pu=Publication.query.filter_by(slug=slug).first_or_404()
        if form.commmentaire.errors:
            obj_response.html('#erreur',','.join(form.commmentaire.errors))
        else:
            #Commentaire de l'utilisataire
            commentaire_une=Commentaire()
            #Les champs d'enregistrement.
            commentaire_une.commentaire = form.commmentaire.data
            commentaire_une.statut = True
            commentaire_une.primaire = True
            commentaire_une.secondaire = False
            commentaire_une.vist_id=user_mac()
            commentaire_une.publication_id =article_pu.id 
            #Enregistrement dans le formulaire pour vérification
            form.populate_obj(commentaire_une)
            #Enregistrement des information
            article_pu.nbr_cmt=article_pu.nbr_cmt+1
            db.session.add(commentaire_une)
            db.session.commit()
            #Les données
            commentaire_pub=Commentaire.query.filter_by(publication_id=article_pu.id, statut=True).order_by(Commentaire.id.asc()).all()
            pub_one=render_template('sijax/commentaire.html', commentaire_pub=commentaire_pub)
            obj_response.html('#commet',pub_one)
            pub_one_c=render_template('sijax/page_stat.html', une_pub=article_pu)
            obj_response.html('#page_stat',pub_one_c)

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('like_page', like_page)
        g.sijax.register_callback('commentaire', commentaire)

        
        return g.sijax.process_request()
    else:
        title=title_page("Actualité")
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
        form=FormCommetaire()
        comm=FormCommetaired()
        commentaire_pub=Commentaire.query.filter_by(publication_id=article_pu.id, statut=True).order_by(Commentaire.id.desc()).all()
        pub_meilleur=Publication.query.filter(Publication.id!=article_pu.id, Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.id.desc()).limit(6).all()
        return render_template('asdi/une_pub.html',comm=comm, title=title, une_pub=article_pu, form=form, commentaire_pub=commentaire_pub, pub_meilleur=pub_meilleur)


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

@asdi.route('/actualites')
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
    
    return render_template('asdi/actualites.html',title=title, pub=pub, pub_meilleur=pub_meilleur)


@asdi.route('/vision')
def vision():
    #Titre de l'onglet
    title=title_page('Vision')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    return render_template('asdi/vision.html',title=title)


@asdi.route('/mission')
def mission():
    #Titre de l'onglet
    title=title_page("Mission")
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()


    return render_template('asdi/domaine.html',title=title)


