$j = jQuery

newcharform = $j '#addchar_m_form'
newcharbtn = $j '#newchar_btn'
modal = $j '#addchar_modal'
charname = $j '#addchar_m_name'
hpin = $j '#addchar_m_hp'

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
    if atkname.val() == ""
      atkname.focus().select()
    else
      atkcmd.focus().select()

  newcharbtn.click ->
    charname.val ""
    modal.modal('toggle')

  newcharform.submit ->
    data = {'name': charname.val(),
    'hp': hpin.val(),
    'callback': 'setup_char'}
    template = "storeable_character.mako"
    data = JSON.stringify(data)
    window.ws.send("add_storeable('#{template}','#{data}')")
    modal.modal('toggle')
    return false

  atkform.submit ->
    name = atkname.val()
    data = {}
    data[name] = atkcmd.val().trim()
    data = JSON.stringify(data)
    window.ws.send("update_storeable('#{atkid.html()}','#{data}','attack')")
    atkmodal.modal('toggle')
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
    default_text: hp.html()
    callback: updatehp,
    element_id: id,
    bg_over: '#3A87AD',
    bg_out: hp.css('background-color')})

  $j("#char_addatk_#{id}").click ->
    atkname.val ""
    atkcmd.val ""
    atkid.html id
    atkmodal.modal('toggle')

$j.dnd.editAttack = (id, name, cmd) ->
  atkname.val name
  atkcmd.val cmd
  atkid.html id
  atkmodal.modal 'toggle'

$j.dnd.doAttack = (name,cmd,wielder) ->
  $j.dnd.post_to_chat(wielder, "I'm attacking with #{name}!")
  $j.dnd.diceroll(cmd)

$j.dnd.callbacks['setup_char'] = setupchar
