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
    hp: hpin.val(),
    callback: 'setup_char'
    template: "storeable_character.mako"}
    $j.dnd.send "add_storeable", data
    modal.modal('toggle')
    return false

  atkform.submit ->
    name = atkname.val()
    subdict = {}
    subdict[name] = atkcmd.val().trim()
    $j.dnd.updatestoreable(atkid.html(), subdict, 'attack')
    atkmodal.modal('toggle')
    return false

updatehp = (pass, text, orig) ->
  id = $j(this).attr('idnum')
  data = {hp: text}
  $j.dnd.updatestoreable(id, data)
  return text

setupchar = (charid) ->
  hp = $j("#char_hp_#{charid}")
  hp.attr('idnum', charid)

  $j("#char_hp_#{charid}").editInPlace({
    default_text: hp.html()
    callback: updatehp,
    element_id: charid,
    bg_over: '#3A87AD',
    bg_out: hp.css('background-color')})

  $j("#char_addatk_#{charid}").click ->
    atkname.val ""
    atkcmd.val ""
    atkid.html charid
    atkmodal.modal('toggle')

$j.dnd.editAttack = (m_atkid, name, cmd) ->
  atkname.val name
  atkcmd.val cmd
  atkid.html m_atkid
  atkmodal.modal 'toggle'

$j.dnd.doAttack = (name,cmd,wielder) ->
  $j.dnd.userchat("#{wielder} is attacking with #{name}!")
  $j.dnd.diceroll(cmd)

$j.dnd.callbacks['setup_char'] = setupchar