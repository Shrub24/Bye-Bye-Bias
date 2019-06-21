//truncate template text
//Inject test stuff

Handlebars.registerHelper('cards', function(items, options) {
    console.log(items);
});

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

var colorsEnum = {
    
}

window.onload = function() {
    var data = {
        "Cards": [
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
        ]
    }
    
    var templateCard = Handlebars.template(precompiledTemplateCard);
    var content = document.querySelector("#items > div.simplebar-wrapper > div.simplebar-mask > div > div > div");

    content.innerHTML = templateCard(data);
}