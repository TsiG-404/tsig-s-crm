from flask import Blueprint, jsonify
from models import db, Lead, Opportunity, Ticket
from flask_login import login_required
from sqlalchemy import func
from models import OrderItem




analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
@login_required
def get_analytics():
    lead_count = Lead.query.count()
    open_tickets = Ticket.query.filter_by(status='Open').count()
    opps_by_stage = db.session.query(
        Opportunity.stage, db.func.count(Opportunity.id)
    ).group_by(Opportunity.stage).all()

    total_sales = db.session.query(
    func.sum(OrderItem.price_at_order * OrderItem.quantity)
).scalar() or 0
    return jsonify({
    'leads': lead_count,
    'open_tickets': open_tickets,
    'opportunities_by_stage': dict(opps_by_stage),
    'total_sales': float(total_sales)
})

    return jsonify({
        'leads': lead_count,
        'open_tickets': open_tickets,
        'opportunities_by_stage': dict(opps_by_stage)
    })
