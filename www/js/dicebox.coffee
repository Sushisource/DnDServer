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
    return if not $j.dnd.validate(instr)
    window.ws.send "dicebox('#{instr}')"
    return false

diceroll = (result) ->
  $j.dnd.post_to_chat(result.name, "Rolls #{result.result}")

$j.dnd.callbacks['diceroll'] = diceroll
