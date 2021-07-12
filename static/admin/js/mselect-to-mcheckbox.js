// create a copy of the original function used by django to add the realted field
var dismissAddAnotherPopupCopy = Function("win", "newId", "newRepr", 'return ' + dismissAddAnotherPopup.toString())();

(function($) {

  // overwrite the original function used by django to add the realted field
  dismissAddAnotherPopup = function dismissAddAnotherPopup(win, newId, newRepr) {
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById('mcheckbox-' + name);
    // if the field was a multiple checkbox 
    if(elem) {
      $(
            '<tr>'
          + '<td><label for="' + name +'_' + newId + '" class="mcheckbox-label">' + newRepr + '</td>'
          + '<td><input type="checkbox" id="' + name.replace(/^id_/, '') + '_' + newId + '" name="' + name.replace(/^id_/, '') +'" value="' + newId + '" checked="checked" /></td>'
          + '</tr>'
        ).appendTo(elem);

      win.close();
    }
    // else call the default function previously copied
    else {
      dismissAddAnotherPopupCopy(win, newId, newRepr);
    }
  }

  // convert a multiple select in a multiple checkbox
  var mselectTOmcheckbox = function mselectTOmcheckbox(selector) {

    var elements = $(selector);

    elements.each(function(index, item) {
      var id = $(item).attr('id'),
          name = $(item).attr('name'),
          options = $(item).children();

      var mcheckbox_table = $('<table/>', {
        id: 'mcheckbox-' + id,
        className: 'mcheckbox-table'
      }).appendTo(
        mcheckbox_container = $('<div/>', {
            className: 'mcheckbox-container'
        })
      );

      options.each(function(index, option) {
        var value = $(option).attr('value'),
            label = $(option).text(),
            selected = $(option).attr('selected');

        var checkbox_row = $(
            '<tr>'
          + '<td><label for="' + name +'_' + value + '" class="mcheckbox-label">' + label + '</td>'
          + '<td><input type="checkbox" id="' + name + '_' + value + '" name="' + name +'" value="' + value + '" ' + (selected ? 'checked="checked"' : '') + '/></td>'
          + '</tr>'
        ).appendTo(mcheckbox_table);
      })

      mcheckbox_container.insertAfter(item);

      try {
        mcheckbox_container.resizable({handles: "se"});
      }
      catch(e) {
        // resizing not supported
        console.log('resizing not supported');
      }

      $(item).nextAll('.help').hide();
      $(item).remove();

    })

  };

  // apply the conversion to the desired elements (change the selector)
  $(document).ready(function() {
    mselectTOmcheckbox('select[multiple="multiple"]');
  })
  
    $(document).ready(function() {
    mselectTOmcheckbox('select[id="id_collaboratecareeventrecipientsproperties2_set-1-role_type"]');
  })

})(django.jQuery)