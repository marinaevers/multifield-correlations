webpackHotUpdatecorrelation_heatmap("main",{

/***/ "./src/lib/components/CorrelationHeatmap.js":
/*!**************************************************!*\
  !*** ./src/lib/components/CorrelationHeatmap.js ***!
  \**************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return CorrelationHeatmapD3; });
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! d3 */ "./node_modules/d3/src/index.js");
function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }

var CorrelationHeatmapD3 = /*#__PURE__*/function () {
  function CorrelationHeatmapD3(el, props) {
    _classCallCheck(this, CorrelationHeatmapD3);
    this.props = props;
    this.update = this.update.bind(this);
    this.drawHeatmap = this.drawHeatmap.bind(this);
    this.svg = d3__WEBPACK_IMPORTED_MODULE_0__["select"](el).append('svg').attr("width", props.width + 3 * props.margin).attr("height", props.height + 2 * props.margin).append("g").attr("transform", "translate(" + props.margin + "," + props.margin + ")");
    this.drawHeatmap();
  }
  _createClass(CorrelationHeatmapD3, [{
    key: "drawHeatmap",
    value: function drawHeatmap() {
      var _this = this;
      // Axes heatmap
      var x = d3__WEBPACK_IMPORTED_MODULE_0__["scaleBand"]().range([0, this.props.width]).domain(this.props.segmentIDs).padding(0.01);
      var y = d3__WEBPACK_IMPORTED_MODULE_0__["scaleBand"]().range([0, this.props.height]).domain(this.props.segmentIDs.reverse()).padding(0.01);

      // Add axes
      var tickwidth = this.props.width / this.props.segmentIDs.length;
      this.svg.append("g").attr("transform", "translate(0, " + this.props.height + ")").call(d3__WEBPACK_IMPORTED_MODULE_0__["axisBottom"](x)).selectAll(".tick").data(this.props.segmentIDs.reverse()).append("rect").attr("width", tickwidth).attr("height", 5).attr("transform", "translate(" + -0.5 * tickwidth + ", 0)").attr("fill", function (d) {
        return _this.props.cmap[d.substring(0, d.indexOf(' '))];
      });
      var tickheight = this.props.height / this.props.segmentIDs.length;
      this.svg.append("g").call(d3__WEBPACK_IMPORTED_MODULE_0__["axisLeft"](y)).selectAll(".tick").data(this.props.segmentIDs.reverse()).append("rect").attr("width", 5).attr("height", tickheight).attr("transform", "translate(-5, " + -0.5 * tickheight + ")").attr("fill", function (d) {
        return _this.props.cmap[d.substring(0, d.indexOf(' '))];
      });
      this.svg.selectAll(".tick text").attr("font-size", 0);

      // Build color scale
      var myColor = d3__WEBPACK_IMPORTED_MODULE_0__["scaleSequential"](d3__WEBPACK_IMPORTED_MODULE_0__["interpolateRdBu"]).domain([1, -1]);
      function kde(kernel, thresholds, data) {
        return thresholds.map(function (t) {
          return [t, d3__WEBPACK_IMPORTED_MODULE_0__["mean"](data, function (d) {
            return kernel(t - d);
          })];
        });
      }
      function epanechnikov(bandwidth) {
        return function (x) {
          return Math.abs(x /= bandwidth) <= 1 ? 0.75 * (1 - x * x) / bandwidth : 0;
        };
      }

      // TODO: Select suitable value
      var bandwidth = 0.05;
      var props = this.props;

      // draw heatmap
      this.svg.selectAll().data(this.props.data, function (d) {
        return d.id1 + ":" + d.id2;
      }).enter().append("rect").attr("x", function (d) {
        return x(d.id1);
      }).attr("y", function (d) {
        return y(d.id2);
      }).attr("width", x.bandwidth()).attr("height", y.bandwidth()).style("fill", function (d) {
        return myColor(d.total);
      }).attr("opacity", 0.5).on('mouseover', function (d, i) {
        d3__WEBPACK_IMPORTED_MODULE_0__["select"](this).transition().duration('50').attr('opacity', '.85');
        props.setProps({
          hoverData: [i.id1, i.id2]
        });
      }).on('mouseout', function (d, i) {
        d3__WEBPACK_IMPORTED_MODULE_0__["select"](this).transition().duration('50').attr('opacity', '.5');
      });
      if (this.props.showDistribution) {
        var _loop = function _loop() {
          var d = _this.props.data[i];
          var xDens = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().range([x(d.id1), x(d.id1) + x.bandwidth()]).domain([-1, 1]);
          var thresholds = xDens.ticks(50);
          var densities = kde(epanechnikov(bandwidth), thresholds, d.correlations);
          var yDens = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().range([y(d.id2), y(d.id2) + y.bandwidth()]).domain([10, 0]); //d.correlations.length*0.75
          var line = d3__WEBPACK_IMPORTED_MODULE_0__["line"]().curve(d3__WEBPACK_IMPORTED_MODULE_0__["curveBasis"]).x(function (xd) {
            return xDens(xd[0]);
          }).y(function (yd) {
            return yDens(yd[1]);
          });
          _this.svg.append("path").datum(densities).attr("fill", "none").attr("stroke", "#000").attr("stroke-width", 1.5).attr("stroke-linejoin", "round").attr("d", line);
        };
        for (var i in this.props.data) {
          _loop();
        }
      }

      // Color bar
      var legendProps = {
        title: this.props.colorBarTitle,
        tickSize: 6,
        width: 30,
        height: this.props.height,
        // + tickSize,
        marginTop: 0,
        marginRight: 0,
        marginBottom: 0,
        // + tickSize,
        marginLeft: 3,
        ticks: this.props.width / 64
      };
      function ramp(color) {
        var n = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 256;
        var canvas = document.createElement("canvas");
        canvas.width = 1;
        canvas.height = n;
        var context = canvas.getContext("2d");
        for (var _i = 0; _i < n; ++_i) {
          context.fillStyle = color(_i / (n - 1));
          context.fillRect(0, /*n - 1 - i, 1*/_i, 1, 1);
        }
        return canvas;
      }
      var n = Math.min(myColor.domain().length, myColor.range().length);
      var xColorScale = myColor.copy().rangeRound(d3__WEBPACK_IMPORTED_MODULE_0__["quantize"](d3__WEBPACK_IMPORTED_MODULE_0__["interpolate"](legendProps.marginTop, legendProps.height - legendProps.marginBottom), n));
      this.svg.append("image").attr("x", this.props.width + legendProps.marginLeft).attr("y", legendProps.marginTop).attr("width", legendProps.width - legendProps.marginLeft - legendProps.marginRight).attr("height", legendProps.height - legendProps.marginTop - legendProps.marginBottom).attr("preserveAspectRatio", "none").attr("xlink:href", ramp(myColor.copy().domain(d3__WEBPACK_IMPORTED_MODULE_0__["quantize"](d3__WEBPACK_IMPORTED_MODULE_0__["interpolate"](0, 1), n))).toDataURL()).style("opacity", 0.5);
      this.legendTitle = this.svg.append("g").style("font", this.props.fontSize + "px times").attr("transform", 'translate(' + (this.props.width + legendProps.width) + ',0)') // myColor + legendProps.width
      .call(d3__WEBPACK_IMPORTED_MODULE_0__["axisRight"](xColorScale)).call(function (g) {
        return g.select(".domain").remove();
      }).append("text").attr("x", -legendProps.width + legendProps.marginLeft).attr("y", -5).attr("fill", "black").attr("text-anchor", "start").attr("font-size", this.props.fontSize).text(legendProps.title);
    }
  }, {
    key: "update",
    value: function update(props) {
      this.props = props;
      this.svg.selectAll('*').remove();
      this.drawHeatmap();
    }
  }]);
  return CorrelationHeatmapD3;
}();


/***/ })

})
//# sourceMappingURL=819c5cb-main-wps-hmr.js.map
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiI4MTljNWNiLW1haW4td3BzLWhtci5qcyIsInNvdXJjZVJvb3QiOiIifQ==