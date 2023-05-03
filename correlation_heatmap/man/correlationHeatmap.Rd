% Auto-generated: do not edit by hand
\name{correlationHeatmap}

\alias{correlationHeatmap}

\title{CorrelationHeatmap component}

\description{
ExampleComponent is an example component. It takes a property, `label`, and displays it. It renders an input with the property `value` which is editable by the user.
}

\usage{
correlationHeatmap(id=NULL, cmap=NULL, colorBarTitle=NULL, data=NULL,
fontSize=NULL, height=NULL, hoverData=NULL, margin=NULL,
segmentIDs=NULL, showDistribution=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{cmap}{Named list. }

\item{colorBarTitle}{Character. }

\item{data}{Unnamed list. Data to be visualized. The expected data structure is a 2D array with a
dictionary as each entry for the matrix. The entry 'total' stores the
correlation over the whole ensemble while 'correlations' is an array
with the pairwise correlations for each ensemble member}

\item{fontSize}{Numeric. }

\item{height}{Numeric. }

\item{hoverData}{Unnamed list. }

\item{margin}{Numeric. }

\item{segmentIDs}{Unnamed list. }

\item{showDistribution}{Logical. }

\item{width}{Numeric. }
}

\value{named list of JSON elements corresponding to React.js properties and their values}

