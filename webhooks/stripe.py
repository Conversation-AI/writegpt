import json
import stripe
from flask import Blueprint, request
import os
# import user model
from models.user import User


stripe_bp = Blueprint('stripe', __name__)

# Initialize Stripe API with your API keys
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Handle Stripe webhook events
@stripe_bp.route('/', methods=['POST'])
def handle_stripe_webhook():
    payload = request.data
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    
    # Handle the event
    event_type = event['type']
    if event_type == 'customer.created':
        handle_customer_created(event)
    elif event_type == 'customer.updated':
        handle_customer_updated(event)
    elif event_type == 'customer.deleted':
        handle_customer_deleted(event)
    elif event_type == 'customer.subscription.created':
        handle_customer_subscription_created(event)
    elif event_type == 'customer.subscription.updated':
        handle_customer_subscription_updated(event)
    elif event_type == 'customer.subscription.deleted':
        handle_customer_subscription_deleted(event)
    return "OK", 200

# Handle customer.created webhook event
# Creates a new user record in our database (or updates an existing one with the customer ID)
def handle_customer_created(event):
    customer_id = event['data']['object']['id']
    customer_email = event['data']['object']['email']
    customer_name = event['data']['object']['name']

    # Search for the user by email address
    user = User.get_by_email(customer_email)

    if user:
        # Update the user's customer ID and name
        user.customer_id = customer_id
        user.name = user.name or customer_name # Only update name if it's not set
        user.save()
    else:
        # If the user is not found, create a new user record
        user = User(email=customer_email, name=customer_name, customer_id=customer_id)
        user.save()

# Handle customer.updated webhook event
def handle_customer_updated(event):
    customer_id = event['data']['object']['id']
    customer_email = event['data']['object']['email']
    customer_name = event['data']['object']['name']

    # Add your business logic to handle customer updated event here
    # For example, you may want to update a customer record in your database
    # with the new email and name data

    # Search for the user by customer ID
    user = User.get_by_customer_id(customer_id)

    if user:
        # Update the user's email and name
        user.email = customer_email
        user.name = customer_name
        user.save()

# Handle customer.deleted webhook event
def handle_customer_deleted(event):
    customer_id = event['data']['object']['id']

    # Add your business logic to handle customer deleted event here
    # For example, you may want to delete a customer record from your database

    # Search for the user by customer ID
    user = User.get_by_customer_id(customer_id)

    if user:
        # Delete the customer id from the user record
        user.customer_id = None
        user.save()

# Handle customer.subscription.created webhook event
def handle_customer_subscription_created(event):
    subscription_id = event['data']['object']['id']
    subscription_item_id = event['data']['object']['items']['data'][0]['id']
    subscription_status = event['data']['object']['status']

    customer_id = event['data']['object']['customer']

    # Add your business logic to handle subscription created event here
    # For example, you may want to create a new subscription record in your database
    # and save the subscription ID, customer ID, customer email, customer name, and subscription item ID

    # Search for the user by customer ID
    user = User.get_by_customer_id(customer_id)

    if user:
        # Update all the subscription data
        user.subscription_id = subscription_id
        user.subscription_item_id = subscription_item_id
        user.billing_status = subscription_status
        user.save()

# Handle customer.subscription.updated webhook event
def handle_customer_subscription_updated(event):
    subscription_id = event['data']['object']['id']
    subscription_item_id = event['data']['object']['items']['data'][0]['id']
    subscription_status = event['data']['object']['status']

    customer_id = event['data']['object']['customer']

    # Add your business logic to handle subscription updated event here
    # For example, you may want to adjust the usage records or billing for the customer
    # or update the subscription status in your database

    # Search for the user by customer ID
    user = User.get_by_customer_id(customer_id)

    if user:
        # Update the subscription related info
        user.subscription_id = subscription_id
        user.subscription_item_id = subscription_item_id
        user.billing_status = subscription_status
        user.save()

# Handle customer.subscription.deleted webhook event
def handle_customer_subscription_deleted(event):
    customer_id = event['data']['object']['customer']
    subscription_status = event['data']['object']['status']

    # Add your business logic to handle subscription deleted event here
    # For example, you may want to adjust the usage records or billing for the customer
    # or update the subscription status in your database

    # Search for the user by customer ID
    user = User.get_by_customer_id(customer_id)

    if user:
        # Update the subscription related info
        user.subscription_id = None
        user.subscription_item_id = None
        user.billing_status = subscription_status
        user.save()
