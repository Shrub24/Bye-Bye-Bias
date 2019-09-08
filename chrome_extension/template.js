var precompiledTemplateCard = {"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
  var stack1;

return "         <a href=\""
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.URL : depth0), depth0))
  + "\">\n            <div class=\"card\"  title=\""
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Title : depth0), depth0))
  + "\">\n            <div class=\"title\">"
  + ((stack1 = container.lambda((depth0 != null ? depth0.truncatedTitle : depth0), depth0)) != null ? stack1 : "")
  + "</div>\n            <div class=\"date\">"
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Date : depth0), depth0))
  + "</div>\n            <div class=\"info\">\n               <!--\n                  <object type=\"image/svg+xml\" data=\"./info_icon.svg\" class=\"info-icon\"></object>\n                  <object type=\"image/svg+xml\" data=\"./head_icon.svg\" class=\"info-icon\"></object>\n               -->\n               <div class=\"publisher\">Publisher: "
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Publisher : depth0), depth0))
  + "</div>\n               <div class=\"author\">Author: "
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Author : depth0), depth0))
  + "</div>\n            </div>\n            </div>\n         </a>";
},"useData":true}