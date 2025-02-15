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
bp_admin = Blueprint('bp_admin', __name__)

@bp_admin.route('/add_subject',methods=['POST'])
def add_subject():
     if 'admin' in session:
          if request.method == 'POST':
              subject_name = request.form['subject_name']
              description = request.form['description']
              subject = Subject(subject_name=subject_name, description=description)
              db.session.add(subject)
              db.session.commit()
              flash('Subject added successfully!!!', category='success')
              return redirect('/admin_dashboard')
         
     else:
        return redirect('/login')
     
@bp_admin.route('/edit_subject/<int:subject_id>',methods=['POST'])
def edit_subject( subject_id):
     if 'admin' in session:
          subject = Subject.query.filter_by(id=subject_id).first()
          if not subject:
                return redirect('/admin_dashboard')
               
          else:
               if request.method == 'POST':
                    subject_name = request.form['subject_name']
                    description = request.form['description']
                    subject.subject_name = subject_name
                    subject.description = description
                    db.session.commit()
                    flash('Subject edited successfully!!!', category='success')
                    return redirect('/admin_dashboard')
               
     else:
        return redirect('/login')
     
@bp_admin.route('/delete_subject/<int:subject_id>')
def delete_subject(subject_id):
        if 'admin' in session:
            subject = Subject.query.filter_by(id=subject_id).first()
            if not subject:
                    return redirect('/admin_dashboard')
            else:
                db.session.delete(subject)
                db.session.commit()
                flash('Subject deleted successfully!!!', category='success')
                return redirect('/admin_dashboard')
        else:
            return redirect('/login')
        
@bp_admin.route('/show_subject/<int:subject_id>')
def show_subject(subject_id):
    if 'admin' in session:
        subject= Subject.query.filter_by(id=subject_id).first()
        unit = Unit.query.filter_by(subject_id=subject_id).all()
        return render_template('show_subject.html',subject=subject,unit=unit)
    else:
        return redirect('/login')
    

@bp_admin.route('/add_unit/<int:subject_id>',methods=['POST'])
def add_unit(subject_id):
     if 'admin' in session:
          if request.method == 'POST':
              unit_name = request.form['unit_name']
              description = request.form['description']
              unit = Unit(unit_name=unit_name, description=description,subject_id=subject_id)
              db.session.add(unit)
              db.session.commit()
              flash('Unit added successfully!!!', category='success')
              return redirect('/show_subject/'+str(subject_id))
     else:
        return redirect('/login')
     
@bp_admin.route('/edit_unit/<int:unit_id>',methods=['POST'])
def edit_unit( unit_id):
     if 'admin' in session:
          unit = Unit.query.filter_by(id=unit_id).first()
          
          if not unit:
                return redirect('/admin_dashboard')
               
          else:
               if request.method == 'POST':
                    unit_name = request.form['unit_name']
                    description = request.form['description']
                    unit.unit_name = unit_name
                    unit.description = description
                    db.session.commit()
                    flash('Unit edited successfully!!!', category='success')
                    return redirect('/show_subject/'+str((unit.subject_id)))
               
     else:
        return redirect('/login')
     

@bp_admin.route('/delete_unit/<int:unit_id>')
def delete_unit(unit_id):
        if 'admin' in session:
            unit = Unit.query.filter_by(id=unit_id).first()
            if not unit:
                    return redirect('/admin_dashboard')
            else:
                db.session.delete(unit)
                db.session.commit()
                flash('Unit deleted successfully!!!', category='success')
                return redirect('/show_subject/'+str((unit.subject_id)))
        else:
            return redirect('/login')
      

@bp_admin.route('/show_unit/<int:unit_id>')
def show_unit(unit_id):
    if 'admin' in session:
        unit= Unit.query.filter_by(id=unit_id).first()
        quiz = Quiz.query.filter_by(unit_id=unit_id).all()
        return render_template('show_unit.html',unit=unit,quiz=quiz)
    else:
        return redirect('/login')

        



