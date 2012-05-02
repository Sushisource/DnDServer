$j = jQuery

boxarena = $j '#boxarena'

$j ->
  $j.dnd.callbacks['showstoreable'] = (renderme) ->
    console.log(renderme)
    boxarena.append(renderme)