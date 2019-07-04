var serverUrl = "http://localhost:8000/"

function fetchUrlAndStore(urlToFetch) {
  var filtered = Object.keys(localStorage).filter(function (value) {
    return JSON.parse(localStorage.getItem(value)).hasOwnProperty("date");
  });

  fetch(serverUrl + "?" + urlToFetch, {method: "GET"}).then(function (response) {
    if (!response.ok) {
      return false
    }
    return response.json();
  })
  .then(function(body) {
    if (body && body != "unknown") {
      body.day = new Date();
      localStorage.setItem(urlToFetch, JSON.stringify(body));

      if(filtered.length > 50) {
        if(filtered != []) {
          var oldest = filtered.reduce(function(acc, val) {
            return JSON.parse(localStorage.getItem(acc)).date < JSON.parse(localStorage.getItem(val)).date ? acc : val;
          });
          localStorage.removeItem(oldest);
        }
      }
    }
    else{
      // Invalid response
    }
  })
  .catch(function(err) {
    // No server
  });
}

// Listen for any changes to the URL of any tab.
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
      if(localStorage.getItem('fetchOnLoad') == "true") {
        // Check storage first
        // todo store no stored solution value?
        if(localStorage.getItem(tab.url) == undefined) {
          chrome.pageAction.hide(tabId)
          // Cached result doesnt exist and fetchOnLoad is true therefore fetch now
          fetchUrlAndStore(tab.url)
          if(localStorage.getItem(tab.url) != undefined) {
            chrome.pageAction.show(tabId)
          }
        }
        else {
          // Cached version exists
          chrome.pageAction.show(tabId);
        }
      }
});

chrome.runtime.onInstalled.addListener(function (details) {
  if(details.reason == "install") {
    localStorage.setItem('reduceAnimations', 'false');
    localStorage.setItem('fetchOnLoad', 'true');
  }
});