from fmapp import app,admin
from fmapp.models import *
from flask_admin.contrib.sqla import ModelView

class TransactionAdmin(ModelView):
        column_list = ('name', 'amount','date')
        column_sortable_list = ('date')
        column_default_sort = ('date', True)

admin.add_view(ModelView(Wallet, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Transaction, db.session))
