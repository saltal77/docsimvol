//LOADER
$(window).on("load", function () {
   "use strict";
	 $(".loading-page").fadeOut(800);
});

jQuery(function ($) {
   "use strict";
   var $root = $("html, body");

   /*---------- Loader ----------*/
   var counter = 0;
   var $load_text = $(".loading-page .counter h2");
   var c = 0;
   var i = setInterval(function () {
      $load_text.html(c + "%");
      $load_text.css("width", c + "%");
      counter++;
      c++;
      if (counter == 101) {
         clearInterval(i);
      }
   }, 50);


   /*---------- Back To Top ----------*/
   $("a[href='#top']").on("click", function () {
      $root.animate({
         scrollTop: 100
      }, "slow");
      return false;
   });


   /* ---------- Skills ----------*/
   $(".skills li").each(function () {
      $(this).appear(function () {
         $(this).animate({
            opacity: 1,
            left: "0px"
         }, 800);
         var b = jQuery(this).find(".progress-bar").attr("data-width");
         $(this).find(".progress-bar").animate({
            width: b + "%"
         }, 1300, "linear");
      });
   });



   /*---------- Search On Click ----------*/
   $(".search_btn").on("click", function (event) {
      event.preventDefault();
      $("#search").addClass("open");
      $("#search > form > input[type='search']").focus();
   });

   $("#search, #search button.close").on("click keyup", function (event) {
      if (event.target == this || event.target.className == "close" || event.keyCode == 27) {
         $(this).removeClass("open");
      }
   });



   /* ---------- Tabs ----------*/
   $(".items > li > a").on("click", function (e) {
      e.preventDefault();
      var $this = $(this);
      if ($this.hasClass("expanded")) {
         $this.removeClass("expanded");
      } else {
         $(".items a.expanded").removeClass("expanded");
         $this.addClass("expanded");
         $(".sub-items").filter(":visible").slideUp("normal");
      }
      $this.parent().children("ul").stop(true, true).slideToggle("normal");
   });



   /*---------- Cubeportfolio ----------*/
   $("#projects").cubeportfolio({
      filters: "#project-filter",
      layoutMode: "grid",
      defaultFilter: "*",
      animationType: "slideDelay",
      gapHorizontal: 30,
      gapVertical: 30,
      gridAdjustment: "responsive",
      lightboxDelegate: ".cbp-lightbox",
      lightboxGallery: true,
   });



   /*---------- Revolution ----------*/
   /*Main Slider*/
   var revapi = $("#rev_slider_3 , #rev_slider_2 , #rev_slider_4").revolution({
      sliderType: "standard",
      sliderLayout: "fullwidth",
      scrollbarDrag: "true",
      spinner: "off",
      delay: 3000,
      navigation: {
         arrows: {
            enable: true
         }
      },
      touch: {
         touchenabled: "on",
         swipe_threshold: 75,
         swipe_min_touches: 1,
         swipe_direction: "horizontal",
         drag_block_vertical: false
      },
      responsiveLevels: [1240, 1024, 778, 480],
      gridwidth: [1170, 992, 767, 480],
      gridheight: [750, 650, 550, 400],
   });



   /*---------- Owl Carousel ----------*/
   $("#services_slider , #team_slider , #news_slider").owlCarousel({
      autoPlay: 3000, //Set AutoPlay to 3 seconds
      items: 3,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
      itemsDesktopSmall: [1024, 2],
      itemsTablet: [768, 2],
      itemsMobile: [479, 1]
   });

   $("#team2_slider").owlCarousel({
      autoPlay: 3000,
      items: 4,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
      itemsDesktopSmall: [1024, 2],
      itemsTablet: [768, 2],
      itemsMobile: [479, 1]
   });

   var owl = $("#logistic_team_slider");
   owl.owlCarousel({
      autoPlay: 5000,
      pagination: true,
      navigation: false,
      singleItem: true,
      transitionStyle: "goDown"
   });

   // Testinomial home slider
   var owl = $("#testinomial_slider");
   owl.owlCarousel({
      autoPlay: 3000,
      pagination: true,
      navigation: false,
      singleItem: true,
      transitionStyle: "fade"
   });
   // Testinomial home slider
   var owl = $("#upcoming_slider");
   owl.owlCarousel({
      autoPlay: 3000,
      pagination: false,
      navigation: true,
      singleItem: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
   });

   var owl = $("#testinomial2_slider");
   owl.owlCarousel({
      autoPlay: 3000,
      pagination: true,
      navigation: false,
      singleItem: true,
      transitionStyle: "fade"
   });

   $("#bloghome_slider").owlCarousel({
      autoPlay: 3000,
      singleItem: true,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
   });

   var owl = $("#latest_blog_slider");
   owl.owlCarousel({
      autoPlay: 3000,
      transitionStyle: "goDown",
      singleItem: true,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-chevron-up'></i>",
      "<i class='fa fa-chevron-down'></i>"
    ],
   });

   $("#partners_slider").owlCarousel({
      autoPlay: 3000,
      items: 5,
      pagination: true,
      navigation: false,
      itemsDesktopSmall: [1024, 5],
      itemsTablet: [768, 3],
      itemsMobile: [479, 1]
   });

   $("#web_slider").owlCarousel({
      autoPlay: 3000,
      items: 2,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
   });

   $("#commerce_slider").owlCarousel({
      autoPlay: 3000, //Set AutoPlay to 3 seconds
      items: 3,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
   });

   $("#best_selling_slider , #feature_slider").owlCarousel({
      autoPlay: 3000,
      items: 4,
      pagination: false,
      navigation: true,
      navigationText: [
      "<i class='fa fa-angle-left'></i>",
      "<i class='fa fa-angle-right'></i>"
    ],
   });

   // Footer news slider
   var sync1 = $("#sync1");
   var sync2 = $("#sync2");

   sync1.owlCarousel({
      singleItem: true,
      autoPlay: 3000,
      slideSpeed: 1000,
      navigation: false,
      pagination: false,
      afterAction: syncPosition,
      responsiveRefreshRate: 200,
   });

   sync2.owlCarousel({
      items: 4,
      itemsDesktop: [1199, 10],
      itemsDesktopSmall: [979, 10],
      itemsTablet: [768, 8],
      itemsMobile: [479, 4],
      pagination: false,
      responsiveRefreshRate: 100,
      afterInit: function (el) {
         el.find(".owl-item").eq(0).addClass("synced");
      }
   });

   function syncPosition(el) {
      var current = this.currentItem;
      $("#sync2")
         .find(".owl-item")
         .removeClass("synced")
         .eq(current)
         .addClass("synced")
      if ($("#sync2").data("owlCarousel") !== undefined) {
         center(current)
      }
   }

   $("#sync2").on("click", ".owl-item", function (e) {
      e.preventDefault();
      var number = $(this).data("owlItem");
      sync1.trigger("owl.goTo", number);
   });

   function center(number) {
      var sync2visible = sync2.data("owlCarousel").owl.visibleItems;
      var num = number;
      var found = false;
      for (var i in sync2visible) {
         if (num === sync2visible[i]) {
            var found = true;
         }
      }

      if (found === false) {
         if (num > sync2visible[sync2visible.length - 1]) {
            sync2.trigger("owl.goTo", num - sync2visible.length + 2)
         } else {
            if (num - 1 === -1) {
               num = 0;
            }
            sync2.trigger("owl.goTo", num);
         }
      } else if (num === sync2visible[sync2visible.length - 1]) {
         sync2.trigger("owl.goTo", sync2visible[1])
      } else if (num === sync2visible[0]) {
         sync2.trigger("owl.goTo", num - 1)
      }

   }


   /* ---------- Fact Counters ----------*/
   $(".number-counters").appear(function () {
      $(".number-counters [data-to]").each(function () {
         var e = $(this).attr("data-to");
         $(this).delay(6e3).countTo({
            from: 1,
            to: e,
            speed: 3000,
            refreshInterval: 50
         })
      })
   });



   /*----------Zoomer ----------*/
   $("#product-zoom").elevateZoom({
      zoomType: "inner",
      cursor: "crosshair",
      zoomWindowFadeIn: 500,
      zoomWindowFadeOut: 750
   });

   var gallery = $("#gal1");
   gallery.find("a").hover(function () {
      var smallImage = $(this).attr("data-image");
      var largeImage = $(this).attr("data-zoom-image");
      var ez = $("#product-zoom").data("elevateZoom");
      ez.swaptheimage(smallImage, largeImage);
   });



   /*---------- Selected ----------*/
   var office_menu = $(".office_menu");
   office_menu.find("ul").hide();
   office_menu.on("click", ".selected", function () {
      // jQuery(this).parent('.office_menu').find('ul').slideToggle();
      var checkClass = $(this).hasClass("active");
      if (!checkClass) {
         $(this).addClass("active");
         $(this).parent(office_menu).find("ul").slideDown();
      } else {
         $(this).removeClass("active");
         $(this).parent(office_menu).find("ul").slideUp();
      }
   });
   office_menu.on("click", "ul a", function (e) {
      e.preventDefault();
      $(".addressbox").fadeOut();
      var clickDataVal = $(this).data("office");

      var txt = $(this).html();
      $(this).parents(office_menu).find(".selected").html(txt);
      $(this).parents(office_menu).find(".selected").removeClass("active");
      $(this).parents("ul").slideUp();

      $(".addressbox").each(function () {
         var elemDataVal = $(this).data("office");
         if (clickDataVal == elemDataVal) {
            $(this).delay(300).fadeIn();
         }
      });
   });


   /*---------- Typewriter ----------*/
   $("#typewriter").typewriter({
      prefix: "A ",
      text: ["frontend developer and web designer", "Bootstrap and make responsive websites", "HTML5 and CSS3 Validate W3C"],
      typeDelay: 90,
      waitingTime: 1500,
      blinkSpeed: 200
   });



   /*---------- Map ----------*/
   var map;
   if ($("#map").length > 0) {
      map = new GMaps({
         el: "#map",
         lat: 37.186493,
         lng: 37.315107,
         scrollwheel: false
      });

      map.addMarker({
         lat: 37.186493,
         lng: 37.315107,
         title: "Marker with InfoWindow",
         infoWindow: {
            content: '<p>Advisor Melbourne, Merrick Way, <br>FL 12345 Australia<a href="#"  target="_blank">Themeforest</a></p>'
         }
      });

   }

});