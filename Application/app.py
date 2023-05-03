# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import base64
import json
import os
import time
import dateutil.parser

import pandas as pd
import sklearn
from dash import Dash, html, dcc, Input, Output, State, ctx
import plotly.express as px
import plotly.graph_objs as go
from matplotlib import pyplot as plt

import numpy as np
import umap
import multi_field_map_view as mfmv
import correlation_heatmap as cm
import dash_daq as daq
from datetime import datetime#, timedelta
from dateutil.relativedelta import relativedelta
from scipy.fft import fft, fftfreq
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
from dash.exceptions import PreventUpdate

import statsmodels.api as sm

class Global():
    def __init__(self):
        self.fields = []
        self.d = None
        self.segmentationLength = {}
        self.correlations = None
        self.segments = None
        self.timeseries = None
        self.x = 0
        self.y = 0
        self.cmap = {}
        self.monthly = False
        self.allSeriesAvailable = False
        self.allSeries = {}


app = Dash(__name__, suppress_callback_exceptions=True)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
nNeighbors = 500
minDist = 0.1
anti = False

units = {"psl": "Pa", "pr": "mm/month", "tasAnomaly": "K", "tsAnomaly": "K", "prAnomaly": "mm/month","prRelativeAnomaly": "%", "pslAnomaly": "Pa"}

df = pd.DataFrame()
data = Global()

configWithoutLasso = {'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d']}
config = {'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d']}

# --------------------------------------------
# App Layout
# --------------------------------------------
app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            dcc.Upload(
                id='select-data',
                children=html.Div([
                    html.Button('Select Dataset')#, style={'width': '100%'})
                ]),
                style={
                    'width': '25%'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(children=[html.Label("Select fields:")], style={"width": "15%"}),
            html.Div(children=[dcc.Dropdown(
                data.fields,
                data.fields,
                multi=True,
                id='field-selection'
            )], style={"width": "60%"})
        ], style=dict(display='flex')),
        html.Div(children=[
            # dcc.Dropdown(["UMAP", "t-SNE"], "UMAP", id="projectionMethod"),
            dcc.Tabs(id="tabs-umap", value="tab1-projection", children=[
                dcc.Tab(label="UMAP", value="tab1-projection", children=[
                    html.Div(children=[
                        dcc.Graph(
                            id='projection',
                            config={'displaylogo': False}  # ,
                            # figure=fig
                        ),
                        html.Div(children=[
                            dcc.Textarea(
                                id='textarea-annotation',
                                value='Label',
                                style={'width': '40%'},
                            ),
                            html.Button('Annotate', id='submit-annotate',
                                style={'width': '30%'}),
                            html.Button('Clear Annotations', id='clear-annotate',
                                style={'width': '30%'})
                        ], style=dict(display='flex')),
                    ])
                ]),
                dcc.Tab(label="Settings",value="tab2-settings", children=[
                    html.Div(children=[
                        html.Div(children=[html.Label("Neighbors:")], style={"width": "30%"}),
                        html.Div(children=[dcc.Slider(1, 500, value=nNeighbors, id='neighbor-slider')],
                                 style={"width": "70%"})
                    ], style=dict(display='flex')),
                    html.Div(children=[
                        html.Div(children=[html.Label("Minimum distance:")], style={"width": "30%"}),
                        html.Div(children=[dcc.Slider(0.00, 0.99, value=0.1, id='minDist-slider')],
                                 style={"width": "70%"})
                    ], style=dict(display='flex')),
                    html.Div(children=[
                        html.Div(children=[html.Label("Antikorrelation as small distance:")], style={"width": "30%"}),
                        html.Div(children=[daq.ToggleSwitch(id='toggle-anti', value=False)], style={"width": "70%"})
                    ], style=dict(display='flex')),
                    html.Div(children=[
                        html.Div(children=[html.Label("Show line plot:")], style={"width": "30%"}),
                        html.Div(children=[daq.ToggleSwitch(id='toggle-linking',value=False)], style={"width": "70%"})
                    ], style=dict(display='flex')),
                    html.Div(children=[
                        html.Div(children=[html.Label("Show heatmap:")], style={"width": "30%"}),
                        html.Div(children=[daq.ToggleSwitch(id='toggle-heatmap',value=False)], style={"width": "70%"})
                    ], style=dict(display='flex')),
                    html.Div(children=[
                        html.Div(children=[html.Label("Show distribution:")], style={"width": "30%"}),
                        html.Div(children=[daq.ToggleSwitch(id='toggle-distribution',value=True)], style={"width": "70%"})
                    ], style=dict(display='flex')),
                ])
            ]),
        ], style={'display': 'inline-block', "width": "50%"}),
        html.Div(id = 'mapDiv', children=[
        ], style={"width": "50%", 'float':'right', "margin-top": "61px"})
    ]),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='lineplot',
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d']}
            )
        ], style={'display': 'inline-block', "width": "50%", "margin-top": "61px"}),
        html.Div(children=[
            dcc.Tabs(id="tabs-details", value="tab1-heatmap", children=[
                dcc.Tab(label="Heatmap", value="tab1-heatmap", children=[
                    html.Div(children=[
                        cm.CorrelationHeatmap(
                            id='heatmap',
                            data = [],
                            segmentIDs=[],
                            margin=40,
                            cmap=data.cmap
                        )
                    ])
                ]),
                dcc.Tab(label="Fourier",value="tab2-fourier", children=[
                    dcc.Graph(
                        id='fourier',
                        config={'displaylogo': False}
                    ),
                ])
            ])
        ], style={'display': 'inline-block', "width": "50%", 'float':'right'})
    ])

])


