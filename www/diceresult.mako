Rolls ${query}:</br>
 ${total}
% for graph in graphs:
    <svg id="g${graph['id']}" class="dicebar"></svg><br>
    <script type="text/javascript">
        (function() {
        var data = ${graph['rolls']};
        var a=d3.max(data),d=d3.min([10,a]),b=d3.scale.linear().domain([0,a]).range([0,100]),e=d3.scale.ordinal().domain(d3.range(0,data.length)).rangeRoundBands([0,405]),a=d3.select("#g${graph['id']}"),a=a.append("g").attr("transform","translate(10,10)"),f=405/data.length-2;a.selectAll("line").data(b.ticks(d)).enter().append("line").attr("y1",function(c){return-1*b(c)+100}).attr("y2",function(c){return-1*b(c)+100}).attr("x1",-10).attr("x2",420);a.selectAll("rect").data(data).enter().append("rect").attr("width",
        f).attr("y",function(){return 100}).attr("x",function(c,a){return e(a)}).attr("height",0).transition().delay(function(c,a){return 800*(a/data.length)}).duration(800).ease(d3.ease("exp-in-out")).attr("y",function(c){return 100-b(c)}).attr("height",b);20>=data.length&&a.selectAll("text").data(data).enter().append("text").attr("x",function(c,a){return e(a)}).attr("y",95).attr("dx",3).text(function(a,b){return 0==a?"":(b+1).toString()});a.selectAll(".rule").data(b.ticks(d)).enter().append("text").attr("class",
        "rule").attr("x",-10).attr("y",function(a){return-1*b(a)+100}).attr("text-anchor","right").text(function(a){return a.toString()})}).call(this);
    </script>
% endfor