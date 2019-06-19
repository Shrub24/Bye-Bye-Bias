var div = document.createElement("div"); 
var footer_array = document.getElementsByTagName('footer');
if (!footer_array.length == 0) {
	var footer = footer_array[footer_array.length - 1];
	footer.parentNode.insertBefore(div, footer);
}
div.innerText = "test123";