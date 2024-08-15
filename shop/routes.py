from shop import app
from flask import render_template, request, redirect, url_for
from shop.models import User, Item
from shop.forms import RegistrationForm, LoginForm, AddItemFrom, SearchForm
from shop import db
from bcrypt import hashpw, gensalt
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os


@app.route('/')
def homepage():
    # Only displaying 4 items
    items = Item.query.limit(limit=4).all()
    return render_template('index.html', items = items)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        # Adding user to the database after validation
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data, password_hash=hashpw(form.password.data.encode('utf-8'), gensalt()))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile'))
    

    return render_template('register.html', form=form)

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    # Form to filter results
    form = SearchForm()
    if request.method == 'POST':
        # If a post request is sent it means that the user is trying to reserve an item
        # Getting the requested item
        item_to_reserve = Item.query.filter_by(id=request.form.get('item_id')).first()
        # Changing item's attribute booked to True
        item_to_reserve.booked = True
        # Changing item's attribute booker_id to logged in user id
        item_to_reserve.booker_id = current_user.id
        db.session.commit()

    # If get parameters are set
    search_query = request.args.get('search', '')
    selected_category = request.args.get('category', '')

    # If selected_category is 0 it means that no category was selected so i make it None
    if selected_category == '0':
        selected_category = None

    query = Item.query

    # Applying the filters
    if search_query:
        query = query.filter(Item.name.like(f'%{search_query}%'))
    if selected_category:
        query = query.filter_by(category=selected_category)
    # Filtering for items that are not reserved
    query = query.filter_by(booked=False)

    # Obtaining the results
    items = query.all()
    return render_template('shop.html', items = items, form = form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        # Getting item to unreserve and changing attributes
        item_to_unreserve = Item.query.filter_by(id=request.form.get('item_id')).first()
        item_to_unreserve.booked = False
        item_to_unreserve.booker_id = None

        db.session.commit()

    # Getting item booked by current user
    items = Item.query.filter_by(booker_id=current_user.id)
    return render_template('profile.html', items = items)

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    
    if form.validate_on_submit():
        return redirect(url_for('profile'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    # Page used to delete or add new items in the shop
    # Only the owner of the shop can access it
    if current_user.is_owner:
        form = AddItemFrom()

        if form.validate_on_submit():
            file = form.image.data
            # Securing the file name
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            item = Item(name=form.name.data, description=form.description.data, price=form.price.data, image=filename, category=form.category.data)
            db.session.add(item)
            db.session.commit()

        return render_template('management_page.html', form=form)
    else:
        return redirect(url_for('homepage'))

