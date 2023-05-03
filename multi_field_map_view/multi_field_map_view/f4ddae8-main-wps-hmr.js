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
function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }

var MultiFieldMapViewD3 = /*#__PURE__*/function () {
  function MultiFieldMapViewD3(el, props) {
    _classCallCheck(this, MultiFieldMapViewD3);
    this.props = props;
    this.svg = d3__WEBPACK_IMPORTED_MODULE_0__["select"](el).append('svg').attr("width", props.width).attr("height", props.height);
    this.svg.append("svg:image").attr("x", 0).attr("y", 0).attr("src", "/data2/Sciebo/Promotion/EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/test2.png");
    //.attr("href", "https://cdn.eso.org/images/thumb700x/eso1907a.jpg")
  }
  _createClass(MultiFieldMapViewD3, [{
    key: "update",
    value: function update(props) {
      this.props = props;
    }
  }]);
  return MultiFieldMapViewD3;
}();


/***/ })

})
//# sourceMappingURL=f4ddae8-main-wps-hmr.js.map
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJmNGRkYWU4LW1haW4td3BzLWhtci5qcyIsInNvdXJjZVJvb3QiOiIifQ==