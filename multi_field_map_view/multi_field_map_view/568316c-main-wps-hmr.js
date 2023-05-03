webpackHotUpdatemulti_field_map_view("main",{

/***/ "../../EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/coastline-world.png":
/*!*********************************************************************************************************************************!*\
  !*** /data2/Sciebo/Promotion/EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/coastline-world.png ***!
  \*********************************************************************************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = (__webpack_require__.p + "eb283f16ee4db6f94accc57a8b09932d.png");

/***/ }),

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
    this.svg.append("svg:image").attr('x', -9).attr('y', -12).attr('width', 800).attr('height', 400).attr("src", function (d) {
      var imagePath = __webpack_require__(/*! /data2/Sciebo/Promotion/EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/coastline-world.png */ "../../EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/coastline-world.png");
      return imagePath;
    });
    //.attr("xlink:href", "coastline-world.png")
    /*this.svg.append("defs")
        .append("pattern")
        .attr("id", "bg")
        .append("image")
        .attr("width", 50)
        .attr("height", 100)
        .attr("xlink:href", "file:///data2/Sciebo/Promotion/EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/test.png");*/

    //this.svg.style("background","url('file:///data2/Sciebo/Promotion/EigenePaper/MultiFieldCorrelation/multi-field-correlations/Application/assets/test.png') no-repeat")
    //.style("background-size", "800px 400px");
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
//# sourceMappingURL=568316c-main-wps-hmr.js.map
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiI1NjgzMTZjLW1haW4td3BzLWhtci5qcyIsInNvdXJjZVJvb3QiOiIifQ==