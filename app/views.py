from itertools import izip, chain, repeat

from flask import render_template, request, redirect, flash
from flask.ext.security import Security, login_required, logout_user, roles_required, current_user, utils
from flask.ext.admin import Admin, expose, AdminIndexView, base
from flask.ext.admin.contrib.sqla import ModelView
import flask.ext.restless
from flask.ext.restless import ProcessingException
from gcm import *

from models import *
from forms import *


# --------- FLASK Security has a very nice documentation. read more here -> https://pythonhosted.org/Flask-Security/
security = Security(app, user_datastore)


def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return izip(*[chain(iterable, repeat(padvalue, n - 1))] * n)


def send_push_notification_with_payload(category, payload):
    gcm = GCM("YOUR_API_KEY_HERE")
    data = {'data': payload, 'param2': 'value2'}

    if category != "all":
        selected_users = AndroidUsers.query.filter_by(category=category).all()
    else:
        selected_users = AndroidUsers.query.all()

    # --------- group them by 1000 ---------
    for chunk_Users in grouper(500, selected_users, 'x'):
        print "------- processing new chunk -----"
        reg_ids = [user.reg_id for user in chunk_Users if user != 'x']


        response = gcm.json_request(registration_ids=reg_ids, data=data, delay_while_idle=True)

        # Handling errors
        if 'errors' in response:
            for error, reg_ids in response['errors'].items():
                # Check for errors and act accordingly
                if error == 'NotRegistered':
                    # Remove reg_ids from database
                    for reg_id in reg_ids:
                        invalid_user = AndroidUsers.query.filter(AndroidUsers.reg_id == reg_id).first()
                        db.session.delete(invalid_user)
                        db.session.commit()

                if error == 'InvalidRegistration':
                    # Remove invalid registration ids from the database
                    for reg_id in reg_ids:
                        invalid_user = AndroidUsers.query.filter(AndroidUsers.reg_id == reg_id).first()
                        db.session.delete(invalid_user)
                        db.session.commit()

        if 'canonical' in response:
            for reg_id, canonical_id in response['canonical'].items():
                # Repace reg_id with canonical_id in your database
                print "replacing with canonical_id " + canonical_id
                db.session.query(AndroidUsers).filter(AndroidUsers.reg_id == reg_id).update({AndroidUsers.reg_id: canonical_id})
                db.session.commit()

    return response


@app.route('/send_push_notifications', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def send_push_notifications():
    form = SendPushNotificationsForm(request.form)

    if request.method == 'POST':
        if form.validate():
            payload = form.payload.data
            category = form.category.data

            logging.info("@ " + category)
            logging.info(">> " + payload)

            ret = send_push_notification_with_payload(category, payload)
            flash(ret)

    return render_template("send_push_notifications.html", form=form)


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
@roles_required('admin')
def index(page=1):
    m_users = AndroidUsers()
    list_records = m_users.list_all(page, app.config['LISTINGS_PER_PAGE'])
    return render_template("index.html", list_records=list_records)


@app.route('/api_info')
@login_required
@roles_required('admin')
def api_info():
    return render_template("api_info.html")


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(request.args.get('next') or '/')


# Executes before the first request is processed.
@app.before_first_request
def before_first_request():
    logging.info("-------------------- initializing admin ---------------------")
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    encrypted_password = utils.encrypt_password('123123')
    if not user_datastore.get_user('me@me.com'):
        user_datastore.create_user(email='me@me.com', password=encrypted_password, active=True, confirmed_at=datetime.datetime.now())
    db.session.commit()
    user_datastore.add_role_to_user('me@me.com', 'admin')
    db.session.commit()


# -------------------------- REST API PART ------------------------------------
# --------- FLASK RESTLESS has a very nice documentation. read more here -> https://flask-restless.readthedocs.org/en/latest/index.html

api_manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
def post_preprocessor(data=None, **kw):
    auth = request.headers.get('Authorization', '').lower()
    if auth != 'mysecretauthkey':
        raise ProcessingException(description='Not Authorized',
                                  code=401)
    pass

blueprint = api_manager.create_api(
    AndroidUsers,
    methods=['POST'],
    url_prefix='/api/v1',
    collection_name='androidusers',
    allow_patch_many=False,
    preprocessors={
        'POST': [post_preprocessor],
    }
)
# --------------------------  END REST API PART ------------------------------------



# -------------------------- ADMIN PART ------------------------------------
# --------- FLASK ADMIN has a very nice documentation. read more here -> http://flask-admin.readthedocs.org/en/latest/

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


# ------- visible only to admin user, else returns "not found" -----------
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.has_role('admin'):
            return render_template('other/404.html'), 404
        return self.render('admin/index.html')


class AndroidUsersAdminView(MyModelView):
    can_create = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(AndroidUsersAdminView, self).__init__(AndroidUsers, session, **kwargs)


class UserAdminView(MyModelView):
    column_exclude_list = ('password')

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(UserAdminView, self).__init__(User, session, **kwargs)


class RoleView(MyModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


admin = Admin(app, 'GCM Server Admin', index_view=MyAdminIndexView())
admin.add_view(AndroidUsersAdminView(db.session))
admin.add_view(UserAdminView(db.session))
admin.add_view(RoleView(db.session))
admin.add_link(base.MenuLink('Web Home', endpoint="index"))
admin.add_link(base.MenuLink('Logout', endpoint="log_out"))

# --------------------------  END ADMIN PART ---------------------------------

