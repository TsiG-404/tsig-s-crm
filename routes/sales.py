from flask import Blueprint, request, jsonify
from models import db, Lead, Opportunity

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    lead = Lead(**data)
    db.session.add(lead)
    db.session.commit()
    return jsonify({"message": "Lead created", "lead_id": lead.id}), 201

@sales_bp.route('/leads/<int:lead_id>/convert', methods=['POST'])
def convert_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    opp = Opportunity(
        lead_id=lead.id,
        name=f"Opportunity for {lead.name}",
        value=1000  # placeholder value
    )
    db.session.add(opp)
    db.session.commit()
    return jsonify({"message": "Lead converted to opportunity", "opp_id": opp.id})
