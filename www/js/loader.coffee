$j = jQuery

$j.getScript "js/initiative.js"
$j.getScript "js/dicebox.js"
$j.getScript "js/chatbox.js", ->
  window.ws.send "get_state()"
