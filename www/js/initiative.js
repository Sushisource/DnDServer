// Generated by CoffeeScript 1.3.1
(function() {
  var $j, add_char, addchar, addchar_form, addmodal, change_init, charname_input, del_char, init_initlist, initadd, initiative_input, initiativelist, m_add_char, sort_initlist, upd_char;

  $j = jQuery;

  initadd = $j('#init_add');

  addmodal = $j('#addchar');

  addchar = $j('#addchar_add');

  addchar_form = $j('#addchar_form');

  charname_input = $j('#charname');

  initiative_input = $j('#initiative');

  initiativelist = $j('#initiativelist');

  $j(function() {
    initadd.click(function() {
      return addmodal.modal('toggle');
    });
    addmodal.modal({
      keyboard: false,
      show: false
    });
    $j('#addchar input').bind('keypress', function(e) {
      if ((e.keyCode || e.which) === 13) {
        return addchar_form.submit();
      }
    });
    addchar.click(function() {
      return addchar_form.submit();
    });
    return addchar_form.submit(function() {
      var initv;
      initv = initiative_input.val();
      if (isNaN(initv) || initv === null || initv === "") {
        alert("Initiative must be a number");
        return false;
      }
      window.ws.send("add_char('" + (charname_input.val()) + "'," + initv + ")");
      addmodal.modal('toggle');
      return false;
    });
  });

  sort_initlist = function() {
    var listitems;
    listitems = initiativelist.children('.initchar').get();
    listitems.sort(function(ia, ib) {
      var a, b;
      a = parseInt($j($j(ia).find('.badge')[0]).html());
      b = parseInt($j($j(ib).find('.badge')[0]).html());
      if (a > b) {
        return 1;
      } else if (a < b) {
        return -1;
      } else {
        return 0;
      }
    });
    return $j.each(listitems, function() {
      return initiativelist.append(listitems);
    });
  };

  m_add_char = function(char, init) {
    var item;
    item = "<li id='" + char + "' class='hide initchar'><div class='pull-right' style='margin-top:5px;'>";
    item += "<a class='badge badge-inverse' id='init_" + char + "'>" + init + "</a>";
    item += "<a id='init_del_" + char + "' class='btn' href=#\n  style='padding:2px; height:15px; width:15px; margin:0 5px;'>\n  <i class='icon-trash'></i>\n</a></div>";
    item += "<a href='#'>" + char + "</a></li>";
    initiativelist.append(item).children(':last').fadeIn(200);
    $j("#init_del_" + char).click(function() {
      return window.ws.send("del_char('" + char + "')");
    });
    return $j("#init_" + char).click(function() {
      return change_init(char);
    });
  };

  add_char = function(char) {
    m_add_char(char.name, char.init);
    return sort_initlist();
  };

  upd_char = function(char) {
    $j("#init_" + char.name).html(char.init);
    return 0;
  };

  del_char = function(char) {
    return $j("#" + char).fadeOut(function() {
      return $j("#" + char).remove();
    });
  };

  change_init = function(char) {
    charname_input.val(char);
    initiative_input.val($j("#init_" + char).html());
    addmodal.modal('toggle');
    return document.getElementById('initiative').focus();
  };

  init_initlist = function(chars) {
    var char, init;
    initiativelist.children('.initchar').remove();
    for (char in chars) {
      init = chars[char];
      m_add_char(char, init);
    }
    return sort_initlist();
  };

  $j.dnd.callbacks['initlist'] = init_initlist;

  $j.dnd.callbacks['addchar'] = add_char;

  $j.dnd.callbacks['updatechar'] = upd_char;

  $j.dnd.callbacks['delchar'] = del_char;

}).call(this);
