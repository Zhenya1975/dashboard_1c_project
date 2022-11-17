import dash
from dash import dcc, callback_context, Input, Output, State
from dash import html

import dash_bootstrap_components as dbc
# from flask_login.utils import login_required
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template


# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

available_graph_templates: ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark',
                            'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

data_file = "'project/datafiles/next_payments_test_data.csv'"
df_local = pd.read_csv('./datafiles/next_payments_test_data.csv')
# print(df_local)

url = 'https://drive.google.com/file/d/1DmH3A7I9eONqE2JZKLCCC_dGd3dmDbLO/view?usp=share_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)
df["Дата получения платежа"] = pd.to_datetime(df["Дата получения платежа"], format="%Y-%m-%d")
# print(df)
df['date'] = df['Дата получения платежа']



df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
# print(df)

monthly_expected_sales = df.groupby([df['year'], df['month'], df['Продукт']])['Сумма платежа'].sum()

# monthly_expected_sales = df.groupby([(df.date.dt.year), (df.index.month)]).sum()
# print(monthly_expected_sales)

# df = pd.DataFrame(
#     {
#         "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#         "Amount": [4, 1, 2, 2, 4, 5],
#         "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
#     }
# )


def create_dash_application(flask_app):
    # dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CERULEAN])
    # server = dash_app.server
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
    )
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[url_theme1, dbc_css])

    dash_app.layout = html.Div(
        dbc.Container(

            [html.Div(style={'paddingLeft': '15px', 'paddingRight': '20px', 'paddingTop': '5px', 'paddingBottom': '5px',
                             # 'color': 'white'
                             },
                      children=[
                          dbc.Row([
                              dbc.Col(width=12, children=[html.H3('DASHBOARD'), ]),
                          ]),
                          dcc.Input(
                              id="dummy_input",
                          ),
                          dcc.Graph(
                                  id="next_payments_graph",
                                  # figure=px.histogram(df, x="date", y="Сумма платежа", color="Продукт", histfunc="sum")

                              ),
                      ]
                      ),
             ],

        # children=[
        #     html.H1(children="Hello Dash"),
        #     html.Div(
        #         children="""
        #     Dash: A web application framework for Python.
        # """
        #     ),
        #     dcc.Graph(
        #         id="example-graph",
        #         figure=px.bar(df, x="Fruit", y="Amount", color="City", barmode="group"),
        #     ),
        # ],
            fluid=False, className='custom_container')
    )





    # for view_function in dash_app.server.view_functions:
    #     if view_function.startswith(dash_app.config.url_base_pathname):
    #         dash_app.server.view_functions[view_function] = login_required(
    #             dash_app.server.view_functions[view_function]
    #         )
    init_callbacks(dash_app)

    return dash_app


def init_callbacks(dash_app):
    @dash_app.callback([Output('next_payments_graph', 'figure'),
                       ],
                      [Input('dummy_input', 'value'),
                       ])
    def deals_tab(dummy_input):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['Сумма платежа'],
            # fill='tozeroy',
            name='Стоимость ожиданий',
        ))
        return [fig]