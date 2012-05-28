initadd = $j '#init_add'
addmodal = $j '#addinit_item'
addchar = $j '#addinit_add'
addchar_form = $j '#addinit_form'
charname_input = $j '#initname'
initiative_input = $j '#initiative'
initiativelist = $j '#initiativelist'
well = $j '#initlistwell'

$j ->
  well.show()
  addmodal.on 'shown', ->
    charname_input.focus().select()

  initadd.click ->
    charname_input.val ""
    initiative_input.val ""
    addmodal.modal('toggle')

  $j('#initname, #initiative').bind 'keypress', (e) ->
    if ((e.keyCode || e.which) == 13)
      addchar_form.submit()

  addchar.click ->
    addchar_form.submit()

  addchar_form.submit ->
    name = charname_input.val().trim()
    initv = initiative_input.val()
    if isNaN(initv) or initv is null or initv is ""
      alert("Initiative must be a number")
      return false
    $j.dnd.send "add_inititem", {name: name, initiative: initv}
    addmodal.modal('toggle')
    return false

sort_initlist = ->
  listitems = initiativelist.children('.initchar').get()
  listitems.sort (ia, ib) ->
    a = parseInt $j($j(ia).find('.badge')[0]).html()
    b = parseInt $j($j(ib).find('.badge')[0]).html()
    if a < b
      return 1
    else if a > b
      return -1
    else
      return 0
  $j.each listitems, ->
    initiativelist.append listitems

add_char = (ichar) ->
  item = "<li id='init_i_#{ichar.cid}' class='hide initchar'><div class='pull-right' style='margin-top:5px;'>"
  item += "<a class='badge badge-inverse' id='init_#{ichar.cid}'>#{ichar.init}</a>"
  item += """<a id='init_del_#{ichar.cid}' class='btn' href=#
                  style='padding:2px; height:15px; width:15px; margin:0 5px;'>
                  <i class='icon-trash'></i>
                </a></div>"""
  item += "<a href='#'>#{ichar.name}</a></li>"
  initiativelist.append(item).children(':last').fadeIn(200)
  #Add function handles to buttons / badge
  $j("#init_del_#{ichar.cid}").click ->
    $j.dnd.send "del_inititem", {name: ichar.name}
  $j("#init_#{ichar.cid}").click ->
    change_init ichar
  sort_initlist()

upd_char = (ichar) ->
  $j("#init_#{ichar.cid}").html ichar.init
  sort_initlist()

del_char = (ichar) ->
  $j("#init_i_#{ichar.cid}").fadeOut ->
    $j("#init_i_#{ichar.cid}").remove()

change_init = (ichar) ->
  charname_input.val ichar.name
  initiative_input.val $j("#init_#{ichar.cid}").html()
  addmodal.on 'shown', ->
    initiative_input.focus().select()
  addmodal.modal 'toggle'

init_initlist = (chars) ->
  initiativelist.children('.initchar').remove()
  for ichar, charobj of chars
    add_char(charobj)

$j.dnd.callbacks['initlist'] = init_initlist
$j.dnd.callbacks['addchar'] = add_char
$j.dnd.callbacks['updatechar'] = upd_char
$j.dnd.callbacks['delchar'] = del_char
