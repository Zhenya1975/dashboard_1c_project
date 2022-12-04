from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_application.dash_functions as dash_functions

product_categories_options = dash_functions.product_select_content()
product_type_options = dash_functions.product_types_select_content()


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
                             dbc.Col(
                                     children=[
                                         html.Div([
                                             html.H4('Информация о будущих платежах по договорам лизинга в разрезе статусов договора'),
                                             dcc.Checklist(
                                                 id="checklist_tab_1",
                                                 options=["Asia", "Europe", "Africa", "Americas", "Oceania"],
                                                 value=["Americas", "Oceania"],
                                                 inline=True
                                             ),
                                             dcc.Graph(id="next_payments_by_agreement_status"),

                                         ])

                                     ]),

                         ]),


                     ]),



        ]
    )
    return tab_1