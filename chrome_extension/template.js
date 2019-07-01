var precompiledTemplateCard = {"1":function(container,depth0,helpers,partials,data) {
  var stack1, helper;

return "         <a href=\""
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.URL : depth0), depth0))
  + "\">\n            <div class=\"card\" style=\"background-color: "
  + container.escapeExpression(((helper = (helper = helpers.Color || (depth0 != null ? depth0.Color : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : {},{"name":"Color","hash":{},"data":data}) : helper)))
  + "\" title=\""
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Title : depth0), depth0))
  + "\">\n            <div class=\"title\">"
  + ((stack1 = container.lambda((depth0 != null ? depth0.truncatedTitle : depth0), depth0)) != null ? stack1 : "")
  + "</div>\n            <div class=\"date\">"
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Date : depth0), depth0))
  + "</div>\n            <div class=\"info\">\n               <object type=\"image/svg+xml\" data=\"./info_icon.svg\" class=\"info-icon\"></object>\n               <div class=\"publisher\">"
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Publisher : depth0), depth0))
  + "</div>\n               <object type=\"image/svg+xml\" data=\"./head_icon.svg\" class=\"info-icon\"></object>\n               <div class=\"author\">"
  + container.escapeExpression(container.lambda((depth0 != null ? depth0.Author : depth0), depth0))
  + "</div>\n            </div>\n            </div>\n         </a>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
  var stack1;

return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.Cards : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true}