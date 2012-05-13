$j = jQuery
$j.getScript "js/storeables.js"
$j.getScript "js/initiative.js"
$j.getScript "js/dicebox.js"
$j.getScript "js/charcards.js"
$j.getScript "js/chatbox.js", ->
  $j.dnd.send "get_state"
