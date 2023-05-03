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
    this.svg = d3__WEBPACK_IMPORTED_MODULE_0__["select"](el).append('svg').attr("width", props.width + 2 * props.margin).attr("height", props.height + 2 * props.margin).append("g").attr("transform", "translate(" + props.margin + "," + props.margin + ")");
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
      this.svg.append("g").attr("transform", "translate(0, " + this.props.height + ")").call(d3__WEBPACK_IMPORTED_MODULE_0__["axisBottom"](x));
      this.svg.append("g").call(d3__WEBPACK_IMPORTED_MODULE_0__["axisLeft"](y));

      // Build color scale
      // TODO: Adapt
      var myColor = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().range(["white", "#69b3a2"]).domain([-1, 1]);
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
      var bandwidth = 0.1;

      // draw heatmap
      this.svg.selectAll().data(this.props.data, function (d) {
        return d.id1 + ":" + d.id2;
      }).enter().append("rect").attr("x", function (d) {
        return x(d.id1);
      }).attr("y", function (d) {
        return y(d.id2);
      }).attr("width", x.bandwidth()).attr("height", y.bandwidth()).style("fill", function (d) {
        return myColor(d.total);
      });
      // TODO: Remove after finding solution for lines
      /*const xDens = d3.scaleLinear()
          .range([x(this.props.data[0].id1), x(this.props.data[0].id1)+x.bandwidth()])
          .domain([-1, 1]);
      const thresholds = xDens.ticks();
      console.log(this.props.data[0].correlations);
      const densities = kde(epanechnikov(bandwidth), thresholds, this.props.data[0].correlations);
      console.log(densities);
      const yDens = d3.scaleLinear()
          .range([y(this.props.data[0].id2), y(this.props.data[0].id2)+y.bandwidth()])
          .domain([3, 0]);
      const line = d3.line()
          .curve(d3.curveBasis)
          .x(xd => xDens(xd[0]))
          .y(yd => yDens(yd[1]));*/
      var _loop = function _loop() {
        var d = _this.props.data[i];
        var xDens = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().range([x(d.id1), x(d.id1) + x.bandwidth()]).domain([-1, 1]);
        var thresholds = xDens.ticks(50);
        var densities = kde(epanechnikov(bandwidth), thresholds, d.correlations);
        var yDens = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().range([y(d.id2), y(d.id2) + y.bandwidth()]).domain([5, 0]);
        var line = d3__WEBPACK_IMPORTED_MODULE_0__["line"]().curve(d3__WEBPACK_IMPORTED_MODULE_0__["curveBasis"]).x(function (xd) {
          return xDens(xd[0]);
        }).y(function (yd) {
          return yDens(yd[1]);
        });
        _this.svg //.selectAll("lines")
        //.data(this.props.data)//, function(d) {return d.id1+":"+d.id2})
        //.enter()
        .append("path").datum(densities)
        /*.datum(function(d) {
            const xDens = d3.scaleLinear()
                .range([x(d.id1), x(d.id1)+x.bandwidth])
                .domain(0, 1)
            const thresholds = xDens.ticks(40);
            return kde(epanechnikov(bandwidth), thresholds, d.correlations);
        })*/.attr("fill", "none").attr("stroke", "#000").attr("stroke-width", 1.5).attr("stroke-linejoin", "round")
        /*.attr("d", function(d) {
            const xDens = d3.scaleLinear()
                .range([x(d.id1), x(d.id1) + x.bandwidth()])
                .domain([-1, 1]);
            const yDens = d3.scaleLinear()
                .range([y(d.id2), y(d.id2) + y.bandwidth()])
                .domain([0, 3]);
            const thresholds = xDens.ticks(40);
            const densities = kde(epanechnikov(bandwidth), thresholds, d.correlations);
            return d3.line()
                .curve(d3.curveBasis)
                .x(xd => xDens(xd[0]))
                .y(yd => yDens(yd[1]))
        })*/.attr("d", line);
      };
      for (var i in this.props.data) {
        _loop();
      }
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
//# sourceMappingURL=1a42ed5-main-wps-hmr.js.map
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiIxYTQyZWQ1LW1haW4td3BzLWhtci5qcyIsInNvdXJjZVJvb3QiOiIifQ==