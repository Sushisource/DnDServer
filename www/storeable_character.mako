<div class="storeable well" id="char_${id}">
    <h1>${root['name']}</h1>
    <span class="label label-important pull-right" id="char_hp_${id}">${root['hp']}</span>
    <br/>
    % if 'attack' in data:
    <h3>Attacks:</h3>
    % for name, command in data['attack'].items():
            <div class="clickrow">
                <a onclick="jQuery.dnd.doAttack('${name}','${command}','${root['name']}')"
                   href="#">
                    ${name}:</a>
                <i>${command}</i>
                <a onclick="jQuery.dnd.editAttack(${id},'${name}','${command}')"
                   href="#"
                   class="icon-edit pull-right"></a>
            </div>
    % endfor
    % endif
    <button class="btn btn-mini btn-info pull-right" id="char_addatk_${id}">+atk</button>
</div>