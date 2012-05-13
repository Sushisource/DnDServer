$j = jQuery

dicebox = $j '#dice_form'
diceinput = $j '#dice_in'
dicebtn = $j '#dice_okbtn'

$j ->
  dicebox.show()

  dicebtn.click ->
    dicebox.submit()

  dicebox.submit ->
    instr = diceinput.val().trim()
    $j.dnd.send "dicebox", {rollstr: instr}
    return false

diceroll = (result) ->
  $j.dnd.post_to_chat(result.name, result.result)

$j.dnd.diceroll = (roll) ->
  diceinput.val roll
  dicebtn.click()

$j.dnd.callbacks['diceroll'] = diceroll