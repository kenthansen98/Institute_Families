import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e2541bd6b619d89f63257496f6b158cc'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from institutefamilies import routes