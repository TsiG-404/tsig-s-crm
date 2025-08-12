# staff_routes.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user, login_required
from db import db
from models import Staff, Product

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/add', methods=['GET'])
@login_required
def add_staff_form():
    if current_user.role != 'shop_owner':
        return "Unauthorized", 403
    return render_template('add_staff.html')

from werkzeug.security import generate_password_hash

@staff_bp.route('/staff/add', methods=['POST'])
@login_required
def add_staff():
    if current_user.role != 'shop_owner':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    password = data.get('password')

    if not all([name, email, role, password]):
        return jsonify({'message': 'Missing fields'}), 400

    existing = Staff.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': 'Staff with this email already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_staff = Staff(
        name=name,
        email=email,
        role=role,
        shop_id=current_user.shop_id,
        password_hash=hashed_password
    )
    db.session.add(new_staff)
    db.session.commit()

    return jsonify({'message': 'Staff member added successfully'})


@staff_bp.route('/product/add', methods=['GET'])
@login_required
def add_product_form():
    if current_user.role not in ['shop_owner', 'storager']:
        return "Unauthorized", 403
    return render_template('add_product.html')

@staff_bp.route('/product/add', methods=['POST'])
@login_required
def add_product():
    if current_user.role not in ['shop_owner', 'storager']:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')

    if not name or price is None:
        return jsonify({'message': 'Missing name or price'}), 400

    new_product = Product(
        name=name,
        description=description,
        price=price,
        shop_id=current_user.shop_id
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'})
from flask import render_template

@staff_bp.route('/product/add', methods=['GET'])
@login_required
def product_add_form():
    if current_user.role not in ['shop_owner', 'storager']:
        return "Unauthorized", 403
    return render_template('add_product.html')
