const button = document.querySelector('#buy_now_btn');

button.addEventListener('click', event => {
    fetch('http://127.0.0.1:5001/stripe_pay')
    .then((result) => { return result.json(); })
    .then((data) => {
        console.log(data)
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
            print('test')
            print(result.error.message)
        });
    })
});