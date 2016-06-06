from fmapp import app,admin
from fmapp.models import *
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Wallet, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Transaction, db.session))