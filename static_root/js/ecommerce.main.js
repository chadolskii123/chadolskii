$(document).ready(function () {
    let stripeFormModule = $(".stripe-payment-form")
    let stripeModuleToken = stripeFormModule.attr("data-token")
    let stripeModuleNextUrl = stripeFormModule.attr("data-next-url")

    let stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card"


    let stripeTemplate = $.templates("#stripeTemplate")
    let stripeTemplateDataContext = {
        name: "Stripe",
        publishKey: stripeModuleToken,
        nextUrl: stripeModuleNextUrl,
        btnTitle: stripeModuleBtnTitle,
    }
    let stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml);


// https secure site when live
    let
        paymentForm = $(".payment-form");
    if (paymentForm.length > 1) {
        alert("Only One payment form is allowed per page");
        paymentForm.css('display', 'none');
    } else if (paymentForm.length === 1) {
        let pubKey = paymentForm.attr('data-token')
        let nextUrl = paymentForm.attr('data-next-url');

        const stripe = Stripe(pubKey);
        const elements = stripe.elements();
        // Custom styling can be passed to options when creating an Element.
        const style = {
            base: {
                // Add your base input styles here. For example:
                fontSize: '16px',
                color: '#32325d',
            },
        };

        // Create an instance of the card Element.
        const card = elements.create('card', {style});

        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');


        const form2 = $('#payment-form');
        let btnLoad = form2.find(".btn-load")
        let btnLoadDefaultHtml = btnLoad.html();
        let btnLoadDefaultClasses = btnLoad.attr("class");
        // Create a token or display an error when the form is submitted.
        const form = document.getElementById('payment-form');
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            btnLoad.blur()
            let loadTime = 1500
            let currentTimeout
            let errorHtml = "<i class='fa fa-warning'></i> An Error Occured"
            let errorClasses = "btn btn-danger disabled"
            let loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
            let loadingClasses = "btn btn-success disabled"

            const {token, error} = await stripe.createToken(card);
            if (error) {
                // Inform the customer that there was an error.
                const errorElement = document.getElementById('card-errors');
                errorElement.textContent = error.message;
                currentTimeout = displayBtnStatus(btnLoad, errorHtml, errorClasses, 1000, currentTimeout)
            } else {
                // Send the token to your server.
                currentTimeout = displayBtnStatus(btnLoad, loadingHtml, loadingClasses, 2000, currentTimeout)
                stripeTokenHandler(nextUrl, token);
            }
        });

        function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout) {
            // if (timeout) {
            //     clearTimeout(timeout)
            // }
            if (!loadTime) {
                loadTime = 1500
            }
            btnLoad.html(newHtml)
            btnLoad.removeClass(btnLoadDefaultClasses)
            btnLoad.addClass(newClasses)
            return setTimeout(function () {
                btnLoad.html(btnLoadDefaultHtml)
                btnLoad.removeClass(newClasses)
                btnLoad.addClass(btnLoadDefaultClasses)
            }, 1000)
        }


        function redirectToNext(nextPath, timeoffset) {
            if (nextPath) {
                setTimeout(function () {
                    window.location.href = nextPath;
                }, timeoffset)
            }
        }

        const stripeTokenHandler = (nextUrl, token) => {
            // Insert the token ID into the form so it gets submitted to the server
            /*const form = document.getElementById('payment-form');
            const hiddenInput = document.createElement('input');
            hiddenInput.setAttribute('type', 'hidden');
            hiddenInput.setAttribute('name', 'stripeToken');
            hiddenInput.setAttribute('value', token.id);
            form.appendChild(hiddenInput);
            */

            let paymentMethodEndpoint = '/billing/payment_method/create/'
            let data = {
                'token': token.id,
            }
            $.ajax({
                data: data,
                url: paymentMethodEndpoint,
                method: "POST",
                success: function (data) {
                    let successMsg = data.message || "Success! Your card was added!"
                    card.clear();
                    // if (nextUrl) {
                    //     successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting... ";
                    // }
                    // if ($.alert) {
                    //     $.alert(successMsg)
                    // } else {
                    //     alert(successMsg)
                    // }
                    // btnLoad.html(btnLoadDefaultHtml);
                    // btnLoad.attr('class', btnLoadDefaultClasses)
                    redirectToNext(nextUrl, 0)
                },
                error: function (error) {
                    console.log(error);
                    btnLoad.html(btnLoadDefaultHtml);
                    btnLoad.attr('class', btnLoadDefaultClasses)
                }
            })

        }
    }
});