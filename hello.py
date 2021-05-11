import os
from threading import Thread
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = "beardtao_test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = "smtp.126.com"
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = os.environ.get('mail_username')
app.config['MAIL_PASSWORD'] = os.environ.get('mail_password')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField('请输入名称', validators=[DataRequired()])
    submit = SubmitField('提交')


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, index=True)
    password = db.Column(db.String())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


def send_mail(username):
    title = "welcome"
    msg = Message(title, sender="beardtao@126.com", recipients=['beardtao@163.com'])
    msg.html = "<h1> welcome new user %s</h1>" % username
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data, password='123456')
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            send_mail(form.name.data)
        else:
            session['known'] = True
        session['name'] = request.form.get("name")
        form.name.data = ""
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
