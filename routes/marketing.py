from flask import Blueprint, request, jsonify
from models import db, Campaign, Lead, EmailLog
from flask_login import login_required

marketing_bp = Blueprint('marketing', __name__)

@marketing_bp.route('/campaigns', methods=['GET'])
@login_required
def list_campaigns():
    campaigns = Campaign.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'content': c.content,
        'sent_count': c.sent_count,
        'target_segment': c.target_segment,
        'created_at': c.created_at.isoformat()
    } for c in campaigns])

@marketing_bp.route('/campaigns', methods=['POST'])
@login_required
def create_campaign():
    data = request.get_json()
    campaign = Campaign(**data)
    db.session.add(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign created', 'campaign_id': campaign.id}), 201

@marketing_bp.route('/campaigns/<int:id>/send', methods=['POST'])
@login_required
def send_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    leads = Lead.query.all()

    if campaign.target_segment:
        leads = [l for l in leads if campaign.target_segment.lower() in (l.source or '').lower()]

    for lead in leads:
        log = EmailLog(campaign_id=id, recipient_email=lead.email)
        db.session.add(log)

    campaign.sent_count += len(leads)
    db.session.commit()

    return jsonify({'message': f'Campaign sent to {len(leads)} leads'})
