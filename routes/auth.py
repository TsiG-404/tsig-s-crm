from flask import Blueprint, request, jsonify, session, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Shop

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'].lower())
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email').lower()
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    return render_template('login.html')



'''
@auth_bp.route('/signup-owner', methods=['GET', 'POST'])
def signup_owner():
    if request.method == 'GET':
        return render_template('signup_owner.html')

    data = request.get_json()
    email = data['email'].lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(name=data['name'], email=email, role='owner')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    shop_slug = data['shop_name'].strip().lower().replace(' ', '-')
    shop = Shop(name=data['shop_name'], storage_name=data['storage_name'], owner=user)
    db.session.add(shop)
    db.session.commit()

    return jsonify({'message': 'Shop owner created', 'shop_slug': shop_slug})
from flask import render_template_string, current_app
import os
'''
import os
from flask import current_app, render_template

@auth_bp.route('/signup-owner', methods=['GET', 'POST'])
def signup_owner():
    if request.method == 'GET':
        return render_template('signup_owner.html')

    data = request.get_json()
    email = data['email'].lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create user
    user = User(name=data['name'], email=email, role='shop_owner')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    # Create shop
    shop_slug = data['shop_name'].strip().lower().replace(' ', '-')
    shop = Shop(name=data['shop_name'], storage_name=data['storage_name'], owner=user)
    db.session.add(shop)
    db.session.commit()

    # Fetch products and staff (probably empty now)
    products = []  # or Product.query.filter_by(shop_id=shop.id).all() if any
    staff_list = [] # or Staff.query.filter_by(shop_id=shop.id).all()

    # Render shop page to HTML string
    html_content = render_template('shop_page.html', shop=shop, products=products, staff_list=staff_list)

    # Prepare path to save static file
    shops_dir = os.path.join(current_app.static_folder, 'shops')
    os.makedirs(shops_dir, exist_ok=True)
    file_path = os.path.join(shops_dir, f"{shop_slug}.html")

    # Write the rendered HTML to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Return the URL to the static shop page
    shop_url = f"/static/shops/{shop_slug}.html"
    return jsonify({'message': 'Shop owner created', 'shop_url': shop_url})


@auth_bp.route('/signup-customer', methods=['GET', 'POST'])
def signup_customer():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email'].lower()
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 409

        user = User(
            name=data['name'],
            email=email,
            role='customer'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Customer account created'})
    else:
        return render_template('signup_customer.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})



#isos oxi? 
from flask_login import login_user
from models import Staff

@auth_bp.route('/login-staff', methods=['GET', 'POST'])
def login_staff():
    if request.method == 'GET':
        return render_template('login_staff.html')

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    staff = Staff.query.filter_by(email=email).first()
    if not staff or not staff.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(staff)
    return jsonify({'message': 'Logged in successfully'})
