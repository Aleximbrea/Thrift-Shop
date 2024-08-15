
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'awcdny7ac_&%"RWF'
app.config['UPLOAD_FOLDER'] = 'shop\static\imgs'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Importing application routes
from shop import routes