$j = jQuery

newcharform = $j '#addchar_m_form'
newcharbtn = $j '#newchar_btn'
modal = $j '#addchar_modal'
charname = $j '#addchar_m_name'
hp = $j '#addchar_m_hp'

atkmodal = $j '#addatk_modal'
atkform = $j '#addatk_m_form'
atkname = $j '#addatk_m_name'
atkcmd = $j '#addatk_m_cmd'
atkbtn = $j '#addatk_m_btn'
atkid = $j '#addatk_m_id'

$j ->
  newcharbtn.show()

  modal.on 'shown', ->
    charname.focus().select()
  atkmodal.on 'shown', ->
    atkname.focus().select()

  newcharbtn.click ->
    charname.val ""
    modal.modal('toggle')

  newcharform.submit ->
    data = {'name': charname.val(),
    'hp': hp.val(),
    'callback': 'setup_char'}
    template = "storeable_character.mako"
    data = JSON.stringify(data)
    window.ws.send("add_storeable('#{template}','#{data}')")
    modal.modal('toggle')
    return false

  atkform.submit ->
    data = {}
    return false

updatehp = (pass, text, orig) ->
  id = $j(this).attr('idnum')
  data = {'hp': text }
  data = JSON.stringify(data)
  window.ws.send("update_storeable('#{id}','#{data}')")
  return text

setupchar = (id) ->
  hp = $j("#char_hp_#{id}")
  hp.attr('idnum', id)

  $j("#char_hp_#{id}").editInPlace({
    callback: updatehp,
    element_id: id,
    bg_over: '#3A87AD',
    bg_out: hp.css('background-color')})

  $j("#char_addatk_#{id}").click ->
    atkname.val ""
    atkcmd.val ""
    atkid.html id
    atkmodal.modal('toggle')

$j.dnd.callbacks['setup_char'] = setupchar
