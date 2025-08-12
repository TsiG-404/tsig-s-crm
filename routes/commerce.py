from flask import Blueprint, request, jsonify
from models import db, Product, Order, OrderItem
from flask_login import login_required

commerce_bp = Blueprint('commerce', __name__)

@commerce_bp.route('/products', methods=['GET'])
@login_required
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id, 'name': p.name,
        'price': float(p.price), 'stock': p.stock
    } for p in products])

@commerce_bp.route('/products', methods=['POST'])
@login_required
def create_product():
    data = request.get_json()
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product_id': product.id}), 201

@commerce_bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()  # contains: customer_email, items: [{product_id, quantity}]
    order = Order(customer_email=data['customer_email'])
    db.session.add(order)
    db.session.flush()  # so we get order.id

    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            db.session.rollback()
            return jsonify({'error': f"Insufficient stock for {product.name}"}), 400
        product.stock -= item['quantity']
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item['quantity'],
            price_at_order=product.price
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'Order placed', 'order_id': order.id})

@commerce_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'customer_email': o.customer_email,
        'status': o.status,
        'created_at': o.created_at.isoformat()
    } for o in orders])



from flask import Blueprint, render_template
from models import Shop, Product, Staff
#from models import Shop, Product, StaffProfile

from db import db

commerce_bp = Blueprint('commerce', __name__)

@commerce_bp.route('/shop/<int:shop_id>')
def shop_page(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    products = Product.query.filter_by(shop_id=shop.id).all()
    staff_list = Staff.query.filter_by(shop_id=shop.id).all()

    return render_template('shop_page.html', shop=shop, products=products, staff_list=staff_list)
