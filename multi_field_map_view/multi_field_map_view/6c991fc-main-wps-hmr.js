webpackHotUpdatemulti_field_map_view("main",{

/***/ "./src/lib/components/MultiFieldMapView.js":
/*!*************************************************!*\
  !*** ./src/lib/components/MultiFieldMapView.js ***!
  \*************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return MultiFieldMapViewD3; });
/* harmony import */ var d3__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! d3 */ "./node_modules/d3/src/index.js");
/* harmony import */ var _lasso__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./lasso */ "./src/lib/components/lasso.js");
function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }


var MultiFieldMapViewD3 = /*#__PURE__*/function () {
  function MultiFieldMapViewD3(el, props) {
    _classCallCheck(this, MultiFieldMapViewD3);
  }
  _createClass(MultiFieldMapViewD3, [{
    key: "drawPolygons",
    value: function drawPolygons() {
      var props = this.props;
      var x = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().domain([0, this.props.imageWidth]).range([0, this.props.width]);
      var y = d3__WEBPACK_IMPORTED_MODULE_0__["scaleLinear"]().domain([this.props.imageHeight, 0]).range([0, this.props.height]);
      this.svg.selectAll('polygons').data(this.props.polygons).enter().append('polygon').attr('class', 'polygon').attr('points', function (d) {
        return d.points.map(function (p) {
          return [x(p[0]), y(p[1])];
        });
      }).attr('stroke', function (d) {
        return props.colormap[d.field];
      }).attr('stroke-width', 3).attr('fill', 'none');
    }
  }, {
    key: "update",
    value: function update(props) {
      this.props = props;
      this.svg.selectAll('.polygon').remove();
      this.drawPolygons();
    }
  }]);
  return MultiFieldMapViewD3;
}();


/***/ })

})
//# sourceMappingURL=6c991fc-main-wps-hmr.js.map
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiI2Yzk5MWZjLW1haW4td3BzLWhtci5qcyIsInNvdXJjZVJvb3QiOiIifQ==