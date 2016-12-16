from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
#rom flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/vagrant/www/Finance-Manager/fm.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/practo/Desktop/project/fmn.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fmn'
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

app.secret_key = "SUperSecretKeyHAHAHA123213-12"

db = SQLAlchemy(app)
#migrate = Migrate(app, db)
admin = Admin(app, name='Welcome to Finance Manager', template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CsrfProtect(app)

app.config.from_object('fmapp.config')

from fmapp import views, models, admin_models, clientviews
