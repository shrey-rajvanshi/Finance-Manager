from fmapp import db
from datetime import datetime
from flask.ext.login import UserMixin
from fmapp import *


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    authenticated = db.Column(db.Boolean, default=False)
    last_synced = db.Column(db.String(10))

    def get_id(self):
        return self.id

    def check_password(self, password):
        if self.password is None:
            return False
        return self.password == password

    # methods
    @classmethod
    def authenticate(cls, user_name, password):
        user = User.query.filter(db.or_(User.username == user_name)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def is_user_name_taken(cls, user_name):
        return db.session.query(db.exists().where(User.username == user_name)).scalar()

    @classmethod
    def is_email_taken(cls, email_address):
        return db.session.query(db.exists().where(User.email == email_address)).scalar()




@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)
