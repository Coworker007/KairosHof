from flask import render_template, request, flash, redirect, url_for, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from estate_management.core.userforms import UserForm, GuestForm, StaffForm, ServiceForm, LoginForm, EnquiryForm, NewsForm, SubscriptionForm, UpdateUserForm, CodeForm, GeneratorForm
from estate_management.usermodels import User,Role, Estate, Guest, Staff, Service, Enquiry, Publication, Subscription, Code
from estate_management.core.picture_handler import add_profile_pic
from estate_management.core.guardCodeGenerator import code_generator, strpool
from estate_management import db, stripe_key
import stripe
import flask_admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import BaseView, expose
from flask_admin import *
from estate_management import app, static_path, db, SQLAlchemy, babel
from datetime import date
from flask_admin.model import typefmt
from flask_admin.model.template import macro

from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms.widgets import TextArea
from werkzeug.datastructures import MultiDict
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, HiddenField,StringField, TextAreaField,BooleanField, TextField, IntegerField, DateTimeField, PasswordField, RadioField, SelectMultipleField, ValidationError,SelectField, widgets, FileField
from wtforms.validators import Required as required
from flask_admin.form import SecureForm, rules
from estate_management.core.guardCodeGenerator import code_generator, strpool

from flask_babel import lazy_gettext

from flask_admin.contrib.fileadmin import FileAdmin

from flask_babel import gettext, ngettext

from redis import Redis
from flask_admin.contrib import rediscli

import os.path as op

from flask_babelex import Babel

from werkzeug.security import generate_password_hash, check_password_hash








adminapp = Blueprint('adminapp',__name__, template_folder='templates.admin')
admin = Admin(app, name='Admin', template_mode='bootstrap4')





def formatter(view, context, model, name):
    # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name
    pass

def type_formatter(view, value):
    # `view` is current administrative view
    # `value` value to format
    pass

def date_format(view, value):
    return value.strftime('%d.%m.%Y %H:%M:%S')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        type(None): typefmt.null_formatter,
        date: date_format
    })

from flask_admin.actions import action

class MyModelView(ModelView):
    column_type_formatters = dict()

class AdminModelView(sqla.ModelView):
    form_base_class = SecureForm
    #can_delete = False  # disable model deletion
    #page_size = 50  # the number of entries to display on the list view
    #def is_accessible(self):
    #    return current_user.is_authenticated
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_view_details = True
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('core.login', next=request.url))



import os.path as op






