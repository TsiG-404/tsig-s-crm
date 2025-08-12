from flask import Blueprint, request, jsonify
from models import db, Ticket
from flask_login import login_required

service_bp = Blueprint('service', __name__)

@service_bp.route('/tickets', methods=['GET'])
@login_required
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([{
        'id': t.id,
        'subject': t.subject,
        'status': t.status,
        'created_at': t.created_at.isoformat(),
        'assigned_to': t.assigned_to
    } for t in tickets])

@service_bp.route('/tickets', methods=['POST'])
@login_required
def create_ticket():
    data = request.get_json()
    ticket = Ticket(**data)
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket created', 'ticket_id': ticket.id}), 201

@service_bp.route('/tickets/<int:ticket_id>', methods=['PATCH'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.get_json()
    if 'status' in data:
        ticket.status = data['status']
    if 'assigned_to' in data:
        ticket.assigned_to = data['assigned_to']
    db.session.commit()
    return jsonify({'message': 'Ticket updated'})
