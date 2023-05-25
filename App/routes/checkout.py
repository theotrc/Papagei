from flask import redirect, Blueprint
import stripe


checkout_blue= Blueprint("checkout", __name__, static_folder="../static", template_folder="../templates")




@checkout_blue.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="localhost" + '/success.html',
            cancel_url="localhost" + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)