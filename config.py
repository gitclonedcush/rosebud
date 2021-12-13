import dash
import dash_bootstrap_components as dbc

from recommendation_engine import read_data, get_genres, get_popular_movies

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

ratings, movies, merged = read_data()
popular_movies = get_popular_movies(merged)
genres = get_genres(movies)