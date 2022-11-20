import datetime

import dash
from dash import dcc, Input, Output
from dash import html

import dash_bootstrap_components as dbc
# from flask_login.utils import login_required
import plotly.express as px
import pandas as pd

from dash_bootstrap_templates import load_figure_template


import dash_application.tab_general_market_position as tab_general_market_position
import dash_application.dash_functions as dash_functions
# dash_functions.prepare_df_from_csv('/Users/zupanikevgenij/pycharm_projects/dashboard_1c_project/project/datafiles/next_payments_test_data_2.csv')

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

df_local = pd.read_csv('./datafiles/next_payments_test_data_2.csv')
# print(df_local)

# url = 'https://drive.google.com/file/d/1DmH3A7I9eONqE2JZKLCCC_dGd3dmDbLO/view?usp=share_link'
# url = 'https://drive.google.com/file/d/114FNn99SAQQsLB_-l0vItgs1Xj-6RtzQ/view?usp=share_link'
# path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
# df_expected_sales = pd.read_csv(path)
df_expected_sales = df_local
df_expected_sales["Дата получения платежа"] = pd.to_datetime(df_expected_sales["Дата получения платежа"], format="%Y-%m-%d")
# print(df)
df_expected_sales['date'] = df_expected_sales['Дата получения платежа']
today = datetime.datetime.now()
df_expected_sales = df_expected_sales.loc[df_expected_sales['date']>today]
# print(df_expected_sales)

df_expected_sales = df_expected_sales.copy()
df_expected_sales['month'] = df_expected_sales.date.dt.month
df_expected_sales['year'] = df_expected_sales.date.dt.year
# print(df_expected_sales.info())

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
                                      tab_general_market_position.tab_general_market_position(),
                                      tab_temp,


                                      # tab_deal.deal_tab(),
                                      # tab_order.order_tab(),

                                  ]),
                          ]),

                      ]
                      ),
             ],


            fluid=True,
            # className='custom_container'
        )
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
                        Output('next_payments_by_types_graph', 'figure'),
                       ],
                      [Input('dummy_input', 'value'),
                       ])
    def deals_tab(dummy_input):

        fig = px.histogram(df_expected_sales,
                           x="date",
                           y="Сумма платежа",
                           histfunc="sum",
                           title="Платежи в разрезе продуктов",
                           color='Продукт',
                           # text_auto=True
                           text_auto='.3s'
                           )

        fig.update_traces(
            # xbins_size="M1",
            xbins=dict(
                # end='2016-12-31 12:00',
                size='M1',
                # start='1983-12-31 12:00'
            )
        )
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
            tickformat="%b\n%Y"
        )
        fig.update_layout(
            template = 'seaborn',
            barmode='stack',
            bargap=0.1,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-1.2,
                xanchor="left",
                x=0
            ),
            yaxis_title="Руб",
        )

        next_payments_by_types_fig = px.histogram(df_expected_sales,
                           x="date",
                           y="Сумма платежа",
                           histfunc="sum",
                           title="Платежи в разрезе типов",
                           color='Тип имущества',
                           text_auto='.3s'
                           )

        next_payments_by_types_fig.update_traces(
            # xbins_size="M1",
            xbins=dict(
                # end='2016-12-31 12:00',
                size='M1',
                # start='1983-12-31 12:00'
            )
        )
        next_payments_by_types_fig.update_xaxes(
            # showgrid=True,
            ticklabelmode="period",
            dtick="M1",
            tickformat="%b\n%Y"
        )
        next_payments_by_types_fig.update_layout(
            template = 'seaborn',
            # barmode='stack',
            bargap=0.1,
            legend=dict(
                # orientation="h",
                # yanchor="bottom",
                # y=-0.5,
                # xanchor="left",
                # x=0
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




        return [fig, next_payments_by_types_fig]