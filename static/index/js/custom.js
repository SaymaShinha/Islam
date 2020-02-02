// Jquery with no conflict
$(document).ready(function($) {

	//##########################################
	// Superfish
	//##########################################

	//$("ul.sf-menu").superfish({
	// animation: {height:'show'},   // slide-down effect without fade-in
     //   delay:     200 ,              // 1.2 second delay on mouseout
      //  autoArrows:  false,
       // speed: 200
   // });

    //##########################################
	// HOME SLIDER
	//##########################################

    $('.home-slider').flexslider({
    	animation: "fade",
    	controlNav: false,
    	keyboardNav: true
    });

    //##########################################
	// PROJECT SLIDER
	//##########################################

    $('.project-slider').flexslider({
    	animation: "fade",
    	controlNav: true,
    	directionNav: false,
    	keyboardNav: true
    });


	//##########################################
	// Tweet feed
	//##########################################

	/*$("#tweets").tweet({
        count: 3,
        username: "ansimuz"
    });*/

	//##########################################
	// Top Widget
	//##########################################



	//##########################################
	// Tool tips
	//##########################################







	//##########################################
	// PrettyPhoto
	//##########################################

	$('a[data-rel]').each(function() {
	    $(this).attr('rel', $(this).data('rel'));
	});

	$("a[rel^='prettyPhoto']").prettyPhoto();


});

