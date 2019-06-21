// server GET stuff
var source_url = "http://localhost:8000"

function update_info(url){
	var xmlHttp = new XMLHttpRequest();
	chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    	current_url = tabs[0].url
        try {
        	xmlHttp.open("GET", url + "?" + current_url, false);
    		xmlHttp.send();
    		info = JSON.parse(xmlHttp.responseText)
            // replace these with where u want the actual stuff
            var topic = info["topic"]
            var strength = info["strength"]
            var articles = info["articles"]
        }
        catch(e) {
            // todo log error
            // alert(e)
            var topic = "undefined"
            var strength = 0
            var articles = {}
        }
		document.getElementById("topic").innerHTML = topic
		document.getElementById("strength").innerHTML = strength
		document.getElementById("articles").innerHTML = create_dual_html_list(articles)
	});
}

// remove this when no longer needed, currently for debugging and show
function create_dual_html_list(dict){
	var str = "<ul>"
	keys = Object.keys(dict)
	keys.forEach(function(key){
		str += "<li>" + key + " " + dict[key]
	})

	str += "</ul>";
	return str
}

// merge window.onload and "DOMContentLoaded" at some point
document.addEventListener('DOMContentLoaded', function() {
  update_info(source_url)
});


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
        "thisPage":22,
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
