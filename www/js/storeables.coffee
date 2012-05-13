$j = jQuery

boxarena = $j '#boxarena'

$j ->
  $j.dnd.callbacks['showstoreable'] = (renderme) ->
    boxarena.append("<div id='storeable_#{renderme.id}'>#{renderme.output}</div>")

  $j.dnd.callbacks['updatestoreable'] = (renderme) ->
    st = $j("#storeable_#{renderme.id}")
    st.html(renderme.output)

  $j.dnd.updatestoreable = (id, data, subdict='root') ->
    sendme = {id: id, subdict_name:subdict}
    sendme['subdict'] = data
    $j.dnd.send "update_storeable", sendme