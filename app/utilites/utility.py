from .. import db
from ..models import Historique, Internaute, Visiteur
from slugify import slugify
from datetime import datetime, date
import os
import secrets
import random
import string
import time
import uuid
from flask import session

#Titre
def title_page(nom="Dashbord"):
    title=f'{nom} | ASDI'
    return title

#Historique
def message_historique(message=None, user=None):
    historique=Historique(message=message, pseudonyme=user)
    db.session.add(historique)
    db.session.commit()

#Slug de l'article
def slug_publication(titre=None):
    return slugify(titre)

#Date de la modification
def date_modification():
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string


#Utilisateur unique
def code_usermac(length=4):
    #Code pour généer un mot de passe unique
    your_letters='AEIOU1234567890'
    return ''.join((random.choice(your_letters) for i in range(length)))


#Les nombres de visteurs par jours
def lesvisteurs():
    if 'visiteur' in session:
        pass
    else:
        session["visiteur"]=True
        date_aujour=date.today()
        dt_ver=Internaute.query.filter_by(date_vist=date_aujour).first()
        if dt_ver is None:
            compteur=Internaute(nombre_vis=1, date_vist=date_aujour)
            db.session.add(compteur)
            db.session.commit()
        else:
            dt_ver.nombre_vis=dt_ver.nombre_vis+1
            db.session.commit()


#Adresse mac unique
def macadress():
    var=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    return var


#Ideintification de l'utilisateur sur base de l'adresse MAC
def user_mac():
    adre_unique_mac=macadress()
    code_user=code_usermac()
    verification_visteur=Visiteur.query.filter_by(adress_mac=adre_unique_mac).first()
    if verification_visteur is None:
        visiteur_user=Visiteur(pseudonyme=code_user, adress_mac=adre_unique_mac)
        db.session.add(visiteur_user)
        db.session.commit()
        return visiteur_user.id
    else:
        return verification_visteur.id


#Enregistremt de l'article lu en cours
def enr_art(article, var_lu_art, article_pu):
    if article is False and var_lu_art==False:
      article_nombre_lu=article_pu.nbr_lu+1
      article_pu.nbr_lu=article_nombre_lu
      db.session.commit()
      session["ver"]=article_pu.id
    elif article is True and var_lu_art==False or article is False and var_lu_art==True :
        article_nombre_lu=article_pu.nbr_lu+1
        article_pu.nbr_lu=article_nombre_lu
        db.session.commit()
        session["ver"]=article_pu.id



#verification de l'article
def ver_enre_article(id_art):
    variable=False
    if 'id_pu' in session:
        id_pub = session['id_pu']
        if id_art==id_pub:
            variable=True
        else:
            variable=id_pub
    else:
        variable=False
    return variable

#verification de l'article pour marque comme lues
def ver_enre_lu(id_art):
    variable=False
    if 'ver' in session:
        id_pub = session['ver']
        if id_art==id_pub:
            variable=True
        else:
            variable=False
    else:
        variable=False
    return variable

    

    