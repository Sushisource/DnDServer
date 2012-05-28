Rolls ${query}:</br>
 ${total}
% for graph in graphs:
    <svg id="g${graph['id']}" class="dicebar"></svg><br>
    <script type="text/javascript">
        var data = ${graph['rolls']};
        var max = d3.max(data);
        var ticks = d3.min([10,max]);
        var y = d3.scale.linear()
            .domain([0, max]).range([0, 100]);
        var x = d3.scale.ordinal()
            .domain(d3.range(0,data.length)).rangeRoundBands([0, 405],.01);
        var gr = d3.select("#g${graph['id']}");
        gr = gr.append("g").attr("transform", "translate(10,10)");
        var wid = 405 / data.length - 2;
        gr.selectAll("line")
            .data(y.ticks(ticks))
            .enter().append("line")
            .attr("y1", function(d) { return -1 * y(d) + 100})
            .attr("y2", function(d) { return -1 * y(d) + 100})
            .attr("x1", -10)
            .attr("x2", 420);
        gr.selectAll("rect")
            .data(data)
          .enter().append("rect")
            .attr("width", wid)
            .attr('y', function(dat) {return 100})
            .attr('x', function(datum, index) {return x(index)})
            .attr("height", 0)
            .transition()
            .duration(750)
            .attr('y', function(dat) {return 100 - y(dat)})
            .attr("height", y);
        if(data.length<=20) //Label sides if die <=d20
        {
            gr.selectAll("text")
                .data(data)
                .enter().append("text")
                .attr('x', function(datum, index) {return x(index);})
                .attr('y', 100 - 5)
                .attr('dx', 3)
                .text(function (datum, index) {
                        if(datum == 0) return "";
                        return (index+1).toString()})
        }
        gr.selectAll(".rule")
                .data(y.ticks(ticks))
                .enter().append("text")
                .attr("class", "rule")
                .attr("x", -10)
                .attr("y", function(d) { return -1 * y(d) + 100})
                .attr("text-anchor", "right")
                .text(function (datum, index) {
                    return (datum).toString()});
    </script>
% endfor