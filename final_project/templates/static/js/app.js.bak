function initViz() {
	var containerDiv = document.getElementById("vizContainer"),
		url_home = "https://public.tableau.com/views/TeamStats_16582409510560/HomeTeam",
		
		options = {
			hideTabs: true,
			onFirstInteractive: function () {
				console.log("Run this code when the viz has finished loading.");
			}
		};

	var viz = new tableau.Viz(containerDiv, url_home, options);
	
	var containerDiv1 = document.getElementById("vizContainer1"),
	url_away = "https://public.tableau.com/views/TeamStats_16582409510560/AwayTeam",
	
	options = {
		hideTabs: true,
		onFirstInteractive: function () {
			console.log("Run this code when the viz has finished loading.");
		}
	};

	var viz = new tableau.Viz(containerDiv1, url_away, options);
	// Create a viz object and embed it in the container div.
}