// Funcions Async
async function compile(code, show_lexer) {
    let result = await eel.parser_coding(code, show_lexer)();
    if(result === 'OK')
        $('#form-result').css({'color': 'green'});
    else if(result === 'Not Code :(')
        $('#form-result').css({'color': 'black'});
    else
        $('#form-result').css({'color': 'red'});
    $('#form-result')[0].value = result;
    get_dom();
}

async function get_dom() {
    let data = await eel.get_dom()();
    root = data[0];
    root.x0 = height / 2;
    root.y0 = 0;
    update(root);
}

var treeData = [];


// ************** Generate the tree diagram	 *****************
var margin = {top: 20, right: 0, bottom: 20, left: 0},
	width = 460,
	height = 500 - margin.top - margin.bottom;

var i = 0,
	duration = 750;

var tree = d3.layout.tree()
	.size([height, width]);

var diagonal = d3.svg.diagonal()
	.projection(function(d) { return [d.x, d.y]; });

var svg = d3.select(".modal-body").append("svg")
	.attr("width", "100%" /*width + margin.right + margin.left*/)
	.attr("height", height + margin.top + margin.bottom)
    .append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var root = [];
root.x0 = height / 2;
root.y0 = 0;

update(root);

d3.select(self.frameElement).style("height", "520px");

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
	  links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 80; d.x = d.x /1.2 });

  // Update the nodes…
  var node = svg.selectAll("g.node")
	  .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
	  .attr("class", "node")
	  .attr("transform", function(d) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
	  .on("click", click);

  nodeEnter.append("circle")
	  .attr("r", 1e-6)
	  .attr("class", "tooltips")
	  .attr("data-placement", "top")
	  .attr("data-original-title", function(d) { return d.name; })
	  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnter.append("text")
	  .attr("x", "-15")
	  .attr("y", function(d) {
	  	return d.children || d._children ? 0 : 25;
	  })
	  .attr("dy", ".35em")
	  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
	  .text(function(d) { return d.name; })
	  .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  nodeUpdate.select("circle")
	  .attr("r", 10)
	  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeUpdate.select("text")
	  .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
	  .duration(duration)
	  .attr("transform", function(d) { return "translate(" + source.x + "," + source.y + ")"; })
	  .remove();

  nodeExit.select("circle")
	  .attr("r", 1e-6);

  nodeExit.select("text")
	  .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
	  .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
	  .attr("class", "link")
	  .attr("d", function(d) {
		var o = {x: source.x0, y: source.y0};
		return diagonal({source: o, target: o});
	  });

  // Transition links to their new position.
  link.transition()
	  .duration(duration)
	  .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
	  .duration(duration)
	  .attr("d", function(d) {
		var o = {x: source.x, y: source.y};
		return diagonal({source: o, target: o});
	  })
	  .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
	d.x0 = d.x;
	d.y0 = d.y;
  });

  nodeEnter.attr("height", function (d) {
      return node.height;
  })
}

// Toggle children on click.
function click(d) {
  if (d.children) {
	d._children = d.children;
	d.children = null;
  } else {
	d.children = d._children;
	d._children = null;
  }
  update(d);
}

// Function Event
$('#button-compile').click(function (e) {
    e.preventDefault();
    // Get cuota and user data
    compile($('#form-code')[0].value, false);
});

$('#button-clear').click(function (e) {
    e.preventDefault();
    // Clear all
    $('#form-result')[0].value = '';
    $('#form-code')[0].value = '';
    root = [];
    root.x0 = height / 2;
    root.y0 = 0;

    update(root);
});
