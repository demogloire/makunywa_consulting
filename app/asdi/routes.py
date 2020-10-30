from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User
from flask_login import login_user, current_user, logout_user, login_required
from ..utilites.utility import title_page, slug_publication, message_historique, date_modification
from . import asdi


@asdi.route("/")
def accueil():
    #Titre de l'onglet
    title=title_page('Accueil')
    return render_template('asdi/index.html',title=title)

