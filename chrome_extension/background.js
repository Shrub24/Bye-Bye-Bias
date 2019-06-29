var serverUrl = "http://localhost:8000"

function getData(callback){
  var httpRequest = new XMLHttpRequest();
  
	chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
      var current_url = tabs[0].url

      httpRequest.onload(function () {
        callback();
      });

      httpRequest.open("GET", serverUrl + "?" + current_url, true);
      httpRequest.send();

      info = JSON.parse(httpRequest.responseText)
      return info;
	});
}