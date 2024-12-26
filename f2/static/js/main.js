/*  ---------------------------------------------------
Template Name: Ashion
Description: Ashion ecommerce template
Author: Colorib
Author URI: https://colorlib.com/
Version: 1.0
Created: Colorib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Product filter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.property__gallery').length > 0) {
            var containerEl = document.querySelector('.property__gallery');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay, .offcanvas__close").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".header__menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Accordin Active
    --------------------*/
    $('.collapse').on('shown.bs.collapse', function () {
        $(this).prev().addClass('active');
    });

    $('.collapse').on('hidden.bs.collapse', function () {
        $(this).prev().removeClass('active');
    });

    /*--------------------------
        Banner Slider
    ----------------------------*/
    $(".banner__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*--------------------------
        Product Details Slider
    ----------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop: false,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<i class='arrow_carrot-left'></i>","<i class='arrow_carrot-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
        mouseDrag: false,
        startPosition: 'URLHash'
    }).on('changed.owl.carousel', function(event) {
        var indexNum = event.item.index + 1;
        product_thumbs(indexNum);
    });

    function product_thumbs (num) {
        var thumbs = document.querySelectorAll('.product__thumb a');
        thumbs.forEach(function (e) {
            e.classList.remove("active");
            if(e.hash.split("-")[1] == num) {
                e.classList.add("active");
            }
        })
    }


    /*------------------
		Magnific
    --------------------*/
    $('.image-popup').magnificPopup({
        type: 'image'
    });


    $(".nice-scroll").niceScroll({
        cursorborder:"",
        cursorcolor:"#dddddd",
        boxzoom:false,
        cursorwidth: 5,
        background: 'rgba(0, 0, 0, 0.2)',
        cursorborderradius:50,
        horizrailenabled: false
    });

    /*------------------
        CountDown
    --------------------*/
    // For demo preview start
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    if(mm == 12) {
        mm = '01';
        yyyy = yyyy + 1;
    } else {
        mm = parseInt(mm) + 1;
        mm = String(mm).padStart(2, '0');
    }
    var timerdate = mm + '/' + dd + '/' + yyyy;
    // For demo preview end


    // Uncomment below and use your date //

    /* var timerdate = "2020/12/30" */

	$("#countdown-time").countdown(timerdate, function(event) {
        $(this).html(event.strftime("<div class='countdown__item'><span>%D</span> <p>Day</p> </div>" + "<div class='countdown__item'><span>%H</span> <p>Hour</p> </div>" + "<div class='countdown__item'><span>%M</span> <p>Min</p> </div>" + "<div class='countdown__item'><span>%S</span> <p>Sec</p> </div>"));
    });

    /*-------------------
		Range Slider
	--------------------- */
	var rangeSlider = $(".price-range"),
    minamount = $("#minamount"),
    maxamount = $("#maxamount"),
    minPrice = rangeSlider.data('min'),
    maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
    range: true,
    min: minPrice,
    max: maxPrice,
    values: [minPrice, maxPrice],
    slide: function (event, ui) {
        minamount.val(ui.values[0]);
        maxamount.val(ui.values[1]);
        }
    });
    minamount.val(rangeSlider.slider("values", 0));
    maxamount.val(rangeSlider.slider("values", 1));

    /*------------------
		Single Product
	--------------------*/
	$('.product__thumb .pt').on('click', function(){
		var imgurl = $(this).data('imgbigurl');
		var bigImg = $('.product__big__img').attr('src');
		if(imgurl != bigImg) {
			$('.product__big__img').attr({src: imgurl});
		}
    });
    
    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
	proQty.on('click', '.qtybtn', function () {
		var $button = $(this);
		var oldValue = $button.parent().find('input').val();
		if ($button.hasClass('inc')) {
			var newVal = parseFloat(oldValue) + 1;
		} else {
			// Don't allow decrementing below zero
			if (oldValue > 0) {
				var newVal = parseFloat(oldValue) - 1;
			} else {
				newVal = 0;
			}
		}
		$button.parent().find('input').val(newVal);
    });
    
    /*-------------------
		Radio Btn
	--------------------- */
    $(".size__btn label").on('click', function () {
        $(".size__btn label").removeClass('active');
        $(this).addClass('active');
    });

    $('.add-to-wishlist').click(function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        var csrf_token = $(this).data('csrf');
        $.ajax({
            method: 'POST',
            url: '/cart/add-to-wishlist/',
            data: {
                'item_id': item_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function(response) {
                swal("Success!", response.status, "success");
                updateWishlistCount();
            },
            error: function() {
                window.location.href = '/account/login/';
                return;
            }
        }); 
    });

    $(document).on('click', '.remove-to-wishlist', function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        var csrf_token = $(this).data('csrf');
    
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to remove this product from your wishlist?",
            icon: "warning",
            buttons: ["Cancel", "Remove"],
            dangerMode: true,
        }).then(function (confirmed) {
            if (confirmed) {
                $.ajax({
                    method: 'POST',
                    url: '/cart/remove-to-wishlist/',
                    data: {
                        'item_id': item_id,
                        'csrfmiddlewaretoken': csrf_token
                    },
                    success: function(response) {
                        $('.wishlistdata').load(location.href + " .wishlistdata");
                        updateWishlistCount();
                    }
                });
            }
        });
    });
    

    function updateWishlistCount() {
        var initialCount = parseInt($('.wishdata').text());
        console.log(initialCount)
      
        $.ajax({
          url: '/cart/wishlist/count/',
          type: 'GET',
          success: function(data) {
            var updatedCount = data.wishCount;
            if (updatedCount !== initialCount) {
              $('.wishdata').text(updatedCount);
            }
          },
        });
    }



    $('.add-to-cart').click(function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        var size = "";
        var radioButtons = document.querySelectorAll('input[type="radio"]');
        for (var i = 0; i < radioButtons.length; i++) {
            if (radioButtons[i].checked) {
                size = radioButtons[i].value;
                break;
            }
        }
        console.log(size)
        var quantity = document.getElementById('quantity-input').value;
        var csrf_token = $(this).data('csrf');
        $.ajax({
            method: 'POST',
            url: '/cart/add-to-cart/',
            data: {
                'item_id': item_id,
                'size':size,
                'quantity':quantity,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function(data) {
                swal("Success!", data.status, "success");
                updateCartCount();
            },
            error: function(data) {
                alert(data.status);
            }
        }); 
    });
    
    function updateActive(elem) {
        // remove active class from all labels
        const labels = document.querySelectorAll('.size__btn label');
        labels.forEach(label => label.classList.remove('active'));
        
        // add active class to clicked label
        const clickedLabel = elem.parentNode;
        clickedLabel.classList.add('active');
      }

      $(document).on('click', '.remove-to-cart', function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        var cart_id = $(this).data('cart');
        var csrf_token = $(this).data('csrf');
    
        swal({
            title: "Are you sure?",
            text: "Are you sure you want to remove this product from your cart?",
            icon: "warning",
            buttons: ["Cancel", "Remove"],
            dangerMode: true,
        }).then(function (confirmed) {
            if (confirmed) {
                $.ajax({
                    method: 'POST',
                    url: '/cart/remove-to-cart/',
                    data: {
                        'item_id': item_id,
                        'cart_id': cart_id,
                        'csrfmiddlewaretoken': csrf_token
                    },
                    success: function(response) {
                        $('.cartlistdata').load(location.href + " .cartlistdata");
                        updateCartCount();
                    }
                });
            }
        });
    });
    
    $(document).on('click', '.decquantity', function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        console.log(item_id)
        var cart_id = $(this).data('cart');
        console.log(cart_id)
        var csrf_token = $(this).data('csrf');
        $.ajax({
            method: 'POST',
            url: '/cart/decrease_quantity/',
            data: {
                'item_id': item_id,
                'cart_id':cart_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function(response) {
                swal("Success!", response.status, "success");
                $('.cartlistdata').load(location.href + " .cartlistdata");
                updateCartCount();
            }
        }); 
    });

    $(document).on('click', '.incquantity', function(e) {
        e.preventDefault();
    
        var item_id = $(this).data('id');
        console.log(item_id)
        var cart_id = $(this).data('cart');
        console.log(cart_id)
        var csrf_token = $(this).data('csrf');
        $.ajax({
            method: 'POST',
            url: '/cart/increase_quantity/',
            data: {
                'item_id': item_id,
                'cart_id':cart_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function(response) {
                swal("Success!", response.status, "success");
                $('.cartlistdata').load(location.href + " .cartlistdata");
                updateCartCount();
            }
        }); 
    });


    function updateCartCount() {
        var initialCount = parseInt($('.cartdata').text());
        console.log(initialCount)
      
        $.ajax({
          url: '/cart/cart/count/',
          type: 'GET',
          success: function(data) {
            var updatedCount = data.cartCount;
            if (updatedCount !== initialCount) {
              $('.cartdata').text(updatedCount);
            }
          },
        });
    }

})(jQuery);

setTimeout(() => {
    $('#message').fadeOut('slow')
}, 4000);
