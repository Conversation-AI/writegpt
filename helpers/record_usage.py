import os
import stripe
import time

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


# Helper function that updates usage record given a user
def update_usage_record_by_user(user):
    subscription_item_id = user.subscription_item_id
    # increment usage by 1
    usage_record = stripe.SubscriptionItem.create_usage_record(
        subscription_item_id,
        quantity=1,
        timestamp=int(time.time()),
    )

    print("usage record added/updated : ", usage_record)
