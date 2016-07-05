from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/vagrant/www/Finance-Manager/fm.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fmn'
db = SQLAlchemy(app)

admin = Admin(app, name='Welcome to Shrey\'s  Finance Manager', template_mode='bootstrap3')

from fmapp import views, models, admin_models, clientviews
