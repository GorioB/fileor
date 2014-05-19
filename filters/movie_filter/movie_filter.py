import guessit
from tmdbsimple import TMDB
tmdb = TMDB('7adc974f0bea6f2cd15917c97aab8d2a')

if __name__=="__main__":
	import sys
	sys.path.insert(0,"../../lib")
	import base
else:
	import lib.base as base

def findMovieTMDB(name,year=None):
	search = tmdb.Search()
	searchQuery = {'query':name}
	if year:
		searchQuery.update({'year':year})
	response = search.movie(searchQuery)
	return search.results[0]['title'],search.results[0]['id']

def getGenre(id):
	identity = tmdb.Movies(id)
	response = identity.info()
	return identity.genres

def guessMovieDetails(path):
	rVal = []
	guess = guessit.guess_movie_info(path,info=['filename'])
	if 'title' in guess:
		rVal.append(guess['title'])
		if 'year' in guess:
			rVal.append(guess['year'])

	return rVal

if __name__=="__main__":
	d = raw_input("> ")
	d = guessMovieDetails(d)
	if len(d)==2:
		d = findMovieTMDB(d[0],d[1])
	else:
		d = findMovieTMDB(d[0])
	print getGenre(d[1])