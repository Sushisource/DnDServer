$j = jQuery

chat = $j "#chat_in"

diceroll = (result) ->
  $j.dnd.post_to_chat(result.name, result.result)

$j.dnd.diceroll = (roll) ->
  chat.val "/d " + roll
  chat.submit()

$j.dnd.callbacks['diceroll'] = diceroll