var sentiments;
var exampleNum = 0;

//Hardcoded examples
var examples = []

var entities = [[0, 3], [4, 7]]
var text = "the car is back"
examples.push([text, entities])

var text = "this hole is very fun"
var entities = [[5, 9], [13, 17]]
examples.push([text, entities])

var text = "Trump isn't a great guy"
var entities = [[0,5],[20, 23]]
examples.push([text, entities])

var text = "Obama is very cool"
var entities = [[0, 5]]
examples.push([text, entities])

var text = "He's just Biden his time"
var entities = [[0, 4], [10, 15]]
examples.push([text, entities])

window.onload = function() {
    var example_element = document.getElementById("example_text");
    firstExample = getNextExample()
    example_element.innerHTML = generateExampleHTML(firstExample[1], firstExample[0])
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
    var example_element = document.getElementById("example_text");
    console.log(sentiments)
    for(var i=0; i < sentiments.length;i++) {
        console.log(document.getElementById(i.toString()).innerHTML + ": " + sentiments[i])
    }
    var nextExample = getNextExample()
    example_element.innerHTML = generateExampleHTML(nextExample[1], nextExample[0])
}

function getNextExample() {
    if(exampleNum < examples.length) {
        exampleNum += 1
    }
    else{
        exampleNum = 1
    }
    return examples[exampleNum - 1]
}