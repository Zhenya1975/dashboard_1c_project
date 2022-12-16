import datetime

import dash
from dash import dcc, Input, Output
from dash import html

import dash_bootstrap_components as dbc
# from flask_login.utils import login_required
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_templates import load_figure_template


import dash_application.tab_general_market_position as tab_general_market_position
import dash_application.tab_1 as tab_1
import dash_application.tab_3 as tab_3


import dash_application.dash_functions as dash_functions


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


# url = 'https://drive.google.com/file/d/1DmH3A7I9eONqE2JZKLCCC_dGd3dmDbLO/view?usp=share_link'
# url = 'https://drive.google.com/file/d/114FNn99SAQQsLB_-l0vItgs1Xj-6RtzQ/view?usp=share_link'
# path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
# df_expected_sales = pd.read_csv(path)
df_expected_sales = df_local
df_expected_sales["Дата получения платежа"] = pd.to_datetime(df_expected_sales["Дата получения платежа"], format="%Y-%m-%d")

df_expected_sales['date'] = df_expected_sales['Дата получения платежа']
today = datetime.datetime.now()
df_expected_sales = df_expected_sales.loc[df_expected_sales['date']>today]


df_expected_sales = df_expected_sales.copy()
df_expected_sales['month'] = df_expected_sales.date.dt.month
df_expected_sales['year'] = df_expected_sales.date.dt.year


# monthly_expected_sales = df_expected_sales.groupby([df_expected_sales['year'], df_expected_sales['month'], df_expected_sales['Продукт']])['Сумма платежа'].sum()

# monthly_expected_sales = df.groupby([(df.date.dt.year), (df.index.month)]).sum()


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
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/", external_stylesheets=[url_theme1, dbc_css])



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
                                      html.H3('Интерактивный дашборд')
                                  ]
                              )
                          ]),
                          # добавляем следующий ряд, в который уложим табы
                          html.Div([

                              dcc.Tabs(
                                  id="tabs-with-classes",
                                  value='tab_1',
                                  parent_className='custom-tabs',
                                  className='custom-tabs-container',
                                  children=[
                                      tab_1.tab_1_content(),
                                      # tab_general_market_position.tab_general_market_position(),
                                      # tab_3.tab_3_content()


                                      # 4tab_deal.deal_tab(),
                                      # tab_order.order_tab(),

                                  ]),
                          ]),

                      ]
                      ),
             ],


            fluid=True,
            className="dbc"
            # className='custom_container'
        )
    )





    # for view_function in dash_app.server.view_functions:
    #     if view_function.startswith(dash_app.config.url_base_pathname):
    #         dash_app.server.view_functions[view_function] = login_required(
    #             dash_app.server.view_functions[view_function]
    #         )
    init_callbacks(dash_app)
    init_callbacks_tab_1(dash_app)
    init_callbacks_tab_3(dash_app)

    return dash_app

