var viz_home
var viz_away
var viz_avg
var _ParamA = "Arsenal"
var _ParamB ="Arsenal"

var baseurl = "https://public.tableau.com/views/TeamStats_16582409510560/"



function openPage(evt, xyz) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace("active", "");
  }
  
  document.getElementById(xyz).style.display = "block";
  evt.currentTarget.className += " active";

  var _selpage = document.getElementById(xyz).id
}


// document.getElementById("Home").click();
  
function submit_btn() {
  var _ParamA = document.getElementById("TeamA").value;
  var _ParamB = document.getElementById("TeamB").value;
  console.log(_ParamA)
  console.log("button pressed")
  // if (_selpage="Dashboard") {
  console.log*('createComparisonViz')
  createComparisonViz(_ParamA, _ParamB);
  // } 
}

function createComparisonViz(_ParamA, _ParamB) {
  // Home Team Viz url
	// var _ParamA = "Manchester City"
  // var _ParamB ="Chelsea"
  console.log("create " + _ParamA)
  var url_home = baseurl + "HomeTeam?:showVizHome=no&TeamA_param=" + _ParamA
	var url_away = baseurl + "AwayTeam?:showVizHome=no&TeamB_param=" + _ParamB

  var containerDiv = document.getElementById("vizContainer"),
  	
		options = {
			hideTabs: true,
			onFirstInteractive: function () {
				console.log("Home loaded.");
			}
		};

    if (viz_home) { // If a viz object exists, delete it.
      viz_home.dispose();
    }
	 viz_home = new tableau.Viz(containerDiv, url_home, options);
  
   // Away Team Viz URL
	var containerDiv1 = document.getElementById("vizContainer1"),

	options = {
		hideTabs: true,
		onFirstInteractive: function () {
			console.log("Away Loaded");
		}
	};
  if (viz_away) { // If a viz object exists, delete it.
    viz_away.dispose();
  }
	viz_away = new tableau.Viz(containerDiv1, url_away, options);
	// Create a viz object and embed it in the container div.

}

function createShotsViz() {

  var url_avg = baseurl + "ShotsbyMonths"

  // Avg Shots viz
	var avgShotsContainer = document.getElementById("vizContainerAvg"),
  
	options = {
		hideTabs: true,
		onFirstInteractive: function () {
			console.log("Average Shots Loaded");
		}
	};

  if (viz_avg) { // If a viz object exists, delete it.
    viz_avg.dispose();
  }
  viz_avg = new tableau.Viz(avgShotsContainer, url_avg, options);
	// Create a viz object and embed it in the container div.
}

function openNav() {
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}

function selWeekFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("match_week");
  filter = input.value.toUpperCase();
  table = document.getElementById("upcoming_matches");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

window.onload = function() {
  document.getElementById('Home').click();
};