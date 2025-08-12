from flask import Flask, render_template, jsonify, request, session, redirect, url_for, abort
from flask_login import LoginManager, login_required, current_user
from db import db
from models import User
from flask_login import login_user


# Blueprints
from routes.sales import sales_bp
from routes.auth import auth_bp
from routes.service import service_bp
from routes.analytics import analytics_bp
from routes.marketing import marketing_bp
from routes.commerce import commerce_bp
from routes.experience import experience_bp
from routes.shop import shop_bp
from routes.staff_routes import staff_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(sales_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(service_bp, url_prefix='/service')
app.register_blueprint(analytics_bp, url_prefix='/analytics')
app.register_blueprint(marketing_bp, url_prefix='/marketing')
app.register_blueprint(commerce_bp, url_prefix='/commerce')
app.register_blueprint(experience_bp, url_prefix='/experience')
app.register_blueprint(shop_bp, url_prefix='/shop')
app.register_blueprint(staff_bp)
#app.register_blueprint(staff_bp)


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

from models import Shop, User, Product, Ticket, Order  # make sure these are imported
@app.route('/dashboard')
@login_required
def dashboard():
    role = current_user.role
    if role == 'shop_owner':
        return render_template('dashboard_shop_owner.html', user=current_user)
    
    #elif role == 'admin':
       # return render_template('dashboard_admin.html', user=current_user)
    elif role == 'admin':
    

        shops = Shop.query.all()
        users = User.query.all()
        products = Product.query.all()
        tickets = Ticket.query.all()
        orders = Order.query.all()

        return render_template(
        'dashboard_admin.html',
        user=current_user,
        shops=shops,
        users=users,
        products=products,
        tickets=tickets,
        orders=orders
        )

    
    elif role == 'marketer':
        return render_template('dashboard_marketer.html', user=current_user)
    elif role == 'support':
        return render_template('dashboard_support.html', user=current_user)
    elif role == 'storager':
        return render_template('dashboard_storager.html', user=current_user)
    elif role == 'customer':
        # Load necessary customer data
        shops = Shop.query.all()
        tickets = Ticket.query.filter_by(customer_email=current_user.email).all()
        orders = Order.query.filter_by(customer_email=current_user.email).all()
        products = Product.query.all()
        total_orders = len(orders)
        total_spent = sum(order.total for order in orders)

        return render_template(
            'dashboard_customer.html',
            user=current_user,
            shops=shops,
            tickets=tickets,
            orders=orders,
            products=products,
            total_orders=total_orders,
            total_spent=total_spent
        )
    else:
        abort(403)


@app.route('/analytics')
def analytics():
    analytics_data = {
        "leads": 120,
        "open_tickets": 15,
        "opportunities_by_stage": {
            "Prospect": 30,
            "Qualified": 20,
            "Proposal": 10,
            "Closed Won": 50,
            "Closed Lost": 10
        },
        "total_sales": 34500.75,
        "sales_by_day": {
            "2025-06-01": 5000,
            "2025-06-02": 7000,
            "2025-06-03": 8000,
            "2025-06-04": 7500,
            "2025-06-05": 4000
        },
        "sentiment_counts": {
            "positive": 40,
            "neutral": 30,
            "negative": 10
        }
    }
    return jsonify(analytics_data)

@app.route('/customer/profile')
def customer_profile():
    email = request.args.get('email', '').lower()
    customer_profiles = {
        "alice@example.com": {
            "email": "alice@example.com",
            "total_orders": 5,
            "total_spent": 1200.50,
            "experiences": [
                {
                    "interaction_type": "call",
                    "sentiment": "positive",
                    "created_at": "2025-05-30T10:00:00",
                    "notes": "Discussed new features."
                },
                {
                    "interaction_type": "support",
                    "sentiment": "neutral",
                    "created_at": "2025-06-01T14:30:00",
                    "notes": "Resolved billing issue."
                }
            ]
        },
        "bob@example.com": {
            "email": "bob@example.com",
            "total_orders": 2,
            "total_spent": 400,
            "experiences": []
        }
    }
    profile = customer_profiles.get(email)
    if profile:
        return jsonify(profile)
    else:
        return jsonify({"message": "Customer not found"}), 404
    


@app.route('/admin/shops')
@login_required
def admin_shops():
    if current_user.role != 'admin':
        abort(403)
    shops = Shop.query.all()
    return render_template('admin_shops.html', shops=shops)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin_users.html', users=users)

# Similarly for products, tickets, orders...


from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from db import db
from models import Staff

staff_bp = Blueprint('staff', __name__)

from flask import render_template

@staff_bp.route('/staff/add', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role != 'shop_owner':
        return render_template('unauthorized.html'), 403  # Or use `abort(403)`

    if request.method == 'GET':
        return render_template('add_staff.html')

    # Handle POST (AJAX submission)
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    role = data.get('role')

    if not all([name, email, role]):
        return jsonify({'message': 'Missing fields'}), 400

    existing = Staff.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': 'Staff with this email already exists'}), 400

    new_staff = Staff(name=name, email=email, role=role, shop_id=current_user.shop_id)
    db.session.add(new_staff)
    db.session.commit()

    return jsonify({'message': 'Staff member added successfully'})




from models import Product

@staff_bp.route('/product/add', methods=['POST','GET'])
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


# Test login users
@app.route('/test_login/<role>')
def test_login(role):
    test_users = {
        "shop_owner": {
            'name': 'Alice ShopOwner', 'role': 'shop_owner',
            'shop': {'name': 'Alice Store', 'storage_name': 'Alice Storage', 'id': 101}
        },
        "admin": {'name': 'Bob Admin', 'role': 'admin'},
        "marketer": {
            'name': 'Carol Marketer', 'role': 'marketer',
            'shop': {'name': 'Carol Store', 'storage_name': 'Carol Storage', 'id': 102}
        },
        "support": {
            'name': 'Dave Support', 'role': 'support',
            'shop': {'name': 'Dave Store', 'storage_name': 'Dave Storage', 'id': 103}
        },
        "storager": {
            'name': 'Eve Storager', 'role': 'storager',
            'shop': {'name': 'Eve Store', 'storage_name': 'Eve Storage', 'id': 104}
        }
    }
    user = User.query.filter_by(role=role).first()
    if not user:
        # Optionally create a test user if none exists
        user = User(name=f'Test {role.title()}', email=f'{role}@example.com', role=role)
        user.set_password('test123')  # or some dummy password
        db.session.add(user)
        db.session.commit()

    login_user(user)  # <-- log in user here!
    return redirect(url_for('dashboard'))




from models import User, Staff

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return user
    return Staff.query.get(int(user_id))





if __name__ == '__main__':
   # app.register_blueprint(staff_bp)

    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(name='Admin', email='admin@example.com', role='admin')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
