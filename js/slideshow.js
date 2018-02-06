var current_slide = 0;

function scroll() {
	
	// Wrap around end of slides if needed
	var slides = $(".slides");
	if (current_slide >= slides.length-1) {
		current_slide = -1;
	};
	
	// Change to next slide
	show_slide(current_slide+1, auto=true);
	
	// Update slide reference
	current_slide++;

};

function show_slide(n, auto=false) {
	// Get images and thumbnails
	var slides = $(".slides");
	var thumbs = $(".slideshow-thumbnails");
	
	// Deactivate current slide
	$(slides.get(current_slide)).css("display", "none");
	$(thumbs.get(current_slide)).css("opacity", "0.6");
	
	// Update target slide
	$(slides.get(n)).css("display", "block");
	$(thumbs.get(n)).css("opacity", "1");
	
	// Updated slide reference
	if (!auto) {
		current_slide = n;
	}
};

function clicked() {
	// Toggle autoscroll if manually clicked
	clearInterval(scroller);
}

// Enable autoscrolling
var scroller = setInterval(scroll, 5000);
