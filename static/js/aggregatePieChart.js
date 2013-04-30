getData().done(drawGraph);
var symptoms, svg;

function drawGraph (data) {
  // based on http://bl.ocks.org/mbostock/3887235
  symptoms = d3.entries(data);

  var width = 500,
      height = 400,
      radius = Math.min(width, height) / 2;

  var color = d3.scale.category20();

  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(0);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function (d) { return d.value; });

  svg = d3.select(".chart").append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var g = svg.selectAll(".arc")
      .data(pie(symptoms))
    .enter().append("g")
      .attr("class", "arc");

  g.append("path")
      .attr("d", arc)
      .style("fill", function(d) { return color(d.data.key); });

   svg.selectAll(".arc")
     .append("text")
     .attr("transform", function(d) {
        return "translate(" + arc.centroid(d) + ") rotate(" + convertRadiansToDegrees(d) + ")";
      })
     .attr("dy", ".35em")
     .attr("text-anchor", "middle")
     .text(function(d) {
        return d.data.key;
      });
}

function convertRadiansToDegrees(d) {
  var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
  return a > 90 ? a - 180 : a;
}

function getData () {
  var filter = {},
      startDate = $('input[name="start_date"]').val(),
      endDate = $('input[name="end_date"]').val();
  if (startDate !== "") { filter.start_date = startDate; }
  if (endDate !== "") { filter.end_date = endDate; }

  var symptomsData = $.getJSON('/symptoms', filter);
  return symptomsData;
}