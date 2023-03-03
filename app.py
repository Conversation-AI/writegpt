from flask import Flask, render_template, redirect, url_for
import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta

from models.api_key import ApiKey

# set up the Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=360) # 1 year
jwt = JWTManager(app)

# register the blueprints
from apis.auth import auth_bp
from apis.user import user_bp
from apis.billing import billing_bp
from apis.key import key_bp
from webhooks.stripe import stripe_bp
from apis.service import service_bp
from views.views import views_bp
from apis.demo_service import demo_service_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(billing_bp, url_prefix='/api/billing')
app.register_blueprint(stripe_bp, url_prefix='/webhooks/stripe')
app.register_blueprint(key_bp, url_prefix='/api/key')
app.register_blueprint(service_bp, url_prefix='/api/v1')
app.register_blueprint(views_bp)
app.register_blueprint(demo_service_bp, url_prefix='/api/demo')


@app.route('/generate_email', methods=['POST'])
@app.route('/summarize_website', methods=['POST'])
def get_access():
    checkout_url = url_for('views.buy', _external=True)
    return f"Please visit {checkout_url} to get API access.", 410


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # start the app
    app.run(host='0.0.0.0', port=port, debug=True)