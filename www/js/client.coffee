$j = jQuery
$j.dnd = {}
$j.dnd.callbacks = {}

dispatch = (protocol, data) ->
  func = $j.dnd.callbacks[protocol]
  if typeof func is 'undefined'
    console.log "Undefined callback '" + protocol + "'"
    return;
  func(data)

echo = (message) ->
  console.log message

init_websocket = ->
  #Setup websockets
  window.ws = new WebSocket "ws://192.168.1.10:9000/ws"
  window.ws.onopen = (e) ->
    console.log "Connected"
    $j(".brand").css('color', 'white')
    window.ws.send "get_state()"
  window.ws.onmessage = (e) ->
    dat = JSON.parse(e.data)
    protocol = dat[0]
    data = dat[1]
    console.log "-#{protocol}- \n"
    dispatch(protocol, data)
  window.ws.onclose = (e) ->
    console.log "Lost connection"
    $j(".brand").css('color', 'red')
    #Try to reconnect
    init_websocket()
  window.ws.onerror = (e) ->
    console.log "Error: " + e.message

$j ->
  init_websocket()
  $j.dnd.callbacks['echo'] = echo
