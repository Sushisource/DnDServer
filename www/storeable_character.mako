<div class="storeable well" id="char_${id}">
    <h1>${root['name']}</h1>
    <span class="label label-important pull-right" id="char_hp_${id}">${root['hp']}</span>
    <br/>
    % if 'attacks' in data:
    <h3>Attacks:</h3>
        % for atk in data['attacks']:
                atk
        % endfor
    % endif
    <button class="btn btn-mini btn-info pull-right" id="char_addatk_${id}">+atk</button>
</div>