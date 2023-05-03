import * as d3 from 'd3'
export default class CorrelationHeatmapD3 {
    constructor(el, props) {
        this.props = props;
        this.update = this.update.bind(this);
        this.drawHeatmap = this.drawHeatmap.bind(this);

        this.svg = d3.select(el).append('svg')
            .attr("width", props.width+3*props.margin)
            .attr("height", props.height+2*props.margin)
            .append("g")
            .attr("transform", "translate(" + props.margin + "," + props.margin + ")");

        this.drawHeatmap();
    }

    drawHeatmap() {
        // Axes heatmap
        const x = d3.scaleBand()
            .range([0, this.props.width])
            .domain(this.props.segmentIDs)
            .padding(0.01);
        const y = d3.scaleBand()
            .range([0, this.props.height])
            .domain(this.props.segmentIDs.reverse())
            .padding(0.01);

        // Add axes
        const tickwidth = this.props.width/this.props.segmentIDs.length
        this.svg.append("g")
            .attr("transform", "translate(0, " + this.props.height + ")")
            .call(d3.axisBottom(x))
            .selectAll(".tick")
            .data(this.props.segmentIDs.reverse())
            .append("rect")
            .attr("width", tickwidth)
            .attr("height", 5)
            .attr("transform", "translate(" + (-0.5)*tickwidth + ", 0)")
            .attr("fill", d => this.props.cmap[d.substring(0, d.indexOf(' '))])

        const tickheight = this.props.height/this.props.segmentIDs.length
        this.svg.append("g")
            .call(d3.axisLeft(y))
            .selectAll(".tick")
            .data(this.props.segmentIDs.reverse())
            .append("rect")
            .attr("width", 5)
            .attr("height", tickheight)
            .attr("transform", "translate(-5, " + (-0.5)*tickheight + ")")
            .attr("fill", d => this.props.cmap[d.substring(0, d.indexOf(' '))])

        this.svg.selectAll(".tick text")
            .attr("font-size", 0);

        // Introduce Zoom
        const zoom = d3.zoom()
            .on('zoom', handleZoom);


        const svg = this.svg;
        function handleZoom(e) {
            svg
                .attr('transform', e.transform)
        }

        // Build color scale
        const myColor = d3.scaleSequential(d3.interpolateRdBu)
            .domain([1, -1]);

        function kde(kernel, thresholds, data) {
            return thresholds.map(t => [t, d3.mean(data, d => kernel(t - d))]);
        }

        function epanechnikov(bandwidth) {
            return x => Math.abs(x /= bandwidth) <= 1 ? 0.75 * (1 - x * x) / bandwidth : 0;
        }

        // TODO: Select suitable value
        const bandwidth = 0.05;

        const props = this.props;

        // draw heatmap
        this.svg.selectAll()
            .data(this.props.data, function(d) {return d.id1+":"+d.id2})
            .enter()
            .append("rect")
            .attr("x", function(d) {return x(d.id1)})
            .attr("y", function(d) {return y(d.id2)})
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .style("fill", function(d) {return myColor(d.total)})
            .attr("opacity", 0.5)
            .on('mouseover', function (d, i) {
                d3.select(this).transition()
                    .duration('50').attr('opacity', '.85');
                props.setProps({hoverData:[i.id1, i.id2]})
            })
            .on('mouseout', function (d, i) {
                d3.select(this).transition()
                    .duration('50').attr('opacity', '.5')});
        if(this.props.showDistribution) {
            for (const i in this.props.data) {
                const d = this.props.data[i];
                const xDens = d3.scaleLinear()
                    .range([x(d.id1), x(d.id1) + x.bandwidth()])
                    .domain([-1, 1]);
                const thresholds = xDens.ticks(50);
                const densities = kde(epanechnikov(bandwidth), thresholds, d.correlations);
                const yDens = d3.scaleLinear()
                    .range([y(d.id2), y(d.id2) + y.bandwidth()])
                    .domain([10, 0]); //d.correlations.length*0.75
                const line = d3.line()
                    .curve(d3.curveBasis)
                    .x(xd => xDens(xd[0]))
                    .y(yd => yDens(yd[1]));
                this.svg
                    .append("path")
                    .datum(densities)
                    .attr("fill", "none")
                    .attr("stroke", "#000")
                    .attr("stroke-width", 1.5)
                    .attr("stroke-linejoin", "round")
                    .attr("d", line);
            }
        }

        // Color bar
        const legendProps = {
            title: this.props.colorBarTitle, tickSize: 6, width: 30, height: this.props.height,// + tickSize,
            marginTop: 0, marginRight: 0, marginBottom: 0,// + tickSize,
            marginLeft: 3, ticks: this.props.width / 64
        };

        function ramp(color, n = 256) {
            const canvas = document.createElement("canvas");
            canvas.width = 1;
            canvas.height = n;
            const context = canvas.getContext("2d");
            for (let i = 0; i < n; ++i) {
                context.fillStyle = color(i / (n - 1));
                context.fillRect(0, /*n - 1 - i, 1*/i,1, 1);
            }
            return canvas;
        }

        const n = Math.min(myColor.domain().length, myColor.range().length);
        const xColorScale = myColor.copy().rangeRound(d3.quantize(d3.interpolate(legendProps.marginTop, legendProps.height - legendProps.marginBottom), n));
        this.svg.append("image")
            .attr("x", this.props.width + legendProps.marginLeft)
            .attr("y", legendProps.marginTop)
            .attr("width", legendProps.width - legendProps.marginLeft - legendProps.marginRight)
            .attr("height", legendProps.height - legendProps.marginTop - legendProps.marginBottom)
            .attr("preserveAspectRatio", "none")
            .attr("xlink:href", ramp(myColor.copy().domain(d3.quantize(d3.interpolate(0, 1), n))).toDataURL())
            .style("opacity", 0.5);
        this.legendTitle = this.svg.append("g")
            .style("font", this.props.fontSize + "px times")
            .attr("transform", 'translate(' + (this.props.width+legendProps.width) + ',0)') // myColor + legendProps.width
            .call(d3.axisRight(xColorScale))
            .call(g => g.select(".domain").remove())
            .append("text")
            .attr("x", -legendProps.width + legendProps.marginLeft)
            .attr("y", -5)
            .attr("fill", "black")
            .attr("text-anchor", "start")
            .attr("font-size", this.props.fontSize)
            .text(legendProps.title);

        this.svg.call(zoom);
    }

    update(props) {
        this.props = props;
        this.svg.selectAll('*').remove();
        this.drawHeatmap();
    }
}