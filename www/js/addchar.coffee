$j = jQuery

newcharform = $j '#addchar_m_form'
newcharbtn = $j '#newchar_btn'
addnewcharbtn = $j '#addchar_m_btn'
modal = $j '#addchar_modal'
charname = $j '#addchar_m_name'

$j ->
  newcharbtn.show()

  modal.on 'shown', ->
    charname.focus().select()

  newcharbtn.click ->
    charname.val ""
    modal.modal('toggle')

  addnewcharbtn.click ->
    newcharform.submit()

  newcharform.submit ->
    data = {'name': charname.val()}
    template = "storeable_character.mako"
    data = JSON.stringify(data)
    window.ws.send("add_storeable('#{template}','#{data}')")
    modal.modal('toggle')
    return false