# --------------------------------------------
# Callbacks
# --------------------------------------------
@app.callback(
    Output('field-selection', 'options'),
    Output('field-selection', 'value'),
    Output('neighbor-slider', 'max'),
    Output('mapDiv', 'children'),
    Output('heatmap', 'cmap'),
    Input('select-data', 'contents')
)
def load_data(contents):
    if contents is None:
        raise PreventUpdate
    # Load data
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    global data
    data = Global()
    # this is a dict!
    configDict= json.loads(decoded)
    data.fields = configDict["fields"]
    data.d = np.load(configDict["dPath"])
    if "allSeriesAvailable" in configDict:
        data.allSeriesAvailable = configDict["allSeriesAvailable"]
    numSeg = 0
    for field in data.fields:
        data.segmentationLength[field] = len(np.unique(np.load(os.path.join(configDict["segmentationPath"], field + ".npy"))))
        numSeg += data.segmentationLength[field]
    data.correlations = np.memmap(configDict["correlationsPath"], mode='r', dtype='float32', shape=(numSeg, numSeg, configDict["numRuns"]))
    with open(configDict["segmentPointsPath"], "r") as file:
        json_object = file.read()
    data.segments = json.loads(json_object)
    with open(configDict["segmentMedianPath"], "r") as file:
        json_object = file.read()
    data.timeseries = json.loads(json_object)
    numSteps = len(data.timeseries[data.fields[0]]['0'][0])
    if data.allSeriesAvailable:
        for field in data.fields:
            data.allSeries[field] = np.memmap(os.path.join(configDict["segmentationPath"], field+"AllSeries.dat"),
                                              dtype='float32', mode='r', shape=(data.segmentationLength[field], configDict["numRuns"], numSteps))
    data.segmentations = {}
    for f in data.fields:
        data.segmentations[f] = np.load(os.path.join(configDict["segmentationPath"], f + ".npy"))
        for i, s in enumerate(sorted(np.unique(data.segmentations[f]))):
            data.segmentations[f][data.segmentations[f]==s] = i
    data.x = configDict["x"]
    data.y = configDict["y"]
    data.cmap = configDict["cmap"]
    data.monthly = configDict["monthly"]
    print("Data loaded, preparing UMAP")
    global df
    df = pd.DataFrame()
    print(data.d.shape)
    reducer = umap.UMAP(random_state=0, metric='precomputed', n_neighbors=int(nNeighbors), min_dist=minDist)
    embedding = reducer.fit_transform(data.d)
    df["x"] = embedding[:, 0]
    df["y"] = embedding[:, 1]
    fieldList = []
    for f in data.fields:
        fieldList += [f] * data.segmentationLength[f]
    df["field"] = fieldList
    map = mfmv.MultiFieldMapView(
        id='map',
        imageWidth=data.x,
        imageHeight=data.y,
        polygons=[],
        colormap=data.cmap,
        path="/assets/blank.png"  # borderEuropeCentered.png"
    )
    return data.fields, data.fields, len(data.d), map, data.cmap

