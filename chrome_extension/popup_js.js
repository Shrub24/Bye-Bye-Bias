var source_url = "http://localhost:8000"

function get_info(url){
	var xmlHttp = new XMLHttpRequest();
	chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    	current_url = tabs[0].url
    	alert(current_url)
    	xmlHttp.open("GET", url + "?" + current_url, false);
		xmlHttp.send();
		// alert(xmlHttp.responseText)
		return xmlHttp.responseText
	});
}

function main(){
	get_info(source_url)
}

document.addEventListener('DOMContentLoaded', function() {
  main()
});