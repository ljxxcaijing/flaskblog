from werkzeug.security import generati_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from flask.ext.login import login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serialiaer
from flask import current_app
from . import db

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    usrname = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(ab.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dump({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

class User(db.Model):
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
