import React, {Component} from 'react';
import PropTypes from 'prop-types';
import MultiFieldMapViewD3 from './MultiFieldMapView';

/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class MultiFieldMapView extends Component {
    componentDidMount() {
        this.multifieldmap = new MultiFieldMapViewD3(this.el, this.props);
    }

    componentDidUpdate(prevProps, prevState) {
        Object.keys(this.props).forEach(propName => {
            if (propName === "polygons" && this.props[propName] !== prevProps[propName]) {
                this.multifieldmap.update(this.props);
            }
            if (propName === "highlighted" && this.props[propName] !== prevProps[propName]) {
                this.multifieldmap.updateHighlight(this.props);
            }
        });
    }

    render() {
        return <div id={this.props.id} ref={el => {this.el = el}} />;
    }
}

MultiFieldMapView.defaultProps = {
    width: 800,
    height: 400,
    //path: "/src/lib/components/coastline-world.png"
};

MultiFieldMapView.propTypes = {
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
    imageWidth: PropTypes.number,
    imageHeight: PropTypes.number,
    polygons: PropTypes.array.isRequired,
    colormap: PropTypes.object.isRequired,
    path: PropTypes.string,
    selection: PropTypes.array,
    highlighted: PropTypes.array
};
