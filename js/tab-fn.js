$(function() {
	
	function reset_tabs() {
		// Refresh tabs & content styles currently in view
		$(".tab-button").removeClass("clicked");
		$(".tabbed-content").removeClass("selected");
	};
	
	////// Configure tabbed content (applications.htm)
	
	//   Initialize first tab:
	$("#geology").toggleClass('selected');
	$("#button-geology").toggleClass('clicked');
	
	// Add button events for Examples page
	$("#button-targets").on('click', function() {
		reset_tabs();
		$("#buried-targets").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-linear").on('click', function() {
		reset_tabs();
		$("#linear-features").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-decimetre").on('click', function() {
		reset_tabs();
		$("#decimetre").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-archeology").on('click', function() {
		reset_tabs();
		$("#archeology").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-geology").on('click', function() {
		reset_tabs();
		$("#geology").toggleClass('selected');
		$(this).addClass("clicked");
	});
		
	////// Configure tabbed content (publications.htm)
	
	//   Initialize first tab:
	$("#articles").toggleClass('selected')
	$("#button-articles").toggleClass('clicked');
	
	// Add button events for Publications page
	$("#button-articles").on('click', function() {
		reset_tabs();
		$("#articles").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-phds").on('click', function() {
		reset_tabs();
		$("#phds").toggleClass('selected');
		$(this).addClass("clicked");
	});
	$("#button-conferences").on('click', function() {
		reset_tabs();
		$("#conferences").toggleClass('selected');
		$(this).addClass("clicked");
	});
});
