# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MultiFieldMapView(Component):
    """A MultiFieldMapView component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- colormap (dict; required)

- height (number; default 400)

- highlighted (list; optional)

- imageHeight (number; optional)

- imageWidth (number; optional)

- path (string; optional)

- polygons (list; required)

- selection (list; optional)

- width (number; default 800)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'multi_field_map_view'
    _type = 'MultiFieldMapView'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, imageWidth=Component.UNDEFINED, imageHeight=Component.UNDEFINED, polygons=Component.REQUIRED, colormap=Component.REQUIRED, path=Component.UNDEFINED, selection=Component.UNDEFINED, highlighted=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colormap', 'height', 'highlighted', 'imageHeight', 'imageWidth', 'path', 'polygons', 'selection', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colormap', 'height', 'highlighted', 'imageHeight', 'imageWidth', 'path', 'polygons', 'selection', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['colormap', 'polygons']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(MultiFieldMapView, self).__init__(**args)
