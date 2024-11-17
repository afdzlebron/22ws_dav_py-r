# -*- coding: utf-8 -*-

################################### Beispiel Einzelhandelsumsätze##############################
#################################


import dash
import  dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import os

## Lesen der Datensätze
################################ Gesamtumsatz des Monats  ###################################

monthly_sales_df = pd.read_csv('monthly_sales_df.csv', sep=',')
monthly_sales_df.info()
################################ Ferienumsatz #####################################



holiday_sales = pd.read_csv('holiday_sales.csv', sep=',')

###################### Wochenumsatz #########################


weekly_sale = pd.read_csv('weekly_sale.csv', sep=',')

########################### Umsatz auf Filialebene #######################



store_df = pd.read_csv('store_df.csv', sep=',')

######################## Verkauf auf Abteilungsebene #########################




dept_df = pd.read_csv('dept_df.csv', sep=',')

#########################################


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app.title = 'Einzelhandelsumsätze Dashboard'
server = app.server

navbar = dbc.Navbar( id = 'navbar', children = [
    dbc.Row([
        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px")),
        dbc.Col(
            dbc.NavbarBrand("Einzelhandelsumsätze", style = {'color':'white', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            )

            )


        ],align = "center",
        # no_gutters = True
        ),


    ], color = '#090059')


card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Monate auswählen', style = {'textAlign':'center'}),

            dbc.Row([

                dbc.Col([

                    html.H6('Aktueller Monat'),

                    dcc.Dropdown( id = 'dropdown_base',
        options = [
            {'label':i, 'value':i } for i in monthly_sales_df.sort_values('month')['Month']

            ],
        value = 'Feb',

        )


                    ]),

                dbc.Col([

                    html.H6('Referenzmonat'),

                    dcc.Dropdown( id = 'dropdown_comp',
        options = [
            {'label':i, 'value':i } for i in monthly_sales_df.sort_values('month')['Month']

            ],
        value = 'Jan',

        )


                    ]),




                ])

            ]
        )



    ]


body_app = dbc.Container([

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdwn,style={'height':'150px'})],width = 4),
        dbc.Col([dbc.Card(id = 'card_num1',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num2',style={'height':'150px'})])

        ]),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([dbc.Card(id = 'card_num3',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num4',style={'height':'350px'})])

        ]),

    html.Br(),
    html.Br()


    ],
    style = {'backgroundColor':'#f7f7f7'},
    fluid = True)


app.layout = html.Div(id = 'parent', children = [navbar,body_app])


@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               ],
              [Input('dropdown_base','value'),
                Input('dropdown_comp','value')])
def update_cards(base, comparison):

    sales_base = monthly_sales_df.loc[monthly_sales_df['Month']==base].reset_index()['Weekly_Sales'][0]


    holi_base = monthly_sales_df.loc[monthly_sales_df['Month']==base].reset_index()['Holiday_Sales'][0]



    weekly_base = weekly_sale.loc[weekly_sale['Month']==base].reset_index()
    weekly_comp = weekly_sale.loc[weekly_sale['Month']==comparison].reset_index()



    store_base = store_df.loc[store_df['Month']==base].sort_values('Weekly_Sales',ascending = False).reset_index()[:10]
    store_comp = store_df.loc[store_df['Month']==comparison].sort_values('Weekly_Sales',ascending = False).reset_index()[:10]





    fig = go.Figure(data = [go.Scatter(x = weekly_base['week_no'], y = weekly_base['Weekly_Sales'],\
                                   line = dict(color = 'firebrick', width = 4),name = '{}'.format(base)),
                        go.Scatter(x = weekly_comp['week_no'], y = weekly_comp['Weekly_Sales'],\
                                   line = dict(color = '#090059', width = 4),name = '{}'.format(comparison))])


    fig.update_layout(plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      yaxis_tickprefix = '$',
                      yaxis_ticksuffix = 'M')


    fig2 = go.Figure([go.Bar(x = store_base['Weekly_Sales'], y = store_base['Store'], marker_color = 'indianred',name = '{}'.format(base),\
                             text = store_base['Weekly_Sales'], orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])


    fig3 = go.Figure([go.Bar(x = store_comp['Weekly_Sales'], y = store_comp['Store'], marker_color = '#4863A0',name = '{}'.format(comparison),\
                             text = store_comp['Weekly_Sales'], orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])

    fig2.update_layout(plot_bgcolor = 'white',
                       xaxis = dict(range = [0,'{}'.format(store_base['Weekly_Sales'].max()+3)]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '$',
                      xaxis_ticksuffix = 'M',
                      title = '{}'.format(base),
                      title_x = 0.5)

    fig3.update_layout(plot_bgcolor = 'white',
                       xaxis = dict(range = [0,'{}'.format(store_comp['Weekly_Sales'].max()+3)]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = '$',
                      xaxis_ticksuffix = 'M',
                      title = '{}'.format(comparison),
                      title_x = 0.5)








    card_content = [

        dbc.CardBody(
            [
                html.H6('Gesamtumsatz', style = {'fontWeight':'lighter', 'textAlign':'center'}),

                html.H3('{0}{1}{2}'.format("$", sales_base, "M"), style = {'color':'#090059','textAlign':'center'})

                ]

            )
        ]

    card_content1 = [

        dbc.CardBody(
            [
                html.H6('Ferienumsatz', style = {'fontWeight':'lighter', 'textAlign':'center'}),

                html.H3('{0}{1}{2}'.format("$", holi_base, "M"), style = {'color':'#090059','textAlign':'center'})

                ]

            )
        ]



    card_content2 = [

        dbc.CardBody(
            [
                html.H6('Wöchentlicher Umsatzvergleich', style = {'fontWeight':'bold', 'textAlign':'center'}),

                dcc.Graph(figure = fig, style = {'height':'250px'})


                ]

            )
        ]


    card_content3 = [

        dbc.CardBody(
            [
                html.H6('Geschäfte mit dem höchsten Umsatz', style = {'fontWeight':'bold', 'textAlign':'center'}),

                dbc.Row([
                    dbc.Col([dcc.Graph(figure = fig2, style = {'height':'300px'}),
                ]),
                    dbc.Col([dcc.Graph(figure = fig3, style = {'height':'300px'}),
                ])

                    ])



                ]

            )
        ]





    return card_content, card_content1, card_content2,card_content3


if __name__ == "__main__":
    app.run_server()
    #debug = True
