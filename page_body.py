import dash_bootstrap_components as dbc
from dash import html

from genre_recommend import genre_page
from collaborative_recommend import collab_page

page_body_style = {
	'padding': '2rem'
}

label_style = {
	'color': '#28282B'
}

active_label_style = {
	'background-color': '#FFFFFF',
	'color': '#28282B'
}

tab_style = {
	'background-color': '#FAF9F6',
}


def page_body():

	collaborative_tab = dbc.Card(
		dbc.CardBody(
			[
				html.P('Similar Recommendations', className='card-text'),
				dbc.Button('Recommend', color='success'),
			]
		),
		className='mt-3',
	)

	tabs = dbc.Tabs(
		[
			dbc.Tab(genre_page(), label='Recommend by Genre', label_style=label_style, active_label_style=active_label_style, tab_style=tab_style),
			dbc.Tab(collab_page(), label='Recommend Similar Movies', label_style=label_style, active_label_style=active_label_style, tab_style=tab_style),
		]
	)

	return html.Div(children=tabs, style=page_body_style)

