# AUTO GENERATED FILE - DO NOT EDIT

#' @export
multiFieldMapView <- function(id=NULL, colormap=NULL, height=NULL, highlighted=NULL, imageHeight=NULL, imageWidth=NULL, path=NULL, polygons=NULL, selection=NULL, width=NULL) {
    
    props <- list(id=id, colormap=colormap, height=height, highlighted=highlighted, imageHeight=imageHeight, imageWidth=imageWidth, path=path, polygons=polygons, selection=selection, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MultiFieldMapView',
        namespace = 'multi_field_map_view',
        propNames = c('id', 'colormap', 'height', 'highlighted', 'imageHeight', 'imageWidth', 'path', 'polygons', 'selection', 'width'),
        package = 'multiFieldMapView'
        )

    structure(component, class = c('dash_component', 'list'))
}
