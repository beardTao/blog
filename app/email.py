from threading import Thread
from flask_mail import Mail, Message

mail = Mail()


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
