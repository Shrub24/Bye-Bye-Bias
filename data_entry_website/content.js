var sentiments;
var exampleNum = 0;
// todo dont use global variable pass textID into generate HTML
var e_id = 0;

//Hardcoded examples
// var examples = []
//
// var entities = [[0, 3], [4, 7]]
// var text = "the car is back"
// examples.push([text, entities])
//
// var text = "this hole is very fun"
// var entities = [[5, 9], [13, 17]]
// examples.push([text, entities])
//
// var text = "Trump isn't a great guy"
// var entities = [[0,5],[20, 23]]
// examples.push([text, entities])
//
// var text = "Obama is very cool"
// var entities = [[0, 5]]
// examples.push([text, entities])
//
// var text = "He's just Biden his time"
// var entities = [[0, 4], [10, 15]]
// examples.push([text, entities])
var example1text = "Trump is a really great guy. His wall has been very effective. His policies have benefited America greatly. Sed arcu non odio euismod lacinia at quis risus sed. Aliquet enim tortor at auctor urna nunc id cursus. Pretium aenean pharetra magna ac placerat. Nunc vel risus commodo viverra maecenas accumsan lacus. Sed nisi lacus sed viverra tellus. Quis risus sed vulputate odio ut. Commodo odio aenean sed adipiscing diam donec adipiscing. Faucibus purus in massa tempor nec feugiat. Consectetur purus ut faucibus pulvinar elementum integer enim.\n" +
    "\n" +
    "Leo a diam sollicitudin tempor. Varius duis at consectetur lorem. Turpis egestas maecenas pharetra convallis posuere morbi leo urna. Volutpat odio facilisis mauris sit amet massa vitae tortor. Tellus cras adipiscing enim eu turpis egestas pretium."

var example1entities = [[0, 5], [29, 37], [63, 75], [91, 98]]

var example2text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Felis bibendum ut tristique et. Ullamcorper malesuada proin libero nunc consequat interdum. Neque aliquam vestibulum morbi blandit cursus risus. Integer vitae justo eget magna fermentum iaculis eu. Tellus integer feugiat scelerisque varius morbi enim nunc faucibus a. Egestas purus viverra accumsan in nisl nisi scelerisque eu ultrices. Scelerisque varius morbi enim nunc faucibus. Platea dictumst quisque sagittis purus sit. Massa massa ultricies mi quis hendrerit dolor. Id aliquet lectus proin nibh nisl condimentum id venenatis a. Etiam dignissim diam quis enim lobortis scelerisque fermentum dui faucibus.\n" +
    "\n" +
    "Curabitur vitae nunc sed velit dignissim sodales ut eu sem. Aliquam sem et tortor consequat. Senectus et netus et malesuada fames ac. Id semper risus in hendrerit. Volutpat sed cras ornare arcu dui vivamus. Velit scelerisque in dictum non consectetur a erat nam at. Risus ultricies tristique nulla aliquet enim tortor at. Convallis posuere morbi leo urna. Donec adipiscing tristique risus nec feugiat in fermentum. Eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis.\n" +
    "\n" +
    "Tellus mauris a diam maecenas sed enim. Et leo duis ut diam quam nulla porttitor. Pellentesque habitant morbi tristique senectus et netus et malesuada. Eget gravida cum sociis natoque penatibus et magnis. Nisl tincidunt eget nullam non nisi est sit amet facilisis. Sit amet nisl suscipit adipiscing. Lobortis feugiat vivamus at augue eget arcu dictum. Nam at lectus urna duis convallis. Diam sollicitudin tempor id eu nisl nunc mi. Nunc lobortis mattis aliquam faucibus purus in massa. Eu mi bibendum neque egestas congue quisque. Faucibus turpis in eu mi bibendum neque egestas congue quisque. Vestibulum rhoncus est pellentesque elit. Magna sit amet purus gravida quis blandit turpis cursus in. Massa tempor nec feugiat nisl pretium fusce id. Ac turpis egestas integer eget aliquet nibh praesent tristique. Vitae auctor eu augue ut lectus arcu bibendum at varius. The world is a better place because of Mr Xi and his government."

var example2entities = [[12, 17], [400, 405], [2126, 2131], [2136, 2150]]

window.onload = function() {
    var example_element = document.getElementById("example_text");
    // firstExample = getNextExample()
    example_element.innerHTML = generateExampleHTML(example1entities, example1text);

    document.getElementById("example_text2").innerHTML = generateExampleHTML(example2entities, example2text);
}

//entities is array of ORDERED character indexes (start-inclusive, end-exclusive)
function generateExampleHTML(entities, text) {
    sentiments = Array(entities.length).fill("n");
    var html = text;
    var offset = 0;
    for(var entity of entities) {
        var startIndex = entity[0];
        var endIndex = entity[1];
        var entityName = text.slice(startIndex, endIndex);
        var id_string = e_id.toString();
        var replacementHTML = "<div class='dropdown'><span id=" + id_string + " class='none-highlight'>" + entityName + "</span><div class='dropdown-content'><button class='sentiment-button negative' onclick='sentimentSelected(-1," + id_string + ")'>-1</button><button class='sentiment-button neutral' onclick='sentimentSelected(0," + id_string + ")'>0</button><button class='sentiment-button positive' onclick='sentimentSelected(1," + id_string + ")'>1</button></div></div>";
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
            markElement.className = "negative-highlight";
            break;
        case 0:
            markElement.className = "neutral-highlight";
            break;
        case 1:
            markElement.className = "positive-highlight";
            break;
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