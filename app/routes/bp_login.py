from flask import Flask,render_template,request,redirect,url_for,flash,session,Blueprint
from models.models import User,Subject,Unit,Quiz,Question,Result,db

bp_login = Blueprint('bp_login', __name__)
@bp_login.route("/")
def home():
    return render_template('home.html')

@bp_login.route("/login",methods=['GET','POST'])
def login():
     if request.method == 'GET':
         return render_template('login.html')
     if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            
            if user :
                 if user.if_admin:
                      if user.password == password:
                           session['admin']=user.id
                           return redirect('/admin_dashboard')
                      else:
                           flash('Wrong Password!!!', category='warning')
                           return redirect('/login')
                 else:
                      
                      if user.password == password:
                           
                           if user.is_flagged:
                                flash('Your account is blocked!!!', category='warning')
                                return redirect('/login')
                           else:
                                session['user']=user.id
                                return redirect('/user_dashboard')
                               
                                                   
                      else:
                           flash('Wrong Password!!!', category='warning')
                           return redirect('/login')
            else:
                 flash('User not found!!!', category='warning')
                 return redirect('/login')
        
#create a new user
@bp_login.route("/register",methods=['GET','POST'])

def register_user():
     if request.method == 'GET':
         return render_template('register.html')
     if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            edu_qualification = request.form['edu_qualification']
            dob = request.form['dob']
            user = User(email=email, password=password, full_name=full_name, edu_qualification=edu_qualification, dob=dob, if_admin=False)
            db.session.add(user)
            db.session.commit()
            flash('User registered successfully!!! Login to continue', category='success')

            
            return redirect('/login')

