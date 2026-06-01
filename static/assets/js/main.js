/* ===================================================================
    
    Author          : Valid Theme
    Template Name   : vynzora - Immigration and Visa Consulting Template
    Version         : 1.0
    
* ================================================================= */
(function($) {
	"use strict";

	$(document).ready(function() {


		/* ==================================================
		    # Tooltip Init
		===============================================*/
		$('[data-toggle="tooltip"]').tooltip();

		/* ==================================================
		    # Wow active
		===============================================*/
		if ($(".wow").length) {
			var wow = new WOW({
				boxClass: "wow", // animated element css class (default is wow)
				animateClass: "animated", // animation css class (default is animated)
				mobile: true, // trigger animations on mobile devices (default is true)
				live: true // act on asynchronously loaded content (default is true)
			});
			wow.init();
		}


		/* ==================================================
		    # Youtube Video Init
		 ===============================================*/
				if (typeof $.fn.mb_YTPlayer !== 'undefined') {
		$(".player").mb_YTPlayer({
			videoURL: 'your-video-url',
			containment: 'self',
			autoPlay: true,
			mute: true
		});
	} else {
		console.warn('YTPlayer not available');
	}


		/* ==================================================
		Nice Select Init
		===============================================*/
		$('select#select_active').niceSelect();


		/* ==================================================
		    # imagesLoaded active
		===============================================*/
		$('#gallery-masonary,.blog-masonry').imagesLoaded(function() {

			/* Filter menu */
			$('.mix-item-menu').on('click', 'button', function() {
				var filterValue = $(this).attr('data-filter');
				$grid.isotope({
					filter: filterValue
				});
			});

			/* filter menu active class  */
			$('.mix-item-menu button').on('click', function(event) {
				$(this).siblings('.active').removeClass('active');
				$(this).addClass('active');
				event.preventDefault();
			});

			/* Filter active */
			var $grid = $('#gallery-masonary').isotope({
				itemSelector: '.gallery-item',
				percentPosition: true,
				masonry: {
					columnWidth: '.gallery-item',
				}
			});

			/* Filter active */
			$('.blog-masonry').isotope({
				itemSelector: '.blog-item',
				percentPosition: true,
				masonry: {
					columnWidth: '.blog-item',
				}
			});

		});


		/* ==================================================
		    # Fun Factor Init
		===============================================*/
		$('.timer').countTo();
		$('.fun-fact').appear(function() {
			$('.timer').countTo();
		}, {
			accY: -100
		});


		/* ==================================================
		    # Magnific popup init
		 ===============================================*/
		$(".popup-link").magnificPopup({
			type: 'image',
			// other options
		});

		$(".popup-gallery").magnificPopup({
			type: 'image',
			gallery: {
				enabled: true
			},
			// other options
		});

		$(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
			type: "iframe",
			mainClass: "mfp-fade",
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false
		});

		$('.magnific-mix-gallery').each(function() {
			var $container = $(this);
			var $imageLinks = $container.find('.item');

			var items = [];
			$imageLinks.each(function() {
				var $item = $(this);
				var type = 'image';
				if ($item.hasClass('magnific-iframe')) {
					type = 'iframe';
				}
				var magItem = {
					src: $item.attr('href'),
					type: type
				};
				magItem.title = $item.data('title');
				items.push(magItem);
			});

			$imageLinks.magnificPopup({
				mainClass: 'mfp-fade',
				items: items,
				gallery: {
					enabled: true,
					tPrev: $(this).data('prev-text'),
					tNext: $(this).data('next-text')
				},
				type: 'image',
				callbacks: {
					beforeOpen: function() {
						var index = $imageLinks.index(this.st.el);
						if (-1 !== index) {
							this.goTo(index);
						}
					}
				}
			});
		});


		/* ==================================================
		    _Progressbar Init
		 ===============================================*/
		function animateElements() {
			$('.progressbar').each(function() {
				var elementPos = $(this).offset().top;
				var topOfWindow = $(window).scrollTop();
				var percent = $(this).find('.circle').attr('data-percent');
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle').circleProgress({
						// startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 120,
						thickness: 10,
						lineCap: 'round',
						emptyFill: '#eeeeee',
						fill: {
							gradient: ['#2e1081ff', '#2e1081ff']
						}
					}).on('circle-animation-progress', function(event, progress, stepValue) {
						$(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
					}).stop();
				}
			});

			$('.progressbar-two').each(function() {
				var elementPos = $(this).offset().top;
				var topOfWindow = $(window).scrollTop();
				var percent = $(this).find('.circle-two').attr('data-percent');
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle-two').circleProgress({
						// startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 100,
						thickness: 5,
						lineCap: 'round',
						emptyFill: '#acbdf9',
						fill: {
							gradient: ['#ffffff', '#ffffff']
						}
					}).on('circle-animation-progress', function(event, progress, stepValue) {
						$(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
					}).stop();
				}
			});


			$('.progressbar-three').each(function() {
				var elementPos = $(this).offset().top;
				var topOfWindow = $(window).scrollTop();
				var percent = $(this).find('.circle-three').attr('data-percent');
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle-three').circleProgress({
						// startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 100,
						thickness: 3,
						lineCap: 'round',
						emptyFill: '#dddddd',
						fill: {
							gradient: ['#232323', '#214BE0']
						}
					}).on('circle-animation-progress', function(event, progress, stepValue) {
						$(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
					}).stop();
				}
			});
		}

		animateElements();
		$(window).scroll(animateElements);


		/* ==================================================
            # Hover Active Init
        ===============================================*/
		$('.hover-active-item').on('mouseenter', function() {
			var $this;
			$this = $(this);
			if ($this.hasClass('active')) {
				$this.addClass('active');
			} else {
				$this.addClass('active');
				$this.siblings().removeClass('active');
			}
		})



		/* ==================================================
            # Banner Carousel
         ===============================================*/
		 const bannerFade = new Swiper(".banner-fade", {
            // Optional parameters
            direction: "horizontal",
            loop: true,
            effect: "fade",
            fadeEffect: {
                crossFade: true
            },
			autoplay: true,
            // If we need pagination
            pagination: {
                el: '.baner-one-pagination',
                type: 'bullets',
                clickable: true,
            },

            // Navigation arrows
            navigation: {
                nextEl: ".banner-next-nav",
                prevEl: ".banner-prev-nav"
            }

            // And if we need scrollbar
            /*scrollbar: {
            el: '.swiper-scrollbar',
          },*/
        });


		/* ==================================================
            # Visa Category Carousel
         ===============================================*/
		 const visaCatCarousel = new Swiper(".visa-category-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".visa-category-next",
				prevEl: ".visa-category-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1400: {
					slidesPerView: 3,
					centeredSlides: true,
				},
			},
		});


		/* ==================================================
            # Visa Category Carousel
         ===============================================*/
		 const visaTwoCarousel = new Swiper(".visa-category-two-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 0,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".visa-category-two-next",
				prevEl: ".visa-category-two-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1400: {
					slidesPerView: 3,
					centeredSlides: true,
				},
			},
		});


		/* ==================================================
            # Visa Category Carousel
         ===============================================*/
		 const visaThreeCarousel = new Swiper(".visa-category-three-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 0,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".visa-category-three-next",
				prevEl: ".visa-category-three-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1400: {
					slidesPerView: 3,
				},
			},
		});


		/* ==================================================
            # Visa Category Carousel
         ===============================================*/
		 const visaFourCarousel = new Swiper(".visa-category-four-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".visa-category-four-next",
				prevEl: ".visa-category-four-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1024: {
					slidesPerView: 3,
				},
				1800: {
					slidesPerView: 4,
				},
			},
		});


		/* ==================================================
            # Visa Country Carousel
         ===============================================*/
		 const countrCoverageCarousel = new Swiper(".country-coverage-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".visa-category-two-next",
				prevEl: ".visa-category-two-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1024: {
					slidesPerView: 3,
				},
				1400: {
					slidesPerView: 4,
				},
			},
		});

		/* ==================================================
            # Course Carousel
         ===============================================*/
		 const courseCarousel = new Swiper(".course-style-one-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			centeredSlides: true,
			spaceBetween: 2,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".course-carousel-next",
				prevEl: ".course-carousel-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					centeredSlides: false,
					spaceBetween: 15,
				},
				1200: {
					slidesPerView: 2.5,
				},
				1800: {
					slidesPerView: 3.8,
				},
			},
		});


		/* ==================================================
            # Testimonial Carousel
         ===============================================*/
		 const testimonialOneCarousel = new Swiper(".testimonial-style-one-carousel", {
			// Optional parameters
			direction: "horizontal",
            loop: true,
            effect: "fade",
            fadeEffect: {
                crossFade: true
            },
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".testimonial-style-one-next",
				prevEl: ".testimonial-style-one-prev"
			}
		});



		/* ==================================================
            # Testimonial Carousel
         ===============================================*/
		 const testimonialTwoCarousel = new Swiper(".testimonial-style-two-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			centeredSlides: true,
			spaceBetween: 0,
			autoplay: true,
			// Navigation arrows
			navigation: {
				nextEl: ".testimonial-style-two-next",
				prevEl: ".testimonial-style-two-prev"
			}
		});

		/* ==================================================
            # Testimonial Three Carousel
         ===============================================*/
		 const tesimonialThreeCarousel = new Swiper(".testimonial-style-three-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1024: {
					slidesPerView: 2,
				},
			},
		});


		/* ==================================================
            # Testimonial Four Carousel
         ===============================================*/
		 const tesimonialFourCarousel = new Swiper(".testimonial-four-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			pagination: {
				el: '.testimonial-four-pagination',
				type: 'fraction',
				clickable: true,
			},
			// Navigation arrows
			navigation: {
				nextEl: ".testimonial-style-four-next",
				prevEl: ".testimonial-style-four-prev"
			}
		});


		/* ==================================================
            # Brand Carousel
         ===============================================*/
		 const brandOne = new Swiper(".brand-style-one-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 2,
			spaceBetween: 30,
			autoplay: true,
			breakpoints: {
				768: {
					slidesPerView: 3,
					spaceBetween: 50,
				},
				992: {
					slidesPerView: 3,
					spaceBetween: 50,
				},
				1200: {
					slidesPerView: 4,
					spaceBetween: 50,
				},
				1800: {
					slidesPerView: 6,
					spaceBetween: 80,
				}
			},
		});


		

		/* ==================================================
		    Splite Text
		================================================== */
		let text_split = document.querySelector(".split-text");
		if (text_split) {
			const animEls = document.querySelectorAll('.split-text');
			animEls.forEach(el => {
				var splitEl = new SplitText(el, {
					type: "lines, words",
					linesClass: "line"
				});
				var splitTl = gsap.timeline({
					duration: 0,
					ease: 'power4',
					scrollTrigger: {
						trigger: el,
						start: 'top 90%'
					}
				});

				splitTl.from(splitEl.words, {
					yPercent: "100",
					stagger: 0.025,
				});

			});
		}

		
		/* ==================================================
		    GSAP Element Scroll Animation
		================================================== */

		let upDown_Scroll = document.querySelector(".upDownScrol");
		if (upDown_Scroll) {
			gsap.set(".upDownScrol", {
				yPercent: 30
			});

			gsap.to(".upDownScrol", {
				yPercent: -30,
				ease: "none",
				scrollTrigger: {
					trigger: ".upDownScrol",
					end: "bottom center",
					scrub: 1
				},
			});
		}


		let leftRight_Scroll = document.querySelector(".leftRightScroll");
		if (leftRight_Scroll) {
			gsap.set(".leftRightScroll", {
				xPercent: -15
			});

			gsap.to(".leftRightScroll", {
				xPercent: 15,
				ease: "none",
				scrollTrigger: {
					trigger: ".leftRightScroll",
					end: "left center",
					scrub: 1
				},
			});
		}

		let rightLeft_Scroll = document.querySelector(".rightLeftScroll");
		if (rightLeft_Scroll) {
			gsap.set(".rightLeftScroll", {
				xPercent: 15
			});

			gsap.to(".rightLeftScroll", {
				xPercent: -15,
				ease: "none",
				scrollTrigger: {
					trigger: ".rightLeftScroll",
					end: "right center",
					scrub: 1
				},
			});
		}


		/* ===================================================================
			Accordion Hover
		* ================================================================= */
		let accordion_animation = document.querySelector("#accordion");
		if (accordion_animation) {
			var expand;
			var $accordion, $wideScreen;
			$accordion = $('#accordion').children('li');
			$wideScreen = $(window).width() > 767;
			if ($wideScreen) {
				$accordion.on('mouseenter click', function(e) {
					var $this;
					e.stopPropagation();
					$this = $(this);
					if ($this.hasClass('out')) {
						$this.addClass('out');
					} else {
						$this.addClass('out');
						$this.siblings().removeClass('out');
					}
				});
			} else {
				$accordion.on('touchstart touchend', function(e) {
					var $this;
					e.stopPropagation();
					$this = $(this);
					if ($this.hasClass('out')) {
						$this.addClass('out');
					} else {
						$this.addClass('out');
						$this.siblings().removeClass('out');
					}
				});
			}
		}


		/* ==================================================
		    Hover Tab
		================================================== */
		let selectedIndex = 0;
		$('.country-three-content-list .item').on('click', function (e) {
			$(this).addClass('active').siblings().removeClass('active');
			let arr = [...$('.country-three-content-list .item')];
			arr.forEach((value, index) => {
				if ($(value).hasClass('active')) {
					selectedIndex = index + 1;
				}
			});
			$('.country-three-contents:nth-child(' + selectedIndex + ')').addClass('active').siblings().removeClass('active');
		});


		/* ==================================================
		    Contact Form Validations
		================================================== */
		$('.contact-form').each(function() {
			var formInstance = $(this);
			formInstance.submit(function() {

				var action = $(this).attr('action');

				$("#message").slideUp(750, function() {
					$('#message').hide();

					$('#submit')
						.after('<img src="assets/img/ajax-loader.gif" class="loader" />')
						.attr('disabled', 'disabled');

					$.post(action, {
							name: $('#name').val(),
							email: $('#email').val(),
							phone: $('#phone').val(),
							comments: $('#comments').val()
						},
						function(data) {
							document.getElementById('message').innerHTML = data;
							$('#message').slideDown('slow');
							$('.contact-form img.loader').fadeOut('slow', function() {
								$(this).remove()
							});
							$('#submit').removeAttr('disabled');
						}
					);
				});
				return false;
			});
		});

	}); // end document ready function

	/* ==================================================
        Preloader Init
     ===============================================*/
	 $(window).on('load', function(event) {
		$('#preloader').delay(500).fadeOut(500);
	});
	
})(jQuery); // End jQuery

