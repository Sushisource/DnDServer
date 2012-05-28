chatbox = $j '#chatbox'
chatinbox = $j '#chat_form'
chatinput = $j '#chat_in'

$j.dnd.post_to_chat = (user, message) ->
  labl = 'label-default'
  if user == $j.dnd.username
    labl ='label-info'
  else if user == 'Chief Ripnugget'
    labl = 'label-success'
  output = """<div class='chatitem row-fluid'><span class='username span1 label #{labl}'>
  #{user}</span><span class='chatmsg offset1 span11 label label-inverse'>#{message}</span></div>"""
  chatbox.prepend(output)
  if chatbox.children().length > 100
    chatbox.children().last().remove()

$j.dnd.userchat = (msg) ->
  $j.dnd.send "userchat", {msg: msg}

sizechat = ->
  pos = chatbox.position()
  chatbox.height($j(window).height() - pos.top - 20)

$j ->
  chatbox.show()
  chatinbox.show()
  $j(window).resize ->
    sizechat()
  sizechat()

  chatinbox.submit ->
    $j.dnd.userchat(chatinput.val())
    chatinput.val ""
    return false

chat = (msg) ->
  $j.dnd.post_to_chat(msg.name, msg.msg)

$j.dnd.callbacks['chat'] = chat