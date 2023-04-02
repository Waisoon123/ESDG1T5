import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)
stripe.api_key = 'sk_test_51Mp7eaDR3XsfzYNcNN274W7Hmlsuvr7nDhtFN1UtuVH9dHVBRVVC9PRbhrL5BZ2SVEGfmoFEO8Z7CYr7BuxszJng00ScaMPkRp'

@app.route('/refund/<string:payment_intent_id>', methods=['POST'])
def create_refund(payment_intent_id):
    try:
        # session_id = request.json['session_id']
        
        # # Retrieve the session
        # session = stripe.checkout.Session.retrieve(session_id)
        
        # Get the payment intent ID from the session
        # payment_intent_id = session['payment_intent']
        
        # Create the refund
        refund = stripe.Refund.create(
            payment_intent = payment_intent_id,
            amount=13932, # hardcoded amount - cents
        )
        
        return jsonify(
            {
                "code": 200,
                "data": refund
            }
        )
    except stripe.error.StripeError as e:
        return jsonify(
            {
                "code": 400,
                "data": 'Invalid Request Error: {}'.format(e)
            }
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)