# Admin Users View (Control Users AdminView)
class AdminUsersView(ModelView):

    # update main view to render js file for any js tasks like toggle password
    def render(self, template, **kwargs):
        """
        using extra js in render method allow use
        url_for that itself requires an app context
        """


        self.extra_js = [url_for("static", filename="admin/js/users.js")]

        return super(AdminUsersView, self).render(template, **kwargs)



    # Add Custom Functions To the model aprove or anything
    @action('approve', 'Approve', 'Are you sure you want to approve selected users?')
    def action_approve(self, ids):
        count = 0
        try:
            query = User.query.filter(User.id.in_(ids))
            for user in query.all():
                print(user)
                count += 1
            flash('User was successfully approved {} users were successfully approved'.format(count))

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash('Failed to approve users. {}'.format(error))


    # edit types format like date
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_view_details = True


    def on_model_change(self, form, User, is_created):
        if form.password_hash.data is not None:
            User.password_hash = generate_password_hash(form.password_hash.data)
            User.update()
        else:
           del form.password


    # Form will now use all the other fields in the model

    # Add our own password form field - call it password2

    # inline editable fildes
    column_editable_list = ['firstname','lastname', 'housenumber', 'streetname', 'flatnumber', 'user_role', 'user_estate']

    # over ride inputs types
    form_overrides = {
        'housenumber': IntegerField,
        'dateofbirth': DateField,
        'password_hash': PasswordField
    }

    # selectbox from strings good for role
    form_choices = {
    'gender': [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    }


    # wtf forms
    form_args = {
            'profile_image': {
            'label': 'Profile Image',
            'validators': [required()]
            },
            'firstname': {
            'label': 'First Name',
            'validators': [required()]
            },
            'lastname': {
            'label': 'Last Name',
            'validators': [required()]
            },
            'dateofbirth': {
            'label': 'Date of Birth',
            'validators': [required(message="You need to enter your date of birth")]
            },
            'streetname': {
            'label': 'Streetname',
            'validators': [required()],
            },
            # id used in user.js to add custom toggle
            'password_hash': {
            'label': 'Password',
            'id': 'user_password',
            'validators': [required()]
            },
            'streetname': {
            'label': 'Street name',
            'validators': [required()]
            },
            'housenumber': {
            'label': 'House number',
            'validators': [required(message="House Number Must Be INTEGER")]
            },
            'flatnumber': {
            'label': 'Flat number',
            'validators': [required(message="Flat Number Is Required")]
            },
            'gender': {
            'label': 'Gender',
            'validators': [required()]
            },
            'telephone': {
            'label': 'Telephone',
            'validators': [required()]
            },
            'role': {
            'label': 'Role',
            'validators': [required()]
            },
            'estate': {
            'label': 'Estate',
            'validators': [required()]
            },
    }
    # style and control
    form_widget_args = {
    'streetname': {
        'rows': 1,
        'style': 'color: black'
    }
    }
    # remove these fileds from edit and create
    form_excluded_columns = ['guests', 'staffs', 'services', 'enquiries', 'news', 'subscriptions']
    # open bootstrap modal for create and edit
    create_modal = True
    edit_modal = True
    # which columns has filter for example contains gaurd
    column_filters = [User.role, User.estate, User.gender]
    # which columns can used for search
    column_searchable_list = [User.id, User.firstname, User.username, User.telephone, User.streetname]
    #column_formatters = dict(User.housenumber=macro('render_price'))
    #column_formatters = dict(User.password_hash=lambda v, c, m, p: generate_password_hash(m.password_hash))
    # which columns can be added in create list
    column_create_list = (User.firstname, User.lastname, User.dateofbirth, User.username, User.password_hash, User.streetname, User.housenumber, User.flatnumber, User.gender, User.telephone, User.role, User.estate)








class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AdminGuestsView(ModelView):
    form_overrides = {
        'firstname': StringField,
    }
    #IntegerField
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_filters = ['gender', 'visit_date']
    column_searchable_list = ['firstname', 'lastname', 'telephone']
    column_editable_list = ['firstname', 'lastname']

    column_create_list = ('visit_date', 'firstname', 'lastname', 'gender', 'telephone')
    form_excluded_columns = ['users']
    column_list = ('users', 'visit_date', 'firstname', 'lastname', 'gender', 'telephone')
    form_ajax_refs = {
    'users': {
        'fields': ['id', 'firstname'],
        'page_size': 10
    }
    }
    form_args = {
            'visit_date': {
            'label': 'Visit Date',
            'validators': [required()]
            },
            'firstname': {
            'label': 'First Name',
            'validators': [required()]
            },
            'lastname': {
            'label': 'Last Name',
            'validators': [required()]
            },
            'gender': {
            'label': 'Gender',
            'validators': [required()]
            },
            'telephone': {
            'label': 'Telephone',
            'validators': [required()]
            },
    }
    form_choices = {
    'gender': [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    }


#on_form_prefill(form,id)


class AdminCodeGen(ModelView):

    # callback
    #def on_form_prefill(self,id):
        #from werkzeug.security import generate_password_hash, check_password_hash
        #generate_password_hash()
    # view Customiztion
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_filters = ['gen_date', 'user_id', 'gen_code']
    column_searchable_list = ['gen_code', 'requested_for', 'user_id', 'gen_date']
    column_editable_list = ['requested_for', 'gen_code']
    column_create_list = ('requested_for', 'gen_code', 'gen_date', 'user_id')
    form_excluded_columns = ['id']
    column_list = ('id', 'requested_for', 'user', 'gen_code', 'gen_date')


    """
    def filter_func():
        return db.session.query(Role).filter_by(name="applicant")

    form_args = {
    "roles": {
        "query_factory": filter_func
        }
    }
    """
    #user_id=current_user.id,
    suggest_codes_list = []
    for i in range(5):
        suggest_codes_list.append((i, code_generator(strpool)))
    form_choices = {"gen_code": suggest_codes_list}

    form_args = {
            'requested_for': {
            'label': 'Requested For',
            'validators': [required()]
            },
            'gen_date': {
            'label': 'Generated Code Date',
            'validators': [required()]
            },
            'user': {
            'label': 'User (Creator)',
            'validators': [required()]
            },
            'gen_code': {
            'label': 'Gen Code',
            'validators': [required()],
            },
    }




class AdminServiceView(ModelView):
    #IntegerField
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_filters = ['request_date', 'user_id', 'service_requested']
    column_searchable_list = ['id', 'user_id', 'request_date', 'service_requested']
    column_editable_list = ['service_requested', 'user_id', 'request_date']

    column_create_list = ('service_requested', 'request_date')
    #form_excluded_columns = ['users']
    column_list = ('id','user_id', 'service_requested', 'request_date')
    form_args = {
            'service_requested': {
            'label': 'Service Requested',
            'validators': [required()]
            },
            'request_date': {
            'label': 'Request Date',
            'id': 'req_date',
            'validators': [required()]
            }
    }

admin.add_view(AdminUsersView(User, db.session))
admin.add_view(AdminGuestsView(Guest, db.session))
admin.add_view(AdminCodeGen(Code, db.session))
admin.add_view(FileAdmin(static_path, name='Static Files'))

admin.add_view(AdminServiceView(Service, db.session))
admin.add_view(AdminModelView(Publication, db.session))
admin.add_view(AdminModelView(Subscription, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(Estate, db.session))
#admin.add_view(rediscli.RedisCli(Redis()))

def formatter(view, context, model, name):
    # `view` is current administrative view
    # `context` is instance of jinja2.runtime.Context
    # `model` is model instance
    # `name` is property name
    pass



"""
  {% macro render_price(model, column) %}
    {{ model.price * 2 }}
  {% endmacro %}
class UserView(ModelView):
        can_delete = False  # disable model deletion
        can_create = False
        can_edit = False
        can_delete = False

class PostView(ModelView):
        page_size = 50  # the number of entries to display on the list view
"""

"""
custom views
class Users(BaseView):
    #def is_accessible(self):
    #    return current_user.is_authenticated
    @expose('/')
    def index(self):
        return self.render('adminusers.html')

#admin.add_view(Users(name='Mange Users', endpoint='', category='Users'))
class Guests(BaseView):
    #def is_accessible(self):
    #    return current_user.is_authenticated
    @expose('/')
    def index(self):
        return self.render('adminguests.html')

#admin.add_view(Users(name='Mange Users', endpoint='', category='Users'))

class Codes(BaseView):
    #def is_accessible(self):
    #    return current_user.is_authenticated
    @expose('/')
    def index(self):
        return self.render('admincodes.html')
#admin.add_view(Users(name='Mange Users', endpoint='', category='Users'))
#admin.add_view(ModelView(Code, db.session, name='Code Generator'))

"""
