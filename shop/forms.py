from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, FileField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from shop.models import User
from bcrypt import checkpw
from flask_login import login_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name is required.'), Length(max=50, message='Name is too long')
    ])
    
    surname = StringField('Surname', validators=[
        DataRequired(message='Surname is required.'), Length(max=50, message='Surname is too long')
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Invalid email address.'), 
        Length(max=80, message='Email is too long')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters long.')
    ])
    
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(message='Password confirmation is required.'),
        EqualTo('password', message='Passwords must match.')
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email is not registered.')
        
    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(password.data.encode('utf-8')):
            raise ValidationError('Password is incorrect.')
        elif user and user.check_password(password.data.encode('utf-8')):
            temp = login_user(user)
            if temp: print('Login avvenuto con successo')

class AddItemFrom(FlaskForm):
    image = FileField('Item image', validators=[
        DataRequired(message='Image is required')
    ])
    name = StringField('Item name', validators=[
        DataRequired(message='Name is required'),
        Length(max=30, message='Invalid name length')
    ])
    category = SelectField('Item category', validators=[
        DataRequired(message='Choose a category')
    ], choices=[('1', 'Vehicles'), ('2', 'Clothing'), ('3', 'Health'), ('4', 'Fun'), ('5', 'Home'), ('6', 'Other')]
    )
    description = TextAreaField('Item description', validators=[
        DataRequired(message='Description is required',)
    ], render_kw={"rows": 70, "cols": 11}   )
    price = FloatField('Item price', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, message="Please enter a positive number.")
    ])

class SearchForm(FlaskForm):
    search = StringField('Search')
    category = SelectField('Item category', choices=[('0', 'Category'), ('1', 'Vehicles'), ('2', 'Clothing'), ('3', 'Health'), ('4', 'Fun'), ('5', 'Home'), ('6', 'Other')]
    )

