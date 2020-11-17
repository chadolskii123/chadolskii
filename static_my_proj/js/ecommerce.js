$(document).ready(function () {
    // Contact form Handler
    let contactForm = $(".contact-form");
    let contactFormMethod = contactForm.attr("method")
    let contactFormEndpoint = contactForm.attr("action")

    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Sending...");
        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(defaultText);
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault()

        let contactFormSubmitBtn = contactForm.find("[type='submit']");
        let contactFormSubmitBtnTxt = contactFormSubmitBtn.text();

        let contactFormData = contactForm.serialize()
        let thisForm = $(this)

        displaySubmitting(contactFormSubmitBtn, "", true);

        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                thisForm[0].reset()
                $.alert({
                    title: "success!",
                    content: data.message,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 1000);
            },
            error: function (errorData) {
                console.log(errorData.responseJSON);
                let jsonData = errorData.responseJSON;
                let msg = ""
                $.each(jsonData, function (key, value) {
                    msg += key + " : " + value[0].message + "<br>"
                });
                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false);
                }, 1000);
            }
        });
    });


    // Auto Search
    let searchForm = $(".search_form");
    let searchInput = searchForm.find("[name='q'") // input name ='q'
    let typingTimer;
    let typingInterval = 500; //.5 seconds

    let searchBtn = searchForm.find("[type='submit']");

    // key released
    searchInput.keyup(function (event) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval);
    });
    // key pressed
    searchInput.keydown(function (event) {
        clearTimeout(typingTimer);
    });

    function displaySearching() {
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")
    }

    function performSearch() {
        displaySearching();
        let query = searchInput.val();
        setTimeout(function () {
            window.location.href = '/search/?q=' + query;
        }, 1000)

    }

    // Cart + Add Products
    let productForm = $(".form-product-ajax")

    productForm.submit(function (event) {
        event.preventDefault();
        console.log("form is not sending");
        let thisForm = $(this);
        //let actionEndpoint = thisForm.attr('action');
        let actionEndpoint = thisForm.attr('data-endpoint')
        let httpMethod = thisForm.attr('method');
        let formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                console.log("success");
                console.log(data);
                let submitSpan = thisForm.find(".submit-span");
                if (data.added) {
                    submitSpan.html('<button type="submit" class="btn btn-primary"> Remove?</button>')
                } else {
                    submitSpan.html(' <button type="submit" class="btn btn-success">Add to Cart</button>')
                }
                let navbarCount = $(".navbar-cart-count")

                if (data['cartItemCount'] < 1) {
                    navbarCount.css("display", "none");
                } else {
                    navbarCount.css("display", "contents");
                    navbarCount.text(data.cartItemCount);
                }

                let currentPath = window.location.href;
                console.log(currentPath);
                if (currentPath.indexOf("cart") !== -1) {
                    refreshCart();
                }


            },
            error: function (errorData) {
                $.alert({
                    title: "Oops!",
                    content: "An Error occurred",
                    theme: "modern",
                });
            }
        })
    });

    function refreshCart() {
        let cartTable = $(".cart-table")
        let cartBody = cartTable.find(".cart-body")

        let productRows = cartBody.find(".cart-product")

        let refreshCartUrl = '/api/cart';
        let refreshCartMethod = "GET";
        let data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                let hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                productRows.html("")

                i = data.products.length;
                if (i < 1) {
                    window.location.href = "/cart/"
                }
                $.each(data.products, function (index, value) {
                    console.log(value)
                    let newCartItemRemove = hiddenCartItemRemoveForm.clone();
                    newCartItemRemove.css("display", "block");
                    newCartItemRemove.find(".cart-item-product-id").val(value.id)
                    cartBody.prepend('<tr><th scope=\"row\">' + i + '</th><td><a href ="' + value.url + '">' + value.name + "</a>" + newCartItemRemove.html() + '</td><td>' + value.price + '</td></tr>');
                    i--;
                });

                cartBody.find(".cart-subtotal").text(data.subtotal)
                cartBody.find(".cart-total").text(data.total)
            },
            error: function (errorData) {
                $.alert({
                    title: "Oops!",
                    content: "An Error occurred",
                    theme: "modern",
                });
            }

        })
    }

window.onscroll = function () {
    myFunction()
};

let navbar = document.getElementById("navbar");
let sticky = navbar.offsetTop;
if (curPosition > sticky ){
        navbar.classList.add("sticky")
    } else{
        navbar.classList.remove("sticky");
    }

function myFunction() {
    let curPosition = window.pageYOffset;
    if (curPosition > sticky ){
        navbar.classList.add("sticky")
    } else{
        navbar.classList.remove("sticky");
    }
}

});
