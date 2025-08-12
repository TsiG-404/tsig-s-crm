from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Staff, Product, Shop

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/add-staff', methods=['POST'])
@login_required
def add_staff():
    data = request.get_json()
    staff = Staff(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        shop_id=current_user.shop_id
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({"message": "Staff member added"})

@shop_bp.route('/add-product', methods=['POST'])
@login_required
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        shop_id=current_user.shop_id
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added"})