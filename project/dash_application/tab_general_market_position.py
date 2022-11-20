from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_application.dash_functions as dash_functions

product_categories_options = dash_functions.product_select_content()


def tab_general_market_position():
    tab_general_block = dcc.Tab(
        label='ПОЛОЖЕНИЕ КОМПАНИИ НА РЫНКЕ ЛИЗИНГА',
        value='general_market_position',
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            # в верхнем блоке пусть будут фильтры
            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                            'marginTop': '10px',
                            # 'color': 'white'
                            },
                     children=[
                         dbc.Row(
                             dbc.Col(width=3,
                                 children=[
                                     dcc.Dropdown(

                                         options = product_categories_options,
                                         # value='Montreal',
                                         multi=True,
                                         placeholder="Продукт...",
                                         id='product_select'
                                     )
                                 ]
                             )
                         ),

                     ]),
            # в следующем блоке будут графики
            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                            'marginTop': '10px',
                            # 'color': 'white'
                            },
                     children=[
                         dbc.Row([
                             dbc.Col(
                                     children=[
                                         dcc.Graph(id="payments_plan_fact_cumsum_graph",),

                                     ])
                         ]),

                         # dbc.Row([
                         #     dbc.Col(
                         #             children=[
                         #                 dcc.Graph(id="next_payments_graph",),
                         #
                         #             ])
                         # ]),
                         # dbc.Row([
                         #     dbc.Col(
                         #         children=[
                         #             dcc.Graph(id="next_payments_by_types_graph",),
                         #
                         #         ])
                         # ]),


                         dbc.Row([
                             dbc.Col(
                                 # width=6,
                                 children=[
                                     dcc.Graph(
                                         id="next_payments_graph",

                                     ),
                                 ]
                             ),
                             dbc.Col(
                                 # width=6,
                                 children=[
                                     dcc.Graph(
                                         id="next_payments_by_types_graph",

                                     ),
                                 ]
                             ),

                         ])
                     ]),



        ]
    )
    return tab_general_block