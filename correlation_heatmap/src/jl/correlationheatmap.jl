# AUTO GENERATED FILE - DO NOT EDIT

export correlationheatmap

"""
    correlationheatmap(;kwargs...)

A CorrelationHeatmap component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `cmap` (Dict; required)
- `colorBarTitle` (String; optional)
- `data` (Array; required): Data to be visualized. The expected data structure is a 2D array with a
dictionary as each entry for the matrix. The entry 'total' stores the
correlation over the whole ensemble while 'correlations' is an array
with the pairwise correlations for each ensemble member
- `fontSize` (Real; optional)
- `height` (Real; optional)
- `hoverData` (Array; optional)
- `margin` (Real; optional)
- `segmentIDs` (Array; required)
- `showDistribution` (Bool; optional)
- `width` (Real; optional)
"""
function correlationheatmap(; kwargs...)
        available_props = Symbol[:id, :cmap, :colorBarTitle, :data, :fontSize, :height, :hoverData, :margin, :segmentIDs, :showDistribution, :width]
        wild_props = Symbol[]
        return Component("correlationheatmap", "CorrelationHeatmap", "correlation_heatmap", available_props, wild_props; kwargs...)
end

