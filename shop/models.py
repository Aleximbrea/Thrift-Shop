from shop import db, login_manager
from bcrypt import checkpw
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    surname = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=80), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    is_owner = db.Column(db.Boolean(), default=False, nullable=False)
    items_reserved = db.relationship('Item', backref='booker', lazy=True)

    def check_password(self, password):
        print(password, self.password_hash)
        return checkpw(password, self.password_hash)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=False)
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=False)
    price = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.String(length=100), nullable=False)
    category = db.Column(db.String(length=100), nullable=False)
    booked = db.Column(db.Boolean(), default=False)
    booker_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

