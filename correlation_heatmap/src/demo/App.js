/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import { CorrelationHeatmap } from '../lib';

class App extends Component {

    constructor() {
        super();
        this.state = {
            data: [{'id1': "0", 'id2': "1", 'total':0.5, 'correlations':[0.1,0.1,0.2,0, 0.2, 0.2, 0.3]},
                {'id1': "0", 'id2': "2", 'total':-1, 'correlations':[0.3,0.3,0.3,0, 0.2, 0.2, 0.3]},
                {'id1': "1", 'id2': "2", 'total':1, 'correlations':[-0.3,-0.3,0.2,0, 0.2, 0.2, -0.3]}],
            segmentIDs: ["0", "1", "2"],
            cmap: {"0": "#F0F", "1": "#F00", "2": "#0F0"}
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
            <div>
                <CorrelationHeatmap
                    setProps={this.setProps}
                    {...this.state}
                />
            </div>
        )
    }
}

export default App;
