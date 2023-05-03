import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CorrelationHeatmapD3 from './CorrelationHeatmap';
import Prop from 'ramda/src/prop';

/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class CorrelationHeatmap extends Component {
    componentDidMount() {
        this.correlationHeatmap = new CorrelationHeatmapD3(this.el, this.props);
    }

    componentDidUpdate(prevProps, prevState) {
        Object.keys(this.props).forEach(propName => {
            if (propName === "segmentIDs" && this.props[propName] !== prevProps[propName]) {
                this.correlationHeatmap.update(this.props);
            }
        });
    }
    render() {
        return <div id={this.props.id} ref={el => {this.el = el}} />;
    }
}

CorrelationHeatmap.defaultProps = {
    width: 800,
    height: 400,
    margin: 30,
    fontSize: 12,
    colorBarTitle: "Correlation",
    showDistribution: false
};

CorrelationHeatmap.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
    width: PropTypes.number,
    height: PropTypes.number,
    margin: PropTypes.number,
    /**
     * Data to be visualized. The expected data structure is a 2D array with a
     * dictionary as each entry for the matrix. The entry 'total' stores the
     * correlation over the whole ensemble while 'correlations' is an array
     * with the pairwise correlations for each ensemble member
     */
    data: PropTypes.array.isRequired,
    segmentIDs: PropTypes.array.isRequired,
    fontSize: PropTypes.number,
    colorBarTitle: PropTypes.string,
    showDistribution: PropTypes.bool,
    cmap: PropTypes.object.isRequired,
    hoverData:PropTypes.array
};
