
"use strict"

var dlabSettingsOptions = {};

function getUrlParams(dParam) 
	{
		var dPageURL = window.location.search.substring(1),
			dURLVariables = dPageURL.split('&'),
			dParameterName,
			i;

		for (i = 0; i < dURLVariables.length; i++) {
			dParameterName = dURLVariables[i].split('=');

			if (dParameterName[0] === dParam) {
				return dParameterName[1] === undefined ? true : decodeURIComponent(dParameterName[1]);
			}
		}
	}

(function($) {
	
	"use strict"
	
	/* var direction =  getUrlParams('dir');
	
	if(direction == 'rtl')
	{
        direction = 'rtl'; 
    }else{
        direction = 'ltr'; 
    } */
	
	dlabSettingsOptions = {
		typography: "poppins",
		version: "light",
		layout: "horizontal",
		primary: "color_12",
		secondary: "color_12",
		headerBg: "color_13",
		navheaderBg: "color_13",
		sidebarBg: "color_13",
		sidebarStyle: "mini",
		sidebarPosition: "fixed",
		headerPosition: "static",
		containerLayout: "full",
	};
	
	
	
	new dlabSettings(dlabSettingsOptions); 

	jQuery(window).on('resize',function(){
        /*Check container layout on resize */
		///alert(dlabSettingsOptions.primary);
        dlabSettingsOptions.containerLayout = $('#container_layout').val();
        /*Check container layout on resize END */
        
		new dlabSettings(dlabSettingsOptions); 
	});
	
})(jQuery);