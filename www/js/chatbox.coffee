$j = jQuery

chatbox = $j '#chatbox'

$j.dnd.post_to_chat = (user, message) ->
  labl = 'label-success'
  if user == $j.dnd.username
    labl ='label-info'
  else if user == 'Chief Ripnugget'
    labl = 'label-warning'
  output = """<div class='chatitem row-fluid'><span class='username span1 label #{labl}'>
  #{user}</span><span class='chatmsg offset1 span11 label label-inverse'>#{message}</span></div>"""
  chatbox.prepend(output)
  if chatbox.children().length > 100
    chatbox.children().last().remove()

sizechat = ->
  pos = chatbox.position()
  chatbox.height($j(window).height() - pos.top - 20)

$j ->
  chatbox.show()
  $j(window).resize ->
    sizechat()
  sizechat()

chat = (msg) ->
  $j.dnd.post_to_chat(msg.name, msg.msg)

$j.dnd.callbacks['chat'] = chat
