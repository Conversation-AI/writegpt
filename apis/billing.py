from flask import Blueprint, request

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/record_usage', methods=['POST'])
def record_usage():
    # implementation
    print("record_usage")