@app.callback(
    Output('projection', 'figure'),
    Input('projection', 'figure'),
    Input('neighbor-slider', 'value'),
    Input('minDist-slider', 'value'),
    Input('map','selection'),
    Input('field-selection', 'value'),
    Input('submit-annotate', 'n_clicks'),
    Input('clear-annotate', 'n_clicks'),
    Input('toggle-anti', 'value'),
    State('textarea-annotation', 'value'),
    State('projection', 'selectedData'),
    prevent_initial_call=True
)
def update_output(oldFig, nNeighborsNew, minDistNew, selection, fields, buttonClick, clearClick, nAnti, text, lassoSelection):
    if not data.fields:
        return go.Figure()
    global nNeighbors,minDist,anti
    sel = [f in fields for f in df["field"]]
    if(nNeighborsNew != nNeighbors or minDistNew != minDist or nAnti != anti):
        nNeighbors = nNeighborsNew
        minDist = minDistNew
        anti = nAnti
        reducer = umap.UMAP(random_state=0, metric='precomputed', n_neighbors=int(nNeighbors), min_dist=minDist)
        dist = data.d
        if anti:
            dist = 1 - np.abs(1 - 2*data.d)
        embedding = reducer.fit_transform(dist)
        df["x"] = embedding[:, 0]
        df["y"] = embedding[:, 1]
    df_new = df[sel]
    fig = px.scatter(df_new, x="x", y="y", color="field", template='simple_white', color_discrete_map=data.cmap)
    if selection:
        selection = np.array(selection)
        i = 0
        for f in data.fields:
            if f in fields:
                selectedSegments = list(np.unique(data.segmentations[f][selection[:,1],selection[:,0]]))
                oldFig['data'][i]['selectedpoints'] = selectedSegments
                i += 1
            fig = go.Figure(oldFig)
            fig.update_layout(uirevision="Don't Change")
    if ctx.triggered_id == 'submit-annotate':
        if lassoSelection:
            fig = go.Figure(oldFig)
            if 'range' in lassoSelection: # box select
                x = max(lassoSelection['range']['x'])
                y = max(lassoSelection['range']['y'])
            else: # lasso select
                x = max(lassoSelection['lassoPoints']['x'])
                y = max(lassoSelection['lassoPoints']['y'])
                xx = lassoSelection['lassoPoints']['x']
                yy = lassoSelection['lassoPoints']['y']
                fig.add_trace(go.Scatter(x=xx+[xx[0]], y=yy+[yy[0]], mode='lines', line=dict(color='black', width=2)))
            fig.add_annotation(x=x, y=y, text=text, showarrow=False)
    return fig

@app.callback(
    Output('map', 'polygons'),
    Input('projection', 'selectedData'),
    Input('map','selection'),
    Input('field-selection', 'value'), prevent_initial_call=True
)
def update_map(points, selection, fields):
    if not points and not selection:
        return []
    polygons = []
    if points:
        for p in points['points']:
            field = fields[int(p['curveNumber'])]
            id = str(p['pointIndex'])
            for pol in data.segments[field][id]:
                pol = np.array(pol) + 0.5
                polygons.append({'segID': id,
                                     'points':pol,
                                     'field': field})
    else:
        selection = np.array(selection)
        for field in fields:
            selectedSegments = list(np.unique(data.segmentations[field][selection[:, 1], selection[:, 0]]))
            for id in selectedSegments:
                for pol in data.segments[field][str(int(id))]:
                    pol = np.array(pol) + 0.5
                    polygons.append({'segID': id,
                                     'points': pol,
                                     'field': field})
    return polygons

@app.callback(
    Output('map', 'highlighted'),
    Input('heatmap', 'hoverData')
)
def update_hover(hover):
    if not hover:
        return []
    hover = ["polygon." + h.replace(" ", "-") for h in hover]
    return hover

