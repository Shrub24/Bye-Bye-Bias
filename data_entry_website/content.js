var sentiments;

window.onload = function() {
    var example_element = document.getElementById("example_text");
    // var entities = [[0, 3], [4, 7]]
    // var text = "the car is back"
    var text = "this hole is very fun"
    var entities = [[5, 9], [13, 17]]
    example_element.innerHTML = generateExampleHTML(entities, text)
}

//entities is array of ORDERED character indexes (start-inclusive, end-exclusive)
function generateExampleHTML(entities, text) {
    sentiments = Array(entities.length).fill("n");
    var html = text;
    var offset = 0;
    var e_id = 0
    for(var entity of entities) {
        var startIndex = entity[0];
        var endIndex = entity[1];
        var entityName = text.slice(startIndex, endIndex);
        var id_string = e_id.toString();
        var replacementHTML = "<div class='dropdown'><span><mark id=" + id_string + ">" + entityName + "</mark></span><div class='dropdown-content'><button onclick='sentimentSelected(-1," + id_string + ")'>-1</button><button onclick='sentimentSelected(0," + id_string + ")'>0</button><button onclick='sentimentSelected(1," + id_string + ")'>1</button></div></div>";
        html = html.slice(0, startIndex + offset) + replacementHTML + html.slice(endIndex + offset);
        offset += replacementHTML.length - entityName.length
        e_id += 1
    }
    return html;
}

function sentimentSelected(sentiment, elementID) {
    // console.log(sentiment.toString())
    // console.log(document.getElementById(elementID).innerHTML)
    sentiments[elementID] = sentiment;
    var markElement = document.getElementById(elementID);
    markElement.className = ""
    switch(sentiment) {
        case -1:
            markElement.className = "red-highlight";
            break;
        case 0:
            markElement.className = "grey-highlight";
            break;
        case 1:
            markElement.className = "green-highlight";
            break
        default:
            console.log("invalid sentiment selected")
    } 
}

function submitSentiments() {
    console.log(sentiments)
}