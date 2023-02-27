from flask import Blueprint, request

user_bp = Blueprint('user', __name__)

@user_bp.route('/delete_profile', methods=['POST'])
def delete_profile():
    # implementation
    print("delete_profile")

@user_bp.route('/update_profile', methods=['POST'])
def update_profile():
    # implementation
    print("update_profile")