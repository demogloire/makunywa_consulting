from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Categorie, Publication, Historique, Fichier
from app.publication.forms import AjoutPubForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, slug_publication, message_historique
from slugify import slugify
from . import publication
from .upload import publication_doc



''' Ajouter une publication '''

@publication.route('/ajouter', methods=['GET','POST'])
@login_required
def ajouter():
   title='Publication | Makunywa Consulting'
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


