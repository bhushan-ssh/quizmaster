from flask import Flask,render_template,request,redirect,url_for,flash,session,Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from datetime import datetime,date
import seaborn as seaborn
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
from models.models import User,Subject,Unit,Quiz,Question,Result,db

bp_user = Blueprint('bp_user', __name__)

@bp_user.route("/user_dashboard", methods=['GET','POST'])
def user_dashborad():
    if 'user' in session:
         user_id = session.get('user')
         user= User.query.filter_by(id=user_id).first()
         quizzes = Quiz.query.all()
         return render_template('user_dashboard.html',user=user,quizzes=quizzes)
    else:
         return redirect('/login')

   
@bp_user.route('/attempt_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
     if 'user' in session:
          quiz = Quiz.query.filter_by(id=quiz_id).first()
          session['quiz_id'] = quiz_id
          questions = Question.query.filter_by(quiz_id=quiz_id).all()
          user = User.query.filter_by(id=session['user']).first()
          if quiz.date != date.today():
                flash('Quiz not Available ', category='error')
                return redirect('/user_dashboard')
        
          else:
               if len(questions)> 0:
                 session["time_of_attempt"]=datetime.now()
                 return render_template('attempt_quiz.html', quiz=quiz, questions=questions, user= user)
                     
               else:
                 flash('Quiz is empty', category='error')
                 return redirect('/user_dashboard')
          
                     
          
     else:
        return redirect('/login')

@bp_user.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'user' in session:
        user_id = session.get('user')  
        questions = Question.query.filter_by(quiz_id=quiz_id).all()  
        score = 0

       
        for question in questions:
            answer = request.form.get(str(question.id))
            if answer == str(question.answer): 
                score += 1

        result = Result.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        if result: 
           
            result.score = score  
            db.session.commit() 
        else: 
           
            result = Result(score=score, user_id=user_id, quiz_id=quiz_id, time_of_attempt=session.get("time_of_attempt"))
            db.session.add(result)
            db.session.commit()  

       
        flash('Quiz submitted successfully!!!', category='success')
        return redirect('/user_dashboard/result')

    else:
        return redirect('/login')

@bp_user.route('/user_dashboard/result')
def result():
    if 'user' in session:
        user_id = session.get('user')
        user = User.query.filter_by(id=user_id).first()
        quiz = Quiz.query.filter_by(id=(session.get('quiz_id'))).first()
        quiz_id = session.get('quiz_id')
        results = Result.query.filter_by(user_id=user_id, quiz_id=quiz_id).order_by(Result.time_of_attempt).all()
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        return render_template('result.html', results=results, user= user,quiz=quiz, questions=questions)
    else:
        return redirect('/login')
@bp_user.route('/user_dashboard/scores/')  
def scores():
    if 'user' in session:
        user_id = session.get('user')
        user = User.query.filter_by(id=user_id).first()
        results = Result.query.filter_by(user_id=user_id).order_by(Result.time_of_attempt.desc()).all()
        return render_template('user_scores.html', results=results, user=user)
    else:
        return redirect('/login')

@bp_user.route('/user_profile')
def user_profile():
    if 'user' in session:
        user_id = session.get('user')
        user= User.query.filter_by(id=user_id).first()
        return render_template('user_profile.html',user=user)
    else:
        return redirect('/login')
    
@bp_user.route('/edit_user/<int:user_id>',methods=['POST'])
def edit_user(user_id):
    if 'user' in session:
        user_id = session.get('user')
        user= User.query.filter_by(id=user_id).first()
        full_name=request.form['full_name']
        email=request.form['email']
        dob=request.form['dob']
        edu_qualification=request.form['edu_qualification']
        user.full_name=full_name
        user.email=email
        user.dob=dob
        user.edu_qualification=edu_qualification
        db.session.commit()
        flash('Profile edited successfully!!!', category='success')
        return redirect('/user_profile')
    else:
        return redirect('/login')

@bp_user.route('/user_dashboard/summary')
def user_dashboard_summary():
    if 'user' in session:
        user_id = session['user']
        user = User.query.filter_by(id=user_id).first()

        # Subject-wise Quizzes Available
        subject_data = db.session.query(Subject.subject_name,func.count(Quiz.id).label('quiz_count')).join(Unit, Subject.id == Unit.subject_id).join(Quiz, Unit.id == Quiz.unit_id).group_by(Subject.subject_name).all()

        subjects = [item[0] for item in subject_data]
        quiz_counts = [item[1] for item in subject_data]

        # Generate Bar Chart for Subject-wise Quizzes Available
        plt.figure(figsize=(6, 4))
        seaborn.barplot(x=subjects, y=quiz_counts, palette='coolwarm')
        plt.title('Subject-wise Quizzes Available')
        plt.xlabel('Subjects')
        plt.ylabel('Number of Quizzes')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/images/subject_quizzes.png')
        plt.close()

        # Month-wise Quizzes Attempted
        attempt_data = db.session.query(extract('month', Result.time_of_attempt).label('month'),func.count(Result.id).label('attempts')).filter(Result.user_id == user_id).group_by('month').order_by('month').all()

        months = [f'Month {int(item[0])}' for item in attempt_data]
        attempts = [item[1] for item in attempt_data]

       
        plt.figure(figsize=(4, 4))
        plt.pie(attempts, labels=months, autopct='%1.1f%%', startangle=140, colors=seaborn.color_palette('pastel'))
        plt.title('Month-wise Quizzes Attempted')
        plt.savefig('static/images/monthly_attempts.png')
        plt.close()
        return render_template('user_dashboard_summary.html',user=user,
                               subject_quizzes_img=url_for('static', filename='images/subject_quizzes.png'),
                               monthly_attempts_img=url_for('static', filename='images/monthly_attempts.png'))

    return redirect('/login')      

@bp_user.route('/user_dashboard/search',methods=['GET','POST'])
def user_dashboard_search():
    if 'user' in session:
        if request.method == 'GET':
            search = request.args.get('search') 

            user = session.get('user')
            print (user)
            units = Unit.query.filter(Unit.unit_name.ilike('%'+search+'%')).all()
            subjects = Subject.query.filter(Subject.subject_name.ilike('%'+search+'%')).all()
            quizzes = Quiz.query.filter(Quiz.quiz_name.ilike('%'+search+'%')).all()   

            return render_template('user_dashboard_search.html', units=units, subjects=subjects, quizzes=quizzes,user=user)        
        else:
            return redirect('/user_dashboard')
    else:
          return redirect('/login')
 
@bp_user.route('/logout')
def logout():
    if 'user' in session:
         session.pop('user')
         flash('Logged out successfully!!!', category='success')
         return redirect('/login')


           