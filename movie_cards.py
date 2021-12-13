import dash_bootstrap_components as dbc
from dash import html

def get_movie_card(movie_id, movie_title, with_rating_buttons=False):
	card_width = '12rem'
	ratings_div = ''

	if with_rating_buttons:
		card_width = '16.5rem'
		ratings_div = html.Div(children=[
			dbc.Row(
				[
					dbc.Col(dbc.RadioItems(
						options=[
							{'label': '1', 'value': 1},
							{'value': 2},
							{'value': 3},
							{'value': 4},
							{'label': '5', 'value': 5},
						],
						id=f'{movie_id}-ratings',
						inline=True,
					),
					width='auto'),
				],
				style={ 'paddingLeft': '0.37rem' },
				justify='center'
			)], style={ 'border-top': '0.1rem solid', 'padding-top': '1rem' }
		)

	card = dbc.Col(
		dbc.Card(
			children=[
				dbc.CardImg(src=f'./assets/movie_images/{movie_id}.jpg', top=True),
				dbc.CardBody(
					children=[
						html.P(f'{movie_title}', className='card-text'),
						ratings_div
					],
				),
			],
			style={ 'width': card_width, 'margin-bottom': '1rem' }
		),
		width='auto',
	)

	return card
