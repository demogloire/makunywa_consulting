import os
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Categorie, Publication, Historique, Fichier
from app.publication.forms import AjoutPubForm, EditPubForm, AjMediaForm, AjPDFForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, slug_publication, message_historique, date_modification
from slugify import slugify
from . import publication
from .upload import publication_doc, save_image_mod
import timeago
from datetime import datetime



''' Ajouter une publication '''
@publication.route('/ajouter', methods=['GET','POST'])
@login_required
def ajouter():
   title=title_page('Publication')
   #formulaire
   form=AjoutPubForm()
   #Vérfication des catégories existant
   ver_categorie=Categorie.query.filter_by(statut=True).first()
   if ver_categorie is None:
      return redirect(url_for('categorie.ajoutcate'))

   if form.validate_on_submit():
      #Titre de l'article
      titre_slug=slug_publication(form.titre.data)
      document_pub=publication_doc(form.pdf_document.data)
      image_pub=publication_doc(form.image_article.data)
      #Enregistrement de la publication
      pub=Publication(titre=form.titre.data, resume=form.resume.data, slug=titre_slug, url_img=image_pub,
                        categorie_id=form.categorie.data.id, user_pub=current_user)
      db.session.add(pub)
      db.session.commit()
      #Enregistrement du fichier
      if document_pub is not None:
         fichier_pdf=Fichier(url_pdf=document_pub, pub_fic=pub)
         db.session.add(fichier_pdf)
         db.session.commit()
      message=f"Publication de:{form.titre.data}"
      publication_de=f"{current_user.prenom} {current_user.post_nom}"
      message_historique(message, publication_de)
      flash("Publication ajoutée",'primary')
      return redirect(url_for('publication.index')) 

   return render_template('publication/ajouter.html',  title=title, form=form)

""" Liste des publications """
@publication.route('/', methods=['GET', 'POST'])
def index():
   #Titre
   title=title_page('Publication')
   #Requête d'affichage des categoriesÒ
   listes=Publication.query.order_by(Publication.id.desc()).all()
   #Taille de publication   
   taille=len(listes)

   return render_template('publication/index.html',title=title, liste=listes, taille=taille)

""" Modification de la publication """
@publication.route('/edit_<int:pub_id>_pub', methods=['GET', 'POST'])
def edit(pub_id):

   form=EditPubForm()
   #Titre
   title=title_page('Publication')
   #Requête de vérification du type
   pub_c=Publication.query.filter_by(id=pub_id).first()
   #Titre de la publication
   pub_titre=pub_c.titre

   if pub_titre is None:
      return redirect(url_for('publication.index'))
   
   if form.validate_on_submit():
      titre_slug=slug_publication(form.titre.data) 
      pub_c.titre=form.titre.data
      pub_c.slug=titre_slug
      pub_c.resume=form.resume.data
      pub_c.date_mod=date_modification()
      pub_c.categorie_id=form.categorie.data.id
      db.session.commit()
      #Enregistrement
      message=f"Modification de la publication de:{form.titre.data}"
      publication_de=f"{current_user.prenom} {current_user.post_nom}"
      message_historique(message, publication_de)

      flash("Modification réussie",'primary')
      return redirect(url_for('publication.index'))
      
   if request.method=='GET':
      form.titre.data=pub_c.titre
      form.resume.data=pub_c.resume
      form.categorie.data=pub_c.cat_pub

   return render_template('publication/edit.html', form=form, title=title)


""" Modification de l'image de la publication """
@publication.route('/edit_<int:pub_id>_image', methods=['GET', 'POST'])
def edit_image(pub_id):

   form=AjMediaForm()
   #Titre
   title=title_page('Publication')
   #Requête de vérification du type
   pub_c=Publication.query.filter_by(id=pub_id).first()
   #Titre de la publication
   pub_titre=pub_c.titre

   if pub_c is None:
      return redirect(url_for('publication.index'))
   #Modification de l'image
   if form.validate_on_submit():
      image_pub=save_image_mod(form.image_article.data, pub_c.url_img)
      if image_pub is None:
         return redirect(url_for('publication.edit_image',pub_id=pub_id))
      pub_c.url_img=image_pub
      pub_c.date_mod=date_modification()
      db.session.commit()
      #Enregistrement
      message=f"Modification de l'image de la publication de:{form.titre.data}"
      publication_de=f"{current_user.prenom} {current_user.post_nom}"
      message_historique(message, publication_de)

      flash("Modification réussie",'primary')
      return redirect(url_for('publication.index'))


   return render_template('publication/editim.html', form=form, title=title, titre=pub_titre)


""" Modification du PDF de la publication """
@publication.route('/edit_<int:pub_id>_pdf', methods=['GET', 'POST'])
def edit_pdf(pub_id):
   #Formulaire
   form=AjPDFForm()
   #Titre
   title=title_page('Publication')
   #Requête de vérification du type
   pub_c=Publication.query.filter_by(id=pub_id).first()
   #Titre de la publication
   pub_titre=pub_c.titre
   #Vérifcation des fichiers
   fic_publier=Fichier.query.filter_by(publication_id=pub_id).first()
   #Ancien fichier
   fichier_ancien=None
   if fic_publier is not None:
      fichier_ancien=fic_publier.url_pdf

   if pub_c is None:
      return redirect(url_for('publication.index'))
   #Modification de l'image
   if form.validate_on_submit():

      image_pub=save_image_mod(form.image_article.data, fichier_ancien)
      if image_pub is None:
            return redirect(url_for('publication.edit_pdf',pub_id=pub_id))

      if fic_publier is not None:
         fic_publier.url_pdf=image_pub
         pub_c.date_mod=date_modification()
      else:
         image_en=Fichier(url_pdf=image_pub, publication_id=pub_id)
         db.session.add(image_en)
      
      message=f"Modification du PDF de la publication de:{form.titre.data}"
      publication_de=f"{current_user.prenom} {current_user.post_nom}"
      message_historique(message, publication_de)

      db.session.commit()
      flash("Modification réussie",'primary')
      return redirect(url_for('publication.index'))
   return render_template('publication/editpdf.html', form=form, title=title, titre=pub_titre)


""" Modifier statut de l'Utilisateur """
@publication.route('/statut/<int:pub_id>', methods=['GET', 'POST'])
def statut(pub_id):
   #Titre
   title=title_page('Publication')
   #Requête de vérification du type
   pub_c=Publication.query.filter_by(id=pub_id).first()

   if pub_c is None:
      return redirect(url_for('publication.index'))

   if pub_c.statut == True:
      pub_c.statut=False
      db.session.commit()
      flash("La publication est désactivée sur la plateforme",'primary')
      return redirect(url_for('publication.index'))
   else:
      pub_c.statut=True
      db.session.commit()
      flash("La publication est activée sur la plateforme",'primary')
      return redirect(url_for('publication.index'))
   
   return render_template('user/index.html',title=title)