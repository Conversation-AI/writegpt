from functools import wraps
from flask import request, abort, url_for
from models.api_key import ApiKey
from models.user import User

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401, 'Authorization header is missing')

        auth_header = request.headers['Authorization']
        auth_parts = auth_header.split()

        if len(auth_parts) != 2 or auth_parts[0] != 'Bearer':
            abort(401, 'Invalid Authorization header')

        api_key_secret = auth_parts[1]
        api_key = ApiKey.get_by_secret(api_key_secret)

        if api_key is None:
            abort(401, 'Invalid API key')
        else:
            api_key.update_last_used_at() # Update last used at

            user = User.get_by_id(api_key.user_id)
            if user is None: 
                abort(401, 'User not found')
            elif user.billing_status not in ("active", "trialing"):
                buyURL = url_for('views.buy', _external=True)
                abort(401, f'No active subscription. Please visit {buyURL} to get API access.')

        return f(user, *args, **kwargs)

    return decorated_function
