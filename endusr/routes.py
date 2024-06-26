from flask import render_template, flash, redirect, url_for, request
from .app import app, db
from .models import User
from .forms import LoginForm, RegistrationForm, AddClassForm
from flask_login import login_user, logout_user, current_user, login_required

from host.sql_handler import SQLHandler

sql_handler = SQLHandler()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('is_authenticated')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print('is_authenticated')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, is_lecturer=form.is_lecturer.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/lecturer/dashboard')
@login_required
def lecturer_dashboard():
    if not current_user.is_lecturer:
        return redirect(url_for('home'))
    
    # Query classes for the lecturer
    classes = sql_handler.get_classes(by='lecturer', lecturer_id=current_user.id)
    
    # Query attendance data for each class
    attendance_data = []
    for class_instance in classes:
        attendances = sql_handler.get_attendances(by='class', class_id=class_instance.class_id)
        total_students = len(attendances)
        attended_students = sum(1 for a in attendances if a.status == 'present')
        attendance_data.append({
            'class': class_instance,
            'attended': attended_students,
            'total': total_students
        })
    
    return render_template('lecturer_dashboard.html', classes=classes, attendance_data=attendance_data)



@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.is_lecturer:
        return redirect(url_for('home'))
    user_id = current_user.id
    # Query classes and attendance data for the student
    attendances = sql_handler.get_attendances(by='student', student_id=user_id)
    print(attendances)
    return render_template('student_dashboard.html', attendances=attendances)


@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if not current_user.is_lecturer:
        return redirect(url_for('home'))
    form = AddClassForm()
    if form.validate_on_submit():
        sql_handler.insert_class(
            course_code=form.course_code.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            lecturer_id=current_user.id
        )
        flash('Class added successfully!', 'success')
        return redirect(url_for('lecturer_dashboard'))
    return render_template('add_class.html', form=form)