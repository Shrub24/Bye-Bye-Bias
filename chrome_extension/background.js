var serverUrl = "http://localhost:8000/"

var urls = [
  "https://www.google.com",
  "https://www.bbc.com"
];

function fetchUrlAndStore(urlToFetch) {
  var filtered = Object.keys(localStorage).filter(function (value) {
    return JSON.parse(localStorage.getItem(value)).hasOwnProperty("date");
  });

  fetch(serverUrl + "?" + urlToFetch, {method: "GET"}).then(function (response) {
    return response.json();
  })
  .then(function(body) {
    body.day = new Date();
    localStorage.setItem(urlToFetch, JSON.stringify(body));
  });

  if(filtered.length > 50) {
    if(filtered != []) {
      var oldest = filtered.reduce(function(acc, val) {
        return JSON.parse(localStorage.getItem(acc)).date < JSON.parse(localStorage.getItem(val)).date ? acc : val;
      });
      localStorage.removeItem(oldest);
    }
  }
}

// Listen for any changes to the URL of any tab.
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  for(var i=0; i<urls.length; i++) {
    if (tab.url.indexOf(urls[i]) == 0) {
      chrome.pageAction.show(tabId);
      
      //Check storage first
      if(localStorage.getItem('fetchOnLoad') == "true"  && localStorage.getItem(tab.url) == undefined) {
        //Cached result doesnt exist and fetchOnLoad is true therefore fetch now
        fetchUrlAndStore(tab.url);
      } else {
        //Either a cached version exists or fetchOnLoad is false then let the popup handle it
      }
      break;
    }
  }
});

chrome.runtime.onInstalled.addListener(function (details) {
  if(details.reason == "install") {
    localStorage.setItem('reduceAnimations', 'false');
    localStorage.setItem('fetchOnLoad', 'true');
  }
});