@app.callback(
    Output('heatmap', 'data'),
    Output('heatmap', 'segmentIDs'),
    Output('heatmap', 'showDistribution'),
    Input('projection', 'selectedData'),
    Input('map','selection'),
    Input('toggle-heatmap', 'value'),
    Input('toggle-distribution', 'value'),
    Input('field-selection', 'value'), prevent_initial_call=True
)
def update_heatmap(points, mapSelection, linking, distribution, fields):
    #return [], []
    if (not points and not mapSelection) or not linking:
        return [], [], distribution
    correlations = []
    ids = []
    idx = []
    if points:
        for p1 in points['points']:
            ids.append( fields[int(p1['curveNumber'])]+ " " +str(p1['pointIndex']))
            #ids.append(str(p1['pointIndex']))
            for p2 in points['points']:
                if p1 == p2:
                    continue
                c = {}
                c['id1'] = fields[int(p1['curveNumber'])] + " " +str(p1['pointIndex'])
                c['id2'] =  fields[int(p2['curveNumber'])]+ " " +str(p2['pointIndex'])
                off1 = 0
                for i in range(data.fields.index(fields[p1['curveNumber']])):
                    off1 += data.segmentationLength[data.fields[i]]
                off2 = 0
                for i in range(data.fields.index(fields[p2['curveNumber']])):
                    off2 += data.segmentationLength[data.fields[i]]
                i1 = p1['pointIndex'] + off1
                i2 = p2['pointIndex'] + off2
                if i1 not in idx:
                    idx.append(i1)
                c['total'] = 1 - 2*data.d[i1, i2]
                if distribution:
                    c['correlations'] = data.correlations[i1, i2]
                else:
                    c['correlations'] = []
                correlations.append(c)
    if mapSelection: # mapSelection
        mapSelection = np.array(mapSelection)
        i = 0
        for f1 in data.fields:
            if f1 in fields:
                selectedSegments = list(np.unique(data.segmentations[f1][mapSelection[:, 1], mapSelection[:, 0]]))
                for s1 in selectedSegments:
                    ids.append(f1 + " " + str(int(s1)))
                    j = 0
                    for f2 in data.fields:
                        if f2 in fields:
                            selectedSegments2 = list(np.unique(data.segmentations[f2][mapSelection[:, 1], mapSelection[:, 0]]))
                            for s2 in selectedSegments2:
                                if s1 == s2:
                                    continue
                                c = {}
                                c['id1'] = f1 + " " + str(int(s1))
                                c['id2'] = f2 + " " + str(int(s2))
                                off1 = 0
                                for ii in range(i):
                                    off1 += data.segmentationLength[data.fields[ii]]
                                off2 = 0
                                for ii in range(j):
                                    off2 += data.segmentationLength[data.fields[ii]]
                                i1 = int(s1 + off1)
                                i2 = int(s2 + off2)
                                if i1 not in idx:
                                    idx.append(i1)
                                c['total'] = 1 - 2 * data.d[i1, i2]
                                if distribution:
                                    c['correlations'] = data.correlations[i1, i2]
                                else:
                                    c['correlations'] = []
                                correlations.append(c)
                    j += 1
        i += 1
    if len(idx)<=1:
        return correlations, ids, distribution
    dis = data.d[idx,:]
    dis = dis[:,idx]
    np.fill_diagonal(dis, 0)
    condensed_matrix = squareform(dis, checks=False)
    Y = sch.linkage(condensed_matrix, method='ward')
    Z1 = sch.dendrogram(Y)
    idx1 = Z1['leaves']
    ids = list(np.array(ids)[idx1])
    return correlations, ids, distribution

