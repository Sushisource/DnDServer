$j = jQuery

initadd = $j '#init_add'
addmodal = $j '#addchar'
addchar = $j '#addchar_add'
addchar_form = $j '#addchar_form'
charname_input = $j '#charname'
initiative_input = $j '#initiative'
initiativelist = $j '#initiativelist'

$j ->
  initadd.click ->
    addmodal.modal('toggle')

  addmodal.modal({
    keyboard: false
    show: false
  })

  $j('#addchar input').bind 'keypress', (e) ->
    if ((e.keyCode || e.which) == 13)
      addchar_form.submit()

  addchar.click ->
    addchar_form.submit()

  addchar_form.submit ->
    initv = initiative_input.val()
    if isNaN(initv) or initv is null or initv is ""
      alert("Initiative must be a number")
      return false
    window.ws.send "add_char('#{charname_input.val()}',#{initv})"
    addmodal.modal('toggle')
    return false

sort_initlist = ->
  listitems = initiativelist.children('.initchar').get()
  listitems.sort (ia, ib) ->
    a = parseInt $j($j(ia).find('.badge')[0]).html()
    b = parseInt $j($j(ib).find('.badge')[0]).html()
    if a > b
      return 1
    else if a < b
      return -1
    else
      return 0
  $j.each listitems, ->
    initiativelist.append listitems

m_add_char = (char, init) ->
  item = "<li id='#{char}' class='hide initchar'><div class='pull-right' style='margin-top:5px;'>"
  item += "<a class='badge badge-inverse' id='init_#{char}'>#{init}</a>"
  item += """<a id='init_del_#{char}' class='btn' href=#
                  style='padding:2px; height:15px; width:15px; margin:0 5px;'>
                  <i class='icon-trash'></i>
                </a></div>"""
  item += "<a href='#'>#{char}</a></li>"
  initiativelist.append(item).children(':last').fadeIn(200)
  #Add function handles to buttons / badge
  $j("#init_del_#{char}").click ->
    window.ws.send "del_char('#{char}')"
  $j("#init_#{char}").click ->
    change_init char

add_char = (char) ->
  m_add_char(char.name, char.init)
  sort_initlist()

upd_char = (char) ->
  $j("#init_#{char.name}").html char.init
  0

del_char = (char) ->
  $j("##{char}").fadeOut ->
    $j("##{char}").remove()

change_init = (char) ->
  charname_input.val char
  initiative_input.val $j("#init_#{char}").html()
  addmodal.modal 'toggle'
  document.getElementById('initiative').focus()

init_initlist = (chars) ->
  initiativelist.children('.initchar').remove()
  for char, init of chars
    m_add_char(char, init)
  sort_initlist()

$j.dnd.callbacks['initlist'] = init_initlist
$j.dnd.callbacks['addchar'] = add_char
$j.dnd.callbacks['updatechar'] = upd_char
$j.dnd.callbacks['delchar'] = del_char