@bp_admin.route('/add_quiz/<int:unit_id>',methods=['POST'])
def add_quiz(unit_id):
     if 'admin' in session:
          if request.method == 'POST':
              quiz_name = request.form['quiz_name']
              date = request.form['date']
              duration = request.form['duration']
              note = request.form['note']

              doq=datetime.strptime(date, "%Y-%m-%d")

 

              quiz = Quiz(quiz_name=quiz_name, date=doq, duration=duration,note=note,unit_id=unit_id)
              db.session.add(quiz)
              db.session.commit()
              flash('Quiz added successfully!!!', category='success')
              return redirect('/show_unit/'+str(unit_id))
     else:
        return redirect('/login')

@bp_admin.route('/edit_quiz/<int:quiz_id>',methods=['POST'])
def edit_quiz(quiz_id):
     if 'admin' in session:
          quiz = Quiz.query.filter_by(id=quiz_id).first()
          if quiz:
                if request.method == 'POST':
                     quiz_name = request.form['quiz_name']
                     date = request.form['date']
                     duration = request.form['duration']
                     note = request.form['note']
                     doq=datetime.strptime(date, "%Y-%m-%d")

                     quiz.quiz_name=quiz_name
                     quiz.date=doq
                     quiz.duration=duration
                     quiz.note=note
                     unit_id=quiz.unit_id
              
                     db.session.commit()
                     flash('Quiz edited successfully!!!', category='success')
                     return redirect('/show_unit/'+str(quiz.unit_id))
         
     else:
        return redirect('/admin_dashboard')


@bp_admin.route('/delete_quiz/<int:quiz_id>')
def delete_quiz(quiz_id):
        if 'admin' in session:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            if not quiz:
                    return redirect('/admin_dashboard')
            else:
                db.session.delete(quiz)
                db.session.commit()
                flash('Quiz deleted successfully!!!', category='success')
                return redirect('/show_unit/'+str((quiz.unit_id)))
        else:
            return redirect('/login')

    
@bp_admin.route('/show_quiz/<int:quiz_id>')
def show_quiz(quiz_id):
    if 'admin' in session:
        quiz= Quiz.query.filter_by(id=quiz_id).first()
        question= Question.query.filter_by(quiz_id=quiz_id).all()
        return render_template('show_quiz.html',quiz=quiz,question=question)
    else:
        return redirect('/login')



@bp_admin.route('/add_question/<int:quiz_id>',methods=['POST'])
def add_question(quiz_id):
     if 'admin' in session:
          if request.method == 'POST':
              question= request.form['question']
              option_a = request.form['option_a']
              option_b = request.form['option_b']
              option_c = request.form['option_c']
              option_d = request.form['option_d']
              answer = request.form['answer']
              hints = request.form['hints']
            

              question = Question(question=question, option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, answer=answer, hints=hints, quiz_id=quiz_id)
              db.session.add(question)
              db.session.commit()
              flash('Question added successfully!!!', category='success')
              return redirect('/show_quiz/'+str(quiz_id))
     else:
          return redirect('/login')    
 



@bp_admin.route('/edit_question/<int:question_id>',methods=['POST'])
def edit_question(question_id):
     if 'admin' in session:
          question_curr = Question.query.filter_by(id=question_id).first()
          if question_curr:
                if request.method == 'POST':
                     question= request.form['question']
                     option_a = request.form['option_a']
                     option_b = request.form['option_b']
                     option_c = request.form['option_c']
                     option_d = request.form['option_d']
                     answer = request.form['answer']
                     hints = request.form['hints']

                     question_curr.question=question
                     question_curr.option_a=option_a
                     question_curr.option_b=option_b
                     question_curr.option_c=option_c
                     question_curr.option_d=option_d
                     question_curr.answer=answer
                     question_curr.hints=hints
                     quiz_id=question_curr.quiz_id
              
                     db.session.commit()
                     flash('Question edited successfully!!!', category='success')
                     return redirect('/show_quiz/'+str(quiz_id))
          
                  
          else:
            return redirect('/admin_dashboard')

     else:
          return redirect('/login')

@bp_admin.route('/delete_question/<int:question_id>')
def delete_question(question_id):
        if 'admin' in session:
             question = Question.query.filter_by(id=question_id).first()
             if not question:
                     return redirect('/admin_dashboard')
             else:
                 db.session.delete(question)
                 db.session.commit()
                 flash('Question deleted successfully!!!', category='success')
                 return redirect('/show_quiz/'+str((question.quiz_id)))
