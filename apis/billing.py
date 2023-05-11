import stripe
from flask import Blueprint

billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/record_usage', methods=['POST'])
def record_usage():
    # implementation
    print("record_usage")


@billing_bp.route('/subscribe', methods=['GET'])
def subscribe():
    # implementation
    stripe.api_key = "sk_test_51HjlZsJpcZA607UWB12AhDNgCOl2nUtElkwVolIyI6nMLKif66f0FEttB6EM3IdSHTSPkubGOF9wydt7qpW3AV1k00amr9TfYo"
    email = "gchandni886@gmail.com"

    # Create a customer
    customer = stripe.Customer.create(
        email=email
    )

    payment_method = stripe.PaymentMethod.create(
        type='card',
        card={
            'number': '4242424242424242',
            'exp_month': 12,
            'exp_year': 2024,
            'cvc': '123',
        },
    )
    stripe.PaymentMethod.attach(
        payment_method.id,
        customer=customer.id,
    )

    # Set the payment method as the default for the customer
    customer['invoice_settings']['default_payment_method'] = payment_method.id
    customer.save()

    # Create a subscription
    subscription = stripe.Subscription.create(
        customer=customer['id'],
        items=[{
            'price': 'price_1N6dbIJpcZA607UWXzxvVMGp'
        }],
    )

    print("Subscription ", subscription)

    # Retrieve usage records for the subscription
    # usage_records = stripe.UsageRecord.create(
    #     subscription_item=subscription['items']['data'][0]['id'],
    #     quantity=1
    # )

    usage_records = stripe.SubscriptionItem.create_usage_record(
        subscription['items']['data'][0]['id'],
        quantity=1
        # timestamp=1571252444,
    )

    print("Usage Record ")
    print(usage_records)

    return {"usage_record": usage_records, "subscription": subscription}
