
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from dash.exceptions import PreventUpdate

from recommendation_engine import build_train_and_test, train_and_predict, get_user_top_n
from config import app, movies, ratings, popular_movies
from movie_cards import get_movie_card


movie_cards = []
inputs = []
for _, movie in popular_movies.iterrows():
	movie_cards.append(get_movie_card(movie.MovieID.item(), movie.Title.item(), with_rating_buttons=True))
	inputs.append(Input(f'{movie.MovieID.item()}-ratings', 'value'))


def collab_page():
	collab_tab = dbc.Row(
		children=[
			dbc.Card(
				dbc.CardBody(
					[
						html.P('Suggest Movies You Might Like'),
						dbc.Row(
							justify='between',
							children=[
								dbc.Col(
									dbc.Button('Recommend', color='success', id='collab-recommend-button', n_clicks=0),
									width='auto'
								),
							]
						)
					]
				),
				className='mt-3',
				style={ 'margin-bottom': '4rem' }
			),
			dbc.Card(
				dbc.CardBody(
					children=[
						html.Div(children=[
							html.P('Please take a moment to rate movies, those that you like and dislike, and rate as many as you can to improve our suggestion.'),
							dbc.Alert('Please rate at least one movie.', color='danger', id='rating-alert', is_open=False)
						]),
						html.Div(
							children=[
								dbc.Row(
									html.Div(
										children=[
											dcc.Loading(
												id='loading-1',
												type='default',
												children=html.Div(id='loading-output-1')
											),
										],
										style={ 'marginBottom': '2rem', 'marginTop': '2rem' }
									)
								),
								html.Div(
									dbc.Row(
										movie_cards
									),
									id='movie-rating-cards',
									hidden=False
								)
							],
							id='movie-ratings-input-container'
						),
					]
				)
			)
		]
	)

	return collab_tab


@app.callback(
    Output('ratings-store', 'data'), inputs, State('ratings-store', 'data')
)
def movie_rated(*args):
	ctx = dash.callback_context

	if not ctx.triggered:
		return {}
	else:
		item = ctx.triggered[0]
		movie_id = item['prop_id'].split('.')[0].split('-')[0]
		rating = item['value']

		user_dict = args[-1]

		if not user_dict:
			user_dict = {
				'userID': [6041],
				'itemID': [movie_id],
				'rating': [rating],
			}
		else:
			user_dict['userID'].append(6041)
			user_dict['itemID'].append(movie_id)
			user_dict['rating'].append(rating)

		return user_dict


@app.callback(
    [Output('loading-output-1', 'children'), Output('rating-alert', 'is_open'), Output('movie-rating-cards', 'hidden')], [Input('collab-recommend-button', 'n_clicks'), Input('ratings-store', 'data')]
)
def on_recommend_click(clicked, ratings_store):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'collab-recommend-button' in changed_id:
		if ratings_store is None or ratings_store == {}:
			return '', True, False

		train, test = build_train_and_test(ratings, movies, ratings_store)
		predictions = train_and_predict(train, test)
		top_n = get_user_top_n(predictions, 6041)

		movie_ids = [recommendation[0] for recommendation in top_n]
		top_n_movies = []
		for id in movie_ids:
			movie = movies.loc[movies['MovieID'] == id]
			top_n_movies.append((movie.MovieID.item(), movie.Title.item()))

		movie_cards = []
		for id, title in top_n_movies:
			movie_cards.append(get_movie_card(id, title))

		return dbc.Row(movie_cards), False, True
	else:
		raise PreventUpdate

