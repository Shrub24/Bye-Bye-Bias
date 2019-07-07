var serverUrl = "http://localhost:8000/"

function fetchUrlAndStore(urlToFetch, tabId, callback) {
  localStorage.setItem(urlToFetch, "fetching");
  
  fetch(serverUrl + "?" + urlToFetch, {method: "GET"}).then(function (response) {
    if (!response.ok) {
      return false
    }
    try {
      return JSON.parse(response);
    } catch (error) {
      return response.text();
    }
  })
  .then(function(body) {
    if (body == "unknown") {
      var currentDate = new Date();
      localStorage.setItem(urlToFetch, JSON.stringify({"unknown":true, Date: currentDate}));
    } else if (body) {
      body.day = new Date();
      localStorage.setItem(urlToFetch, JSON.stringify(body));
    } else {
      // Request error
    }

    var filtered = Object.keys(localStorage).filter(function (value) {
      try {
        return JSON.parse(localStorage.getItem(value)).hasOwnProperty("date");
      } catch (error) {
        return false;
      }
    });
    
    if(filtered.length > 50) {
      if(filtered != []) {
        var oldest = filtered.reduce(function(acc, val) {
          return JSON.parse(localStorage.getItem(acc)).date < JSON.parse(localStorage.getItem(val)).date ? acc : val;
        });
        localStorage.removeItem(oldest);
      }
    }
    
    if(callback != undefined)
      callback(urlToFetch, tabId);
  })
  .catch(function(err) {
    // No server
    localStorage.removeItem(urlToFetch);
    throw err;
  });
}

// Listen for any changes to the URL of any tab.
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if(localStorage.getItem('fetchOnLoad') == "true" && localStorage.getItem(tab.url) == undefined) {
    fetchUrlAndStore(tab.url);
  }
});

chrome.runtime.onInstalled.addListener(function (details) {
  if(details.reason == "install") {
    localStorage.setItem('reduceAnimations', 'false');
    localStorage.setItem('fetchOnLoad', 'true');
  }
});