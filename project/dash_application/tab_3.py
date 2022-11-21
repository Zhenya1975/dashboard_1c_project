from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_application.dash_functions as dash_functions

product_categories_options = dash_functions.product_select_content()
product_type_options = dash_functions.product_types_select_content()


def tab_3_content():
    tab_3 = dcc.Tab(
        label='Денежные средства',
        value='tab_3',
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
                                             html.H4('Динамика продолжительности жизни в странах по континентам'),
                                             dcc.Graph(id="tab_3_graph"),
                                             dcc.Checklist(
                                                 id="checklist",
                                                 options=["Asia", "Europe", "Africa", "Americas", "Oceania"],
                                                 value=["Americas", "Oceania"],
                                                 inline=True
                                             ),
                                         ])

                                     ]),

                         ]),


                     ]),



        ]
    )
    return tab_3