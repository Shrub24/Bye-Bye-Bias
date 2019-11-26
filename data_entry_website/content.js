window.onload = function() {
    var example_element = document.getElementById("example_text");
    var entities = ["car", "back"]
    var text = "the car is back"
    example_element.innerHTML = generateExampleHTML(entities, text)
}

function generateExampleHTML(entities, text) {
    // replace with array of character indexes rather than words
    var html = text;
    for(var entity of entities) {
        html = html.replace(new RegExp(entity, "gm"), "<span onmouseover=onHover() onmouseleave=onLeave()><mark>" + entity + "</mark></span>");
    }
    return html;
}

function onHover() {
    console.log("hovered")
}

function onLeave() {
    console.log("left")
}