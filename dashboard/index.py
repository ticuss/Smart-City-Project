from zipfile import ZipFile
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


def get_data(path: str) -> pd.DataFrame:
    """
    Get data from zip file
    """
    with ZipFile(path) as myzip:
        data = myzip.open(path.split(".zip")[0])

    df = pd.read_csv(data, sep=";")
    return df


df_final = get_data("DMR_2021_2022.csv.zip")
df_dec = df_final.groupby(["DATE DECLARATION", "TYPE DECLARATION"]).count()
df_dec = df_dec.reset_index()
df_dec["DATE DECLARATION"] = pd.to_datetime(
    df_dec["DATE DECLARATION"], infer_datetime_format=True, dayfirst=True
)
arrondissement_count = df_final["ARRONDISSEMENT"].value_counts()


fig4 = px.line(
    df_dec,
    x="DATE DECLARATION",
    y="SOUS TYPE DECLARATION",
    color="TYPE DECLARATION",
    title="Declarations par type",
)
fig4.update_xaxes(
    tickformat="%b\n%Y",
    rangeslider_visible=True,
)
fig4.update_layout(
    width=800,
    height=520,
    plot_bgcolor="#1f2c56",
    paper_bgcolor="#1f2c56",
    hovermode="closest",
    titlefont={"color": "white", "size": 20},
    showlegend=False,
    font=dict(family="sans-serif", size=12, color="white"),
),


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Anomalies a Paris",
                                    style={
                                        "margin-bottom": "0px",
                                        "color": "white",
                                        "text-align": "center",
                                    },
                                ),
                                html.H5(
                                    "Anomalies signalées par les services de la DMR",
                                    style={"margin-top": "0px", "color": "white"},
                                ),
                            ]
                        )
                    ],
                    id="title",
                ),
            ],
            id="header",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            children="Anomalies signalées en 2021-2022",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            f"{df_final.count()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children="Categories des anomalies",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            "10",
                            style={
                                "textAlign": "center",
                                "color": "#dd1e35",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children="Sous-categories des anomalies",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            "330",
                            style={
                                "textAlign": "center",
                                "color": "green",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children="Anomalies signalées 2019-2022",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            "2 066 366",
                            style={
                                "textAlign": "center",
                                "color": "#e55467",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Pie(
                                    name="kek",
                                    title="Diagramme de camembert des anomalies par arrondissement",
                                    titlefont={"color": "white", "size": 30},
                                    values=arrondissement_count.values,
                                    textfont=dict(size=13),
                                    rotation=45
                                    # insidetextorientation='radial',
                                ),
                            ],
                            layout=go.Layout(
                                width=800,
                                height=520,
                                plot_bgcolor="#1f2c56",
                                paper_bgcolor="#1f2c56",
                                hovermode="closest",
                                legend={
                                    "orientation": "h",
                                    "bgcolor": "#1f2c56",
                                    "xanchor": "center",
                                    "x": 0.5,
                                    "y": -0.07,
                                },
                                font=dict(family="sans-serif", size=12, color="white"),
                            ),
                        )
                    )
                ),
                html.Div([dcc.Graph(id="example-graph", figure=fig4)]),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    html.Iframe(
                        id="maps",
                        srcDoc=open("dashboard/assets/districts_map.html", "r").read(),
                        width="100%",
                        height="500",
                    ),
                    className="create_container1 twelve columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


if __name__ == "__main__":
    app.run_server(debug=True)
