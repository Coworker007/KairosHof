import os
from flask import Flask, url_for, redirect, session, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
#from flask_security import Security, SQLAlchemyUserDatastore, \
#    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
from .config import LANGUAGES
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import *
from flask_babelex import Babel
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
import stripe




stripe_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.jpeg', '.jpg', '.png']
#app.config['UPLOAD_FOLDER'] = '/static/profile_pics'

static_path = op.join(op.dirname(__file__), 'static')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
#db.drop_all()

Migrate(app,db)


babel = Babel(app)

login_manager = LoginManager()
login_manager.init_app(app)
#babel.init_app(app)
login_manager.login_view = 'core.login'
admin = admin.Admin(name="Admin Panel")






@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    # for automatic select LANGUAGE depend on browser request accept language
    #return request.accept_languages.best_match(list(LANGUAGES.keys()))
    # better to keep user set his own
    return session.get('lang', 'en')


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


from estate_management.usermodels import User, Guest, Staff, Service, Enquiry, Publication, Subscription, Code




# admin views MVCs




"""

class MyModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        # Logic
        return True

admin.add_view(MyModelView(User, session, list_columns=['id', 'name', 'foreign_key']))

class Users(BaseView):
    #def is_accessible(self):
    #    return current_user.is_authenticated
    @expose('/')
    def index(self):
        return self.render('adminusermanger.html')
# admin views MVCs
admin = Admin(app)
#admin.add_view(Users(name='Mange Users', endpoint='', category='Users'))
admin.add_view(ModelView(User, db.session))
"""
#admin.add_view(Users(name='Mange Occupants', endpoint='occupants', category='Users'))
#admin.add_view(Users(name='Mange Guests', endpoint='guests', category='Users'))

#admin.add_view(adminLogin(name='Login'))
#admin.add_view(adminLogOut(name='Logout'))



#admin.add_view(MyView(name='gaurds', endpoint='/gaurds', category='MyView'))

from estate_management.core.userviews import core
from estate_management.admin.adminviews import adminapp


app.register_blueprint(core)
app.register_blueprint(adminapp)

# if you need empty the DB uncomment this
#db.session.commit()   #<--- solution!
#db.drop_all()
#db.create_all()
