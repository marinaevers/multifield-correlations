# AUTO GENERATED FILE - DO NOT EDIT

#' @export
correlationHeatmap <- function(id=NULL, cmap=NULL, colorBarTitle=NULL, data=NULL, fontSize=NULL, height=NULL, hoverData=NULL, margin=NULL, segmentIDs=NULL, showDistribution=NULL, width=NULL) {
    
    props <- list(id=id, cmap=cmap, colorBarTitle=colorBarTitle, data=data, fontSize=fontSize, height=height, hoverData=hoverData, margin=margin, segmentIDs=segmentIDs, showDistribution=showDistribution, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'CorrelationHeatmap',
        namespace = 'correlation_heatmap',
        propNames = c('id', 'cmap', 'colorBarTitle', 'data', 'fontSize', 'height', 'hoverData', 'margin', 'segmentIDs', 'showDistribution', 'width'),
        package = 'correlationHeatmap'
        )

    structure(component, class = c('dash_component', 'list'))
}
