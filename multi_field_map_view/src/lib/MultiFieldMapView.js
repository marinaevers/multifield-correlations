import * as d3 from 'd3';

export default class MultiFieldMapViewD3 {
    constructor(el, props) {
        this.props = props;
        this.drawPolygons = this.drawPolygons.bind(this);
        this.update = this.update.bind(this);
        this.updateHighlight = this.updateHighlight.bind(this);

        this.svg = d3.select(el).append('svg')
            .attr("width", props.width)
            .attr("height", props.height);
        this.svg.style("background","url('"+props.path+"') no-repeat");

        this.svg.style("background-size","800px 400px");

        this.drawPolygons();
        const x = d3.scaleLinear()
            .domain([0, this.props.imageWidth])
            .range([0, this.props.width]);

        const y = d3.scaleLinear()
            .domain([this.props.imageHeight, 0])
            .range([0, this.props.height]);

        const width = this.props.imageWidth;

        var points = d3.range(this.props.imageWidth * this.props.imageHeight).map(function(d) {
            var x = d % width;
            var y = Math.floor(d / width);
            return [x, y];
        });

        const circles = this.svg.selectAll("circle")
            .data(points)
            .enter()
            .append("circle")
            .attr("class", "pixel")
            .attr("cx", function(d) { return x(d[0]); })
            .attr("cy", function(d) { return y(d[1]); })
            .attr("id", function(d) { return d; })
            .attr("r", 0.0);

        // lasso selection based on the drag events
        let coords = [];
        const lineGenerator = d3.line();

        const svg = this.svg;

        const pointInPolygon = function (point, vs) {
            // console.log(point, vs);
            // ray-casting algorithm based on
            // https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html/pnpoly.html

            var x = point[0],
                y = point[1];

            var inside = false;
            for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
                var xi = vs[i][0],
                    yi = vs[i][1];
                var xj = vs[j][0],
                    yj = vs[j][1];

                var intersect =
                    yi > y !== yj > y &&
                    x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
                if (intersect) {inside = !inside;}
            }

            return inside;
        };

        function drawPath() {
            d3.select("#lasso")
                .style("stroke", "black")
                .style("stroke-width", 2)
                .style("fill", "rgba(0,0,0,0.07)")
                .attr("d", lineGenerator(coords));
        }

        function dragStart() {
            coords = [];
            circles.attr("fill", "steelblue");
            d3.select("#lasso").remove();
            svg
                .append("path")
                .attr("id", "lasso");
        }

        function dragMove(event) {
            const mouseX = event.sourceEvent.offsetX;
            const mouseY = event.sourceEvent.offsetY;
            coords.push([mouseX, mouseY]);
            drawPath();
        }

        function dragEnd() {
            const selectedDots = [];
            circles.each((d, i) => {
                const point = [
                    x(d[0]),
                    y(d[1]),
                ];
                if (pointInPolygon(point, coords)) {
                    //selectedDots.push("["+d[0]+","+d[1]+"]");
                    selectedDots.push(d);
                }
            });
            props.setProps({selection:selectedDots});
        }

        const drag = d3
            .drag()
            .on("start", dragStart)
            .on("drag", dragMove)
            .on("end", dragEnd);

        this.svg.call(drag);

        // Introduce Zoom
        const zoom = d3.zoom()
            .on('zoom', handleZoom);


        function handleZoom(e) {
            svg
                .attr('transform', e.transform)
        }
        this.svg.call(zoom);
    }

    drawPolygons() {
        const props = this.props
        const x = d3.scaleLinear()
            .domain([0, this.props.imageWidth])
            .range([0, this.props.width]);

        const y = d3.scaleLinear()
            .domain([this.props.imageHeight, 0])
            .range([0, this.props.height]);

        this.svg.selectAll('polygons')
            .data(this.props.polygons)
            .enter()
            .append('polygon')
            //.attr('class', 'polygon')
            .attr('points', function(d) {
                return d.points.map((p) => [x(p[0]), y(p[1])]);
            })
            .attr('stroke', function(d) {
                return props.colormap[d.field];
            })
            .attr('stroke-width', 3)
            .attr('fill', 'none')
            .attr('class', d => {console.log("polygon." + d.field + "-" + d.segID); return d.field + "-" + d.segID;});
    }

    update(props) {
        this.props = props;
        this.svg.selectAll('polygon').remove();
        this.drawPolygons();
    }

    updateHighlight(props) {
        this.svg.selectAll("polygon")
            .attr("fill", 'none');
        for (const seg of props.highlighted) {
            this.svg.selectAll(seg)
                .attr("fill", "rgba(152,152,152,0.5)");
        }
    }
}