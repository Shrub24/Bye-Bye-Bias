function test() {
    var templateCard = Handlebars.template(precompiledTemplateCard);
    var content = document.querySelector("#items > div.simplebar-wrapper > div.simplebar-mask > div > div > div > #card-container");

    content.innerHTML = templateCard(data);
}

function addClickHandlers() {
    let elementsArray = document.querySelectorAll("a");

    elementsArray.forEach(function(elem) {
        elem.addEventListener("click", function(event) {
            var targetPage = event.currentTarget.href;

            chrome.tabs.create({
                url: targetPage,
              });
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
  test();
  addClickHandlers();
});


//truncate template text
//Inject test stuff

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

var data = {
    "thisPage":22,
    "Cards": [
        {"Title": "5", 
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "Color": getRandomColor(),
        "URL": "http://www.google.com",
    },
    {"Title": "4", 
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "Color": getRandomColor(),
    },
    {"Title": "4", 
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "Color": getRandomColor(),
    },
    {"Title": "4", 
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "Color": getRandomColor(),
    },
    {"Title": "Narrow sea strip pulling the world apart and then putting it together again.", 
        "Date": "4444 44",
        "Publisher": "Jhin",
        "Author": "Idk who made numbers",
        "Color": getRandomColor(),
    },
    ]
}