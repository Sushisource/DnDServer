$j = jQuery

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
    window.ws.send "add_inititem('#{name}',#{initv})"
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

add_char = (char) ->
  item = "<li id='#{char.id}' class='hide initchar'><div class='pull-right' style='margin-top:5px;'>"
  item += "<a class='badge badge-inverse' id='init_#{char.id}'>#{char.init}</a>"
  item += """<a id='init_del_#{char.id}' class='btn' href=#
                  style='padding:2px; height:15px; width:15px; margin:0 5px;'>
                  <i class='icon-trash'></i>
                </a></div>"""
  item += "<a href='#'>#{char.name}</a></li>"
  initiativelist.append(item).children(':last').fadeIn(200)
  #Add function handles to buttons / badge
  $j("#init_del_#{char.id}").click ->
    window.ws.send "del_inititem('#{char.name}')"
  $j("#init_#{char.id}").click ->
    change_init char
  sort_initlist()

upd_char = (char) ->
  $j("#init_#{char.id}").html char.init
  sort_initlist()

del_char = (char) ->
  $j("##{char.id}").fadeOut ->
    $j("##{char.id}").remove()

change_init = (char) ->
  charname_input.val char.name
  initiative_input.val $j("#init_#{char.id}").html()
  addmodal.on 'shown', ->
    initiative_input.focus().select()
  addmodal.modal 'toggle'

init_initlist = (chars) ->
  initiativelist.children('.initchar').remove()
  for char, charobj of chars
    add_char(charobj)

$j.dnd.callbacks['initlist'] = init_initlist
$j.dnd.callbacks['addchar'] = add_char
$j.dnd.callbacks['updatechar'] = upd_char
$j.dnd.callbacks['delchar'] = del_char
