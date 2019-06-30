var testData = {
  "thisPage":5,
  "Cards": [
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "4", 
      "Score": 1,
      "Date": "4444 44",
      "Publisher": "Jhin",
      "Author": "Idk who made numbers",
      "URL": "http://www.google.com",
      },
      {"Title": "Ey", 
      "Score": 3,
      "Date": "1234 11",
      "Publisher": "Me",
      "Author": "Him",
      "URL": "http://www.google.com",
      },
      {"Title": "Ey", 
      "Score": 3,
      "Date": "1234 11",
      "Publisher": "Me",
      "Author": "Him",
      "URL": "http://www.google.com",
      },
      {"Title": "Ey", 
      "Score": 5,
      "Date": "1234 11",
      "Publisher": "Me",
      "Author": "Him",
      "URL": "http://www.google.com",
      },
      {"Title": "Ey", 
      "Score": 9,
      "Date": "1234 11",
      "Publisher": "Me",
      "Author": "Him",
      "URL": "http://www.google.com",
      }
  ]
}

var serverUrl = "http://localhost:8000/"

var urls = [
  "https://www.google.com",
  "https://www.bbc.com"
];

function fetchUrlAndStore(urlToFetch) {
  var filtered = Object.keys(localStorage).filter(function (value) {
    return JSON.parse(localStorage.getItem(value)).hasOwnProperty("date");
  });

  
  testData.date = new Date();
  setTimeout(function () {localStorage.setItem(urlToFetch, JSON.stringify(testData))}, 1000);

  if(filtered.length > 50) {
    if(filtered != []) {
      var oldest = filtered.reduce(function(acc, val) {
        return JSON.parse(localStorage.getItem(acc)).date < JSON.parse(localStorage.getItem(val)).date ? acc : val;
      });
      localStorage.removeItem(oldest);
    }
  }

  /*
  fetch(serverUrl + "?" + urlToFetch, {method: "GET"}).then(function (response) {
    return response.json();
  })
  .then(function(body) {
    localStorage.setItem(urlToFetch, body);
  });
  */
}

// Listen for any changes to the URL of any tab.
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  for(var i=0; i<urls.length; i++) {
    if (tab.url.indexOf(urls[i]) == 0) {
      chrome.pageAction.show(tabId);

      //Check storage first
      if(localStorage.getItem('fetchOnLoad') == "true"  && localStorage.getItem(tab.url) != undefined) {
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