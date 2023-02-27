from flask import Blueprint, request
from models.user import User
from models.api_key import ApiKey
from flask_jwt_extended import get_jwt_identity, jwt_required

key_bp = Blueprint('key', __name__)

@key_bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    api_key = ApiKey(user_id=user_id)
    api_key.save()
    return {
        'api_secret': api_key.secret,
        'user_id': user_id
    }

@key_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_api_secret():
    user_id = get_jwt_identity()
    api_secret = request.json.get('api_secret')
    api_key = ApiKey.get_by_secret(api_secret)
    if api_key is not None and api_key.user_id == user_id:
        api_key.delete()
        return {
            'message': 'API key deleted'
        }
    else:
        return {
            'message': 'API key not found or unauthorized'
        }

@key_bp.route('/list', methods=['GET'])
@jwt_required()
def list_api_secrets():
    user_id = get_jwt_identity()
    api_keys = ApiKey.get_by_user_id(user_id)
    api_key_data = [api_key.to_dict() for api_key in api_keys]
    return {
        'api_keys': api_key_data
    }


@key_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_api_secret():
    user_id = get_jwt_identity()
    old_secret = request.json.get('old_secret')
    new_secret = request.json.get('new_secret')
    api_key = ApiKey.get_by_secret(old_secret)
    if api_key is not None and api_key.user_id == user_id:
        api_key.secret = new_secret
        api_key.save()
        return {
            'message': 'API key updated'
        }
    else:
        return {
            'message': 'API key not found or unauthorized'
        }