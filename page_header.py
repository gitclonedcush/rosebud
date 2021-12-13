from dash import html
import dash_bootstrap_components as dbc

ROSEBUD_LOGO = 'popcorn.svg'

def page_header(logo_src):
	header_content = dbc.Row(
		children=[
			dbc.Col(
				html.Img(src=logo_src, height='260'),
				width='auto'
			),
			dbc.Col(
				children=[
					html.H1('ROSEBUD', className='card-title'),
					html.P('MOVIE RECOMMENDATIONS', className='card-title')
				],
			),
		],
		align='center'
	)

	header = dbc.Card(dbc.CardBody(
		children=[
			header_content
		]
	), color='dark', inverse=True)

	return header

