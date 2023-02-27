from flask import Blueprint, request
# adds imports for datetime and bcrypt
from datetime import datetime
import bcrypt
# import user model
from models.user import User
# import uuid for generating user IDs
import uuid
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


auth_bp = Blueprint('auth', __name__)

# Register a new user
# Usage: POST /api/auth/register
# Request body:
# {
#   "email": "string",
#   "password": "string"
# }
@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  email = data.get('email').lower()
  password = data.get('password')

  # Check if user already exists with given email
  user = User.get_by_email(email)
  if user:
    # User already exists with this email
    if user.password:
        # User already has a password set, return error response
        return {'message': 'User with this email already exists and has a password set.'}, 409
    else:
       # User exists and user.id is set, but user.password is not set
       print('User exists but password is not set. Setting password.')

  # Hash the user's password
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

  # Create user object with data and timestamps
  user = User(email=email, password=hashed_password.decode('utf-8'))

  try:
      # Save user to Firestore
      user.save()

      # Log in user and return JWT token
      jwt_token = create_jwt_token(user.id)
      return {'message': 'User registered successfully.', 'token': jwt_token}, 200
  except Exception as e:
      # Log the error and return an error response
      print(f'Error creating user: {e}')
      return {'message': 'An error occurred while creating user.'}, 500

def create_jwt_token(user_id):
  # Create JWT token with user_id as payload
  jwt_token = create_access_token(identity=user_id)
  return jwt_token

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email').lower()
  password = data.get('password')

  # Get user by email
  user = User.get_by_email(email)
  if not user:
      return {'message': 'Invalid email or password'}, 401

  # Check password
  if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
      return {'message': 'Invalid email or password'}, 401

  # Return success response with JWT token
  jwt_token = create_jwt_token(user.id)
  return {'message': 'Login successful', 'token': jwt_token}, 200

@auth_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
  data = request.get_json()
  current_password = data.get('current_password')
  new_password = data.get('new_password')

  # Get user ID from JWT token
  user_id = get_jwt_identity()

  # Get user by ID
  user = User.get_by_id(user_id)
  if not user:
      return {'message': 'User not found'}, 404

  # Check current password
  if not bcrypt.checkpw(current_password.encode('utf-8'), user.password.encode('utf-8')):
      return {'message': 'Invalid current password'}, 400

  # Hash the new password
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

  # Update user password
  user.password = hashed_password.decode('utf-8')
  user.save()

  return {'message': 'Password changed successfully'}, 200