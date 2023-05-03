# AUTO GENERATED FILE - DO NOT EDIT

export multifieldmapview

"""
    multifieldmapview(;kwargs...)

A MultiFieldMapView component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `colormap` (Dict; required)
- `height` (Real; optional)
- `highlighted` (Array; optional)
- `imageHeight` (Real; optional)
- `imageWidth` (Real; optional)
- `path` (String; optional)
- `polygons` (Array; required)
- `selection` (Array; optional)
- `width` (Real; optional)
"""
function multifieldmapview(; kwargs...)
        available_props = Symbol[:id, :colormap, :height, :highlighted, :imageHeight, :imageWidth, :path, :polygons, :selection, :width]
        wild_props = Symbol[]
        return Component("multifieldmapview", "MultiFieldMapView", "multi_field_map_view", available_props, wild_props; kwargs...)
end