@bp_admin.route('/logout')
def logout():
    if 'admin' in session:
         session.pop('admin')
         flash('Logged out successfully!!!', category='success')
         return redirect('/login')
    
@bp_admin.route("/admin_dashboard", methods=['GET','POST'])
def admin_dashborad():
    users=User.query.all()
    all_subjects= Subject.query.all()
    return render_template('admin_dashboard.html',users=users,all_subjects=all_subjects)


@bp_admin.route('/flag_user/<int:user_id>')
def flag_user(user_id):
      if 'admin' in session:
        user = User.query.filter_by(id=user_id).first()
        user.is_flagged=True
        db.session.commit()
        flash('User flagged successfully!!!', category='info')
        return redirect('/admin_dashboard/users')
      else:
            return redirect('/login')
    
        
@bp_admin.route('/unflag_user/<int:user_id>')
def unflag_user(user_id):
        if 'admin' in session:
            user = User.query.filter_by(id=user_id).first()
            user.is_flagged=False
            db.session.commit()
            flash('User unflagged successfully!!!', category='info')
            return redirect('/admin_dashboard/users')
        else:
                return redirect('/login')
        
@bp_admin.route('/delete_user/<int:user_id>')
def delete_user(user_id):
      if 'admin' in session:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!!!', category='info')
        return redirect('/admin_dashboard/users')
      else:
            return redirect('/login')
      
@bp_admin.route('/admin_dashboard/users')
def admin_dashboard_users():
    if 'admin' in session:
        users=User.query.all()
        return render_template('admin_dashboard_users.html',users=users)
    else:
        return redirect('/login')
@bp_admin.route('/quiz')
def quiz():
    if 'admin' in session:
          quizzes = Quiz.query.all()
          results= Result.query.all()
          return render_template('quiz.html',quizzes=quizzes,results=results)
    else:
          return redirect('/login')

@bp_admin.route('/admin_dashboard/search',methods=['GET','POST'])
def admin_dashboard_search():
    if 'admin' in session:
        if request.method == 'GET':
            search = request.args.get('search') 

            users = User.query.filter(User.full_name.ilike('%'+search+'%')).all()
            units = Unit.query.filter(Unit.unit_name.ilike('%'+search+'%')).all()
            subjects = Subject.query.filter(Subject.subject_name.ilike('%'+search+'%')).all()
            quizzes = Quiz.query.filter(Quiz.quiz_name.ilike('%'+search+'%')).all()
            return render_template('admin_dashboard_search.html', users=users, units=units, subjects=subjects, quizzes=quizzes)
           
        else:
            return redirect('/admin_dashboard')
    else:
        return redirect('/login')
    


@bp_admin.route('/admin_dashboard/summary')
def admin_dashboard_summary():
    if 'admin' in session:
        
        data = db.session.query(Subject.subject_name,func.max(Result.score).label('top_score'),func.count(Result.id).label('attempts')).join(Unit, Subject.id == Unit.subject_id).join(Quiz, Unit.id == Quiz.unit_id).join(Result, Quiz.id == Result.quiz_id).group_by(Subject.subject_name).all()

       
        subjects = [item[0] for item in data]
        top_scores = [item[1] for item in data]
        attempts = [item[2] for item in data]

        
        plt.figure(figsize=(6, 4))
        seaborn.barplot(x=subjects, y=top_scores, palette='viridis')
        plt.title('Subject-wise Top Scores')
        plt.xlabel('Subjects')
        plt.ylabel('Top Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/images/top_scores.png')
        plt.close()

        
        plt.figure(figsize=(4, 4))
        plt.pie(attempts, labels=subjects, autopct='%1.1f%%', startangle=140, colors=seaborn.color_palette('pastel'))
        plt.title('Subject-wise User Attempts')
        plt.savefig('static/images/user_attempts.png')
        plt.close()

        return render_template('admin_dashboard_summary.html',
                  top_scores_img=url_for('static', filename='images/top_scores.png'),
                  user_attempts_img=url_for('static', filename='images/user_attempts.png'))


    return redirect('/login')