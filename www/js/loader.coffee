$j = jQuery

$j.getScript "js/storeables.js"
$j.getScript "js/initiative.js"
$j.getScript "js/dicebox.js"
$j.getScript "js/addchar.js"
$j.getScript "js/chatbox.js", ->
  window.ws.send "get_state()"
