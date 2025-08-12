from flask import Blueprint, request, jsonify
from models import db, ExperienceLog
from flask_login import login_required

experience_bp = Blueprint('experience', __name__)

@experience_bp.route('/experience', methods=['GET'])
@login_required
def list_experiences():
    logs = ExperienceLog.query.order_by(ExperienceLog.created_at.desc()).all()
    return jsonify([{
        'id': log.id,
        'customer_email': log.customer_email,
        'interaction_type': log.interaction_type,
        'notes': log.notes,
        'sentiment': log.sentiment,
        'rating': log.rating,
        'created_at': log.created_at.isoformat()
    } for log in logs])

@experience_bp.route('/experience', methods=['POST'])
@login_required
def create_experience():
    data = request.get_json()
    log = ExperienceLog(**data)
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Experience log saved', 'log_id': log.id})
