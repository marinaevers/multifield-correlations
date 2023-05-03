
module MultiFieldMapView
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/multifieldmapview.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "multi_field_map_view",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "multi_field_map_view.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "multi_field_map_view.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
