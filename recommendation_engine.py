import numpy as np
import pandas as pd
import time

from surprise import SVD
from surprise import Dataset
from surprise import Reader

def read_data():
	ratings = pd.read_csv('./ml-1m/ratings.dat', sep = '::', names = ['UserID', 'MovieID', 'Rating', 'Timestamp'], encoding = 'ISO-8859-1', engine='python')
	movies = pd.read_csv('./ml-1m/movies.dat', sep = '::', names = ['MovieID', 'Title', 'Genres'], encoding = 'ISO-8859-1', engine='python')
	merged = pd.merge(movies, ratings, on = 'MovieID')

	return ratings, movies, merged


def get_genres(movies):
	return pd.DataFrame(movies.Genres.str.split('|').tolist()).stack().unique()


def get_popular_movies_by_genre(movies, genre, count=10):
	'''
	Returns the most popular movies (those with the highest number of ratings) by genre

	Args:
		movies - a dataframe containing the set of all movies and ratings
	'''
	popular = movies[movies['Genres'].str.contains(genre)]
	popular = popular.groupby(['MovieID', 'Title', 'Genres'], as_index=False).agg({'Rating': ['sum']})
	popular['RatingCount'] = popular['Rating']['sum']
	return popular.sort_values(by='RatingCount', ascending=False).head(count)


def get_popular_movies(movies, count=500):
	'''
	Returns the most popular movies (those with the highest number of ratings) by genre

	Args:
		movies - a dataframe containing the set of all movies and ratings
	'''
	popular = movies.groupby(['MovieID', 'Title', 'Genres'], as_index=False).agg({'Rating': ['sum']})
	popular['RatingCount'] = popular['Rating']['sum']
	return popular.sort_values(by='RatingCount', ascending=False).head(count)


def get_highly_rated_movies_by_genre(movies, genre, count=10):
	'''
	Returns the most highly rated (those with the highest mean weighted rating) by genre

	Args:
		movies - a dataframe containing the set of all movies and ratings
	'''
	highly_rated = movies[movies['Genres'].str.contains(genre)]
	highly_rated = highly_rated.groupby(['MovieID', 'Title', 'Genres'], as_index=False).agg({'Rating': ['mean', 'sum']})
	highly_rated['RatingCountWeight'] = np.log(highly_rated['Rating']['sum'])
	highly_rated['RatingScore'] = highly_rated['RatingCountWeight'] * highly_rated['Rating']['mean']
	return highly_rated.sort_values(by='RatingScore', ascending=False).head(count)


def build_train_and_test(ratings, movies, new_user_ratings):
	'''
	Args:
		ratings - ratings dataframe from ratings.dat
		new_user_ratings - dataframe of the form userID, itemID, rating
	'''
	ratings = ratings.drop('Timestamp', axis=1)
	ratings = ratings.rename({
		'UserID': 'userID',
		'MovieID': 'itemID',
		'Rating': 'rating'
	}, axis=1)

	ratings = pd.concat([ratings, pd.DataFrame(new_user_ratings)], axis = 0).reset_index().drop('index', axis=1)

	reader = Reader(rating_scale=(1, 5))
	data = Dataset.load_from_df(ratings[['userID', 'itemID', 'rating']], reader)
	trainset = data.build_full_trainset()

	global_mean = trainset.global_mean
	user_id = new_user_ratings['userID'][0]
	testset = []
	for _, movie in movies.iterrows():
		testset.append((user_id, movie.MovieID, global_mean))

	return trainset, testset


def train_and_predict(trainset, testset):
	algo = SVD(lr_all = 0.007, reg_all = 0.1, n_epochs=10)
	algo.fit(trainset)

	# Predict ratings for all pairs (u, i) that are NOT in the training set.
	predictions = algo.test(testset)

	return predictions


def get_user_top_n(predictions, user_id, n=10):
    '''Return the top-N recommendation for a specific user from a set of predictions.
    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        user_id: id of user
        n(int): The number of recommendation to output for each user. Default
            is 10.
    Returns:
        A list where values are tuples
        [(raw item id, rating estimation), ...] of size n.
    '''

    top_n = []
    for uid, iid, _, est, _ in predictions:
        if uid == user_id:
            top_n.append((iid, est))

    top_n.sort(key=lambda x: x[1], reverse=True)
    return top_n[:n]