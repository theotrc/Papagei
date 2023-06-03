var stripe = Stripe(checkout_public_key);

const button = document.querySelector("#buy_now_btn");

button.addEventListener("click", (event)=>{
    event.preventDefault()

})

stripe.redirectToCheckout({
    sessionId: checkout_session_id
}).then(function(result){
    console.log("payement effectué")
    console.log(result)
});