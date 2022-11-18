import dash
from dash import dcc, Input, Output
from dash import html

import dash_bootstrap_components as dbc
# from flask_login.utils import login_required
import plotly.express as px
import pandas as pd

from dash_bootstrap_templates import load_figure_template


import dash_application.tab_general_market_position as tab_general_market_position


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

########## DATA_FILES ##############

# df_local = pd.read_csv('./datafiles/next_payments_test_data.csv')
# print(df_local)

# url = 'https://drive.google.com/file/d/1DmH3A7I9eONqE2JZKLCCC_dGd3dmDbLO/view?usp=share_link'
url = 'https://drive.google.com/file/d/114FNn99SAQQsLB_-l0vItgs1Xj-6RtzQ/view?usp=share_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df_expected_sales = pd.read_csv(path)
df_expected_sales["Дата получения платежа"] = pd.to_datetime(df_expected_sales["Дата получения платежа"], format="%Y-%m-%d")
# print(df)
df_expected_sales['date'] = df_expected_sales['Дата получения платежа']


df_expected_sales['month'] = df_expected_sales.date.dt.month
df_expected_sales['year'] = df_expected_sales.date.dt.year
# print(df_expected_sales)

# monthly_expected_sales = df_expected_sales.groupby([df_expected_sales['year'], df_expected_sales['month'], df_expected_sales['Продукт']])['Сумма платежа'].sum()

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

    # print(tab_general_market_position.tab_general_market_position())
    tab_temp = dcc.Tab(
        label='Tab one',
        value='general_market_position_temp',
        children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ])
    # print("tab_temp: ", tab_temp)
    # print(tab_general_market_position.tab_general_market_position())

    dash_app.layout = html.Div(
        dbc.Container(

            [html.Div(style={'paddingLeft': '15px', 'paddingRight': '20px', 'paddingTop': '5px', 'paddingBottom': '5px',
                             # 'color': 'white'
                             },
                      children=[
                          # укладываем на всю ширину ряда заголовок
                          dbc.Row([
                              dbc.Col(
                                  children=[
                                      html.H3('DASHBOARD')
                                  ]
                              )
                          ]),
                          # добавляем следующий ряд, в который уложим табы
                          html.Div([
                              dcc.Tabs(
                                  id="tabs-with-classes",
                                  value='general_market_position',
                                  parent_className='custom-tabs',
                                  className='custom-tabs-container',
                                  children=[
                                      tab_temp,

                                      tab_general_market_position.tab_general_market_position(),
                                      # tab_deal.deal_tab(),
                                      # tab_order.order_tab(),

                                  ]),
                          ]),


                          dbc.Row([
                              dbc.Col(width=3, children=[html.H3('DASHBOARD'), ]),
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
        # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
        df = pd.DataFrame(dict(
            date=["2020-01-10", "2020-01-10", "2020-02-10", "2020-02-10", "2020-04-10", "2020-05-10", "2020-06-10"],
            sales=['one', 'two', 'one', 'two', 'two', 'two', 'two'],
            value=[1, 2, 3, 0, 1, 2, 3]
        ))
        df1= pd.DataFrame(dict(
            date=["2020-01-10", "2020-01-10", "2020-02-10", "2020-03-10", "2020-04-10", "2020-05-10", "2020-06-10"],
            value=[4, 2, 12, 0, 1, 2, 3]
        ))
        # fig = px.histogram(df, x="Date", y="AAPL.Close", histfunc="avg", title="Histogram on Date Axes")
        # fig = px.histogram(df, x="date", y="value", histfunc="sum", title="Histogram on Date Axes", color='sales', text_auto=True)
        fig = px.histogram(df_expected_sales, x="date", y="Сумма платежа", histfunc="sum", title="Ожидаемые поступления", color='Продукт',
                           text_auto=True)

        fig.update_traces(xbins_size="M1")
        # fig.add_trace(go.Bar(
        #         x=df1['date'],
        #         y=df1['value'],
        #         # fill='tozeroy',
        #         name='Стоимость ожиданий',
        #     ))

        fig.update_xaxes(
            # showgrid=True,
            ticklabelmode="period",
            dtick="M1",
            # tickformat="%b\n%Y"
        )
        fig.update_layout(
            barmode='stack',
            bargap=0.2,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            yaxis_title="Руб",
        )


        # print(df)
        # print(df.info())
        # fig = go.Figure()
        # fig.add_trace(go.Bar(
        #     x=df['date'],
        #     y=df['Сумма платежа'],
        #     # fill='tozeroy',
        #     name='Стоимость ожиданий',
        # ))
        # fig.add_trace(go.Bar(
        #     x=df['date'],
        #     y=df['Сумма платежа'],
        #     # fill='tozeroy',
        #     name='Стоимость ожиданий',
        # ))
        # fig.update_traces(xbins_size="M1")




        return [fig]