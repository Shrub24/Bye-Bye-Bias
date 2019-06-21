// server GET stuff
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
    // replace these with where u want the actual stuff
		document.getElementById("topic").innerHTML = info["topic"]
		document.getElementById("strength").innerHTML = info["strength"]
		document.getElementById("articles").innerHTML = create_dual_html_list(info["articles"])
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
