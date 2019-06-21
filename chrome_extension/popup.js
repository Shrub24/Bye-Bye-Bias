var source_url = "http://localhost:8000"

function update_info(url){
	var xmlHttp = new XMLHttpRequest();
	chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    	current_url = tabs[0].url
    	xmlHttp.open("GET", url + "?" + current_url, false);
		xmlHttp.send();
		// alert(xmlHttp.responseText)
		info = JSON.parse(xmlHttp.responseText)
		// alert(info["topic"])
		document.getElementById("topic").innerHTML = info["topic"]
		document.getElementById("strength").innerHTML = info["strength"]
		document.getElementById("articles").innerHTML = create_dual_html_list(info["articles"])
	});
}

function create_dual_html_list(dict){
	var str = "<ul>"
	keys = Object.keys(dict)
	keys.forEach(function(key){
		str += "<li>" + key + " " + dict[key]
	})

	str += "</ul>";
	return str
}

document.addEventListener('DOMContentLoaded', function() {
  update_info(source_url)
});