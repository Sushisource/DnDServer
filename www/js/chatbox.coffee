$j = jQuery

chatbox = $j '#chatbox'

$j.dnd.post_to_chat = (user, message) ->
  labl = 'label-success'
  if user == $j.dnd.username
    labl ='label-info'
  output = """<div class='chatitem row-fluid'><span class='username span1 label #{labl}'>
  #{user}</span><span class='chatmsg offset1 span11 label label-inverse'>#{message}</span></div>"""
  chatbox.prepend(output)
  if chatbox.children().length > 100
    chatbox.children().last().remove()

$j ->
  chatbox.show()

chat = (msg) ->
  $j.dnd.post_to_chat(msg.name, msg.msg)

$j.dnd.callbacks['chat'] = chat
