from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
from app.user.forms import AjoutUserForm
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page
from . import user



""" Ajout utilisateur"""
@user.route('/ajouter', methods=['GET','POST'])
def ajouter():
   #Un utilisateur
   form=AjoutUserForm()
   #Titre de l'onglet
   title=title_page("Utilisateur")

   if form.validate_on_submit():
      password_user=form.password.data
      password_hash=bcrypt.generate_password_hash(password_user).decode('utf-8') #génération du password Hacher
      #Enregistrement
      user_nv=User(nom=form.nom.data.upper(), post_nom=form.post_nom.data.upper(), prenom=form.prenom.data.capitalize(),\
      username=form.email.data, password=password_hash, password_onhash=password_user,role=form.role.data,\
      statut=True)
      db.session.add(user_nv)
      db.session.commit()
      flash("Ajout avec success",'primary')
         
   return render_template('user/ajouter.html', form=form, title=title)



# """ Liste des types """
# @categorie.route('/liste', methods=['GET', 'POST'])
# def index():
#    #Titre
#    title=title_page('Catégorie')
#    #Requête d'affichage de la categorisation
#    listes=Categorie.query.order_by(Categorie.id.desc()).all()
   

#    return render_template('categorie/index.html',title=title, liste=listes)

