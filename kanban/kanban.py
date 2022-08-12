import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'kanban.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SECRET_KEY'] = 'DzV0uepzTJMe6rp6SA3XSJHjXOmUSmHG'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=False)
    task_name = db.Column(db.String(150), unique=False, nullable=False)
    status = db.Column(db.String(20), unique=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(
        message="Invalid Email"), Length(max=50)], render_kw={"placeholder": "Email Address"})
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})


class CreateForm(FlaskForm):
    task_name = StringField(validators=[InputRequired(), Length(
        min=2, max=130)], render_kw={"placeholder": "Enter a task"})
    status = RadioField('Status', choices=[(
        'todo', 'To Do'), ('doing', 'Doing'), ('done', 'Done')], validators=[InputRequired()])


@app.route('/', methods=['GET', 'POST'])
# Sign up field
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account is successfully created! Please login to manage your tasks! :)')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful!')
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


# Login required to enter kanban board dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    todo = Task.query.filter_by(status="todo", id=current_user.id).all()
    doing = Task.query.filter_by(status="doing", id=current_user.id).all()
    done = Task.query.filter_by(status="done", id=current_user.id).all()
    return render_template('dashboard.html', username=current_user.username, todo=todo, doing=doing, done=done)


# Login required to add task to board
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = CreateForm(request.form)
    if form.validate_on_submit():

        new_task = Task(id=current_user.id,
                        task_name=form.task_name.data, status=form.status.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('kanban.html', form=form)


@app.route('/doing/<task_id>', methods=['GET', 'POST'])
def doing(task_id):
    task = Task.query.filter_by(task_id=int(task_id)).first()
    task.status = 'doing'
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/done/<task_id>', methods=['GET', 'POST'])
def done(task_id):
    task = Task.query.filter_by(task_id=int(task_id)).first()
    task.status = 'done'
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/delete/<task_id>', methods=['GET', 'POST'])
def delete(task_id):
    deleted = Task.query.filter_by(task_id=int(task_id)).first()
    db.session.delete(deleted)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out. Please login.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
