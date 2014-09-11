import datetime

from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from sqlalchemy import desc

from app import db



# ------------- FLASK-SECURITY STUFF ------------------------
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email


user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# ------------- END FLASK-SECURITY STUFF ------------------------




class AndroidUsers(db.Model):
    __tablename__ = "andorid_users"
    id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.String(255))
    category = db.Column(db.String(255))
    extra_info = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime, default=datetime.datetime.now)


    def add_data(self, reg_id, category, extra_info):
        new_expense = AndroidUsers(reg_id=reg_id, category=category, extra_info=extra_info)
        db.session.add(new_expense)
        db.session.commit()

    def list_all(self, page, LISTINGS_PER_PAGE):
        return AndroidUsers.query.order_by(desc(AndroidUsers.confirmed_at)).paginate(page, LISTINGS_PER_PAGE, False)


    def __repr__(self):
        return '<AndroidUsers %r>' % (self.id)





