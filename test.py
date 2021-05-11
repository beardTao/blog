from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html', items=[1, 2, 3, 4])


@app.route('/index2')
def index2():
    return render_template('template2.html')


@app.route('/index3')
def index3():
    return render_template("yansheng.html")

# app.add_url_rule('/index2', "index2", index2)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, items=[1, 2, 3, 4])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def interval_server_error(e):
    return render_template("500.html"), 500


@app.route("/get-url")
def get_url():
    return url_for("user", name=1, _external=True)


@app.route("/hello", methods=['POST', 'GET'])
def hello():
    name = None
    if request.method == 'POST':
        name = request.form.get("name")
    return render_template("raw_form.html", name=name)