def init_callbacks_tab_1(dash_app):
    @dash_app.callback(
        [
            Output('next_payments_by_agreement_status', 'figure')
        ],
        [
            Input('agreement_status_select', 'value')
        ]
    )
    def tab_1_content(agreement_status_select):
        measure_data = dash_functions.next_payments_by_status_data(agreement_status_select)[0]
        x_data = dash_functions.next_payments_by_status_data(agreement_status_select)[1]
        y_values = dash_functions.next_payments_by_status_data(agreement_status_select)[2]
        text_data = dash_functions.next_payments_by_status_data(agreement_status_select)[3]
        max_y_value = dash_functions.next_payments_by_status_data(agreement_status_select)[4]
        fig = go.Figure(go.Waterfall(
            name="Платежи",
            orientation="v",
            measure = measure_data,
            x = x_data,
            textposition="outside",
            # text=["+60", "+80", "+20", "-40", "-20", "Total"],
            text = text_data,
            y = y_values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

        fig.update_layout(
            paper_bgcolor='WhiteSmoke',
            template='seaborn',
            title="Платежы по договорам лизинга в разрезе статусов договора",
            # showlegend=True
            yaxis_range=[0, max_y_value]
        )
        return [fig]


def init_callbacks_tab_3(dash_app):
    @dash_app.callback(
        Output("tab_3_graph", "figure"),
        Input("checklist", "value"))
    def update_line_chart(continents):
        df = px.data.gapminder()  # replace with your own data source

        mask = df.continent.isin(continents)
        fig = px.line(df[mask],
                      x="year", y="lifeExp", color='country')
        return fig


def init_callbacks(dash_app):
    @dash_app.callback([Output('next_payments_graph', 'figure'),
                        Output('next_payments_by_types_graph', 'figure'),
                        Output('payments_plan_fact_cumsum_graph', 'figure'),
                        Output('payments_fact_donat_by_types_graph', 'figure'),
                       ],
                      [Input('product_select', 'value'),
                       Input('product_type_select', 'value')
                       ])
    def deals_tab(product_select, product_type_select):

        # Обработчик инпута по продуктам
        expected_sales_df = dash_functions.expected_sales_by_products(product_select)
        fig = px.histogram(expected_sales_df,
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
            paper_bgcolor='WhiteSmoke',
            template='seaborn',
            barmode='stack',
            bargap=0.1,
            legend=dict(
                # orientation="h",
                # yanchor="bottom",
                # y=-1.2,
                # xanchor="left",
                # x=0
            ),
            yaxis_title="Руб",
        )

        next_payments_by_types_fig = px.histogram(expected_sales_df,
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
            paper_bgcolor='WhiteSmoke',
            template='seaborn',
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

        ####### ГРАФИК ПЛАН-ФАКТ ########################
        payments_plan_fact_cumsum_fig = go.Figure()
        payments_plan_fact_df = dash_functions.actual_2022_sales(product_select, product_type_select)
        x = payments_plan_fact_df.loc[:, 'date']
        y = payments_plan_fact_df.loc[:, 'payment_cum']

        payments_plan_fact_cumsum_fig.add_trace(go.Scatter(
            x=x,
            y=y,
            fill='tozeroy',
            name='Факт продаж, руб',

        ))
        payments_plan_fact_cumsum_fig.update_xaxes(
            # showgrid=True,
            # ticklabelmode="period",
            # dtick="M1",
            tickformat="%b\n%Y"
        )
        payments_plan_fact_cumsum_fig.update_layout(
            paper_bgcolor='WhiteSmoke',
            template='seaborn',
            title="Платежи. План-факт",
            # title={'text': 'План-факт продаж в 2021 году', 'font': {'color': 'white'}, 'x': 0.5}
            xaxis={'range':['2022-1-1', '2023-1-1']},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="left",
                x=0
            ),
        )

        # Добавляем ряд с ожидаемыми платежами
        expected_payments_plan_fact_df = dash_functions.expected_2022_sales(product_select, product_type_select)
        x_expected = expected_payments_plan_fact_df.loc[:, 'date']
        y_expected = expected_payments_plan_fact_df.loc[:, 'payment_cum']

        payments_plan_fact_cumsum_fig.add_trace(go.Scatter(
            x=x_expected,
            y=y_expected,
            fill='tozeroy',
            name='Ожидаемые поступления, руб',

        ))

        # Добавляем ряд с планом продаж
        plan_data_df = dash_functions.sales_plan_2022(product_select)
        x_plan = plan_data_df['date']
        y_plan = plan_data_df['plan']
        payments_plan_fact_cumsum_fig.add_trace(go.Scatter(
            x=x_plan,
            y=y_plan,
            name='План поступлений, руб',

        ))

        ######## График pie_chart c данными факт на сегодня в разрезе типов #############
        fact_by_categories_data_df = dash_functions.donut_fact_2022_data(product_select)

        labels = fact_by_categories_data_df[0]
        values = fact_by_categories_data_df[1]

        fig_pie_fact_by_types = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig_pie_fact_by_types.update_layout(
            paper_bgcolor='WhiteSmoke',
            template='seaborn',
            title="Факт по типам",
            # title={'text': 'План-факт продаж в 2021 году', 'font': {'color': 'white'}, 'x': 0.5}
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="left",
                x=0
            ),
        )



        return [fig, next_payments_by_types_fig, payments_plan_fact_cumsum_fig, fig_pie_fact_by_types]