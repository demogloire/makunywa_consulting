from flask import render_template, flash, url_for, redirect, request, session, g
from .. import db, bcrypt
from ..models import User
import flask_sijax
from app.user.forms import AjoutUserForm, EditUserForm
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
      return redirect(url_for('user.index'))
         
   return render_template('user/ajouter.html', form=form, title=title)


""" Liste des utilisateurs """
@user.route('/', methods=['GET', 'POST'])
def index():
   #Titre
   title=title_page("Utilisateur")
   #Requête d'affichage des utilisateurs
   listes=User.query.order_by(User.id.desc()).all()
   return render_template('user/index.html',title=title, liste=listes)


""" Statut"""
@user.route('/statut/<int:user_id>', methods=['GET', 'POST'])
def statut(user_id):
   #Titre
   title=title_page('Catégorie')
   #Requête de vérification de l'utilisateur
   user_statu=User.query.filter_by(id=user_id).first()

   if user_statu is None:
      return redirect(url_for('user.index'))

   if user_statu.statut == True:
      user_statu.statut=False
      db.session.commit()
      flash("{} est désactivé".format(user_statu.prenom),'primary')
      return redirect(url_for('user.index'))
   else:
      user_statu.statut=True
      db.session.commit()
      flash("{} est activé".format(user_statu.prenom),'primary')
      return redirect(url_for('categorie.index'))
   
   return render_template('user/index.html',title=title)


""" Modifier"""
@user.route('/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
   form=EditUserForm()
   #Titre
   title=title_page('Utilisateur')
   #Requête de vérification de l'utlisateur
   user_class=User.query.filter_by(id=user_id).first()
   #Le nom du type encours de modification
   user_nom=user_class.prenom

   if user_nom is None:
      return redirect(url_for('user.index'))
   
   if form.validate_on_submit(): 
      user_class.nom=form.nom.data.upper()
      user_class.post_nom=form.post_nom.data.upper()
      user_class.prenom=form.prenom.data.capitalize()
      user_class.role=form.role.data
      db.session.commit()
      flash("Modification réussie",'primary')
      return redirect(url_for('user.index'))
      
   if request.method=='GET':
      form.nom.data=user_class.nom
      form.post_nom.data=user_class.post_nom
      form.prenom.data=user_class.prenom
      form.role.data=user_class.role
      
   return render_template('user/edit.html', form=form, title=title, user_nom=user_nom)


""" Profil """
@flask_sijax.route(user, '/profil')
def profil():
      def register(obj_response):
         title=title_page("Utilisateur")
         listes=User.query.order_by(User.id.desc()).all()
         data_timeline=render_template('sijax/timeline.html', liste=listes)
         obj_response.html('#timeline',data_timeline)
      if g.sijax.is_sijax_request:
        return g.sijax.process_request()
      else:
         title=title_page("Utilisateur")
         listes=User.query.order_by(User.id.desc()).all()
         return render_template('user/profil.html',title=title, liste=listes)
       


   