
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html
from dash.exceptions import PreventUpdate

from config import app, genres, merged
from movie_cards import get_movie_card
from recommendation_engine import get_popular_movies_by_genre, get_highly_rated_movies_by_genre

genre_dropdown_items = []
inputs = []
for i, genre in enumerate(genres):
	genre_dropdown_items.append(dbc.DropdownMenuItem(genre, id=f'genre-{i}'))
	inputs.append(Input(f'genre-{i}', 'n_clicks'))


def genre_page():
	genre_tab = dbc.Row(
		children=[
			dbc.Card(
				dbc.CardBody(
					[
						html.P('Recommend Movie by Genre'),
						dbc.Row(
							justify='between',
							children=[
								dbc.Col(
									dbc.DropdownMenu(genre_dropdown_items, id='genre-dropdown', label='Select Genre', color='info', menu_variant='dark', className='m-1'),
									width='auto'
								),
								dbc.Col(
									html.P(id='selected-genre-p', className='mt-3'),
								),
								dbc.Col(
									dbc.Button('Recommend', color='success', id='recommend-button', n_clicks=0),
									width='auto'
								),
							]
						)
					]
				),
				className='mt-3',
				style={ 'margin-bottom': '2rem' }
			),
			dbc.Card(
				dbc.CardBody(
					children=[
						html.Div(children=[
							html.P('Please select a genre from the dropdown and click "Recommend"', id='movie-rec-info-p'),
						]),
						html.Div(
							children=[
							],
							id='movie-recommendations-container'
						),
					]
				)
			)
		]
	)

	return genre_tab


@app.callback(
    [Output('genre-dropdown', 'label'), Output('selected-genre-p', 'children'), Output('selected-genre', 'data')], inputs
)
def dropdown_genre_selected(*args):
	ctx = dash.callback_context

	if not ctx.triggered:
		return 'Select Genre', '', ''
	else:
		genre_id = ctx.triggered[0]['prop_id'].split('.')[0]
		id = int(genre_id.split('-')[1])
		selected_genre = genres[id]
		return selected_genre, f'Recommend {selected_genre} Movies', selected_genre


@app.callback(
    [Output('movie-rec-info-p', 'children'), Output('genre-store', 'data')], [Input('recommend-button', 'n_clicks'), Input('selected-genre', 'data')]
)
def on_recommend_click(clicked, selected_genre):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'recommend-button' in changed_id:
		if selected_genre == '' or selected_genre is None:
			raise PreventUpdate

		return f'Selected Genre: {selected_genre}', selected_genre
	else:
		raise PreventUpdate


@app.callback(
    Output('movie-recommendations-container', 'children'), [Input('genre-store', 'data')]
)
def display_genre_recommendations(genre_store):
	if not genre_store or genre_store == '':
		raise PreventUpdate

	popular = get_popular_movies_by_genre(merged, genre_store, count=8)
	highly_rated = get_highly_rated_movies_by_genre(merged, genre_store, count=8)

	popular_cards = []
	highly_rated_cards = []

	for _, movie in popular.iterrows():
		popular_cards.append(get_movie_card(movie.MovieID.item(), movie.Title.item()))

	for _, movie in highly_rated.iterrows():
		highly_rated_cards.append(get_movie_card(movie.MovieID.item(), movie.Title.item()))

	return [
		html.P('Popular'),
		dbc.Row(
			popular_cards,
			style={ 'margin-bottom': '2rem' }
		),
		html.P('Highly Rated'),
		dbc.Row(
			highly_rated_cards,
		)
	]
