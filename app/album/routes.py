from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Album, Photo
from app.album.forms import AjoutPhoForm, AjoutEdPForm, AjoutCatForm, EditCatForm
from flask_login import login_user, current_user, logout_user, login_required

from . import album

from app.album.utilities import upload_acif, upload_inactif, save_picture_thumb



''' Ajoute d'un album '''
@album.route('/ajou_album', methods=['GET', 'POST'])
@login_required
@upload_inactif
def ajoutalbm():
   #Titre 
   title="Création d'album"
   #formulaire
   form=AjoutCatForm()

   if form.validate_on_submit():
      nom_cat=form.nom.data.capitalize()
      album_enre=Album(noms=nom_cat)
      db.session.add(album_enre)
      db.session.commit()
      session['album'] = album_enre.id
      session['nom_album']=album_enre.noms
      return redirect(url_for('album.mediaalbm')) 
   return render_template('album/ajouter.html',  title=title, form=form)


@album.route('/media_ajout', methods=['GET', 'POST'])
@login_required
@upload_acif
def mediaalbm():

   #Titre 
   title="Média"
   #formulaire
   form=AjoutPhoForm()

     #Les information de l'album encours d'enregistrements
   if 'album' in session and 'nom_album' in session:
      id_album=session['album']
      nom_album=session['nom_album']

   album_picture=Album.query.filter_by(id=id_album).first_or_404()

   if form.validate_on_submit():
      if form.file.data:
         img_photo=save_picture_thumb(form.file.data)
         enre_media=Photo(photo=img_photo, album_id=id_album)
         album_picture.nbr_picture=int(album_picture.nbr_picture)+1
         db.session.add(enre_media)
         db.session.commit()
         flash("Vous avez ajouté une image dans votre album", "success")
         return redirect(url_for('album.mediaalbm')) 
         
   return render_template('album/ulpload_img.html',nom_album=nom_album,  title=title, form=form)


""" Liste des albums"""
@album.route('/lisalbum', methods=['GET', 'POST'])
@login_required
def listalbum():
   #Titre
   title='Liste des albums'
   #Requête d'affichage de la categorisation
   listes=Album.query.order_by(Album.id.desc()).all()
   return render_template('album/views.html',title=title, liste=listes)



"""Activation d'album """

@album.route('/statut_album/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def statutalb(cat_id):
   #Titre
   title="L'album"


   #Requête de vérification de l'album
   cat_statu=Album.query.filter_by(id=cat_id).first_or_404()

   if cat_statu is None:
      return redirect(url_for('album.listalbum')) 

   if cat_statu.statut == True:
      cat_statu.statut=False
      db.session.commit()
      flash("L'album est désactivé sur la plateforme",'success')
      return redirect(url_for('album.listalbum')) 
   else:
      cat_statu.statut=True
      db.session.commit()
      flash("L'album est activée sur la plateforme",'success')
      return redirect(url_for('album.listalbum'))
   
   return render_template('user/views.html',title=title)

@album.route('finupload', methods=['GET', 'POST'])
def terminerupload():

   if 'album' in session:
      session.pop('album', None)
      return redirect(url_for('album.listalbum'))
   else:
      return redirect(url_for('album.listalbum'))
          
   return render_template('siteweb/otherpage/agenda.html')


# """ Modification de la catégorie  """

@album.route('/edit_<int:cate_id>_cate', methods=['GET', 'POST'])
@login_required
def editalbum(cate_id):
          
   form=EditCatForm()
   #Titre
   title="Modification de l'album"
   #Requête de vérification de l'album
   cate_class=Album.query.filter_by(id=cate_id).first()
   #Le nom du type encours de modification
   cate_nom=cate_class.noms

   if cate_class is None:
      return redirect(url_for('album.listalbum'))
   
   if form.validate_on_submit(): 
      cate_class.noms=form.ed_nom.data.capitalize()
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('album.listalbum'))
      
   if request.method=='GET':
      form.ed_nom.data=cate_class.noms
      
   return render_template('album/edit.html', form=form, title=title, cate_nom=cate_nom)


@album.route('/media_ajout/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def mediaaled(cate_id):
    #Titre 
   title="Média"
   #formulaire
   form=AjoutEdPForm()

   upload_result=None

   cate_class=Album.query.filter_by(id=cate_id).first_or_404()
   #De nom de l'album
   nom_album=cate_class.noms
   #Le nom du type encours de modification
   if cate_class is None:
      return redirect(url_for('album.listalbum'))
   
   if form.validate_on_submit():
      if form.file.data:
         img_file=save_picture_thumb(form.file.data)
         enre_media=Photo(photo=img_file, album_id=cate_id)
         cate_class.nbr_picture= int(cate_class.nbr_picture) + 1
         db.session.add(enre_media)
         db.session.commit()
         flash("Vous avez ajouté une image dans votre album", "success")
         return redirect(url_for('album.mediaaled', cate_id=cate_id)) 
         
   return render_template('album/ulpload_imgc.html',nom_album=nom_album,  title=title, form=form)

   


