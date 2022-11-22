from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_application.dash_functions as dash_functions

product_categories_options = dash_functions.product_select_content()
product_type_options = dash_functions.product_types_select_content()


def tab_general_market_position():
    tab_general_block = dcc.Tab(
        label='Рыночное положение',
        value='general_market_position',
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            # в верхнем - фильтры
            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                            'marginTop': '10px', 'marginBottom': '10px',
                            # 'color': 'white'
                            },
                     children=[
                         dbc.Row([
                             dbc.Col(width=3,
                                 children=[
                                     dcc.Dropdown(

                                         options = product_categories_options,
                                         # value='Montreal',
                                         multi=True,
                                         placeholder="Продукт...",
                                         id='product_select',
                                         optionHeight=50,
                                     )
                                 ]
                             ),
                             dbc.Col(width=3,
                                     children=[
                                         dcc.Dropdown(

                                             options=product_type_options,
                                             # value='Montreal',
                                             multi=True,
                                             placeholder="Тип имущества...",
                                             id='product_type_select',
                                             optionHeight=50,
                                         )
                                     ]
                                     )]
                         ),

                     ]),
            html.Hr(),

            # в следующем блоке будут карточки
            # html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
            #                 'marginTop': '10px','marginBottom': '10px',
            #                 # 'color': 'white'
            #                 },
            #          children=[
            #              dbc.Row([
            #                  dbc.Col(width=3,
            #                      children=[
            #                          dbc.Card([
            #                              dbc.CardHeader("План-факт 2022, руб"),
            #                              dbc.CardBody([
            #                                  html.P(className="card-title", id='card_plan_fact_tab_contract_value'),
            #                                  html.P(className="card-text", id='card_plan_fact_tab_plan_value'),
            #                              ]),
            #                          ],
            #                              # color="light",
            #                              color="secondary",
            #                              outline=True
            #
            #                              # inverse=True
            #                          )
            #                      ]),
            #                  ]),
            #              ]
            #          ),




            # в следующем блоке будут графики
            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                            'marginTop': '10px', 'marginBottom': '10px',
                            # 'color': 'white'
                            },
                     children=[
                         dbc.Row([
                             dbc.Col(width=8,
                                     children=[
                                         dcc.Graph(id="payments_plan_fact_cumsum_graph",),

                                     ]),
                             dbc.Col(width=4,
                                     children=[
                                         dcc.Graph(id="payments_fact_donat_by_types_graph"),

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
                         html.Div(style={
                             # 'paddingLeft': '30px',
                             # 'paddingRight': '20px',
                             'marginTop': '10px', 'marginBottom': '10px',
                                         # 'color': 'white'
                                         },
                                  children=[
                                      dbc.Row([
                                          dbc.Col( style={'marginTop': '10px', 'marginBottom': '10px',},
                                              # width=6,
                                              children=[
                                                  dcc.Graph(
                                                      id="next_payments_graph",

                                                  ),
                                              ]
                                          ),
                                          dbc.Col(style={'marginTop': '10px', 'marginBottom': '10px',},
                                              # width=6,
                                              children=[
                                                  dcc.Graph(
                                                      id="next_payments_by_types_graph",

                                                  ),
                                              ]
                                          ),

                                      ])

                                  ]),

                     ]),



        ]
    )
    return tab_general_block