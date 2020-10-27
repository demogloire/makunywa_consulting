from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Categorie, Publication, Historique, Fichier
from app.publication.forms import AjoutPubForm, EditPubForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, slug_publication, message_historique
from slugify import slugify
from . import publication
from .upload import publication_doc
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
      return redirect(url_for('publication.ajouter')) 

   return render_template('publication/ajouter.html',  title=title, form=form)

""" Liste des publications """
@publication.route('/', methods=['GET', 'POST'])
def index():
   #Titre
   title=title_page('Publication')
   #Requête d'affichage des categoriesÒ
   listes=Publication.query.order_by(Publication.id.desc()).all()
   les_publications=[]
   #Les publications
   for liste in listes:
      pub=[liste.id, liste.titre, liste.slug, liste.url_img, liste.nbr_lu, liste.nbr_like, liste.nbr_cmt, liste.user_pub.prenom, timeago.format(liste.date_mod, datetime.now() , 'fr')]
      les_publications.append(pub)


   print(les_publications,'chanteur malheur')
   

   return render_template('publication/index.html',title=title, liste=les_publications)

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
      pub_c.categorie_id=form.categorie.data.id
      db.session.commit()
      flash("Modification réussie",'primary')
      return redirect(url_for('publication.index'))
      
   if request.method=='GET':
      form.titre.data=pub_c.titre
      form.resume.data=pub_c.resume
      form.categorie.data=pub_c.cat_pub

   return render_template('publication/edit.html', form=form, title=title)