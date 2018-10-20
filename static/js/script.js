/* ====================================
               Preloader
======================================= */
$(window).on('load', function () { // make sure that whole site is loaded
  $('#status').fadeOut();
  $('#preloader').delay(450).fadeOut('slow');
});



/* ====================================
               Navigation
======================================= */
//* Show and Hide grey Nav *//

$(function () {
  // show/hide nav on page load
  showHideNav();

  $(window).scroll(function () {
    // show/hide nav on window's scroll
    showHideNav();
  });

  function showHideNav() {
    if ($(window).scrollTop() > 50) {
      // show grey nav
      $("nav").addClass("grey-nav-top");
      // show white logo
      $(".navbar-brand img").attr("src", "/static/img/logo/logo-original-name2.png");
      // show back to top
      $(".btn-back-to-top").fadeIn();
    } else {
      // hide grey nav
      $("nav").removeClass("grey-nav-top");
      // show logo
      $(".navbar-brand img").attr("src", "/static/img/logo/logo-original-name.png");
      // hide back to top
      $(".btn-back-to-top").fadeOut();
    }
  }

});

/* ====================================
              Search Box
======================================= */
$('#dropdown-items li').on('click', function () {
  $('#dropdown_title').html($(this).find('a').html());
});


/* ====================================
              Animation
======================================= */
// animation when scroll
// $(function () {
//      new WOW().init(); 
// });

// // home animation on page load
// $(window).on('load', function() {

//     $("#home-heading-1").addClass("animated fadeInDown");
//     $("#home-heading-2").addClass("animated fadeInLeft");
//     $("#home-separator").addClass("animated zoomIn");
//     $("#home-heading-3").addClass("animated zoomIn");
//     $("#home-reservation").addClass("animated fadeInUp");
//     $("#arrow-down i").addClass("animated fadeInDown infinite");

// });

/* ====================================
                Home
======================================= */
$(document).ready(function () {
  // HomePage Carousel 
  $('#myCarousel-client').carousel({
    interval: false
  })
  $('#myCarousel-team').carousel({
    interval: false
  })
  $('#myTestimonial').carousel({
    interval: 3000
  })

  // Add Smooth Scrolling
  $("a.smooth-scroll").click(function (event) {

    event.preventDefault();

    var target = $(this).attr("href"); //Get the target
    var scrollToPosition = $(target).offset().top

    $('html').animate({
      'scrollTop': scrollToPosition
    }, 1250, function () {
      window.location.hash = "" + target;
      // Jump to the top of the div with same id
      // Force page to back to the end of the animation
      $('html').animate({
        'scrollTop': scrollToPosition
      }, 0);
    });

    $('body').append("called");

  });

});