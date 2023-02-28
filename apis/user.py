from flask import Blueprint, request
# import user model
from models.user import User
# jwt required
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/delete_profile', methods=['POST'])
def delete_profile():
    # implementation
    print("delete_profile")

@user_bp.route('/update_profile', methods=['POST'])
def update_profile():
    # implementation
    print("update_profile")

# check user profile and returns user data
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    if user:
        return {'message': 'User found.', 'user': user.to_dict()}, 200
    else:
        return {'message': 'User not found.'}, 404