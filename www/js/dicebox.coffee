chat = $j "#chat_in"

$j.dnd.pubdiceroll = (result) ->
  $j.dnd.post_to_chat(result.name, result.result)

$j.dnd.diceroll = (roll) ->
  chat.val "/d " + roll
  chat.submit()

$j.dnd.fancydice = (data) ->


$j.dnd.callbacks['diceroll'] = $j.dnd.pubdiceroll