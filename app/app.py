from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from datetime import datetime,date
import seaborn as seaborn
import matplotlib
import matplotlib.pyplot as plt
import os
from models.models import User,Subject,Unit,Quiz,Question,Result,db
from routes.bp_login import bp_login
from routes.bp_admin import bp_admin
from routes.bp_user import bp_user
matplotlib.use('agg')


curr_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(curr_dir, "static","images")
    
def add_admin():
    if not User.query.filter_by(email='admin1234@gmail.com').first():
        admin = User(email='admin1234@gmail.com', password='1234', full_name='Admin', edu_qualification='B.Tech Computer Science', dob='01/01/2000', if_admin=True)
        db.session.add(admin)
        db.session.commit()

app.register_blueprint(bp_login)
app.register_blueprint(bp_admin)
app.register_blueprint(bp_user)
          
db.init_app(app)
with app.app_context():
       db.create_all()
       add_admin()
         
if __name__ == "__main__":
    app.run(debug=True)