# noinspection PyTypeChecker
@app.callback(
    Output('lineplot', 'figure'),
    Input('projection', 'selectedData'),
    Input('map','selection'),
    Input('toggle-linking', 'value'),
    Input('field-selection', 'value'), prevent_initial_call=True
)
def update_lineplot(points, mapSelection, toggle, fields):
    if (not points and not mapSelection) or not toggle:
        return go.Figure()
    fig = go.Figure()
    minFieldIndex = 10
    selFields = []
    if points:
        for p in points['points']:
            field = fields[int(p['curveNumber'])]
            if field not in selFields:
                selFields.append(field)
            id = str(p['pointIndex'])
            median, lower, upper = data.timeseries[field][id]
            if data.monthly:
                t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(months=1)
            else:
                t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(years=1)
            #x = np.arange(len(upper))
            x = np.concatenate([t, t[::-1]])
            minFieldIndex = min(minFieldIndex, fields.index(field))
            fieldIndex = str(selFields.index(field)+1)
            fig.add_traces(go.Scatter(
                                        x=x,
                                        y=lower + upper[::-1],
                                        fill='toself',
                                        fillcolor=data.cmap[field],
                                        opacity=0.1,
                                        line=dict(color='rgba(255,255,255,0)'),
                                        showlegend=False,
                                        yaxis="y"+fieldIndex
            ))
        for p in points['points']:
            field = fields[int(p['curveNumber'])]
            id = str(p['pointIndex'])
            median, lower, upper = data.timeseries[field][id]
            if data.monthly:
                t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(months=1)
            else:
                t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(years=1)
            fieldIndex = str(selFields.index(field)+1)
            y = "y"+fieldIndex
            fig.add_traces(go.Scatter(x=t,
                                      y=median,
                                      line=dict(color=data.cmap[field], width=1),
                                      mode='lines+markers',
                                      name=field,
                                      yaxis=y,
                                      marker=dict(size=0.01))
                           )
    if mapSelection:
        mapSelection = np.array(mapSelection)
        for f in data.fields:
            if f in fields:
                selectedSegments = list(np.unique(data.segmentations[f][mapSelection[:, 1], mapSelection[:, 0]]))
                if f not in selFields:
                    selFields.append(f)
                for s in selectedSegments:
                    field = f
                    id = str(int(s))
                    median, lower, upper = data.timeseries[field][id]
                    if data.monthly:
                        t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(months=1)
                    else:
                        t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(years=1)
                    x = np.concatenate([t, t[::-1]])
                    minFieldIndex = min(minFieldIndex, fields.index(field))
                    fieldIndex = str(selFields.index(field)+1)
                    fig.add_traces(go.Scatter(
                                                x=x,
                                                y=lower + upper[::-1],
                                                fill='toself',
                                                fillcolor=data.cmap[field],
                                                opacity=0.1,
                                                line=dict(color='rgba(255,255,255,0)'),
                                                showlegend=False,
                                                yaxis="y"+fieldIndex
                    ))
        for f in data.fields:
            if f in fields:
                selectedSegments = list(np.unique(data.segmentations[f][mapSelection[:, 1], mapSelection[:, 0]]))
                for s in selectedSegments:
                    field = f
                    id = str(int(s))
                    median, lower, upper = data.timeseries[field][id]
                    if data.monthly:
                        t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(months=1)
                    else:
                        t = datetime(2006, 1, 1) + np.arange(len(upper)) * relativedelta(years=1)
                    fieldIndex = str(selFields.index(field)+1)
                    y = "y"+fieldIndex
                    fig.add_traces(go.Scatter(x=t,
                                              y=median,
                                              line=dict(color=data.cmap[field], width=1),
                                              mode='lines+markers',
                                              name=field,
                                              yaxis=y,
                                              marker=dict(size=0.01))
                                   )
    numF = len(selFields)
    xMin = (int(numF/2))*0.1
    xMax = 1.0-int(numF/2)*0.1
    yaxes = {}
    for i, f in enumerate(selFields):
        name = "yaxis"
        #if i > 0:
        name += str(i+1)
        if i % 2 == 1:
            side = "right"
            position = xMax + 0.1*int(i/2)
        else:
            side = "left"
            position = max(0, xMin - 0.1*int(i/2))
        unit = ""
        if f in units:
            unit = units[f]
        if i != 0:#minFieldIndex:
            yaxes[name] = dict(
                    title=f + " [" + unit + "]",
                    side = side,
                    anchor="free",
                    overlaying="y",
                    position=position
                )
        else:
            yaxes[name] = dict(
                    title=f + " [" + unit + "]",
                    side = side,
                    anchor="free",
                    position=position
                )
    fig.update_layout(template='simple_white', xaxis = dict(domain=[xMin, xMax]), **yaxes)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output('fourier', 'figure'),
    Input('lineplot', 'selectedData'),
    State('projection', 'selectedData'),
    Input('map','selection'),
    Input('field-selection', 'value'), prevent_initial_call=True
)
def update_fourier(points, selection, mapSelection, fields):# aggregate, fields):
    aggregate = False
    if not points or (not selection and not mapSelection) or not 'range' in points:
        return go.Figure()
    fig = go.Figure()
    label = "1/year"
    fig.update_layout(xaxis_title=label, yaxis_title="Fourier transform", template='simple_white')
    range = points['range']['x']
    start = dateutil.parser.parse(range[0])
    end = dateutil.parser.parse(range[1])
    zero = datetime(2006, 1, 1)
    startIdx = (start.year-zero.year)*12+start.month-zero.month
    endIdx = (end.year-zero.year)*12+end.month-zero.month
    if not data.monthly:
        startIdx /= 12
        endIdx /= 12
    startIdx = int(startIdx)
    endIdx = int(endIdx)
    spec = {}
    if selection:
        for p in selection['points']:
            field = fields[int(p['curveNumber'])]
            id = str(p['pointIndex'])
            if data.allSeriesAvailable:
                median = data.allSeries[field][int(id)][:,startIdx:endIdx+1]
            else:
                median, _, _ = data.timeseries[field][id]
                median = median[startIdx:endIdx+1]
            N = len(median)
            if data.allSeriesAvailable:
                N = len(median[0])
                numRuns = len(median)
                print(N)
                minFFT = np.inf * np.ones(N // 2)
                maxFFT = -np.inf * np.ones(N // 2)
                fourier = np.zeros(N//2)
                for i, m in enumerate(median):
                    # Detrend timeseries
                    m = m-np.mean(m)
                    X = [i for i in np.arange(0, len(m))]
                    X = np.reshape(X, (len(X), 1))
                    y = m
                    model = sklearn.linear_model.LinearRegression()
                    model.fit(X, y)
                    # calculate trend
                    trend = model.predict(X)
                    m = [y[i] - trend[i] for i in np.arange(0, len(m))]
                    fftVar = np.abs(fft(m)[0:N//2])/N
                    minFFT = np.min([minFFT, fftVar], axis=0)
                    maxFFT = np.max([maxFFT, fftVar], axis=0)
                    fourier += fftVar
                fourier /= numRuns
                print(fourier[0])
                print(fourier.shape)
                maxFourier = np.max(fourier)
                minFFT /= maxFourier
                maxFFT /= maxFourier
            else:
                fourier = np.abs(fft(median-np.mean(median)))[0:N//2]#/len(data.allSeries['f1']['0'][0])
            maxFourier = np.max(fourier)
            fourier /= maxFourier
            if not aggregate:
                if data.monthly:
                    xf = fftfreq(N, 1/12)[:N // 2]
                else:
                    xf = fftfreq(N, 1)[:N // 2]
                if not data.allSeriesAvailable:
                    fig.add_traces(go.Scatter(x=xf,
                                              y=np.abs(fourier),
                                              line=dict(color=data.cmap[field], width=2.5),
                                              mode='lines',
                                              name=field,
                                              showlegend=False
                                   ))
                else:
                    xf = list(xf)
                    fig.add_traces(go.Scatter(
                        # x+x[::-1],
                        x=xf + xf[::-1],
                        y=list(minFFT) + list(maxFFT)[::-1],
                        fill='toself',
                        fillcolor=data.cmap[field],
                        opacity=0.1,
                        line=dict(color='rgba(255,255,255,0)'),
                        showlegend=False
                    ))
                    fig.add_traces(go.Scatter(x=xf,  # np.arange(len(median)),
                                              y=np.abs(fourier),
                                              line=dict(color=data.cmap[field], width=2.5),
                                              mode='lines',
                                              name=field,
                                              showlegend=False
                                              ))
            else:
                if field in spec:
                    spec[field].append(list(np.abs(fourier)))
                else:
                    spec[field] = [list(np.abs(fourier))]

    if mapSelection:
        mapSelection = np.array(mapSelection)
        for f in data.fields:
            if f in fields:
                selectedSegments = list(np.unique(data.segmentations[f][mapSelection[:, 1], mapSelection[:, 0]]))
                for s in selectedSegments:
                    field = f
                    id = str(int(s))
                    if data.allSeriesAvailable:
                        median = data.allSeries[field][int(id)][:,startIdx:endIdx + 1]
                    else:
                        median, _, _ = data.timeseries[field][id]
                        median = median[startIdx:endIdx + 1]
                    N = len(median)
                    if data.allSeriesAvailable:
                        N = len(median[0])
                        numRuns = len(median)
                        print(N)
                        minFFT = np.inf * np.ones(N // 2)
                        maxFFT = -np.inf * np.ones(N // 2)
                        fourier = np.zeros(N // 2)
                        for m in median:
                            # Detrend timeseries
                            m = m-np.mean(m)
                            X = [i for i in np.arange(0, len(m))]
                            X = np.reshape(X, (len(X), 1))
                            y = m
                            model = sklearn.linear_model.LinearRegression()
                            model.fit(X, y)
                            # calculate trend
                            trend = model.predict(X)
                            m = [y[i] - trend[i] for i in np.arange(0, len(m))]
                            fftVar = np.abs(fft(m)[0:N//2])/N
                            minFFT = np.min([minFFT, fftVar], axis=0)
                            maxFFT = np.max([maxFFT, fftVar], axis=0)
                            fourier += fftVar
                        fourier /= numRuns
                    else:
                        fourier = np.abs(fft(median - np.mean(median)))[0:N // 2]  
                    maxFourier = np.max(fourier)
                    fourier /= maxFourier
                    minFFT /= maxFourier
                    maxFFT /= maxFourier
                    if not aggregate:
                        if data.monthly:
                            xf = fftfreq(N, 1 / 12)[:N // 2]
                        else:
                            xf = fftfreq(N, 1)[:N // 2]
                        if not data.allSeriesAvailable:
                            fig.add_traces(go.Scatter(x=xf, 
                                                      y=np.abs(fourier),
                                                      line=dict(color=data.cmap[field], width=2.5),
                                                      mode='lines',
                                                      name=field,
                                                      showlegend=False
                                                      ))
                        else:
                            xf = list(xf)
                            fig.add_traces(go.Scatter(
                                # x+x[::-1],
                                x=xf + xf[::-1],
                                y=list(minFFT) + list(maxFFT)[::-1],
                                fill='toself',
                                fillcolor=data.cmap[field],
                                opacity=0.1,
                                line=dict(color='rgba(255,255,255,0)'),
                                showlegend=False
                            ))
                            fig.add_traces(go.Scatter(x=xf,  
                                                      y=np.abs(fourier),
                                                      line=dict(color=data.cmap[field], width=2.5),
                                                      mode='lines',
                                                      name=field,
                                                      showlegend=False
                                                      ))
                    else:
                        if field in spec:
                            spec[field].append(list(np.abs(fourier)))
                        else:
                            spec[field] = [list(np.abs(fourier))]
    if aggregate and not data.allSeriesAvailable:
        for f in spec.keys():
            minSeries = list(np.min(spec[f], axis=0))
            maxSeries = list(np.max(spec[f], axis=0))
            try:
                figB, depth, ix_depth, ix_outliers = sm.graphics.fboxplot(spec[f])
                plt.close(figB)
                medianSeries = spec[f][ix_depth[0]]
            except Exception as e:
                medianSeries = np.mean(spec[f], axis=0).tolist()
            N = endIdx - startIdx
            if data.monthly:
                xf = fftfreq(N, 1 / 12)[:N // 2]
            else:
                xf = fftfreq(N, 1)[:N // 2]
            xf = list(xf)
            fig.add_traces(go.Scatter(x=xf, 
                                      y=np.abs(medianSeries),
                                      line=dict(color=data.cmap[f], width=2.5),
                                      mode='lines',
                                      name=f,
                                      showlegend=False
                                      ))
            fig.add_traces(go.Scatter(
                # x+x[::-1],
                x=xf + xf[::-1],
                y=minSeries + maxSeries[::-1],
                fill='toself',
                fillcolor=data.cmap[f],
                opacity=0.1,
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False
            ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

