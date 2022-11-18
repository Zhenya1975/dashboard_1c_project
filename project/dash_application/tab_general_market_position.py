from dash import dcc, html
import dash_bootstrap_components as dbc



def tab_general_market_position():
    tab_general_block = dcc.Tab(
        label='ПОЛОЖЕНИЕ КОМПАНИИ НА РЫНКЕ ЛИЗИНГА',
        value='general_market_position',
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[


            dbc.Row([
                dbc.Col(width=3,
                        children=[
                            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                                            'marginTop': '10px',
                                            # 'color': 'white'
                                            },
                                     children=[
                                         html.P(),
                                         html.B('Фильтры'),
                                         dcc.Input(
                                             id="dummy_input",
                                         ),

                                     ]
                                     ),
                        ]),
                dbc.Col(width=9,
                        children=[
                            dcc.Graph(
                                id="next_payments_graph",

                            ),


                        ])

            ])
        ]
    )
    return tab_general_block