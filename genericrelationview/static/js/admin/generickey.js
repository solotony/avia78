var script = document.createElement('script');
script.src = 'http://code.jquery.com/jquery-1.11.0.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

django.jQuery(function(jQuery){

  window.generic_view_json = function(self,url,selector, content_type){
    var init = jQuery(self).data("init");
    var contentID = self.id;
    var paramContenID = contentID.replace("id_","").replace("content_type","")
    var objectID = "id_" + paramContenID + selector;
    var id = self.value;

    var x_drop = jQuery("#"+objectID);
    var value = null;
    if( init != null ){
      if( init['id'] == id ){
        value = init['value'];
      }
    } else {
      value = x_drop.val();
      jQuery(self).data("init",{id:id,value:value});
    }

    var x_select = x_drop;

    if( !x_select.is("select")){
      x_select = jQuery("<select/>").attr({
        id : objectID,
        name : x_drop.attr('name')
      }).addClass("rel-generic");
      x_drop.replaceWith(x_select);
    }

    x_select.html('<option value="">---------</option>');
//    if( id != "" ){
      var path = url + "?id=" + id;
      jQuery.getJSON(path,function(data){
        for( var i=0; i<data.length;++i){
          var item = data[i];
          var val = item['pk'];
          var title = item['fields']['title'];
          var option = jQuery("<option/>").val(val).text(title);
          if( value == val ){
            option.attr('selected','selected');
          }
          x_select.append(option);
        }
        x_select.parents("fieldset:first").trigger("generickey_update");
      });
//      }
  };

  jQuery(document).ready(function(){
    jQuery('.generic_view').change();
  });
});
