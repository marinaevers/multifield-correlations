/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import { MultiFieldMapView } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            polygons: [
                {
                    segID: 0,
                    points: [[0,0], [0,5], [5,5], [5,0]],
                    field: 'ts'
                },
                {
                    segID: 1,
                    points: [[7, 7], [5, 7], [9, 11]],
                    field: 'ts'
                },
                {
                    segID: 0,
                    points: [[1,1], [1,6], [6,6], [6,1]],
                    field: 'tas'
                }
            ],
            imageWidth: 192,
            imageHeight: 96,
            colormap: {
                'ts': '#f00',
                'tas': '#0f0'
            }
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
            <div>
                <MultiFieldMapView
                    setProps={this.setProps}
                    {...this.state}
                />
            </div>
        )
    }
}

export default App;
