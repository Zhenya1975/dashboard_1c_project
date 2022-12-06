from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_application.dash_functions as dash_functions

product_categories_options = dash_functions.product_select_content()
product_type_options = dash_functions.product_types_select_content()
agreement_status_options = dash_functions.next_payments_by_agreement_status_options()[0]
year_options = dash_functions.next_payments_donat_chart_year_options_list()

def tab_1_content():
    tab_1 = dcc.Tab(
        label='Будущие платежи',
        value='tab_1',
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[

            # в следующем блоке будут графики
            html.Div(style={'paddingLeft': '30px', 'paddingRight': '20px',
                            'marginTop': '10px', 'marginBottom': '10px',
                            # 'color': 'white'
                            },
                     children=[
                         dbc.Row([
                             dbc.Col(width=9,
                                     children=[
                                         html.Div([
                                             # html.H4('Информация о будущих платежах по договорам лизинга в разрезе статусов договора'),
                                             dcc.Dropdown(
                                                 options=agreement_status_options,
                                                 # value='Montreal',
                                                 multi=True,
                                                 placeholder="Статус договора...",
                                                 id='agreement_status_select',
                                                 optionHeight=50,
                                             ),
                                             html.Div(style={'marginTop': '10px'},
                                                      children=[
                                                          dcc.Graph(id="next_payments_by_agreement_status"),
                                                      ]
                                                      ),



                                         ])

                                     ]),
                             dbc.Col(width=3,
                                     children=[
                                         dcc.Dropdown(
                                             options=year_options,

                                             multi=True,
                                             placeholder="Год...",
                                             id='agreement_year_select',
                                             # optionHeight=50,
                                         ),
                                     ]

                             )

                         ]),


                     ]),



        ]
    )
    return tab_1