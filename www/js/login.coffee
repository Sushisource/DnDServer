loginbox = $j '#login_form'
loginput = $j '#uname'
logbtn = $j '#login_okbtn'
userlabel = $j '#user_label'
$j.dnd.username = "Chief Ripnugget"

$j.dnd.send = (fn, params = {}) ->
  data = {fn: fn, data: params}
  window.ws.send(JSON.stringify(data))

$j ->
  logbtn.click ->
    loginbox.submit()

  loginbox.submit ->
    name = loginput.val().trim()
    $j.dnd.send "add_user", {name: name}
    return false

usr_response = (msg) ->
  $j.dnd.username = msg.name
  userlabel.html $j.dnd.username
  userlabel.show()
  loginbox.fadeOut ->
    loginbox.remove()
    $j.dnd.callbacks['ouser_response'] = otheruser_response
    $j.getScript "js/loader.js"

otheruser_response = (msg) ->
  name = msg.name
  if name is $j.dnd.username
    return
  id = msg.id
  if $j("#ouser_label_#{id}").length != 0
    return
  userlabel.after """
  <span class='label label-success'
                id='ouser_label_#{id}' style='vertical-align: bottom'>#{name}</span>"""

deluser = (id) ->
  $j("#ouser_label_#{id}").remove()

loginput.focus().select()
$j.dnd.callbacks['user_response'] = usr_response
$j.dnd.callbacks['deluser'] = deluser