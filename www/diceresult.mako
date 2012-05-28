Rolls ${query}:</br>
% if onedie['draw']:
    <svg id="diegram_1d${onedie['sides']}" class="diegram"></svg>
    <script type="text/javascript">
    (function() {
        var total = ${total}.0;
        var sides = ${onedie['sides']}.0;
        var radius = 100 * 0.4;
        var id = "diegram_1d"+sides;
        //Setup middle as (0,0) start offscreen
        var gr = d3.select("#"+id).append("g")
                .attr("transform","translate(50,50)").append("g")
                .attr("transform",'translate(-100,-200)rotate(180)');
        //Add drawing
        var pathstr = "M";
        for(var i in d3.range(0,sides)) {
            var vx = radius*Math.cos(2*i*Math.PI/sides);
            var vy = radius*Math.sin(2*i*Math.PI/sides);
            pathstr += vx + " " + vy + "L"
        }
        pathstr = pathstr.slice(0,-1) + "z";
        console.log(pathstr);
        var colorstr = "rgba(0,200,250,"+total/sides+")";
        if(total == sides) {
            colorstr = "rgb(0,200,0)";
        }
        else if (total == 1) {
            colorstr = "rgb(200,0,0)";
        }
        gr.append("path").attr("d",pathstr).attr("fill",colorstr);
        //Add text
        gr.append("text").attr('x',0).attr('y',6)
            .attr("text-anchor","middle").text(total);
        //Roll in
        gr.transition()
            .duration(1000)
            .attr("transform","rotate(0)");
    }).call(this);
    </script>
%else:
<h4>${total}</h4>
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
% endif

