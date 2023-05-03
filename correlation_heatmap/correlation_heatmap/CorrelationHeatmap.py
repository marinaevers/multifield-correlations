# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CorrelationHeatmap(Component):
    """A CorrelationHeatmap component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- cmap (dict; required)

- colorBarTitle (string; default "Correlation")

- data (list; required):
    Data to be visualized. The expected data structure is a 2D array
    with a dictionary as each entry for the matrix. The entry 'total'
    stores the correlation over the whole ensemble while
    'correlations' is an array with the pairwise correlations for each
    ensemble member.

- fontSize (number; default 12)

- height (number; default 400)

- hoverData (list; optional)

- margin (number; default 30)

- segmentIDs (list; required)

- showDistribution (boolean; default False)

- width (number; default 800)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'correlation_heatmap'
    _type = 'CorrelationHeatmap'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, margin=Component.UNDEFINED, data=Component.REQUIRED, segmentIDs=Component.REQUIRED, fontSize=Component.UNDEFINED, colorBarTitle=Component.UNDEFINED, showDistribution=Component.UNDEFINED, cmap=Component.REQUIRED, hoverData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'cmap', 'colorBarTitle', 'data', 'fontSize', 'height', 'hoverData', 'margin', 'segmentIDs', 'showDistribution', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cmap', 'colorBarTitle', 'data', 'fontSize', 'height', 'hoverData', 'margin', 'segmentIDs', 'showDistribution', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['cmap', 'data', 'segmentIDs']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(CorrelationHeatmap, self).__init__(**args)
